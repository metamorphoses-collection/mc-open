"""Line crops at NATIVE resolution for the Capilupi Latin pass. Boxed lines: edition bbox (normalised) on the vFlat scan
'Capilupi - <vflat>.jpg'. Unboxed lines (77, pp. 4/11/12/57-60, K1r): matched by text to the Transkribus PAGE-XML line
(char similarity >= 0.55) and cropped from the Transkribus upload image; else the band between boxed neighbours.
Padding: 30% of line height above/below, 1% of width each side. Writes crops/<id>.jpg + crops.json (id -> source)."""
import os
import json,re,glob,difflib
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
H=Path(__file__).parent; E=json.load(open(Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[2]))/'capilupi'/'edition.json'))
PX=sorted(glob.glob(str(H/'pagexml/**/page/*.xml'),recursive=True))
TK={'p. 4':'08_p04','p. 11':'15_p11','p. 12':'16_p12','p. 57':'61_p57','p. 58':'62_p58','p. 59':'63_p59','p. 60':'64_p60','K1r':'69_K1r_Egio'}
def tklines(stem):
    key=stem.split('_',1)[1]  # p57 / K1r_Egio
    f=[x for x in PX if re.search(r'_\d+_'+re.escape(key.replace('p0','p'))+r'(_|\.)',Path(x).name) or Path(x).name.endswith('_'+key+'.xml')]
    if not f: return []
    s=open(f[0]).read(); out=[]
    for m in re.finditer(r'<TextLine.*?<Coords points="([^"]+)".*?<Unicode>(.*?)</Unicode>',s,re.S):
        pts=[tuple(map(int,p.split(','))) for p in m.group(1).split()]; xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        out.append(dict(box=(min(xs),min(ys),max(xs),max(ys)),text=re.sub(r'<[^>]+>','',m.group(2))))
    return out
norm=lambda t:re.sub(r'[^a-z]','',t.lower().replace('v','u').replace('j','i'))
(H/'crops').mkdir(exist_ok=True); src={}
def save(img,box,iid):
    x0,y0,x1,y1=box; h=y1-y0; W,Hh=img.size
    b=(max(0,int(x0-0.01*W)),max(0,int(y0-0.3*h)),min(W,int(x1+0.01*W)),min(Hh,int(y1+0.3*h)))
    img.crop(b).convert('RGB').save(H/'crops'/f'{iid}.jpg',quality=92)
for p in E['pages']:
    if not p['lines']: continue
    a=f"f{p['vflat']}"; img=None; tk=None
    for k,l in enumerate(p['lines']):
        iid=f"{a}.v{l['n']}" if l.get('n') is not None else f"{a}.u{k}"
        if l.get('bbox'):
            img=img or Image.open(H/'scans'/f"Capilupi - {p['vflat']}.jpg"); W,Hh=img.size; x0,y0,x1,y1=l['bbox']
            save(img,(x0*W,y0*Hh,x1*W,y1*Hh),iid); src[iid]='vflat bbox'; continue
        if tk is None:
            stem=TK.get(p['physical']); tk=(stem,tklines(stem),Image.open(H/'tk_images'/f'{stem}.jpg')) if stem else (None,[],None)
        best=max(tk[1],key=lambda t:difflib.SequenceMatcher(None,norm(t['text']),norm(l['orig'])).ratio(),default=None)
        r=difflib.SequenceMatcher(None,norm(best['text']),norm(l['orig'])).ratio() if best else 0
        if r>=0.55: save(tk[2],best['box'],iid); src[iid]=f'transkribus {tk[0]} sim={r:.2f}'
        else: src[iid]=f'NO CROP (best sim {r:.2f})'
json.dump(src,open(H/'crops.json','w'),indent=1)
import collections; print(collections.Counter(v.split(' ')[0]+' '+v.split(' ')[1] if v.startswith('NO') else v.split(' ')[0] for v in src.values())); print([k for k,v in src.items() if v.startswith('NO')])
