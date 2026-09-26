#!/usr/bin/env python3
"""Plan tokens and verify the 7x7 extended-king adjacency for castello_49_destini."""
import json, os, sys

floors = {
    0: "Bosco", 1: "Citta", 2: "Mare", 3: "Sotterraneo",
    4: "Biblioteca", 5: "Orto", 6: "Torre",
}

row0 = [("la Radura dei Cervi","place"),("il Ruscello di Ferro","place"),("il Faggio Cavo","place"),
        ("la Fonte dei Lupi","place"),("il Sentiero dei Cinghiali","place"),("il Ceppo Bruciato","place"),
        ("la Radura dei Corvi","place")]
row1 = [("Donato il fabbro","char"),("Serafina la tessitrice","char"),("Baldassarre il notaio","char"),
        ("Cecilia la vedova","char"),("Remigio il farmacista","char"),("Ginevra l'ostessa","char"),
        ("Anselmo il sindaco","char")]
row2 = [("l'ancora spezzata","obj"),("la bussola di ottone","obj"),("la rete di canapa","obj"),
        ("il remo intagliato","obj"),("la lanterna del porto","obj"),("il timone di quercia","obj"),
        ("la vela rattoppata","obj")]
row3 = [("la cripta di calce","place"),("il pozzo nero","place"),("la galleria scavata","place"),
        ("la cisterna romana","place"),("la scala a chiocciola","place"),("la volta affrescata","place"),
        ("la camera murata","place")]
row4 = [("Teofilo il copista","char"),("Ildegarda la glossatrice","char"),("Maurilio il bibliotecario","char"),
        ("Elisea la miniatrice","char"),("Bartolo il lettore","char"),("Fiammetta la censora","char"),
        ("Ottavio il cartografo","char")]
row5 = [("la zappa a tre denti","obj"),("il corbello di vimini","obj"),("il melograno maturo","obj"),
        ("la forbice da innesto","obj"),("l'innaffiatoio di rame","obj"),("la pergola di glicine","obj"),
        ("lo spaventapasseri muto","obj")]
row6 = [("la finestra bifora","place"),("la campana fessa","place"),("l'orologio senza lancette","place"),
        ("il parapetto di travertino","place"),("la merlatura guelfa","place"),("la feritoia cieca","place"),
        ("la banderuola di rame","place")]

rows_data = [row0,row1,row2,row3,row4,row5,row6]
tokens = {}
for r in range(7):
    for c in range(7):
        name,typ = rows_data[r][c]
        tokens[(r,c)] = {"name":name, "type":typ}

def ball(i,j):
    out = []
    for r in range(max(0,i-1),min(7,i+2)):
        for c in range(max(0,j-1),min(7,j+2)):
            out.append((r,c))
    return out

page_tokens = {}
for pnum in range(1,50):
    idx = pnum-1
    i = idx % 7
    j = idx // 7
    page_tokens[pnum] = {"i":i,"j":j,"tokens":ball(i,j)}

def cheb(p,q):
    ip=(p-1)%7; jp=(p-1)//7
    iq=(q-1)%7; jq=(q-1)//7
    return max(abs(ip-iq),abs(jp-jq))

violations = 0
for p in range(1,50):
    for q in range(p+1,50):
        d = cheb(p,q)
        tp = set(page_tokens[p]["tokens"])
        tq = set(page_tokens[q]["tokens"])
        shared = tp & tq
        if d <= 2 and not shared:
            print(f"MISS p={p} q={q} d={d}")
            violations += 1
        if d > 2 and shared:
            print(f"FALSE-ADJ p={p} q={q} d={d} shares {shared}")
            violations += 1
print(f"Token-plan violations: {violations}")

for pnum in range(1,50):
    v = page_tokens[pnum]
    names = [tokens[t]["name"] for t in v["tokens"]]
    print(f"p={pnum:2d} (i={v['i']},j={v['j']}) floor={floors[v['i']]} corr={v['j']} : {names}")

plan_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(plan_dir,"_plan.json"),"w",encoding="utf-8") as f:
    json.dump({
        "tokens": {f"{r},{c}": tokens[(r,c)] for (r,c) in tokens},
        "page_tokens": {str(p): {"i":v["i"],"j":v["j"],"token_keys":[f"{r},{c}" for (r,c) in v["tokens"]]} for p,v in page_tokens.items()},
    }, f, indent=2, ensure_ascii=False)
print("plan saved to _plan.json")
