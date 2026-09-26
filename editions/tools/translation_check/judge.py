"""Referee (default Grok 4.7), Bavarius judge.py protocol. Per item: Latin, A and B (Gemini/Opus, per-page random order),
C = the PUBLISHED edition English. Verdict A vs B (SAME/DIFFER/SHIFT_A/SHIFT_B, which is right) and whether C matches the
correct construal (yes/no/partly). CONTROLS hidden from the judge: one item per page (>=4 items) planted as IDENTITY (B:=A,
must be SAME) or SHIFT (B:=next item's B, must be SHIFT_B or DIFFER). Run invalid if controls fail unreviewed.
Usage: python3 judge.py [model] -> judge/<page>.json"""
import json,sys,random,os
from concurrent.futures import ThreadPoolExecutor
from lib import H,BOOK,call,pages,drafts
model=sys.argv[1] if len(sys.argv)>1 else 'x-ai/grok-4.7'
G=drafts('google__gemini-3.1-pro-preview'); O=drafts('anthropic__claude-opus-5.5')
SYS=("You are an expert Latinist refereeing translations of "+BOOK+". For every item you get the Latin and three English "
 "versions A, B, C. Judge MEANING, not wording: synonyms, word order, thou/you and punctuation do not matter. For A vs B give "
 "verdict SAME if they construe the Latin the same way; DIFFER if they construe it differently (then say which is right: A, B, "
 "both or neither); SHIFT_A or SHIFT_B if that version contains words that belong to a neighbouring Latin item or omits this "
 "item's content. Then say whether C matches the correct construal (yes/no/partly); C is also 'no' if it carries a neighbouring "
 "item's content or omits part of this one. Return ONLY JSON: {\"<id>\": {\"ab\": \"SAME|DIFFER|SHIFT_A|SHIFT_B\", \"right\": "
 "\"A|B|both|neither\", \"c\": \"yes|no|partly\", \"note\": \"<=20 words; required if not SAME or if c is not yes; name the "
 "Latin word at issue\"}, ...}")
od=H/'judge'; od.mkdir(exist_ok=True)
def judge_page(pg):
    a=pg['page']; f=od/f'{a}.json'
    if f.exists() or not pg['items']: return
    rng=random.Random('20260925capilupi'+a); swap=rng.random()<0.5
    its=[i for i in pg['items'] if G.get(i['id']) and O.get(i['id'])]
    A={i['id']:(O if swap else G)[i['id']] for i in its}; B={i['id']:(G if swap else O)[i['id']] for i in its}; c=None
    if len(its)>=4:
        k=rng.randrange(len(its)-1); cid=its[k]['id']; kind=rng.choice(['IDENTITY','SHIFT'])
        B[cid]=A[cid] if kind=='IDENTITY' else B[its[k+1]['id']]; c=dict(id=cid,kind=kind)
    out={}; us=[]; size=len(its)
    for size in (len(its),max(6,len(its)//3)):
        try:
            for k in range(0,len(its),size):
                pl=[dict(id=i['id'],kind=i['kind'],latin=i['la'],A=A[i['id']],B=B[i['id']],C=i['en_edition']) for i in its[k:k+size]]
                v,u=call(model,SYS,f"Page {pg['printed']} (cento: {pg['cento'] or '-'}). Items in order:\n"+json.dumps(pl,ensure_ascii=False,indent=0)); out.update(v); us.append(u)
            if {i['id'] for i in its}<=set(out): break
        except Exception as e: print('retry-split',a,repr(e)[:100],flush=True)
    json.dump(dict(page=a,A='opus' if swap else 'gemini',B='gemini' if swap else 'opus',control=c,verdicts=out,usage=us),open(f,'w'),ensure_ascii=False,indent=1)
    print(a,len(out),'/',len(its),'control',c and c['kind'],c and out.get(c['id'],{}).get('ab'),flush=True)
with ThreadPoolExecutor(int(os.environ.get('JUDGE_WORKERS','8'))) as ex:
    for fu in [ex.submit(judge_page,pg) for pg in pages()]:
        try: fu.result()
        except Exception as e: print('ERROR',repr(e)[:200],flush=True)
