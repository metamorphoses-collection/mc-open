"""Mechanical Ross Latin fixes (both blind readers agree; edition dropped an æ-ligature -> 'a', or a tilde -> nasal omitted).
Word-level: align edition and reader words by normalised form; where the reader word = edition word + inserted 'e' (æ) or
+ inserted m/n (tilde), replace the edition word's letters by the reader word written in the EDITION's conventions
(æ->ae, œ->oe, tilde vowel -> vowel+m/n, ſ->s, ß->ss), keeping the edition word's punctuation. Nothing else changes.
Writes mech_fixes.json {id: {before, after, words}}."""
import json,re,unicodedata,difflib
exec(open('compare.py').read().split("rows=[];C=collections.Counter()")[0])
cls=json.load(open('both_classes.json')); R={r['id']:r for r in json.load(open('divergences.json'))}
def to_ed(w):
    w=w.replace('ß','ss').replace('ſ','s').replace('æ','ae').replace('Æ','AE').replace('œ','oe').replace('Œ','OE')
    d=unicodedata.normalize('NFD',w); d=re.sub(r'([aeiouAEIOU])[̃̄](?=[bpmBPM]|$)',r'\1m',d); d=re.sub(r'([aeiouAEIOU])[̃̄]',r'\1n',d)
    return unicodedata.normalize('NFC',d)
W=lambda s:re.findall(r"[^\s]+",s)
core=lambda w:re.sub(r'^[^\w]+|[^\w]+$','',w)
out={}
for i,(lab,k) in cls.items():
    if lab!='mechanical' or 'extra-words' in k: continue
    e=R[i]['edition']; g=R[i]['gemini']; ew,gw=W(e),W(g)
    ne=[norm(core(x)) for x in ew]; ng=[norm(core(x)) for x in gw]; changes=[]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,ne,ng,autojunk=False).get_opcodes():
        if op!='replace' or i2-i1!=j2-j1: continue
        for a,b in zip(range(i1,i2),range(j1,j2)):
            x,y=ne[a],ng[b]
            ok=len(y)==len(x)+1 and any(y[:p]+y[p+1:]==x and y[p] in 'emn' for p in range(len(y)))
            if not ok: continue
            old=ew[a]; c=core(old); new=old.replace(c,to_ed(core(gw[b])),1) if c else old
            if norm(core(new))==y: ew[a]=new; changes.append((old,new))
    if changes:
        after=' '.join(ew)+(' ' if e.endswith(' ') else '')
        out[i]=dict(before=e,after=after,words=changes)
json.dump(out,open('mech_fixes.json','w'),ensure_ascii=False,indent=1); print('lines',len(out),'words',sum(len(v['words']) for v in out.values()))
