"""Blind diplomatic reading of every line crop (the reader never sees the edition text). Batches of 12 crops per call.
Usage: python3 read.py <model> -> reads/<tag>.json {id: text}. Resumable per batch."""
import json,sys,base64,os,re,time,urllib.request,threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
H=Path(__file__).parent
SYS=("You transcribe lines of Latin verse from photographs of a book printed in Rotterdam in 1653 (italic type). Each image shows ONE verse of this small-format book: its first printed line and, below it, the next printed line. A long verse is often completed by a TURNOVER: an indented continuation on the next printed line, often with the first line ending in a hyphen (e.g. 'um-' then 'bræ,'). If the lower line is an indented turnover, transcribe the whole verse as ONE line, joining a hyphenated word without the hyphen; if the lower line is a new verse starting at the left margin, IGNORE it. Ignore marginal source tags such as 'E.3.E.10' at the right. "
 "crop centred on ONE printed line; parts of the lines above and below may show — transcribe ONLY the central, complete line. "
 "Ignore marginal source tags such as 'Æ.IX.', 'G.III.', 'EC.V.' at the left or right edge. Transcribe diplomatically, exactly "
 "as printed: keep u/v and i/j as printed, keep æ and œ ligatures, '&' for the ampersand, 'q;' for the q-semicolon "
 "abbreviation, vowels with a tilde (ũ, ẽ, ã, õ, standing for a following m or n) as printed, NOT expanded, accents (à, ò, ù, é, q́) as printed, punctuation as "
 "printed; write long s as s. Keep capitals as printed. Do not correct misprints; do not normalise to classical spelling; "
 "do not complete damaged words from memory of Virgil — if a letter is unreadable write [?]. Return ONLY JSON mapping each "
 "image id to its transcription.")
def call(model,batch):
    content=[{"type":"text","text":"Image ids in order: "+", ".join(batch)}]
    for i in batch:
        content+= [{"type":"text","text":f"id {i}:"},{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+base64.b64encode(open(H/os.environ.get('CROPS','crops')/f'{i}.jpg','rb').read()).decode()}}]
    body=json.dumps({"model":model,"messages":[{"role":"system","content":SYS},{"role":"user","content":content}],"temperature":0,"max_tokens":12000}).encode()
    req=urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=body,headers={"Authorization":"Bearer "+os.environ['OPENROUTER_API_KEY'],"Content-Type":"application/json"})
    for k in range(5):
        try:
            r=json.load(urllib.request.urlopen(req,timeout=300)); t=r['choices'][0]['message'].get('content') or ''
            return json.loads(re.search(r'\{.*\}',t,re.S).group()),float(r.get('usage',{}).get('cost',0) or 0)
        except Exception as e: err=e; time.sleep(8*(k+1))
    raise err
model=sys.argv[1]; tag=model.replace('/','__')+os.environ.get('TAG',''); (H/'reads').mkdir(exist_ok=True); part=H/'reads'/f'{tag}.partial.json'
st=json.load(open(part)) if part.exists() else {'out':{},'cost':0}
ids=sorted(json.load(open(H/os.environ.get('IDS','crops.json'))),key=lambda s:(int(s.split('.')[0][1:]),s))
todo=[i for i in ids if i not in st['out']]; batches=[todo[k:k+12] for k in range(0,len(todo),12)]; lk=threading.Lock()
def do(b):
    try: tr,c=call(model,b)
    except Exception as e: print('FAIL',b[0],repr(e)[:80],flush=True); return
    with lk:
        st['out'].update({k:v for k,v in tr.items() if k in b}); st['cost']+=c; json.dump(st,open(part,'w'),ensure_ascii=False)
        print(len(st['out']),'/',len(ids),round(st['cost'],2),flush=True)
with ThreadPoolExecutor(8) as ex: list(ex.map(do,batches))
miss=[i for i in ids if i not in st['out']]
json.dump(dict(model=model,cost=st['cost'],missing=miss,reads=st['out']),open(H/'reads'/f'{tag}.json','w'),ensure_ascii=False,indent=1); print('DONE missing',len(miss),'cost',round(st['cost'],2))
