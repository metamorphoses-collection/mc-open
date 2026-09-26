import json,os,re,time,urllib.request,urllib.error
from pathlib import Path
H=Path(__file__).parent
BOOK=("the Centones ex Virgilio of Lelio Capilupi (Rome, Valerio Dorico, c.1555), edited by Antonio Possevino: twelve "
 "Virgilian centos (I Gallus, II De vita monachorum — a satire on monks, III In foeminas — a satire on women, IIII Aristeus, "
 "V Damon, VI Gonzaga, VII Medici, VIII Este, IX Homerus, X Roma, XI Fortuna, XII Salutatio), each composed of lines and "
 "half-lines of Virgil, with prose prefaces, printed side-notes, a closing exchange with Benedetto Egio, and an address by Fulvio Orsini")
def call(model,system,user,attempts=6,max_tokens=16000):
    body=json.dumps({"model":model,"messages":[{"role":"system","content":system},{"role":"user","content":user}],
                     "temperature":0,"max_tokens":max_tokens}).encode()
    req=urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=body,
        headers={"Authorization":"Bearer "+os.environ['OPENROUTER_API_KEY'],"Content-Type":"application/json"})
    err=None
    for k in range(attempts):
        try:
            r=json.load(urllib.request.urlopen(req,timeout=900)); t=r['choices'][0]['message'].get('content') or ''
            m=re.search(r'\{.*\}',t,re.S)
            if not m: raise ValueError('no JSON: '+t[:200])
            return json.loads(m.group()),r.get('usage',{})
        except urllib.error.HTTPError as e: err=e; time.sleep(30*(k+1) if e.code==429 else 8*(k+1))
        except Exception as e: err=e; time.sleep(8*(k+1))
    raise err
def pages(): return json.load(open(H/'items.json'))['pages']
def drafts(tag):
    f=H/'outputs'/f'{tag}.json'
    if not f.exists(): f=H/'outputs'/f'{tag}.partial.json'
    d=json.load(open(f)); return d.get('translations') or d.get('out')
