"""Triage of the referee's flags (c=no/partly). Opus 5.5 sees the target Latin, +/-2 neighbours with their PUBLISHED English,
the Virgil source line(s) the verse quotes (from the edition's loci: the strongest evidence for construal), the published
English, the proposed replacement and the referee note, and classifies the PUBLISHED line:
ERROR = the meaning/construal is wrong (a reader is misled); SHIFT = carries content of a neighbouring line or drops part of
its own (line fidelity only); STYLE = acceptable, the flag is a wording preference. For ERROR/SHIFT it returns a corrected line.
Writes triage.json + triage.tsv. Proposes only."""
import json,sys,csv,collections,os
from concurrent.futures import ThreadPoolExecutor
from lib import H,BOOK,call,pages
E=json.load(open(json.load(open(H/'items.json'))['source']))
VIRG={}
for p in E['pages']:
    for l in p['lines']:
        iid=f"f{p['vflat']}.v{l['n']}" if l.get('n') is not None else None
        if iid: VIRG[iid]=[f"{x.get('cts_urn','').split(':')[-1]} ({x.get('work')}): {x.get('virgil')}" for x in l.get('loci') or [] if x.get('virgil')]
PG={p['page']:p for p in pages()}
rows=json.load(open(H/'review_cj.json'))
SYS=("You are a senior Latinist checking the published English of "+BOOK+". The English faces the Latin line by line; "
 "brackets [ ] mark words the translator supplied for sense, which is allowed when the Latin implies them. Classify the PUBLISHED "
 "English of the target item: ERROR = its meaning or construal is wrong and would mislead a reader (wrong case/agreement, "
 "wrong sense of a word, wrong subject/speaker, wrong tense with consequence); SHIFT = the meaning is right but it carries "
 "unbracketed content that belongs to a neighbouring line, or silently omits a content word of its own; STYLE = acceptable "
 "translation, the objection is a wording preference. A cento reuses Virgil: the Virgil source line shows the original "
 "construal, but the cento may bend it to a new sense, so judge the cento's own context. A referee note and a proposed "
 "replacement are given as advice; they may be wrong. Return ONLY JSON {\"class\": \"ERROR|SHIFT|STYLE\", \"why\": \"<=25 words, "
 "name the Latin word\", \"fix\": \"corrected English for this line only, in the published style, or empty if STYLE\"}.")
def do(r):
    its=PG[[k for k in PG if r['id'].startswith(k+'.')][0]]['items']; k=[i['id'] for i in its].index(r['id'])
    ctx=[dict(id=i['id'],latin=i['la'],published=i['en_edition'],target=i['id']==r['id']) for i in its[max(0,k-2):k+3]]
    u=dict(target=r['id'],kind=r['kind'],page=r['page'],cento=r['cento'],context=ctx,virgil_source=VIRG.get(r['id'],[]),
           published=r['published'],proposed=r['proposed'],referee_note=r['note'])
    try: v,_=call('anthropic/claude-opus-5.5',SYS,json.dumps(u,ensure_ascii=False),max_tokens=4000)
    except Exception as e: v={'class':'FAILED','why':repr(e)[:100],'fix':''}
    return dict(r,triage=v.get('class'),triage_why=v.get('why',''),fix=v.get('fix',''),virgil=' | '.join(VIRG.get(r['id'],[])))
with ThreadPoolExecutor(12) as ex: out=list(ex.map(do,rows))
json.dump(out,open(H/'triage.json','w'),ensure_ascii=False,indent=1)
cols=['id','page','cento','kind','triage','latin','published','fix','triage_why','virgil','verdict','confidence','note','gemini','opus']
with open(H/'triage.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=cols,delimiter='\t',extrasaction='ignore'); w.writeheader(); w.writerows(out)
print(collections.Counter(r['triage'] for r in out)); print(collections.Counter((r['verdict'],r['confidence'],r['triage']) for r in out).most_common())
