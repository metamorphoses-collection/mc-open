#!/usr/bin/env python3
"""Populate metadata.json pages array for castello_49_destini."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE,"_plan.json"), encoding="utf-8"))
tokens = plan["tokens"]
page_tokens = plan["page_tokens"]

# Tarot card mapping per (row, col) — from metadata structure
tarot = {
    0: ["La Luna","Il Matto","La Ruota","L'Eremita","La Torre","Il Diavolo","La Stella"],
    1: ["Il Carro","Il Papa","La Giustizia","L'Imperatore","La Forza","Il Mago","Il Mondo"],
    2: ["Gli Amanti","L'Appeso","Il Sole","La Morte","La Temperanza","Il Bagatto","La Papessa"],
    3: ["Il Giudizio","L'Ambasciatore","Il Cieco","La Sposa","L'Alchimista","Il Calice","La Spada"],
    4: ["Lo Scriba","Il Poeta","Il Matematico","Il Traduttore","L'Architetto","L'Osservatore","Il Cartografo"],
    5: ["Il Giardiniere","La Vipera","Il Melo","Il Giuggiolo","Il Pozzo","La Siepe","Il Sasso"],
    6: ["L'Astronomo","L'Orologiaio","Il Campanaro","Il Corvo","Il Vento","La Finestra","L'Ultima Carta"],
}

floors = {
    0: "I piano del Bosco", 1: "II piano della Citta", 2: "III piano del Mare",
    3: "IV piano del Sotterraneo", 4: "V piano della Biblioteca",
    5: "VI piano dell'Orto", 6: "VII piano della Torre",
}
corridors = {
    0: "Corridoio A (nord)", 1: "Corridoio B (nord-est)", 2: "Corridoio C (est)",
    3: "Corridoio D (centrale)", 4: "Corridoio E (ovest)",
    5: "Corridoio F (sud-ovest)", 6: "Corridoio G (sud)",
}

meta = json.load(open(os.path.join(HERE,"metadata.json"), encoding="utf-8"))

pages_arr = []
for p in range(1,50):
    v = page_tokens[str(p)]
    i,j = v["i"], v["j"]
    ttoks = [tokens[k] for k in v["token_keys"]]
    chars = sorted({t["name"] for t in ttoks if t["type"]=="char"})
    objs  = sorted({t["name"] for t in ttoks if t["type"]=="obj"})
    places= sorted({t["name"] for t in ttoks if t["type"]=="place"})
    entry = {
        "page": p,
        "file": f"source/page_{p:02d}.txt",
        "grid": [i,j],
        "floor": floors[i],
        "corridor": corridors[j],
        "tarot_implicit": tarot[i][j],
        "characters": chars,
        "objects": objs,
        "places": places,
    }
    pages_arr.append(entry)

meta["pages"] = pages_arr
with open(os.path.join(HERE,"metadata.json"),"w",encoding="utf-8") as f:
    json.dump(meta,f,indent=2,ensure_ascii=False)
print(f"wrote metadata.json with {len(pages_arr)} pages")
