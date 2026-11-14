"""Integrity, leakage-boundary and result-accounting audit; no regeneration."""
import collections
import json
from pathlib import Path

from dataset import ROOT, dumps, sha, verify
from experiment import CONFIG, CARD_SCHEMA, CODE_SCHEMA, CODE_SYSTEM, equal
import jsonschema

def main():
    m=verify(); methods=m['methods']; assert len(methods)==45
    assert collections.Counter(s['library'] for s in methods)=={'numpy':15,'sympy':15,'networkx':15}
    assert all(n==5 for n in collections.Counter((s['library'],s['group']) for s in methods).values())
    assert json.loads((ROOT/'frozen/config.json').read_text())==CONFIG
    hashes=json.loads((ROOT/'frozen/protocol_code_hashes.json').read_text())
    for name,digest in hashes.items(): assert sha((ROOT/name).read_bytes())==digest, name
    cards=implementations=observations=passed=0
    generation_failures=[]; context=[]
    for producer in ['small','large']:
        for s in methods:
            p=ROOT/'runs/cards'/producer/f"{s['id']}.json"
            if not p.exists(): continue
            r=json.loads(p.read_text()); cards+=1
            assert len(r['request']['messages'])==2
            if r['valid']:
                jsonschema.validate(r['parsed'],CARD_SCHEMA)
                assert json.loads(r['response']['message']['content'])==r['parsed']
                assert json.loads((ROOT/'cards'/producer/p.name).read_text())==r['parsed']
            else: generation_failures.append(str(p.relative_to(ROOT)))
            context.append(r['response'].get('prompt_eval_count',0)+r['response'].get('eval_count',0))
    for producer,consumer in [('small','small'),('large','large'),('small','large'),('large','small')]:
        c=f'{producer}_to_{consumer}'
        for s in methods:
            p=ROOT/'runs/code'/c/f"{s['id']}.json"
            if not p.exists(): continue
            r=json.loads(p.read_text()); implementations+=1
            card=json.loads((ROOT/'runs/cards'/producer/p.name).read_text())
            if card['valid']:
                assert r['request']['messages']==[{'role':'system','content':CODE_SYSTEM},{'role':'user','content':'Implement this card:\n'+dumps(card['parsed'])}],str(p)
            if r['valid']:
                jsonschema.validate(r['parsed'],CODE_SCHEMA)
                assert json.loads(r['response']['message']['content'])==r['parsed']
                assert (ROOT/'implementations'/c/f"{s['id']}.py").read_text()==r['parsed']['code']
            else: generation_failures.append(str(p.relative_to(ROOT)))
            if 'response' in r: context.append(r['response'].get('prompt_eval_count',0)+r['response'].get('eval_count',0))
            rp=ROOT/'results'/c/p.name
            if not rp.exists(): continue
            result=json.loads(rp.read_text()); tests=json.loads((ROOT/'frozen'/p.name).read_text())['cases']
            assert len(result['cases'])==len(tests)==result['total']
            for ref,row in zip(tests,result['cases']):
                assert row['case_id']==ref['id'] and equal(row['input'],ref['input']) and equal(row['expected'],ref['expected'])
                e,o=row['expected'],row['observed']
                ok=e['error']==o.get('error') if 'error' in e else ('value' in o and equal(e['value'],o['value']))
                assert ok==row['passed']; observations+=1; passed+=ok
            assert result['passed']==sum(t['passed'] for t in result['cases'])
            assert result['all_pass']==all(t['passed'] for t in result['cases'])
    assert max(context,default=0)<CONFIG['card_options']['num_ctx'], 'Context window exhausted'
    complete=cards==90 and implementations==180 and observations==45092
    result=dict(complete=complete,cards=cards,implementations=implementations,observations=observations,passed=passed,generation_failures=generation_failures,max_observed_total_tokens=max(context,default=0),frozen_hashes_ok=True,card_only_reconstruction_prompts_ok=True,unmodified_generated_code_ok=True,case_accounting_ok=True)
    (ROOT/'audit.json').write_text(dumps(result)); print(dumps(result))
    if not complete: raise SystemExit(2)

if __name__=='__main__': main()
