"""Second attempt on English lines whose re-fit was held by the blind check. Opus 5.5 sees the corrected Latin (live),
the current English, the rejected attempt, and +/-2 neighbours; writes a line or keeps the current one. Grok 4.7 compares
new vs current blind; apply only if new is judged better and correct. Writes en_held.json."""
import os
import json,sys,random,collections
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'translation_check'))
from lib import call,BOOK
held={}
for f in ('en_recheck.json','en_recheck_adj.json','en_recheck_adj3.json','en_recheck_adj4.json'):
    for k,v in json.load(open(f)).items():
        if not v.get('fits') and not v.get('apply') and 'error' not in v: held[k]=v
E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[3]))/'ross'/'edition.json')); pages={f"f{p['vflat']}":p for p in E['pages']}
def ctx(iid):
    a,v=iid.split('.'); L=pages[a]['lines']; k=[l['n'] for l in L].index(int(v[1:]))
    return [dict(n=l['n'],latin=l['orig'],english=l.get('en',''),target=j==k) for j,l in enumerate(L) if abs(j-k)<=2]
SYS=("You correct one line of the English facing "+BOOK+" line by line. The Latin of the target line was corrected against "
 "the print, and the current English may no longer fit it. A previous attempt at a fix was rejected by a referee. Write "
 "the line that renders the target Latin correctly, in the published style ([ ] for supplied words; a word may sit across "
 "the line break if the sense is kept), or keep the current English if it is already right. Return ONLY JSON "
 "{\"en\": \"...\", \"kept\": true|false}.")
VER=("You referee two English renderings (A, B) of ONE Latin line of "+BOOK+" (neighbours as context). Judge construal of the "
 "target Latin only; ignore wording. Return ONLY JSON {\"better\": \"A|B|equal\", \"a_ok\": true|false, \"b_ok\": true|false}.")
def do(iid):
    v=held[iid]; c=ctx(iid); cur=[x for x in c if x['target']][0]
    try:
        r,_=call('anthropic/claude-opus-5.5',SYS,json.dumps(dict(target=cur['latin'],current_english=cur['english'],rejected_attempt=v.get('en',''),context=c),ensure_ascii=False),max_tokens=2000)
        if r.get('kept') or r['en'].strip()==cur['english'].strip(): return iid,dict(kept=True)
        fix=r['en'].strip(); sw=random.Random('h'+iid).random()<0.5; A,B=(cur['english'],fix) if sw else (fix,cur['english']); fk='B' if sw else 'A'
        j,_=call('x-ai/grok-4.7',VER,json.dumps(dict(latin=cur['latin'],context=c,A=A,B=B),ensure_ascii=False),max_tokens=2000)
        ok=j['b_ok'] if sw else j['a_ok']
        return iid,dict(before=cur['english'],en=fix,apply=(j.get('better')==fk and ok),fits=False)
    except Exception as e: return iid,dict(error=repr(e)[:100])
with ThreadPoolExecutor(10) as ex: out=dict(ex.map(do,held))
json.dump(out,open('en_held.json','w'),ensure_ascii=False,indent=1)
print(len(held),collections.Counter('kept' if v.get('kept') else ('error' if 'error' in v else ('apply' if v['apply'] else 'hold')) for v in out.values()))
