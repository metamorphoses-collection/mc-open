"""Whole-book independent retranslation (Bavarius harness). Resumable per page; a page missing any id is retried
3x then recorded incomplete, never silently accepted. Usage: python3 run_full.py <model> -> outputs/<tag>.json"""
import json,sys,time
from concurrent.futures import ThreadPoolExecutor
from lib import H,BOOK,call,pages
SYSTEM=("You are an expert translator of Neo-Latin verse and prose. You will receive items from one page of "+BOOK+". "
 "Spelling is as printed (u/v, i/j, æ/œ ligatures, & for et, q; for que, tilde abbreviations such as ũ for um; long s is written s). "
 "Translate every item into accurate, readable English. Keep one English line per Latin verse item: do not merge or split "
 "items, even when the syntax runs on across items (translate each item's own portion). Translate side-notes and prose "
 "in full. Do not add commentary. Return ONLY a JSON object mapping each item id to its English translation.")
def one(model,pg,its):
    user=(f"Page: {pg['printed']}. Cento: {pg['cento'] or '-'}\nItems (in order):\n"+
          json.dumps([{'id':i['id'],'kind':i['kind'],'latin':i['la']} for i in its],ensure_ascii=False,indent=0))
    return call(model,SYSTEM,user)
def do(model,pg):
    want={i['id'] for i in pg['items']}; out={}; us=[]
    for size in (len(pg['items']),max(4,len(pg['items'])//3),max(4,len(pg['items'])//3)):
        try:
            for k in range(0,len(pg['items']),size):
                sub=[i for i in pg['items'][k:k+size] if not str(out.get(i['id'],'')).strip()]
                if not sub: continue
                tr,u=one(model,pg,sub); out.update({x:v for x,v in tr.items() if x in want}); us.append(u)
        except Exception as e: print('retry',pg['page'],repr(e)[:100],flush=True)
        if want<={x for x,v in out.items() if str(v).strip()}: break
    return pg['page'],out,us,sorted(want-{x for x,v in out.items() if str(v).strip()})
if __name__=='__main__':
    model=sys.argv[1]; tag=model.replace('/','__'); od=H/'outputs'; od.mkdir(exist_ok=True)
    part=od/f'{tag}.partial.json'; st=json.load(open(part)) if part.exists() else {'done':[],'out':{},'usage':[],'incomplete':{}}
    todo=[p for p in pages() if p['items'] and p['page'] not in st['done']]
    with ThreadPoolExecutor(6) as ex:
        for a,out,us,miss in ex.map(lambda p:do(model,p),todo):
            st['out'].update(out); st['usage']+=us; st['done'].append(a)
            if miss: st['incomplete'][a]=miss
            json.dump(st,open(part,'w'),ensure_ascii=False); print(model,a,'missing',len(miss),flush=True)
    json.dump(dict(model=model,date=time.strftime('%Y-%m-%d'),usage=st['usage'],incomplete=st['incomplete'],translations=st['out']),open(od/f'{tag}.json','w'),ensure_ascii=False,indent=1)
    print('DONE',model,'incomplete',len(st['incomplete']),'cost',round(sum(float(u.get('cost',0) or 0) for u in st['usage']),2))
