"""Editor review list: every item where the referee judged the PUBLISHED English wrong (c=no) or partly right (c=partly).
Confidence: HIGH = drafts agree (SAME) and C is off; MID = drafts differ but one is judged right; LOW = neither draft right.
Proposed = the referee-preferred draft (Opus if 'right' is both/SAME). Controls checked; a failed control is reported,
its page's verdicts are kept but flagged. Writes review_cj.tsv/json + summary.json. Proposes only; edits nothing."""
import json,glob,csv,collections
from lib import H,pages,drafts
G=drafts('google__gemini-3.1-pro-preview'); O=drafts('anthropic__claude-opus-5.5')
items={i['id']:(p,i) for p in pages() for i in p['items']}; order=[i for p in pages() for i in (x['id'] for x in p['items'])]
rows=[]; ctl=[]; C=collections.Counter(); judged=0
for f in glob.glob(str(H/'judge/*.json')):
    j=json.load(open(f)); m={'A':j['A'],'B':j['B']}; c=j.get('control') or {}
    if c:
        v=j['verdicts'].get(c['id'],{}).get('ab'); ok=(c['kind']=='IDENTITY' and v=='SAME') or (c['kind']=='SHIFT' and v in ('SHIFT_B','DIFFER'))
        ctl.append((j['page'],c['kind'],v,ok))
    for iid,v in j['verdicts'].items():
        if iid not in items: continue
        judged+=1; cv=v.get('c','?'); C[cv]+=1
        if cv not in ('no','partly'): continue
        p,it=items[iid]; ab=v.get('ab'); r=v.get('right')
        is_ctl=iid==c.get('id')
        if ab=='SAME' and not is_ctl: conf,src='HIGH','both drafts agree'
        elif r in ('A','B'): conf,src='MID',m[r]
        elif r=='both': conf,src='MID','both'
        else: conf,src='LOW','neither draft'
        if is_ctl: conf,src='CHECK','control slot (B planted); verdict unreliable'
        prop=G[iid] if src=='gemini' else O.get(iid,'')
        rows.append(dict(id=iid,page=p['printed'],cento=p['cento'] or '',kind=it['kind'],verdict=cv,confidence=conf,latin=it['la'],
                         published=it['en_edition'],proposed=prop,proposed_from=src,gemini=G.get(iid,''),opus=O.get(iid,''),note=v.get('note','')))
rows.sort(key=lambda r:order.index(r['id']))
with open(H/'review_cj.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0]),delimiter='\t'); w.writeheader(); w.writerows(rows)
json.dump(rows,open(H/'review_cj.json','w'),ensure_ascii=False,indent=1)
S=dict(items=len(items),judged=judged,edition_verdicts=C,controls_ok=f"{sum(x[3] for x in ctl)}/{len(ctl)}",control_failures=[x for x in ctl if not x[3]],
       to_cj=collections.Counter((r['verdict'],r['confidence']) for r in rows).most_common(),
       by_kind=collections.Counter(r['kind'] for r in rows),by_cento=collections.Counter(r['cento'] for r in rows))
S={k:(dict(v) if isinstance(v,collections.Counter) else v) for k,v in S.items()}; S['to_cj']=[f"{a}/{b}: {n}" for (a,b),n in S['to_cj']]
json.dump(S,open(H/'summary.json','w'),indent=1,ensure_ascii=False); print(json.dumps(S,indent=1,ensure_ascii=False))
