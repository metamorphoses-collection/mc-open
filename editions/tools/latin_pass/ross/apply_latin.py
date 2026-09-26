"""Apply Ross Latin corrections (mech_fixes.json) + verified English re-check fixes (en_recheck.json, apply=true) to the site
copy: edition.json (orig, note, en), book.json (orig, en), book.txt (line). Guards: current Latin/English must equal what the
checks saw. Writes latin_applied.json."""
import os
import json,sys
from pathlib import Path
D=Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[3]))/'ross'
M=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'mech_fixes.json')); X=json.load(open(sys.argv[2] if len(sys.argv)>2 else 'en_recheck.json'))
NOTE=sys.argv[3] if len(sys.argv)>3 else 'Latin pass 26 Sep 2026: {w} as printed (dropped æ-ligature / nasal tilde restored; two blind readers agree, pattern verified on the scan).'
E=json.load(open(D/'edition.json')); B=json.load(open(D/'book.json')); T=(D/'book.txt').read_text().split('\n')
pages={f"f{p['vflat']}":p for p in E['pages']}; bp={f"f{p['vflat']}":p for p in B['pages']}; log=[]; skipped=[]
for iid,m in M.items():
    a,v=iid.split('.'); n=int(v[1:]); l=[x for x in pages[a]['lines'] if x['n']==n][0]
    if l['orig']!=m['before']: skipped.append(iid); continue
    b=[x for x in bp[a]['lines'] if x['n']==n][0]
    l['orig']=m['after']; b['orig']=m['after']
    w=', '.join(f"{x[1].strip(',.;:')}" for x in m['words'])
    l['latin_pass']=((l['latin_pass']+' | ') if l.get('latin_pass') else '')+NOTE.format(w=w)   # editorial; 'notes' holds Ross's printed notes
    t=[j for j,s in enumerate(T) if s.strip()==m['before'].strip()]
    if len(t)==1: T[t[0]]=T[t[0]].replace(m['before'].strip(),m['after'].strip())
    x=X.get(iid,{}); en_changed=False
    if x.get('apply') and not x.get('fits') and l.get('en')==x['before']: l['en']=x['en']; b['en']=x['en']; en_changed=True
    log.append(dict(id=iid,before=m['before'],after=m['after'],en_changed=en_changed,en=l.get('en')))
open(D/'edition.json','w').write(json.dumps(E,ensure_ascii=False,separators=(',',':'))); open(D/'book.json','w').write(json.dumps(B,ensure_ascii=False)); (D/'book.txt').write_text('\n'.join(T))
json.dump(log,open(Path(__file__).parent/'latin_applied.json','w'),ensure_ascii=False,indent=1)
print('latin',len(log),'english',sum(x['en_changed'] for x in log),'skipped',skipped[:10],len(skipped))
