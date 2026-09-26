"""Final English for triaged ERROR/SHIFT lines, then a blind check.
1) Opus 5.5 writes the final line in the edition's published style (plain, dignified; [ ] for supplied words; punctuation
   continuous with the neighbours), from the triage fix + reason + Virgil source + neighbours' published English.
2) Grok 4.7 compares final vs published blind (random A/B): better A|B|equal, each ok true/false.
APPLY only if the final is judged better AND ok; everything else stays on the editor's residual list. Writes polish.json."""
import json,random,collections
from concurrent.futures import ThreadPoolExecutor
from lib import H,BOOK,call,pages
T=[r for r in json.load(open(H/'triage.json')) if r['triage'] in ('ERROR','SHIFT')]
PG={p['page']:p['items'] for p in pages()}
def ctx(iid):
    its=PG[iid.split('.')[0]]; k=[i['id'] for i in its].index(iid)
    return [dict(id=i['id'],latin=i['la'],published=(None if i['id']==iid else i['en_edition']),target=i['id']==iid) for i in its[max(0,k-3):k+4]]
POL=("You finalise one line of the English translation of "+BOOK+", which faces the Latin line by line in a published scholarly "
 "edition. A checker found the published line wrong (ERROR: construal) or unfaithful to its line (SHIFT: carries a neighbour's "
 "content unbracketed, or drops a word). You get the target Latin with neighbours and their published English, the published line, "
 "a literal corrected draft, the checker's reason, and the Virgil source line. Write the final line: the correct construal, only "
 "this line's content (a line may begin or end mid-clause; words supplied for sense go in [ ]), in the published style: plain, "
 "dignified, idiomatic English, no archaism, punctuation continuous with the neighbouring lines. Change no more than needed. If you "
 "judge the checker wrong, return the published line unchanged. Return ONLY JSON {\"en\": \"...\", \"changed\": true|false}.")
VER=("You referee two English renderings (A, B) of ONE target Latin item of "+BOOK+", printed line by line facing the Latin; "
 "neighbouring lines are context. Judge construal and line fidelity (nothing unbracketed imported from neighbours, no content word "
 "of the target dropped; [ ] marks supplied words, which is allowed). Ignore wording preferences. Return ONLY JSON "
 "{\"better\": \"A|B|equal\", \"a_ok\": true|false, \"b_ok\": true|false, \"note\": \"<=20 words\"}.")
def do(r):
    c=ctx(r['id'])
    p,_=call('anthropic/claude-opus-5.5',POL,json.dumps(dict(target=r['id'],kind=r['kind'],context=c,published=r['published'],
        corrected_draft=r['fix'],reason=f"{r['triage']}: {r['triage_why']}",virgil_source=r['virgil']),ensure_ascii=False),max_tokens=4000)
    fin=p['en'].strip()
    if not p.get('changed') or fin==r['published'].strip(): return dict(id=r['id'],final=fin,apply=False,why='polisher kept published')
    swap=random.Random('pol'+r['id']).random()<0.5; A,B=(r['published'],fin) if swap else (fin,r['published']); fk='B' if swap else 'A'
    v,_=call('x-ai/grok-4.7',VER,json.dumps(dict(target=r['id'],context=c,A=A,B=B),ensure_ascii=False),max_tokens=4000)
    fok=v['b_ok'] if swap else v['a_ok']; pok=v['a_ok'] if swap else v['b_ok']
    ap=v.get('better')==fk and fok
    return dict(id=r['id'],final=fin,apply=ap,final_ok=fok,published_ok=pok,better=('final' if v.get('better')==fk else v.get('better') if v.get('better')=='equal' else 'published'),note=v.get('note',''))
def safe(r):
    try: return do(r)
    except Exception as e: return dict(id=r['id'],apply=False,why='FAILED '+repr(e)[:100])
with ThreadPoolExecutor(12) as ex: out=list(ex.map(safe,T))
json.dump(out,open(H/'polish.json','w'),ensure_ascii=False,indent=1)
tri={r['id']:r['triage'] for r in T}
print(collections.Counter((tri[o['id']],o['apply'],o.get('better',o.get('why'))) for o in out).most_common())
