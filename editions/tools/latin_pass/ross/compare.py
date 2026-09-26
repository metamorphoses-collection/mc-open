"""Compare edition Latin with the two blind readings, LETTERS ONLY (u/v, i/j, ligatures, accents, long s, punctuation,
spacing and case set aside; & = et). Classes: CONFIRMED (both readers = edition); BOTH (readers agree, differ from
edition: strong candidate); ONE (one reader differs); SPLIT (all three differ). Lines whose edition note documents an
emendation (SHOP ERROR / em. / misprint) are marked documented. Writes divergences.tsv/json."""
import json,re,unicodedata,csv,collections
from pathlib import Path
H=Path(__file__).parent
E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[3]))/'ross'/'edition.json'))
ed={}; notes={}; page={}
for p in E['pages']:
    for k,l in enumerate(p['lines']):
        iid=f"f{p['vflat']}.v{l['n']}"
        ed[iid]=l['orig']; notes[iid]=l.get('note') or ''; page[iid]=p['physical']
G=json.load(open(H/'reads/google__gemini-3.1-pro-preview.json'))['reads']; O=json.load(open(H/'reads/anthropic__claude-opus-5.5.json'))['reads']
# pages with missing/shared line boxes: whole-page reads replace the crop reads
PG=json.load(open(H/'reads/page_google__gemini-3.1-pro-preview.json')); PO=json.load(open(H/'reads/page_anthropic__claude-opus-5.5.json'))
G.update({k:v for k,v in PG.items() if not k.endswith('_sim')}); O.update({k:v for k,v in PO.items() if not k.endswith('_sim')})
PAGEREAD={k for k in PG if not k.endswith('_sim')}
# full-width re-reads replace readings taken from truncated crops
import os
for tag,D in (('google__gemini-3.1-pro-preview',G),('anthropic__claude-opus-5.5',O)):
    for suf in ('.wide','.turn'):   # later passes win: full-width, then verse + turnover line
        f=H/'reads'/f'{tag}{suf}.json'
        if f.exists(): D.update(json.load(open(f))['reads'])
def norm(t):
    t=str(t).replace('ß','ss').replace('ſ','s')
    d=unicodedata.normalize('NFD',t)   # tilde/macron on a vowel = omitted nasal: m before b/p/m or at word end, else n (Ross expands)
    d=re.sub(r'([aeiouAEIOU])[\u0303\u0304](?=[bpmBPM]|\W|$)',r'\1m',d); d=re.sub(r'([aeiouAEIOU])[\u0303\u0304]',r'\1n',d); t=unicodedata.normalize('NFC',d)
    t=re.sub(r'q[;́´]*;',r'que',t).replace('q́','que')
    t=t.replace('ÿ','ij').replace('ę','æ').replace('Ę','Æ')
    t=re.sub(r'(?<=[DdFfSsLl])y(?=s)','ij',t)   # printer's y for ij (Dys = Dijs, folys = folijs)
    t=t.replace('&','et').replace('æ','ae').replace('Æ','ae').replace('œ','oe').replace('Œ','oe').replace('ſ','s')
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]','',t.replace('v','u').replace('j','i')).replace('oe','ae')   # æ/œ confusions not counted in Ross
rows=[];C=collections.Counter()
for i,e in ed.items():
    g,o=G.get(i,''),O.get(i,''); ne,ng,no=norm(e),norm(g),norm(o)
    if ne==ng==no: C['CONFIRMED']+=1; continue
    cls='BOTH' if ng==no else ('ONE' if ne in (ng,no) else 'SPLIT')
    doc=bool(re.search(r'SHOP ERROR|\bem\.|misprint|foul',notes[i],re.I))
    C[cls+(' (documented)' if doc else '')]+=1
    rows.append(dict(id=i,page=page[i],cls=cls,documented=doc,src=('page' if i in PAGEREAD else 'crop'),edition=e,gemini=g,opus=o,note=notes[i][:200]))
with open(H/'divergences.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0]),delimiter='\t'); w.writeheader(); w.writerows(rows)
json.dump(rows,open(H/'divergences.json','w'),ensure_ascii=False,indent=1); print(len(ed),dict(C))
