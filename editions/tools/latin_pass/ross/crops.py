"""Ross Latin pass: native-resolution line crops from the vFlat iPhone scans ('Ross - <vflat>.jpg') using the edition's
line boxes (normalised). 30% of line height padding above/below. Unboxed lines listed in unboxed.json for a page read."""
import os
import json
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
H=Path(__file__).parent; E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[3]))/'ross'/'edition.json'))
(H/'crops').mkdir(exist_ok=True); src={}; unboxed=[]
for p in E['pages']:
    if not p['lines']: continue
    img=None
    for l in p['lines']:
        iid=f"f{p['vflat']}.v{l['n']}"
        if not l.get('bbox'): unboxed.append(iid); continue
        if (H/'crops'/f'{iid}.jpg').exists(): src[iid]='bbox'; continue
        img=img or Image.open(H/'scans'/f"Ross - {p['vflat']}.jpg"); W,Hh=img.size; x0,y0,x1,y1=l['bbox']; h=(y1-y0)*Hh
        img.crop((max(0,int(x0*W-0.01*W)),max(0,int(y0*Hh-0.3*h)),min(W,int(x1*W+0.01*W)),min(Hh,int(y1*Hh+0.3*h)))).convert('RGB').save(H/'crops'/f'{iid}.jpg',quality=92)
        src[iid]='bbox'
json.dump(src,open(H/'crops.json','w')); json.dump(unboxed,open(H/'unboxed.json','w')); print('crops',len(src),'unboxed',len(unboxed))
