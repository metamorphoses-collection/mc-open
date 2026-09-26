"""Ross line boxes from the print. Per page: detect printed-line bands (ink profile), give each verse the band under its
existing box centre, set the box's horizontal extent to the band's ink minus a right-margin source tag (a short last ink
segment far right after a gap), and attach an INDENTED unassigned band directly below a verse (its turnover) by union.
Writes ross_boxes.json {id: bbox}; renders review overlays for a sample."""
import os
import json,sys
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS=None
H=Path(__file__).parent; E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[3]))/'ross'/'edition.json'))
S=Path('./scratch/rossbox'); S.mkdir(exist_ok=True)
def bands(im):
    Hh,W=im.shape; col=im[:,int(0.03*W):int(0.97*W)]; ink=(col<120).sum(1).astype(float)
    k=max(3,Hh//300); sm=np.convolve(ink,np.ones(k)/k,'same'); thr=max(3,0.10*np.percentile(sm,99)); on=sm>thr; out=[]; s=None
    for y,v in enumerate(list(on)+[False]):
        if v and s is None: s=y
        if not v and s is not None:
            if y-s>Hh*0.006: out.append([s,y])
            s=None
    return out
def cut_tag(im,a,b,x1):
    # a right-margin source tag = the last ink run after a gap >= 1.2% width, starting right of 0.74W, narrower than 0.17W
    Hh,W=im.shape; cols=((im[a:b,:]<120).sum(0)>1); xs=np.where(cols)[0]; xs=xs[(xs>0.02*W)&(xs<=x1*W+2)]
    if len(xs)<2: return x1
    gaps=np.where(np.diff(xs)>0.012*W)[0]
    if len(gaps):
        g=gaps[-1]; start=xs[g+1]
        if start>0.74*W and (xs[-1]-start)<0.17*W: return xs[g]/W
    return x1
def segs(im,a,b):
    Hh,W=im.shape; cols=((im[a:b,:]<120).sum(0)>1); xs=np.where(cols)[0]; xs=xs[(xs>0.02*W)&(xs<0.99*W)]
    if not len(xs): return []
    out=[[xs[0],xs[0]]]
    for x in xs[1:]:
        if x-out[-1][1]<0.035*W: out[-1][1]=x
        else: out.append([x,x])
    return out
new={}; stats={'pages':0,'turnovers':0,'widened':0}
only=set(map(int,sys.argv[1:]))
for p in E['pages']:
    if not p['lines'] or (only and p['vflat'] not in only): continue
    f=H/'scans'/f"Ross - {p['vflat']}.jpg"
    im=np.asarray(Image.open(f).convert('L'),dtype=np.float32); Hh,W=im.shape; bs=bands(im); stats['pages']+=1
    cen=[(a+b)/2/Hh for a,b in bs]; used={}
    L=[l for l in p['lines'] if l.get('bbox')]
    for l in L:
        c=(l['bbox'][1]+l['bbox'][3])/2; j=int(np.argmin([abs(c-x) for x in cen]))
        if abs(cen[j]-c)<0.02 and j not in used: used[j]=l
    order=sorted(used)
    for n,j in enumerate(order):
        l=used[j]; a,b=bs[j]; sg=segs(im,a,b)
        if not sg: continue
        if len(sg)>1 and sg[-1][0]>0.72*W and (sg[-1][1]-sg[-1][0])<0.16*W: sg=sg[:-1]   # right-margin source tag
        x0=sg[0][0]/W; x1=sg[-1][1]/W; y0=a/Hh; y1=b/Hh
        nxt=order[n+1] if n+1<len(order) else None
        k=j+1
        while k<len(bs) and (nxt is None or k<nxt) and k<=j+2:
            if k in used: break
            s2=segs(im,*bs[k])
            if s2 and s2[0][0]/W>x0+0.04 and (nxt is not None or k==j+1):   # indented continuation = turnover
                if len(s2)>1 and s2[-1][0]>0.72*W and (s2[-1][1]-s2[-1][0])<0.16*W: s2=s2[:-1]
                if s2: y1=bs[k][1]/Hh; x1=max(x1,s2[-1][1]/W); stats['turnovers']+=1
                k+=1
            else: break
        x1=cut_tag(im,bs[j][0],bs[j][1],x1) if k==j+1 else max(cut_tag(im,bs[j][0],bs[j][1],x1),x1 if False else cut_tag(im,bs[j][0],bs[j][1],x1))
        h=(bs[j][1]-bs[j][0])/Hh; bb=[round(x0-0.005,4),round(y0-0.25*h,4),round(min(0.995,x1+0.005),4),round(y1+0.2*h,4)]
        if bb[2]>l['bbox'][2]+0.01: stats['widened']+=1
        new[f"f{p['vflat']}.v{l['n']}"]=bb
json.dump(new,open(H/'ross_boxes.json','w'),indent=0); print(stats,'boxes',len(new),'of',sum(1 for p in E['pages'] for l in p['lines'] if l.get('bbox')))
for vf in (120,67,331,386):
    p=[p for p in E['pages'] if p['vflat']==vf][0]; img=Image.open(H/'scans'/f'Ross - {vf}.jpg').convert('RGB'); W,Hh=img.size; d=ImageDraw.Draw(img)
    for l in p['lines']:
        bb=new.get(f"f{vf}.v{l['n']}")
        if bb: d.rectangle((bb[0]*W,bb[1]*Hh,bb[2]*W,bb[3]*Hh),outline=(220,0,0),width=3)
    img.thumbnail((700,1150)); img.save(S/f'r{vf}.jpg')
