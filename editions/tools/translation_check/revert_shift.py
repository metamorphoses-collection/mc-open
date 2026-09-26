"""Editorial decision, 25 Sep: in verse the SHIFT notion is accepted; make the English the nicest. For every SHIFT whose sense is KEPT
(shift_check.json): restore the original published English if the 25 Sep apply changed it, and flag the line
en_redistributed=true (English moves across the line break within the sentence). LOST shifts keep their correction.
Sync book.json English from edition.json. Writes reverted.json."""
import os
import json
from pathlib import Path
H=Path(__file__).parent; D=Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[2]))/'capilupi'
SC=json.load(open(H/'shift_check.json')); A={a['id']:a for a in json.load(open(H/'applied.json'))}
E=json.load(open(D/'edition.json')); B=json.load(open(D/'book.json'))
pages={f"f{p['vflat']}":p for p in E['pages']}; bpages={f"f{p['vflat']}":p for p in B['pages']}
def slot(iid):
    a,loc=iid.split('.'); pg=pages[a]
    if loc.startswith('v'): return [x for x in pg['lines'] if x.get('n')==int(loc[1:])][0],'en'
    if loc.startswith('u'): return [x for x in pg['lines'] if x.get('n') is None][int(loc[1:])-1],'en'
    if loc.startswith('note'): return pg['marginalia'][int(loc[4:])-1],'text_en'
    if loc.startswith('prose'): return pg['paragraphs_en'],int(loc[5:])-1
rev=[]; flagged=0
for iid,v in SC.items():
    if v.get('sense')!='KEPT': continue
    o,k=slot(iid)
    if iid in A:
        assert o[k]==A[iid]['after'],iid; o[k]=A[iid]['before']; rev.append(dict(id=iid,restored=A[iid]['before'],was=A[iid]['after']))
    if isinstance(o,dict): o['en_redistributed']=True; flagged+=1
for a,bp in bpages.items():
    ep=pages[a]; en={l['n']:l['en'] for l in ep['lines'] if l.get('n') is not None}; eu=[l['en'] for l in ep['lines'] if l.get('n') is None]; bu=0
    for bl in bp['lines']:
        if bl.get('n') is not None: bl['en']=en[bl['n']]
        else: bl['en']=eu[bu]; bu+=1
open(D/'edition.json','w').write(json.dumps(E,ensure_ascii=False,separators=(',',':')))
open(D/'book.json','w').write(json.dumps(B,ensure_ascii=False,indent=1))
json.dump(rev,open(H/'reverted.json','w'),ensure_ascii=False,indent=1); print('reverted',len(rev),'flagged',flagged)
