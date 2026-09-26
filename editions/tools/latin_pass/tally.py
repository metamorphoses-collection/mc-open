"""Tally reader rulings against the hidden key. Controls first (a failed control is reported). Per divergence:
EDITION (print = edition letters) · CORRECT (print = a reader's reading, not the edition) · NEITHER (reader gives the
print) · UNSURE. Writes rulings.json/tsv with the proposed printed text for CORRECT/NEITHER."""
import json,glob,csv,collections,sys
from pathlib import Path
H=Path(__file__).parent; K=json.load(open(H/'adj/key.json')); D={r['id']:r for r in json.load(open(H/'divergences.json'))}
B={i['id']:i for f in glob.glob(str(H/'adj/batch_*.json')) for i in json.load(open(f))}
R={}; [R.update(json.load(open(f))) for f in glob.glob(str(H/'adj/ruling_*.json'))]
miss=[i for i in B if i not in R]; print('rulings',len(R),'/',len(B),'missing',miss[:5])
ctl=[(i,R[i]['choice'],K[i]['true']) for i in B if K[i].get('control') and i in R]
print('controls',sum(c==t for _,c,t in ctl),'/',len(ctl),'failed:',[x for x in ctl if x[1]!=x[2]])
rows=[];C=collections.Counter()
for i,r in D.items():
    if i not in R: continue
    v=R[i]; ch=v.get('choice'); opt=B[i]['options']
    if ch in opt:
        src=K[i]['options'][ch]; txt=opt[ch]; cls='EDITION' if 'edition' in src else 'CORRECT'
    elif ch=='NEITHER': cls,txt,src='NEITHER',v.get('printed',''),[]
    else: cls,txt,src='UNSURE','',[]
    C[(cls,r['documented'])]+=1
    rows.append(dict(id=i,page=r['page'],ruling=cls,documented=r['documented'],edition=r['edition'],printed=txt,agrees_with='+'.join(src),note=v.get('note',''),edition_note=r['note']))
json.dump(rows,open(H/'rulings.json','w'),ensure_ascii=False,indent=1)
with open(H/'rulings.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0]),delimiter='\t'); w.writeheader(); w.writerows(rows)
print(dict(C))
