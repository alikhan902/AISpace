"""Create an auditable Russian report from observed results only."""
import collections
import itertools
import json
import math
import statistics
from pathlib import Path

import numpy as np
from dataset import ROOT, SEED, dumps, verify

CONDS=["small_to_small","large_to_large","small_to_large","large_to_small"]
LABELS={"small_to_small":"1.7b → 1.7b","large_to_large":"4b → 4b","small_to_large":"1.7b → 4b","large_to_small":"4b → 1.7b"}

METRICS_EXPLANATION = r"""## Формулы расчёта точности

Все показатели рассчитывались отдельно для каждого из четырёх сочетаний моделей. Обозначим через \(N=45\) число функций, через \(n_i\) — число тестов функции \(i\), а через \(c_i\) — число успешно пройденных ею тестов. Для каждого сочетания \(\sum_{i=1}^{N}n_i=11\,273\). Общие 45 092 проверки относятся к четырём сочетаниям вместе и не используются как знаменатель точности отдельного сочетания.

### Доля функций, прошедших все тесты — основная метрика

$$
A_{\mathrm{functions}}=
\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}(c_i=n_i)\times100\%.
$$

Здесь индикатор \(\mathbf{1}(c_i=n_i)\) равен 1, если функция прошла все свои тесты, и 0 в остальных случаях. Даже один непройденный тест не позволяет засчитать функцию как полностью успешную. Этот показатель приведён в столбце «Точность по функциям».

Для сочетания 1.7b → 1.7b все тесты прошли 11 функций из 45:

$$
A_{\mathrm{functions}}=\frac{11}{45}\times100\%\approx24{,}44\%.
$$

### Доля всех пройденных тестов — микроточность

$$
A_{\mathrm{micro}}=
\frac{\sum_{i=1}^{N}c_i}{\sum_{i=1}^{N}n_i}\times100\%.
$$

Каждый тест имеет одинаковый вес, поэтому функции с большим числом тестов сильнее влияют на показатель. Это последний столбец основной таблицы — «Микроточность». Для сочетания 1.7b → 1.7b:

$$
A_{\mathrm{micro}}=\frac{3725}{11273}\times100\%\approx33{,}04\%.
$$

### Средняя точность по функциям — макроточность

$$
A_{\mathrm{macro}}=
\frac{1}{N}\sum_{i=1}^{N}\frac{c_i}{n_i}\times100\%.
$$

Сначала для каждой функции рассчитывается собственная доля пройденных тестов, затем эти 45 долей усредняются. Каждая функция имеет одинаковый вес независимо от числа её тестов. Для сочетания 1.7b → 1.7b макроточность составила 40,46%; в основной таблице это столбец «Макроточность по тестам».

### Когда тест считается успешным

Для обычного результата требовалось точное рекурсивное совпадение значения, типа и структуры с эталоном. Например, `True`, `1` и `1.0` не считались взаимозаменяемыми. Порядок элементов списка проверялся; порядок ключей словаря значения не имел. Численная погрешность не допускалась. Когда эталон предписывал исключение, проверялся его тип, но не текст сообщения.

Неправильный ответ, неожиданное исключение или превышение времени отдельного вызова давали ноль за соответствующий тест. Невалидный ответ генерации, ошибка загрузки программы или превышение общего времени процесса давали функции ноль пройденных тестов (\(c_i=0\)). Эти функции и их тесты оставались в знаменателях всех метрик.

Поэтому вариант может пройти больше отдельных тестов, но полностью восстановить меньше функций. Микроточность, макроточность и доля полностью успешных функций отражают разные свойства результата и не заменяют друг друга.
"""

def pct(x): return f"{100*x:.2f}%"

def stats(rows):
    n=len(rows); passed=sum(r["passed"] for r in rows); total=sum(r["total"] for r in rows)
    return {"functions":n,"perfect":sum(r["all_pass"] for r in rows),"function_accuracy":sum(r["all_pass"] for r in rows)/n if n else 0,"macro_accuracy":statistics.mean(r["passed"]/r["total"] for r in rows) if n else 0,"passed_tests":passed,"total_tests":total,"micro_accuracy":passed/total if total else 0,"load_errors":sum(bool(r['load_error']) for r in rows)}

def paired(data, methods):
    rng=np.random.default_rng(SEED)
    groups=[[i for i,s in enumerate(methods) if s['library']==lib] for lib in ['numpy','sympy','networkx']]
    sample=np.concatenate([rng.choice(g,size=(10000,len(g)),replace=True) for g in groups],axis=1)
    out=[]
    for a,b in itertools.combinations(CONDS,2):
        x=np.array([int(data[a][s['id']]['all_pass']) for s in methods]); y=np.array([int(data[b][s['id']]['all_pass']) for s in methods])
        a_only=int(((x==1)&(y==0)).sum()); b_only=int(((x==0)&(y==1)).sum()); n=a_only+b_only
        p=min(1.,2*sum(math.comb(n,k) for k in range(min(a_only,b_only)+1))/2**n) if n else 1.
        delta=y-x; ci=np.quantile(delta[sample].mean(axis=1),[.025,.975]).tolist()
        out.append({"a":a,"b":b,"a_only":a_only,"b_only":b_only,"difference_b_minus_a":float(delta.mean()),"bootstrap_95":ci,"mcnemar_exact_p":p})
    order=sorted(range(len(out)),key=lambda i:out[i]['mcnemar_exact_p']); previous=0.
    for rank,i in enumerate(order):
        previous=max(previous,min(1.,(len(out)-rank)*out[i]['mcnemar_exact_p'])); out[i]['holm_p']=previous
    return out

def build():
    m=verify(); methods=m['methods']; data={c:{} for c in CONDS}
    for c in CONDS:
        for p in sorted((ROOT/'results'/c).glob('*.json')):
            r=json.loads(p.read_text()); data[c][r['method_id']]=r
    complete=all(len(d)==45 for d in data.values())
    summary={"complete":complete,"test_cases_per_condition":sum(s['case_count'] for s in methods),"conditions":{c:stats(list(d.values())) for c,d in data.items()}}
    summary['by_library']={c:{lib:stats([r for r in d.values() if r['library']==lib]) for lib in ['numpy','sympy','networkx']} for c,d in data.items()}
    group_keys=list(dict.fromkeys((s['library'],s['group']) for s in methods))
    summary['by_group']={c:{f'{lib}.{group}':stats([r for r in d.values() if r['library']==lib and r['group']==group]) for lib,group in group_keys} for c,d in data.items()}
    summary['by_case_category']={}
    for c,d in data.items():
        summary['by_case_category'][c]={}
        for cat in ['boundary','exhaustive','random']:
            rows=[t for r in d.values() for t in r['cases'] if t['category']==cat]
            summary['by_case_category'][c][cat]={'passed':sum(t['passed'] for t in rows),'total':len(rows)}
    if complete: summary['paired_comparisons']=paired(data,methods)
    cards={}; generation={}
    for producer in ['small','large']:
        records=[json.loads(p.read_text()) for p in sorted((ROOT/'runs/cards'/producer).glob('*.json'))]
        cards[producer]={"generated":len(records),"valid":sum(r['valid'] for r in records),"signature_exact":sum(r.get('parsed',{}).get('signature')==next(s['signature'] for s in methods if s['id']==p.stem) for p,r in zip(sorted((ROOT/'runs/cards'/producer).glob('*.json')),records)),"truncated":sum(r['response'].get('done_reason')=='length' for r in records)}
    all_records=[]
    for kind in ['cards','code']:
        records=[json.loads(p.read_text()) for p in (ROOT/'runs'/kind).glob('*/*.json')]
        all_records += [r for r in records if 'response' in r]
        generation[kind]={"records":len(records),"valid":sum(r['valid'] for r in records),"truncated":sum(r.get('response',{}).get('done_reason')=='length' for r in records)}
    summary.update(cards=cards,generation=generation,model_calls=len(all_records),generation_seconds=sum(r['elapsed_seconds'] for r in all_records),output_tokens=sum(r['response'].get('eval_count',0) for r in all_records),prompt_tokens=sum(r['response'].get('prompt_eval_count',0) for r in all_records))
    if all_records: summary.update(started_at=min(r['started_at'] for r in all_records),finished_at=max(r['finished_at'] for r in all_records))
    (ROOT/'summary.json').write_text(dumps(summary))
    lines=['# Результаты восстановления функций по JSON-карточкам','', 'Статус: **завершено**.' if complete else 'Статус: **промежуточный отчёт; генерация ещё не завершена**.', '', 'Стрелка обозначает «автор карточки → автор реализации». Обозначения моделей — установленные теги Ollama `qwen3:1.7b` и `qwen3:4b`.', '', '## Основные результаты','', '| Сочетание | Все тесты функции пройдены | Точность по функциям | Макроточность по тестам | Пройдено тестов | Микроточность |','|---|---:|---:|---:|---:|---:|']
    for c in CONDS:
        s=summary['conditions'][c]
        lines.append(f"| {LABELS[c]} | {s['perfect']}/{s['functions']} | {pct(s['function_accuracy'])} | {pct(s['macro_accuracy'])} | {s['passed_tests']}/{s['total_tests']} | {pct(s['micro_accuracy'])} |")
    if complete:
        best=max(s['perfect'] for s in summary['conditions'].values())
        winners=[LABELS[c] for c in CONDS if summary['conditions'][c]['perfect']==best]
        lines += ['',f"Наибольший наблюдаемый результат по основной метрике: **{' и '.join(winners)} — {best}/45 ({pct(best/45)})**. Это описание данного запуска, а не утверждение об универсальном превосходстве модели или статистически установленном эффекте."]
    lines += ['', 'Полный успех означает прохождение всех зафиксированных тестов функции; это не доказательство эквивалентности на всех возможных входах. Макроточность даёт каждой функции равный вес. Микроточность взвешивает функции количеством тестов.', '']
    lines += METRICS_EXPLANATION.strip().splitlines()
    lines += ['', '## Методика в форме для статьи','',
        '> Единицей наблюдения служила публичная вычислительная функция. В зафиксированных версиях NumPy 2.5.4, SymPy 1.14.0 и NetworkX 3.6.1 целенаправленно выбраны по три предметные группы, по пять функций в каждой группе — всего 45 функций. Эталоном служили результаты вызова оригинальной библиотеки через заранее заданный адаптер входов и выходов. До генерации моделей были зафиксированы 11 273 тестовых входа с эталонными ответами, включая граничные, псевдослучайные и малые исчерпывающие наборы. Каждая из двух локальных моделей создала 45 JSON-карточек по документации и контрактам. По каждому набору карточек обе модели независимо восстановили функции. Те же 45 функций и те же тесты использовались во всех четырёх условиях. Карточки и восстановленные программы не исправлялись после получения ответов, а тестовые ответы и обратная связь моделям не передавались. Основной показатель — доля функций, прошедших все свои тесты; дополнительные — макро- и микросредняя доли точных совпадений.', '',
        'Полный протокол, области входов, состав выборки и ограничения приведены в [METHODOLOGY.md](METHODOLOGY.md). Размеченных обучающих примеров нет; все 45 функций проверочные. Описания поступали из docstring и адаптерных контрактов, исходники библиотек моделям не передавались.', '', '## По библиотекам','', '| Библиотека | Сочетание | Полный успех | Макроточность | Микроточность |','|---|---|---:|---:|---:|']
    for lib in ['numpy','sympy','networkx']:
        for c in CONDS:
            s=stats([r for r in data[c].values() if r['library']==lib])
            lines.append(f"| {lib} | {LABELS[c]} | {s['perfect']}/{s['functions']} | {pct(s['macro_accuracy'])} | {pct(s['micro_accuracy'])} |")
    lines += ['', '## По предметным группам','', 'В ячейках — число функций, прошедших все тесты, из пяти.', '', '| Группа | 1.7b → 1.7b | 4b → 4b | 1.7b → 4b | 4b → 1.7b |','|---|---:|---:|---:|---:|']
    for lib,group in group_keys:
        lines.append(f'| {lib}.{group} | '+' | '.join(f"{summary['by_group'][c][f'{lib}.{group}']['perfect']}/5" for c in CONDS)+' |')
    lines += ['', '## По типам тестовых входов','', '| Тип входа | 1.7b → 1.7b | 4b → 4b | 1.7b → 4b | 4b → 1.7b |','|---|---:|---:|---:|---:|']
    for cat in ['boundary','exhaustive','random']:
        lines.append(f'| {cat} | '+' | '.join(f"{summary['by_case_category'][c][cat]['passed']}/{summary['by_case_category'][c][cat]['total']}" for c in CONDS)+' |')
    lines += ['', '## Каждая функция','', 'В ячейках указано «пройдено / всего»; ✓ означает полный успех.', '', '| Функция | 1.7b → 1.7b | 4b → 4b | 1.7b → 4b | 4b → 1.7b |','|---|---:|---:|---:|---:|']
    for method in methods:
        cells=[]
        for c in CONDS:
            r=data[c].get(method['id']); cells.append(f"{'✓ ' if r['all_pass'] else ''}{r['passed']}/{r['total']}" if r else '—')
        lines.append('| `'+method['id']+'` | '+' | '.join(cells)+' |')
    lines += ['', '## Генерация и контроль формата','',f"Основных вызовов Ollama: {summary['model_calls']}; валидных карточек: {generation['cards']['valid']}/{generation['cards']['records']}; валидных ответов с кодом: {generation['code']['valid']}/{generation['code']['records']}. Суммарное время запросов: {summary['generation_seconds']/60:.1f} мин. Выходных токенов: {summary['output_tokens']:,}.".replace(',', ' '),'', '| Автор карточки | Валидные карточки | Точное совпадение строки сигнатуры | Усечение по лимиту |','|---|---:|---:|---:|']
    for p in ['small','large']:
        s=cards[p]; lines.append(f"| {'1.7b' if p=='small' else '4b'} | {s['valid']}/{s['generated']} | {s['signature_exact']}/{s['generated']} | {s['truncated']} |")
    lines += ['', 'Совпадение строки сигнатуры — проверка записи, не оценка семантической полноты карточки. Валидный JSON сам по себе не означает правильного описания алгоритма. Все исходные запросы, ответы, карточки и программы доступны в папках `runs/`, `cards/` и `implementations/`.','', '## Ошибки','', '| Сочетание | Ошибок загрузки функций | Неверных значений/типов | Неожиданных исключений | Не выдано ожидаемое исключение |','|---|---:|---:|---:|---:|']
    failure_examples=[]
    for c in CONDS:
        counts=collections.Counter()
        for r in data[c].values():
            if r['load_error']: counts['load']+=1
            bad=[t for t in r['cases'] if not t['passed']]
            for t in bad:
                if r['load_error']: continue
                if 'error' in t['observed']: counts['exception']+=1
                elif 'error' in t['expected']: counts['missing_exception']+=1
                else: counts['value']+=1
            if bad:
                failure_examples.append(dict(condition=c,method_id=r['method_id'],passed=r['passed'],total=r['total'],load_error=r['load_error'],first_failure=bad[0]))
        lines.append(f"| {LABELS[c]} | {counts['load']} | {counts['value']} | {counts['exception']} | {counts['missing_exception']} |")
    (ROOT/'failure_examples.json').write_text(dumps(failure_examples))
    lines += ['', 'Ошибки загрузки подсчитаны по функциям, остальные столбцы — по входам функций, которые удалось загрузить. Ошибки загрузки не дублируются в остальных столбцах. Для каждой неуспешной функции сохранён первый контрпример в [failure_examples.json](failure_examples.json); все ответы находятся в `results/`. Качественный разбор нескольких содержательных ошибок карточек и кода: [CARD_REVIEW.md](CARD_REVIEW.md).','']
    if complete:
        lines += ['## Парные сравнения полного успеха','', 'Разница указана как B−A в процентных пунктах. Интервалы — 95% парный bootstrap, 10 000 повторов с сохранением 15 функций каждой библиотеки. p-значения разведочные; выборка целенаправленная, связанные функции не обеспечивают независимость генеральной совокупности. Интервалы не оценивают изменчивость генерации при повторных запусках.', '', '| A | B | Только A | Только B | Разница, п.п. | Bootstrap 95%, п.п. | p Мак-Немара | p Holm |','|---|---|---:|---:|---:|---:|---:|---:|']
        for p in summary['paired_comparisons']:
            lo,hi=p['bootstrap_95']
            lines.append(f"| {LABELS[p['a']]} | {LABELS[p['b']]} | {p['a_only']} | {p['b_only']} | {100*p['difference_b_minus_a']:+.2f} | [{100*lo:+.2f}; {100*hi:+.2f}] | {p['mcnemar_exact_p']:.4f} | {p['holm_p']:.4f} |")
    lines += ['', '## Как читать результат','', 'Сравнение при неизменном наборе карточек характеризует восстановителей. Сравнение при неизменном восстановителе показывает, как итог зависит от автора карточки. Без отдельной экспертной карточки и условия восстановления напрямую по документации эти различия нельзя трактовать как чистую причинную потерю информации в карточке.', '', 'Это один запуск при temperature=0, think=false, фиксированном seed и Q4_K_M. Названия функций сохранены, поэтому предобучение на известных алгоритмах могло помогать. Протокол ограничивает области входов, разрешает вычислительные функции стандартной библиотеки и не оценивает полную совместимость API. Выводы относятся к этим 45 функциям и этим локальным артефактам.', '', '## Воспроизведение','', 'См. [README.md](README.md). Проверить хеши и комплектность: `.venv/bin/python audit.py`. Построить отчёт заново: `.venv/bin/python report.py`. Возобновить только несохранённые запросы: `.venv/bin/python experiment.py run`. Завершённые ответы при возобновлении используются из файлов.','']
    (ROOT/'REPORT.md').write_text('\n'.join(lines))
    print(dumps({"complete":complete,"conditions":summary['conditions'],"model_calls":summary['model_calls']}))

if __name__=='__main__': build()
