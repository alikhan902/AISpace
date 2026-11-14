"""Resume-safe 2x2 Ollama benchmark. No model receives test feedback."""
import argparse
import collections
import datetime
import hashlib
import json
import os
import platform
import subprocess
import time
import urllib.request
from pathlib import Path

import jsonschema
from dataset import ROOT, SEED, dumps, sha, verify

MODELS={"small":"qwen3:1.7b","large":"qwen3:4b"}
CARD_SCHEMA={"type":"object","properties":{
    "method_id":{"type":"string"}, "signature":{"type":"string"},
    "purpose":{"type":"string"}, "inputs":{"type":"string"},
    "output":{"type":"string"}, "algorithm":{"type":"array","items":{"type":"string"}},
    "edge_cases":{"type":"array","items":{"type":"string"}},
    "constraints":{"type":"array","items":{"type":"string"}}},
    "required":["method_id","signature","purpose","inputs","output","algorithm","edge_cases","constraints"],"additionalProperties":False}
CODE_SCHEMA={"type":"object","properties":{"code":{"type":"string"}},"required":["code"],"additionalProperties":False}
CARD_SYSTEM="""You write precise JSON behavioral specification cards for Python functions. Use only the supplied reference brief. Summarize the function in English so a separate programmer can implement it without the reference. Preserve the exact solve signature, input domain, output shape, sorting, boundary cases and error rules. Describe an algorithm in plain language or mathematical formulas, not Python source. Never include executable code. Do not invent extra requirements. The card must be self-contained. Return only JSON matching the schema."""
CODE_SYSTEM="""Implement a Python function from a JSON behavioral card. The card is the only task specification. Return a JSON object with a single string field code containing executable Python source. Define solve with the card's exact signature. Use only Python's standard library. Allowed imports: math, itertools, functools, collections, heapq, bisect, statistics, fractions, operator, typing. Do not import or call NumPy, SymPy, NetworkX or any other third-party library. Do not read files, use network, introspection, eval, exec, input or print. Implement computations yourself using built-ins and the allowed standard library. Return plain JSON-compatible values, not iterators or sets; use string keys in dictionaries. Include any helper functions in the code. No tests or main block. Raise ValueError where the card requires it."""
OPTIONS={"temperature":0,"seed":SEED,"num_ctx":8192,"num_predict":2048,"num_thread":4}
CONFIG={"models":MODELS,"think":False,"card_options":OPTIONS,"code_options":dict(OPTIONS,num_predict=3072),"card_schema":CARD_SCHEMA,"code_schema":CODE_SCHEMA,"card_system":CARD_SYSTEM,"code_system":CODE_SYSTEM,"generation_repeats":1,"case_timeout_seconds":.5,"method_timeout_seconds":45,"sequence":["cards_small","small_to_small","cards_large","large_to_large","small_to_large","large_to_small"]}

def api(path, body=None):
    req=urllib.request.Request("http://127.0.0.1:11434/api/"+path,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=600) as r: return json.load(r)

def write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(dumps(value)); tmp.replace(path)

def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def init():
    manifest=verify()
    conf=ROOT/"frozen/config.json"
    if conf.exists(): assert json.loads(conf.read_text())==CONFIG,"Config differs from frozen protocol"
    else: write(conf,CONFIG)
    environment=ROOT/"frozen/environment.json"
    current_tags=api("tags")
    if not environment.exists():
        write(environment,{"created_at":stamp(),"python":platform.python_version(),"platform":platform.platform(),"ollama_version":api("version"),"tags":current_tags,
            "model_details":{k:api("show",{"model":v}) for k,v in MODELS.items()},
            "hardware":subprocess.run(["nvidia-smi"],capture_output=True,text=True).stdout,
            "manifest_sha256":sha((ROOT/"frozen/manifest.json").read_bytes()),"config_sha256":sha(conf.read_bytes()),
            "pip_freeze":subprocess.run([str(ROOT/".venv/bin/python"),"-m","pip","freeze"],capture_output=True,text=True).stdout})
    else:
        env=json.loads(environment.read_text()); old={m['name']:m['digest'] for m in env['tags']['models']}; now={m['name']:m['digest'] for m in current_tags['models']}
        for model in MODELS.values(): assert old[model]==now[model],"Model digest changed"
        assert env['manifest_sha256']==sha((ROOT/'frozen/manifest.json').read_bytes())
    return manifest

def generate(path, model, system, user, schema, options):
    request={"model":MODELS[model],"messages":[{"role":"system","content":system},{"role":"user","content":user}],"format":schema,"stream":False,"think":False,"keep_alive":"30m","options":options}
    if path.exists():
        record=json.loads(path.read_text()); assert record["request"]==request; return record
    start=time.monotonic()
    record={"started_at":stamp(),"request":request}
    # No retries for model output failures. Transport failures stop the run and can be resumed.
    response=api("chat",request)
    record.update(response=response,elapsed_seconds=time.monotonic()-start,finished_at=stamp())
    try:
        parsed=json.loads(response["message"]["content"]); jsonschema.validate(parsed,schema)
        if response.get("done_reason")!="stop": raise ValueError("generation_truncated:"+str(response.get("done_reason")))
        record["parsed"]=parsed; record["valid"]=True
    except Exception as e: record.update(valid=False,error=type(e).__name__+":"+str(e)[:300])
    write(path,record)
    return record

def cards(manifest, producer):
    for i,s in enumerate(manifest["methods"],1):
        p=ROOT/"runs/cards"/producer/f"{s['id']}.json"
        data=json.loads((ROOT/"frozen"/f"{s['id']}.json").read_text())
        user="Create the specification card for this reference brief.\nJSON schema:\n"+dumps(CARD_SCHEMA)+"\nReference brief:\n"+dumps(data["brief"])
        rec=generate(p,producer,CARD_SYSTEM,user,CARD_SCHEMA,OPTIONS)
        if rec["valid"]: write(ROOT/"cards"/producer/f"{s['id']}.json",rec["parsed"])
        print(f"{stamp()} cards_{producer} {i}/45 {s['id']} valid={rec['valid']} {rec['elapsed_seconds']:.1f}s",flush=True)

def reconstruct(manifest, producer, consumer):
    condition=f"{producer}_to_{consumer}"
    for i,s in enumerate(manifest["methods"],1):
        card=json.loads((ROOT/"runs/cards"/producer/f"{s['id']}.json").read_text())
        path=ROOT/"runs/code"/condition/f"{s['id']}.json"
        if card["valid"]:
            rec=generate(path,consumer,CODE_SYSTEM,"Implement this card:\n"+dumps(card["parsed"]),CODE_SCHEMA,dict(OPTIONS,num_predict=3072))
            if rec["valid"]:
                codepath=ROOT/"implementations"/condition/f"{s['id']}.py"
                codepath.parent.mkdir(parents=True,exist_ok=True); codepath.write_text(rec["parsed"]["code"])
        else:
            rec={"valid":False,"error":"invalid_card","elapsed_seconds":0}; write(path,rec)
        evaluate(s,condition,rec)
        print(f"{stamp()} {condition} {i}/45 {s['id']} valid={rec['valid']} {rec['elapsed_seconds']:.1f}s",flush=True)

def sandbox(code, inputs):
    cmd=["bwrap","--unshare-all","--die-with-parent","--new-session","--ro-bind","/usr","/usr","--symlink","usr/lib","/lib","--symlink","usr/lib","/lib64","--symlink","usr/bin","/bin","--proc","/proc","--dev","/dev","--tmpfs","/tmp","--dir","/app","--ro-bind",str(ROOT/"worker.py"),"/app/worker.py","--chdir","/tmp","--clearenv","--setenv","PATH","/usr/bin","/usr/bin/python","-I","/app/worker.py"]
    try:
        p=subprocess.run(cmd,input=json.dumps({"code":code,"inputs":inputs}),text=True,capture_output=True,timeout=45)
        if p.returncode: return {"load_error":f"worker_exit_{p.returncode}","stderr":p.stderr[-2000:]}
        return json.loads(p.stdout)
    except subprocess.TimeoutExpired: return {"load_error":"method_timeout"}
    except Exception as e: return {"load_error":"sandbox_error:"+str(e)}

def equal(a,b):
    # bool must not be accepted as int; int and float are not interchangeable.
    if type(a) is not type(b): return False
    if isinstance(a,list): return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    if isinstance(a,dict): return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    return a==b

def evaluate(spec, condition, rec):
    path=ROOT/"results"/condition/f"{spec['id']}.json"
    if path.exists(): return json.loads(path.read_text())
    cases=json.loads((ROOT/"frozen"/f"{spec['id']}.json").read_text())["cases"]
    start=time.monotonic()
    result={"method_id":spec["id"],"library":spec["library"],"group":spec["group"],"condition":condition,"total":len(cases)}
    if rec["valid"]: worker=sandbox(rec["parsed"]["code"],[c["input"] for c in cases])
    else: worker={"load_error":rec.get("error","invalid_generation")}
    rows=[]
    for i,c in enumerate(cases):
        observed=worker.get("outputs",[])[i] if i<len(worker.get("outputs",[])) else {"error":worker.get("load_error","missing_output")}
        expected=c["expected"]
        passed=(expected["error"]==observed.get("error")) if "error" in expected else ("value" in observed and equal(expected["value"],observed["value"]))
        rows.append({"case_id":c["id"],"category":c["category"],"passed":passed,"expected":expected,"observed":observed,"input":c["input"]})
    result.update(passed=sum(r["passed"] for r in rows),all_pass=all(r["passed"] for r in rows),load_error=worker.get("load_error"),elapsed_seconds=time.monotonic()-start,cases=rows)
    write(path,result); return result

def selftest():
    r=sandbox("def solve(n):\n    return n * n\n",[{"n":4}]); assert r=={"outputs":[{"value":16}]},r
    assert 'forbidden_import' in sandbox("import numpy\ndef solve(): return 1",[{}])["load_error"]
    r=sandbox("def solve():\n    raise ValueError('expected')",[{}]); assert r['outputs'][0]['error']=='ValueError'
    r=sandbox("def solve():\n    while True: pass",[{}]); assert r['outputs'][0]['error']=='CaseTimeout'
    assert not equal(True,1) and not equal(1,1.0) and equal({"a":[1]}, {"a":[1]})
    print("Sandbox, import restrictions, timeout, exception and strict-comparison checks passed.")

def run():
    manifest=init(); selftest()
    for producer,consumer in [("small",None),("small","small"),("large",None),("large","large"),("small","large"),("large","small")]:
        if consumer is None: cards(manifest,producer)
        else: reconstruct(manifest,producer,consumer)
    print("EXPERIMENT_COMPLETE",flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("action",choices=["run","selftest","init"]); args=p.parse_args()
    {"run":run,"selftest":selftest,"init":init}[args.action]()
