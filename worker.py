"""Runs only inside bubblewrap; receives code and inputs, never oracle outputs."""
import ast
import builtins
import contextlib
import copy
import io
import json
import resource
import signal
import sys

resource.setrlimit(resource.RLIMIT_CPU, (30, 31))
resource.setrlimit(resource.RLIMIT_AS, (768*1024**2, 768*1024**2))
resource.setrlimit(resource.RLIMIT_FSIZE, (1024**2, 1024**2))
resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
ALLOWED={"math","itertools","functools","collections","heapq","bisect","statistics","fractions","operator","typing"}
FORBIDDEN={"eval","exec","compile","open","input","globals","locals","vars","getattr","setattr","delattr","__import__","breakpoint","help","dir","exit","quit"}

class CaseTimeout(Exception): pass

def alarm(*args): raise CaseTimeout()
signal.signal(signal.SIGALRM, alarm)

def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level or name.split('.')[0] not in ALLOWED: raise ImportError("Import is not allowed: "+name)
    return builtins.__import__(name,globals,locals,fromlist,level)

def validate_value(value):
    if type(value) in (type(None),bool,int,float,str): return
    if type(value) is list:
        for v in value: validate_value(v)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for v in value.values(): validate_value(v)
        return
    raise TypeError("Return value must use plain JSON types and string dictionary keys")

def main():
    request=json.load(sys.stdin)
    try:
        code=request["code"]
        if len(code)>64000: raise ValueError("code_too_long")
        tree=ast.parse(code)
        for n in ast.walk(tree):
            if isinstance(n,(ast.Import,ast.ImportFrom)):
                modules=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module or ""]
                if any(m.split('.')[0] not in ALLOWED for m in modules): raise ValueError("forbidden_import")
                if isinstance(n,ast.ImportFrom) and n.level: raise ValueError("relative_import")
            if isinstance(n,ast.Attribute) and n.attr.startswith('_'): raise ValueError("private_attribute")
            if isinstance(n,ast.Name) and (n.id in FORBIDDEN or n.id.startswith('__')): raise ValueError("forbidden_name:"+n.id)
        safe={k:v for k,v in vars(builtins).items() if k not in FORBIDDEN and not k.startswith('_')}
        safe['__import__']=safe_import
        ns={"__builtins__":safe,"__name__":"candidate"}
        signal.setitimer(signal.ITIMER_REAL, 2)
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(tree,"candidate.py","exec"),ns)
        signal.setitimer(signal.ITIMER_REAL,0)
        if not callable(ns.get("solve")): raise ValueError("missing_solve")
    except BaseException as e:
        print(json.dumps({"load_error":type(e).__name__+":"+str(e)[:300]})); return
    outputs=[]
    for kw in request["inputs"]:
        try:
            signal.setitimer(signal.ITIMER_REAL, .5)
            with contextlib.redirect_stdout(io.StringIO()): value=ns["solve"](**copy.deepcopy(kw))
            validate_value(value)
            # Reject coercions such as tuple->list and int dictionary keys->string.
            value=json.loads(json.dumps(value,allow_nan=False))
            if len(json.dumps(value))>100000: raise ValueError("output_too_large")
            outputs.append({"value":value})
        except BaseException as e:
            outputs.append({"error":type(e).__name__,"message":str(e)[:300]})
        finally: signal.setitimer(signal.ITIMER_REAL,0)
    print(json.dumps({"outputs":outputs}))

if __name__=="__main__": main()
