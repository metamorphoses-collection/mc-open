"""Adjudication packets. Every divergence (143) + 16 hidden controls (CONFIRMED lines: true text vs one-letter
falsifications) -> 4 batches. Options are shown unlabelled (A/B/C, random order, deduplicated by exact string); the
edition is not identified. For page-read lines the crop is the whole page (reader told the line text to find).
Writes adj/batch_<k>.json (for readers) and adj/key.json (option -> source, control truth; NOT shown to readers)."""
import os
import json,random,re
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
H=Path(__file__).parent; R=json.load(open(H/'divergences.json')); rng=random.Random(20260925)
E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[2]))/'capilupi'/'edition.json'))
ed={}
for p in E['pages']:
    for k,l in enumerate(p['lines']): ed[f"f{p['vflat']}.v{l['n']}" if l.get('n') is not None else f"f{p['vflat']}.u{k}"]=(l['orig'],p['vflat'])
(H/'adj').mkdir(exist_ok=True); (H/'adj/img').mkdir(exist_ok=True)
items=[]; key={}
def img_for(iid,src):
    if src=='crop': return str(H/'crops'/f'{iid}.jpg')
    vf=ed[iid][1]; out=H/'adj/img'/f'page_{vf}.jpg'
    if not out.exists(): Image.open(H/'scans'/f'Capilupi - {vf}.jpg').convert('RGB').save(out,quality=92)
    return str(out)
for r in R:
    opts=list(dict.fromkeys([r['edition'],r['gemini'],r['opus']])); rng.shuffle(opts)
    lab={chr(65+k):o for k,o in enumerate(opts)}
    items.append(dict(id=r['id'],image=img_for(r['id'],r['src']),whole_page=(r['src']=='page'),options=lab))
    key[r['id']]=dict(options={k:[s for s,v in (('edition',r['edition']),('gemini',r['gemini']),('opus',r['opus'])) if v==o] for k,o in lab.items()})
def falsify(t):
    for _ in range(50):
        k=rng.randrange(len(t))
        if t[k].isalpha() and t[k].islower():
            c=rng.choice([x for x in 'aceilmnorstu' if x!=t[k]]); return t[:k]+c+t[k+1:]
div={r['id'] for r in R}
conf=[i for i in ed if i not in div and (H/'crops'/f'{i}.jpg').exists() and len(ed[i][0])>25]
for n,i in enumerate(rng.sample(conf,16)):
    true=ed[i][0]; opts=[true,falsify(true)]+([falsify(true)] if n%2 else []); rng.shuffle(opts)
    lab={chr(65+k):o for k,o in enumerate(opts)}; cid=f"{i}#c"
    items.append(dict(id=cid,image=img_for(i,'crop'),whole_page=False,options=lab))
    key[cid]=dict(control=True,true=[k for k,o in lab.items() if o==true][0])
rng.shuffle(items)
for b in range(4):
    json.dump(items[b::4],open(H/'adj'/f'batch_{b}.json','w'),ensure_ascii=False,indent=1)
json.dump(key,open(H/'adj/key.json','w'),ensure_ascii=False,indent=1)
print('items',len(items),'controls',16,[len(items[b::4]) for b in range(4)])
