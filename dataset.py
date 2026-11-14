"""Frozen, exact-valued behavioral benchmark. Models never receive test cases."""
import hashlib
import inspect
import itertools
import json
import random
from pathlib import Path

import numpy as np
import sympy as sp
import networkx as nx

ROOT = Path(__file__).resolve().parent
SEED = 20261114
VERSIONS = {"numpy": np.__version__, "sympy": sp.__version__, "networkx": nx.__version__}

def dumps(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2)

def sha(x):
    return hashlib.sha256(x).hexdigest()

def normalize(x):
    if isinstance(x, np.ndarray):
        return normalize(x.tolist())
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer, sp.Integer)):
        return int(x)
    if isinstance(x, dict):
        return {str(k): normalize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [normalize(v) for v in x]
    return x

ARRAY = "a is a one-dimensional list of integers, possibly empty. Return Python int or list[int], as appropriate; no NumPy objects. All intermediate values fit signed int64."
GRAPH = "n is an integer >= 1; vertices are 0,...,n-1. edges is a list of distinct [u,v] pairs with 0<=u<v<n. Construct a simple undirected unweighted graph including isolated vertices. Return plain JSON-compatible Python values. Dictionary vertex keys must be strings."

def specs():
    out = []
    def add(lib, group, name, signature, contract):
        out.append(dict(id=f"{lib}.{name}", library=lib, group=group, name=name,
                        signature=signature, contract=contract))
    for name in ["sum", "prod", "cumsum", "cumprod"]:
        add("numpy", "reductions", name, "solve(a)", ARRAY + " Use NumPy's default operation on the whole 1-D list, with dtype=int64.")
    add("numpy", "reductions", "diff", "solve(a, n=1)", ARRAY + " n is an integer from 0 to 5. Compute the n-th discrete forward difference; n=0 returns a copy of a. If n>=len(a), the result is empty unless n=0.")
    for name in ["gcd", "lcm", "floor_divide", "remainder", "power"]:
        domain = "x and y are integers or 1-D lists of integers. Support scalar/scalar, scalar/list, list/scalar and lists of the same length (including empty). Scalar/scalar returns int, all other inputs return a list. No other broadcasting is required. Values and results fit signed int64."
        domain += " Divisors are nonzero." if name in ["floor_divide", "remainder"] else ""
        domain += " Exponents are integers in 0..8; define 0**0 as 1." if name == "power" else ""
        add("numpy", "integer_arithmetic", name, "solve(x, y)", domain)
    add("numpy", "ordering_counting", "unique", "solve(a)", ARRAY + " Use default unique behavior: sorted distinct values only, no indices or counts.")
    add("numpy", "ordering_counting", "bincount", "solve(a, minlength=0)", "a is a list of nonnegative integers; minlength is a nonnegative integer. Return the int count list with NumPy's default unweighted behavior. Empty input is allowed.")
    add("numpy", "ordering_counting", "searchsorted", "solve(a, v, side='left')", "a is a nondecreasing list of integers, possibly empty; v is an integer or list of integers; side is 'left' or 'right'. Return int for scalar v and list[int] for list v. No sorter argument.")
    add("numpy", "ordering_counting", "sort", "solve(a)", ARRAY + " Return ascending sorted values; no in-place modification is required.")
    add("numpy", "ordering_counting", "count_nonzero", "solve(a)", ARRAY + " Return a single Python int counting nonzero values.")
    for name in ["factorial", "fibonacci", "lucas", "catalan"]:
        upper = 35 if name in ["factorial", "catalan"] else 100
        add("sympy", "combinatorics", name, "solve(n)", f"n is an integer in 0..{upper}. Return the exact Python int, with arbitrary precision; no symbolic result.")
    add("sympy", "combinatorics", "binomial", "solve(n, k)", "n is an integer in 0..50; k is an integer in -3..55. Return the exact Python int binomial coefficient, including zero when k<0 or k>n.")
    for name in ["divisors", "divisor_count", "totient", "mobius"]:
        add("sympy", "divisors", name, "solve(n)", "n is a positive integer <=5000. Return an exact Python int, except divisors returns an ascending list of all positive divisors. For divisors use generator=False, proper=False; divisor_count uses default modulus=1, proper=False.")
    add("sympy", "divisors", "divisor_sigma", "solve(n, k=1)", "n is a positive integer <=1000, k is an integer in 0..4. Return an exact Python int.")
    for name in ["isprime", "nextprime", "prevprime", "primefactors", "factorint"]:
        dom = "n is an integer in -20..10000." if name == "isprime" else "n is a positive integer <=5000."
        if name == "nextprime": dom = "n is an integer in -10..5000. Use ith=1, the first prime strictly greater than n."
        if name == "prevprime": dom = "n is an integer in 3..5000. Return the prime strictly less than n."
        typ = {"isprime": "bool", "nextprime": "int", "prevprime": "int", "primefactors": "ascending list of distinct positive prime factors", "factorint": "dict with string prime keys and integer multiplicities (1 gives {})"}[name]
        add("sympy", "primes", name, "solve(n)", dom + f" Return a plain Python {typ}, no symbolic objects.")
    for name in ["number_connected_components", "connected_components", "is_connected", "is_tree", "is_bipartite"]:
        typ = "Return components as internally sorted lists, with the outer list lexicographically sorted." if name == "connected_components" else "Return int for number_connected_components and bool for predicates."
        add("networkx", "connectivity", name, "solve(n, edges)", GRAPH + " " + typ)
    add("networkx", "distances", "shortest_path_length", "solve(n, edges, source, target)", GRAPH + " source and target are valid vertices. Return the integer shortest-path length; raise ValueError if there is no path. source==target returns 0.")
    add("networkx", "distances", "single_source_shortest_path_length", "solve(n, edges, source)", GRAPH + " source is a valid vertex. Return a dict with string vertex keys and integer shortest-path lengths for reachable nodes only; include source:0. No cutoff.")
    for name in ["eccentricity", "diameter", "radius"]:
        add("networkx", "distances", name, "solve(n, edges)", GRAPH + " Return a dict of every vertex's eccentricity for eccentricity (string keys), otherwise an int. For a disconnected graph raise ValueError. A singleton has eccentricity, diameter and radius 0.")
    for name in ["triangles", "bridges", "articulation_points", "core_number"]:
        typ = {"triangles":"Return a dict mapping every string vertex key to its integer triangle count.", "bridges":"Return sorted [u,v] bridge pairs with u<v, lexicographically sorted. Work across all components.", "articulation_points":"Return an ascending list of articulation vertices, across all components.", "core_number":"Return a dict mapping every string vertex key to its integer core number, including isolated vertices."}[name]
        add("networkx", "local_structure", name, "solve(n, edges)", GRAPH + " " + typ)
    add("networkx", "local_structure", "node_connected_component", "solve(n, edges, node)", GRAPH + " node is a valid vertex. Return the ascending list of vertices in its component, including node.")
    assert len(out) == 45
    return out

def oracle(spec, kw):
    lib, name = spec["library"], spec["name"]
    if lib == "numpy":
        f = getattr(np, name)
        if name in ["sum", "prod", "cumsum", "cumprod"]:
            value = f(np.array(kw["a"], dtype=np.int64), dtype=np.int64)
        elif name in ["gcd", "lcm", "floor_divide", "remainder", "power"]:
            value = f(np.asarray(kw["x"], dtype=np.int64), np.asarray(kw["y"], dtype=np.int64))
        elif name == "searchsorted":
            value = f(np.asarray(kw["a"], dtype=np.int64), kw["v"], side=kw.get("side", "left"))
        else:
            args = dict(kw); a = np.asarray(args.pop("a"), dtype=np.int64)
            value = f(a, **args)
    elif lib == "sympy":
        args = [kw["n"]]
        if "k" in kw: args.append(kw["k"])
        value = getattr(sp, name)(*args)
    else:
        g = nx.Graph(); g.add_nodes_from(range(kw["n"])); g.add_edges_from(kw["edges"])
        args = {k:v for k,v in kw.items() if k not in ["n", "edges"]}
        if "node" in args: args["n"] = args.pop("node")
        try:
            value = getattr(nx, name)(g, **args)
        except (nx.NetworkXNoPath, nx.NetworkXError) as e:
            raise ValueError(str(e)) from e
        if name == "connected_components": value = sorted(sorted(c) for c in value)
        if name == "node_connected_component": value = sorted(value)
        if name == "bridges": value = sorted(sorted(e) for e in value)
        if name == "articulation_points": value = sorted(value)
    return normalize(value)

def cases_for(spec):
    rng = random.Random(SEED + int(sha(spec["id"].encode())[:8], 16))
    lib, name = spec["library"], spec["name"]
    cases, seen = [], set()
    def add(kw, category):
        key = dumps(kw)
        if key not in seen:
            seen.add(key); cases.append({"input":kw,"category":category})
    if lib == "numpy":
        arrays = [[],[0],[1],[-1],[0,0],[1,1,1],[-3,-2,-1],[3,-1,0,3,-1],[5,4,3,2,1],[-2,2,-2,2]]
        arrays += [[rng.randint(-3,3) for _ in range(rng.randint(0,12))] for _ in range(130)]
        if name in ["gcd","lcm","floor_divide","remainder","power"]:
            for x in range(-7,8):
                for y in range(0,6) if name == "power" else range(-7,8):
                    if y==0 and name in ["floor_divide","remainder"]: continue
                    add(dict(x=x,y=y), "exhaustive")
            for i in range(90):
                size = rng.randrange(0,12)
                x = [rng.randint(-12,12) for _ in range(size)]
                y = [rng.randrange(0,9) if name=="power" else rng.choice([j for j in range(-12,13) if j or name not in ["floor_divide","remainder"]]) for _ in range(size)]
                if i%3==0: x=rng.randint(-10,10)
                if i%3==1: y=rng.randrange(0,9) if name=="power" else rng.choice([-7,-1,1,7])
                add(dict(x=x,y=y),"random")
        else:
            for i,a in enumerate(arrays):
                cat = "boundary" if i<10 else "random"
                if name == "diff":
                    for n in range(6): add(dict(a=a,n=n),cat)
                elif name == "bincount":
                    for ml in [0,1,5,10]: add(dict(a=[abs(x) for x in a],minlength=ml),cat)
                elif name == "searchsorted":
                    for side in ["left","right"]:
                        add(dict(a=sorted(a),v=list(range(-5,6)),side=side),cat)
                        add(dict(a=sorted(a),v=rng.randrange(-5,6),side=side),cat)
                else: add(dict(a=a),cat)
    elif lib == "sympy":
        if name == "binomial":
            for n in range(0,16):
                for k in range(-2,n+3): add(dict(n=n,k=k),"exhaustive")
            for i in range(100): add(dict(n=rng.randrange(16,51),k=rng.randrange(-3,56)),"random")
        elif name == "divisor_sigma":
            for n in list(range(1,40))+[rng.randrange(40,1001) for _ in range(90)]:
                for k in range(5): add(dict(n=n,k=k),"exhaustive" if n<40 else "random")
        elif name in ["factorial","catalan","fibonacci","lucas"]:
            for n in range(36 if name in ["factorial","catalan"] else 101): add(dict(n=n),"exhaustive")
        else:
            lo = -20 if name=="isprime" else -10 if name=="nextprime" else 3 if name=="prevprime" else 1
            for n in range(lo,101): add(dict(n=n),"exhaustive")
            for n in [121,169,221,341,561,1105,1729,2047,4096,4999,5000]+[rng.randint(101,5000) for _ in range(150)]: add(dict(n=n),"random")
            if name=="isprime":
                for n in [7919,8191,9999,10000]: add(dict(n=n),"boundary")
    else:
        graphs=[]
        for n in range(1,5):
            pairs=list(itertools.combinations(range(n),2))
            for mask in range(1<<len(pairs)):
                graphs.append((n,[list(e) for j,e in enumerate(pairs) if mask>>j&1],"exhaustive"))
        for n in [5,6,8,12]:
            graphs += [(n,[],"boundary"),(n,[[i,i+1] for i in range(n-1)],"boundary"),(n,[[0,i] for i in range(1,n)],"boundary"),(n,[list(e) for e in itertools.combinations(range(n),2)],"boundary")]
        for i in range(100):
            n=rng.randint(5,12); p=rng.choice([.1,.2,.4,.6,.9])
            graphs.append((n,[list(e) for e in itertools.combinations(range(n),2) if rng.random()<p],"random"))
        for n,edges,cat in graphs:
            kw=dict(n=n,edges=edges)
            if name=="shortest_path_length":
                for s,t in [(0,0),(0,n-1),(n-1,0),(rng.randrange(n),rng.randrange(n))]: add(dict(kw,source=s,target=t),cat)
            elif name=="single_source_shortest_path_length":
                for s in sorted({0,n-1}): add(dict(kw,source=s),cat)
            elif name=="node_connected_component":
                for v in sorted({0,n-1}): add(dict(kw,node=v),cat)
            else: add(kw,cat)
    for i,c in enumerate(cases):
        c["id"] = f"{spec['id']}:{i:04d}"
        try: c["expected"]={"value":oracle(spec,c["input"])}
        except ValueError: c["expected"]={"error":"ValueError"}
    return cases

KNOWN = {
"numpy.sum": ({"a":[-2,0,3]},1), "numpy.prod": ({"a":[]},1),
"numpy.cumsum": ({"a":[2,-3,4]},[2,-1,3]), "numpy.cumprod": ({"a":[-2,3,0]},[-2,-6,0]),
"numpy.diff": ({"a":[1,4,9,16],"n":2},[2,2]), "numpy.gcd": ({"x":-12,"y":18},6),
"numpy.lcm": ({"x":-12,"y":18},36), "numpy.floor_divide": ({"x":-7,"y":3},-3),
"numpy.remainder": ({"x":-7,"y":3},2), "numpy.power": ({"x":[0,-2],"y":[0,3]},[1,-8]),
"numpy.unique": ({"a":[3,-1,3,0]},[-1,0,3]), "numpy.bincount": ({"a":[2,2,0],"minlength":5},[1,0,2,0,0]),
"numpy.searchsorted": ({"a":[1,2,2,4],"v":[0,2,5],"side":"right"},[0,3,4]),
"numpy.sort": ({"a":[2,-1,2]},[-1,2,2]), "numpy.count_nonzero": ({"a":[0,-1,2,0]},2),
"sympy.factorial": ({"n":6},720), "sympy.binomial": ({"n":5,"k":7},0),
"sympy.fibonacci": ({"n":10},55), "sympy.lucas": ({"n":0},2), "sympy.catalan": ({"n":5},42),
"sympy.divisors": ({"n":12},[1,2,3,4,6,12]), "sympy.divisor_count": ({"n":12},6),
"sympy.divisor_sigma": ({"n":12,"k":2},210), "sympy.totient": ({"n":1},1), "sympy.mobius": ({"n":30},-1),
"sympy.isprime": ({"n":561},False), "sympy.nextprime": ({"n":7},11), "sympy.prevprime": ({"n":7},5),
"sympy.primefactors": ({"n":360},[2,3,5]), "sympy.factorint": ({"n":360},{"2":3,"3":2,"5":1})}

def validate_oracle(items):
    g={"n":4,"edges":[[0,1],[1,2],[1,3]]}
    graph_values={"number_connected_components":1,"connected_components":[[0,1,2,3]],"is_connected":True,"is_tree":True,"is_bipartite":True,"shortest_path_length":2,"single_source_shortest_path_length":{"0":0,"1":1,"2":2,"3":2},"eccentricity":{"0":2,"1":1,"2":2,"3":2},"diameter":2,"radius":1,"triangles":{"0":0,"1":0,"2":0,"3":0},"bridges":[[0,1],[1,2],[1,3]],"articulation_points":[1],"core_number":{"0":1,"1":1,"2":1,"3":1},"node_connected_component":[0,1,2,3]}
    for s in items:
        if s["library"]=="networkx":
            kw=dict(g)
            if s["name"]=="shortest_path_length": kw.update(source=0,target=2)
            if s["name"]=="single_source_shortest_path_length": kw.update(source=0)
            if s["name"]=="node_connected_component": kw.update(node=2)
            expected=graph_values[s["name"]]
        else: kw,expected=KNOWN[s["id"]]
        assert dumps(oracle(s,kw))==dumps(expected),(s["id"],kw)

def prepare():
    target=ROOT/"frozen"
    if (target/"manifest.json").exists():
        verify(); print("Frozen dataset already exists and hashes match."); return
    target.mkdir(exist_ok=True)
    items=specs(); validate_oracle(items)
    manifest={"seed":SEED,"versions":VERSIONS,"selection":"purposive: 3 libraries x 3 subject groups x 5 functions; no sampled population claim", "methods":[]}
    for s in items:
        module={"numpy":np,"sympy":sp,"networkx":nx}[s["library"]]
        doc=inspect.getdoc(getattr(module,s["name"])) or ""
        # Documentation, not hidden tests or hand-written reference implementations.
        brief=dict(s,version=VERSIONS[s["library"]],documentation=doc[:9000],documentation_truncated=len(doc)>9000)
        case=cases_for(s)
        payload={"brief":brief,"cases":case}
        data=dumps(payload).encode(); (target/f"{s['id']}.json").write_bytes(data)
        manifest["methods"].append(dict(s,case_count=len(case),sha256=sha(data),doc_sha256=sha(doc.encode()),documentation_truncated=len(doc)>9000))
    (target/"manifest.json").write_text(dumps(manifest))
    print(dumps({"methods":len(items),"tests":sum(s['case_count'] for s in manifest['methods']),"versions":VERSIONS,"oracle_known_checks":45}))

def verify():
    m=json.loads((ROOT/"frozen/manifest.json").read_text())
    assert VERSIONS==m["versions"], "Library versions changed"
    for s in m["methods"]: assert sha((ROOT/"frozen"/f"{s['id']}.json").read_bytes())==s["sha256"],s["id"]
    return m

if __name__=="__main__": prepare()
