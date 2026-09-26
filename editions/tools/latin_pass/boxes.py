"""Capilupi line-box audit + rebuild. For each page: binarise the vFlat scan, take the ink profile per row over the text
column, find printed line bands. Audit: a line box is GOOD if its vertical centre falls inside a band that no other box
claims. Rebuild (pages with bad/missing boxes): if the number of bands below the running head equals the number of edition
lines, assign bands to lines in order; horizontal extent = ink extent of the band within the column. Writes boxes_audit.json."""
import os
import json,sys
import numpy as np
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
H=Path(__file__).parent; E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[2]))/'capilupi'/'edition.json'))
def bands(vf,x0f=0.17,x1f=0.83):
    im=np.asarray(Image.open(H/'scans'/f'Capilupi - {vf}.jpg').convert('L'),dtype=np.float32); Hh,W=im.shape
    col=im[:,int(x0f*W):int(x1f*W)]; ink=(col<110).sum(1).astype(float)
    k=max(3,Hh//400); sm=np.convolve(ink,np.ones(k)/k,'same'); thr=max(4,0.12*np.percentile(sm,99))
    on=sm>thr; out=[]; s=None
    for y,v in enumerate(on):
        if v and s is None: s=y
        if not v and s is not None:
            if y-s>Hh*0.008: out.append([s,y])
            s=None
    # merge bands separated by tiny gaps (descenders/accents)
    m=[]
    for b in out:
        if m and b[0]-m[-1][1]<Hh*0.004: m[-1][1]=b[1]
        else: m.append(b)
    # x extent per band
    res=[]
    for a,b in m:
        seg=im[a:b,:]; xs=np.where((seg<110).sum(0)>1)[0]; xs=xs[(xs>0.12*W)&(xs<0.9*W)]
        if len(xs): res.append((a/Hh,b/Hh,xs.min()/W,xs.max()/W))
    return res,W,Hh
audit={}
for p in E['pages']:
    if not p['lines']: continue
    bs,W,Hh=bands(p['vflat'])
    good=0; bad=[]; used={}
    for l in p['lines']:
        bb=l.get('bbox')
        if not bb: bad.append((l.get('n'),'missing')); continue
        c=(bb[1]+bb[3])/2; hit=[i for i,b in enumerate(bs) if b[0]<=c<=b[1]]
        if len(hit)==1 and hit[0] not in used: used[hit[0]]=l.get('n'); good+=1
        else: bad.append((l.get('n'),'off-line' if not hit else 'shared'))
    audit[p['vflat']]=dict(page=p['physical'],lines=len(p['lines']),bands=len(bs),good=good,bad=bad)
json.dump(audit,open(H/'boxes_audit.json','w'),indent=1)
tot=sum(a['lines'] for a in audit.values()); g=sum(a['good'] for a in audit.values())
print('lines',tot,'good',g,'bad',tot-g)
for vf,a in audit.items():
    if a['bad']: print(vf,a['page'],'lines',a['lines'],'bands',a['bands'],'bad',len(a['bad']),a['bad'][:6])
