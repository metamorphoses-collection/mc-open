"""Apply the 8 Latin corrections verified by eye at native resolution (25 Sep 2026) to the site copy:
edition.json (orig + note), book.json (diplomatic), book.txt (the line). Each change is a single-word replacement,
guarded (the old word must occur exactly once in the line). Writes latin_applied.json."""
import os
import json
from pathlib import Path
D=Path(os.environ.get('MC_EDITIONS', Path(__file__).resolve().parents[2]))/'capilupi'
P='Latin pass 25 Sep 2026 (two blind readers + adjudication + native-resolution check)'
CH=[('f71.v2','cœpit','cæpit',f'cæpit with æ-ligature as printed. {P}.'),
    ('f77.v29','fœdera','fædera',f'fædera with æ-ligature as printed. {P}.'),
    ('f38.v20','usq;','usque;',f'usque printed in full. {P}.'),
    ('f76.v18','cæca','cœca',f'cœca with œ-ligature as printed (supersedes earlier æ ruling). {P}.'),
    ('f39.v2','Inferniq;','Inserniq;',f'Misprint as printed: long s for f (read Inferniq;). {P}.'),
    ('f70.v31','iustitiam','iustitam',f'Misprint as printed: iustitam (read iustitiam, Aen. 6.620); supersedes earlier ruling. {P}.'),
    ('f72.v2','fugiunt','fagiunt',f'Misprint as printed: fagiunt (read fugiunt). {P}.'),
    ('f71.v14','Mulcentem','Muleentem',f'Misprint as printed: Muleentem (read Mulcentem, Georg. 4.510). {P}.')]
E=json.load(open(D/'edition.json')); B=json.load(open(D/'book.json')); T=(D/'book.txt').read_text().split('\n')
pages={f"f{p['vflat']}":p for p in E['pages']}; bp={f"f{p['vflat']}":p for p in B['pages']}; log=[]
for iid,old,new,note in CH:
    a,v=iid.split('.'); n=int(v[1:])
    l=[x for x in pages[a]['lines'] if x.get('n')==n][0]; before=l['orig']
    assert before.count(old)==1,(iid,before); l['orig']=before.replace(old,new)
    l['note']=(l['note']+' | ' if l.get('note') else '')+note
    b=[x for x in bp[a]['lines'] if x.get('n')==n][0]; assert b['diplomatic']==before,(iid,'book.json'); b['diplomatic']=l['orig']
    k=[j for j,t in enumerate(T) if t==before]; assert len(k)==1,(iid,'book.txt',len(k)); T[k[0]]=l['orig']
    log.append(dict(id=iid,before=before,after=l['orig'],note=note))
open(D/'edition.json','w').write(json.dumps(E,ensure_ascii=False,separators=(',',':')))
open(D/'book.json','w').write(json.dumps(B,ensure_ascii=False,indent=1))
(D/'book.txt').write_text('\n'.join(T))
json.dump(log,open(Path(__file__).parent/'latin_applied.json','w'),ensure_ascii=False,indent=1); print('applied',len(log))
