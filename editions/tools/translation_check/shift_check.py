"""Editorial rule (25 Sep 2026): a SHIFT is acceptable if the sense is correct and not lost. For each SHIFT, Opus 5.5 reads the
target and its +/-2 neighbours (Latin + published English) and answers: taken TOGETHER, does the published English of this
line and its neighbours render the target's Latin correctly and completely? KEPT = sense carried (content only moved across
the line break) -> leave; LOST = a content word/clause of the target is rendered nowhere, or is wrong, or the English belongs
to another passage -> goes to polish. Resumable cache. Writes shift_check.json {id: {sense, why}}."""
import json,threading
from concurrent.futures import ThreadPoolExecutor
from lib import H,BOOK,call,pages
T=json.load(open(H/'triage.json'))
T=[r for r in T if r['triage']=='SHIFT']
PG={p['page']:p['items'] for p in pages()}
SYS=("You check the English facing "+BOOK+" line by line. Word order across line breaks is free: content may legitimately "
 "sit on the neighbouring English line. For the TARGET Latin line, read the published English of the target AND its "
 "neighbours together. Answer KEPT if every content word of the target Latin is rendered correctly somewhere in that "
 "English (moved across the line break is fine). Answer LOST if any content word or clause of the target is rendered "
 "nowhere, or rendered wrongly, or if the English beside it belongs to a different passage. Return ONLY JSON "
 "{\"sense\": \"KEPT|LOST\", \"why\": \"<=20 words; for LOST name the missing/wrong Latin word\"}.")
C=H/'cache_shift'; C.mkdir(exist_ok=True); n=[0]; lk=threading.Lock()
def do(r):
    c=C/(r['id']+'.json')
    if c.exists(): return r['id'],json.load(open(c))
    its=PG[r['id'].split('.')[0]]; k=[i['id'] for i in its].index(r['id'])
    ctx=[dict(id=i['id'],latin=i['la'],published=i['en_edition'],target=i['id']==r['id']) for i in its[max(0,k-2):k+3]]
    try: v,_=call('anthropic/claude-opus-5.5',SYS,json.dumps(dict(target=r['id'],context=ctx),ensure_ascii=False),max_tokens=2000)
    except Exception as e: return r['id'],{'sense':'FAILED','why':repr(e)[:100]}
    json.dump(v,open(c,'w'),ensure_ascii=False)
    with lk:
        n[0]+=1
        if n[0]%100==0: print('progress',n[0],flush=True)
    return r['id'],v
with ThreadPoolExecutor(16) as ex: out=dict(ex.map(do,T))
json.dump(out,open(H/'shift_check.json','w'),ensure_ascii=False,indent=1)
import collections; print(len(out),collections.Counter(v.get('sense') for v in out.values()))
