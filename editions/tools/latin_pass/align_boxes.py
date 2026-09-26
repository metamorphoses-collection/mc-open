"""Line boxes from the print: detect printed-line bands (tall bands split at the ink minimum), then align edition lines to
bands in reading order by dynamic programming (cost = distance between a line's existing box centre and the band centre,
0 for unboxed lines; skipping a band costs a constant, so headings/catchwords/notes are skipped). Each line gets its band's
geometry: vertical band expanded for ascenders/descenders, horizontal = page text column (median of good boxes) clipped to
the band's ink. Changed pages rendered for review. Writes aligned_boxes.json {line_key: bbox}."""
import os
import json,sys
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS=None
H=Path(__file__).parent; E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[2]))/'capilupi'/'edition.json'))
S=Path('./scratch/rebox'); S.mkdir(exist_ok=True)
def bands(im,x0f,x1f):
    Hh,W=im.shape; col=im[:,int(x0f*W):int(x1f*W)]; ink=(col<110).sum(1).astype(float)
    k=max(3,Hh//400); sm=np.convolve(ink,np.ones(k)/k,'same'); thr=max(4,0.10*np.percentile(sm,99))
    on=sm>thr; out=[]; s=None
    for y,v in enumerate(list(on)+[False]):
        if v and s is None: s=y
        if not v and s is not None:
            if y-s>Hh*0.006: out.append([s,y])
            s=None
    med=np.median([b-a for a,b in out]) if out else 1
    res=[]
    for a,b in out:
        n=int((b-a)/med+0.25)   # split only bands >= 1.75x the median line height
        if n>=2:   # split merged lines at the n-1 deepest minima
            seg=sm[a:b]; cuts=[]
            for c in range(1,n):
                lo=int(c*(b-a)/n-(b-a)/(3*n)); hi=int(c*(b-a)/n+(b-a)/(3*n)); cuts.append(a+lo+int(np.argmin(seg[lo:hi])))
            edges=[a]+cuts+[b]; res+= [[edges[i],edges[i+1]] for i in range(n)]
        else: res.append([a,b])
    return res,med
def align(L,bs):
    # DP over lines x bands, monotone; skip band cost SK; line must take a band
    n,m=len(L),len(bs); SK=0.02; INF=1e9
    cen=[(b[0]+b[1])/2 for b in bs]
    D=np.full((n+1,m+1),INF); D[0,:]=np.arange(m+1)*SK; P={}
    for i in range(1,n+1):
        for j in range(1,m+1):
            c=0 if L[i-1] is None else abs(L[i-1]-cen[j-1])
            a=D[i-1,j-1]+c; b=D[i,j-1]+SK
            if a<=b: D[i,j]=a; P[(i,j)]='m'
            else: D[i,j]=b; P[(i,j)]='s'
    i,j=n,int(np.argmin(D[n,:])+0) ; j=max(j,n); j=int(np.argmin(D[n,n:])+n); out=[None]*n
    while i>0 and j>0:
        if P.get((i,j))=='m': out[i-1]=j-1; i-=1; j-=1
        else: j-=1
    return out
new={}; report=[]
only=set(map(int,sys.argv[1:]))
for p in E['pages']:
    if not p['lines'] or (only and p['vflat'] not in only): continue
    im=np.asarray(Image.open(H/'scans'/f"Capilupi - {p['vflat']}.jpg").convert('L'),dtype=np.float32); Hh,W=im.shape
    boxed=[l['bbox'] for l in p['lines'] if l.get('bbox')]
    shared=len({tuple(b) for b in boxed})<len(boxed)
    xs0=np.median([b[0] for b in boxed]) if boxed and not shared else 0.17; xs1=np.percentile([b[2] for b in boxed],90) if boxed and not shared else 0.83
    raw,med=bands(im,max(0.12,xs0+0.02),min(0.9,xs1-0.02)); bs=[(a/Hh,b/Hh) for a,b in raw]
    L=[None if (not l.get('bbox') or shared) else (l['bbox'][1]+l['bbox'][3])/2 for l in p['lines']]
    if len(bs)<len(L): report.append((p['physical'],'too few bands',len(bs),len(L))); continue
    asg=align(L,bs); changed=[]
    for k,(l,bi) in enumerate(zip(p['lines'],asg)):
        a,b=bs[bi]; h=b-a; y0=a-0.45*h; y1=b+0.25*h
        seg=im[int(a*Hh):int(b*Hh),:]; cols=np.where((seg<110).sum(0)>1)[0]; cols=cols[(cols>=(xs0-0.01)*W)&(cols<=(xs1+0.02)*W)]
        x0=max(xs0-0.005,cols.min()/W-0.005) if len(cols) else xs0; x1=(cols.max()/W+0.005) if len(cols) else xs1
        bb=[round(x0,4),round(y0,4),round(x1,4),round(y1,4)]; key=f"f{p['vflat']}."+(f"v{l['n']}" if l.get('n') is not None else f"u{k}")
        old=l.get('bbox'); 
        if not old or shared or abs((old[1]+old[3])/2-(y0+y1)/2)>0.25*h or abs(old[3]-old[1]-(y1-y0))>0.6*h: new[key]=bb; changed.append(l.get('n') or f'u{k}')
    if changed:
        report.append((p['physical'],len(changed),changed[:10]))
        img=Image.open(H/'scans'/f"Capilupi - {p['vflat']}.jpg").convert('RGB'); d=ImageDraw.Draw(img)
        for k,l in enumerate(p['lines']):
            key=f"f{p['vflat']}."+(f"v{l['n']}" if l.get('n') is not None else f"u{k}"); bb=new.get(key) or l.get('bbox')
            if bb: d.rectangle((bb[0]*W,bb[1]*Hh,bb[2]*W,bb[3]*Hh),outline=(220,0,0) if key in new else (0,150,0),width=4); d.text((max(0,bb[0]*W-80),bb[1]*Hh),str(l.get('n') or f'u{k}'),fill=(0,0,220))
        img.thumbnail((1000,1450)); img.save(S/f"p{p['vflat']}.jpg")
json.dump(new,open(H/'aligned_boxes.json','w'),indent=1)
print('changed',len(new)); [print(r) for r in report]
