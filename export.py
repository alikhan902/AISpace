"""Package the final observations without environments or model weights."""
import hashlib
import json
import zipfile
from pathlib import Path
from dataset import ROOT, dumps

def main():
    audit=json.loads((ROOT/'audit.json').read_text()); assert audit['complete'], 'Run audit.py after completion'
    for producer,label in [('small','1_7b'),('large','4b')]:
        paths=sorted((ROOT/'cards'/producer).glob('*.json'))
        assert len(paths)==45
        (ROOT/f'cards_qwen3_{label}.json').write_text(dumps([json.loads(p.read_text()) for p in paths]))
    dirs=['frozen','cards','runs','implementations','results','LICENSES']
    files=[]
    for directory in dirs:
        files.extend(p for p in (ROOT/directory).rglob('*') if p.is_file())
    files.extend(p for p in ROOT.iterdir() if p.is_file() and p.suffix in ['.py','.md','.json','.txt'] and p.name!='ARTIFACT_SHA256.json')
    files=sorted(set(files))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    checks=ROOT/'ARTIFACT_SHA256.json'; checks.write_text(dumps(hashes)); files.append(checks)
    archive=ROOT/'qwen_method_benchmark_results.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files: z.write(p,str(p.relative_to(ROOT)))
    print(dumps({'archive':str(archive),'bytes':archive.stat().st_size,'files':len(files)}))

if __name__=='__main__': main()
