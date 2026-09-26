"""English re-check for Latin lines corrected in the Latin pass. Opus 5.5 sees the old and new Latin, the current English,
and +/-2 neighbours; answers whether the English already fits the corrected Latin, else writes a minimal fix. Grok 4.7 then
compares fix vs current blind. Apply only if the fix is judged better and correct. Writes en_recheck.json."""
import os
import json,sys,random,collections
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'translation_check'))
from lib import call,BOOK
M=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'mech_fixes.json'))
E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[3]))/'ross'/'edition.json'))
pages={f"f{p['vflat']}":p for p in E['pages']}
SYS=("You check the English facing "+BOOK+" line by line after a correction of the LATIN transcription (the old Latin had "
 "a dropped æ-ligature or a dropped nasal tilde, e.g. qua→quae, nata→natae, arena→arenam). Given the old Latin, the corrected "
 "Latin, the current English and the neighbouring lines, decide whether the current English already renders the corrected "
 "Latin correctly (translators often understood the intended word). If yes return {\"fits\": true}. If not, write a minimal fix "
 "in the published style ([ ] for supplied words; a word may sit across the line break if the sense is kept): return "
 "{\"fits\": false, \"en\": \"...\", \"why\": \"<=20 words\"}. Return ONLY JSON.")
VER=("You referee two English renderings (A, B) of ONE Latin line of "+BOOK+" (neighbours given as context). Judge construal "
 "of the given Latin only; ignore wording. Return ONLY JSON {\"better\": \"A|B|equal\", \"a_ok\": true|false, \"b_ok\": true|false}.")
def ctx(iid,new):
    a,v=iid.split('.'); L=pages[a]['lines']; k=[l['n'] for l in L].index(int(v[1:]))
    return [dict(n=l['n'],latin=(new if j==k else l['orig']),english=l.get('en',''),target=j==k) for j,l in enumerate(L) if abs(j-k)<=2]
def do(item):
    iid,m=item; a,v=iid.split('.'); l=[x for x in pages[a]['lines'] if x['n']==int(v[1:])][0]; en=l.get('en','')
    try:
        r,_=call('anthropic/claude-opus-5.5',SYS,json.dumps(dict(old_latin=m['before'],corrected_latin=m['after'],current_english=en,context=ctx(iid,m['after'])),ensure_ascii=False),max_tokens=2000)
        if r.get('fits'): return iid,dict(fits=True,en=en)
        fix=r['en'].strip(); sw=random.Random(iid).random()<0.5; A,B=(en,fix) if sw else (fix,en); fk='B' if sw else 'A'
        j,_=call('x-ai/grok-4.7',VER,json.dumps(dict(latin=m['after'],context=ctx(iid,m['after']),A=A,B=B),ensure_ascii=False),max_tokens=2000)
        ok=j['b_ok'] if sw else j['a_ok']
        return iid,dict(fits=False,before=en,en=fix,why=r.get('why',''),apply=(j.get('better')==fk and ok))
    except Exception as e: return iid,dict(error=repr(e)[:120])
with ThreadPoolExecutor(12) as ex: out=dict(ex.map(do,M.items()))
json.dump(out,open(sys.argv[2] if len(sys.argv)>2 else 'en_recheck.json','w'),ensure_ascii=False,indent=1)
print(collections.Counter('error' if 'error' in v else ('fits' if v['fits'] else ('apply' if v['apply'] else 'hold')) for v in out.values()))
