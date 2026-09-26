"""Whole-page reading for pages whose line boxes are missing or shared (K1v shares one box for 7 lines; pp. 4/11/12/57-60
and K1r had lines without boxes). The vFlat scan is sent at native resolution as two overlapping halves; each reader
transcribes every verse line of the main text in order (no tags, headings, notes). Each target edition line is then
aligned to the most similar page-read line (letters-only similarity). Output: reads/page_<tag>.json {id: text, _sim}."""
import json,sys,base64,io,os,re,time,difflib,urllib.request,unicodedata
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
H=Path(__file__).parent
E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[2]))/'capilupi'/'edition.json'))
SRC=json.load(open(H/'crops.json'))
bad={}
for p in E['pages']:
    for k,l in enumerate(p['lines']):
        iid=f"f{p['vflat']}.v{l['n']}" if l.get('n') is not None else f"f{p['vflat']}.u{k}"
        if p['vflat']==40 or not SRC[iid].startswith('vflat'): bad.setdefault(p['vflat'],[]).append((iid,l['orig']))
SYS=("You transcribe a page of Latin verse printed in Rome c.1555 (italic type), given as two overlapping halves of one "
 "photograph (top, then bottom). Transcribe EVERY line of the main text block, top to bottom, one per list item, including "
 "headings only if they are part of the verse block. Ignore marginal source tags such as 'Æ.IX.', 'G.III.', marginal notes, "
 "page numbers, running heads and catchwords. Lines in the overlap appear in both halves: list each printed line once. "
 "Transcribe diplomatically as printed: u/v and i/j as printed, æ œ ligatures, '&', 'q;', tilde/macron vowels and accents as "
 "printed, punctuation as printed, long s as s; no corrections, no completion from memory; unreadable letters as [?]. "
 "Return ONLY JSON {\"lines\": [\"...\", ...]}.")
def b64(im):
    b=io.BytesIO(); im.convert('RGB').save(b,'JPEG',quality=90); return base64.b64encode(b.getvalue()).decode()
def call(model,vf):
    im=Image.open(H/'scans'/f'Capilupi - {vf}.jpg'); W,Hh=im.size
    halves=[im.crop((0,0,W,int(Hh*0.56))),im.crop((0,int(Hh*0.44),W,Hh))]
    content=[{"type":"text","text":"Top half, then bottom half:"}]+[{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+b64(h)}} for h in halves]
    body=json.dumps({"model":model,"messages":[{"role":"system","content":SYS},{"role":"user","content":content}],"temperature":0,"max_tokens":16000}).encode()
    req=urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=body,headers={"Authorization":"Bearer "+os.environ['OPENROUTER_API_KEY'],"Content-Type":"application/json"})
    for k in range(4):
        try:
            r=json.load(urllib.request.urlopen(req,timeout=600)); t=r['choices'][0]['message'].get('content') or ''
            return json.loads(re.search(r'\{.*\}',t,re.S).group())['lines']
        except Exception as e: err=e; time.sleep(10*(k+1))
    raise err
def norm(t):
    t=unicodedata.normalize('NFD',str(t).replace('&','et').replace('æ','ae').replace('œ','oe'))
    return re.sub(r'[^a-z]','',''.join(c for c in t if not unicodedata.combining(c)).lower().replace('v','u').replace('j','i'))
model=sys.argv[1]; tag=model.replace('/','__'); out={}
for vf,targets in bad.items():
    lines=call(model,vf)
    for iid,orig in targets:
        best=max(lines,key=lambda x:difflib.SequenceMatcher(None,norm(x),norm(orig)).ratio())
        out[iid]=best; out[iid+'_sim']=round(difflib.SequenceMatcher(None,norm(best),norm(orig)).ratio(),2)
    print(model,vf,len(lines),'lines read,',len(targets),'targets',flush=True)
json.dump(out,open(H/'reads'/f'page_{tag}.json','w'),ensure_ascii=False,indent=1)
