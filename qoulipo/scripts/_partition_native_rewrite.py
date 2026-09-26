#!/usr/bin/env python3
"""
Native French rewrite of every page in qoulipo/partition_du_texte/source/.

Goals:
  - eliminate keyword cycling on the small fixed lexicon
    (parchemin, chronique, épée, foi, langue, nombre, pari, complot, jeu, Maliette ...)
  - translate any English-language pages into native French verse
  - preserve the page's existing formal envelope (stanza count, approx line count)
  - keep the 5 poetic-form communities (sonnet / ballade / villanelle / rondeau / haiku-sequence
    / anaphora-prose-poem) so the NLP k=8 graph remains structured

This rewrites IN PLACE. After running, regenerate graph_k8.json and metadata.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import anthropic

os.environ.setdefault(
    "ANTHROPIC_API_KEY",
    "<REDACTED:set ANTHROPIC_API_KEY env var>",
)

SRC = Path("corpus/qoulipo/partition_du_texte/source")   # relative to the qoulipo/ folder

SYSTEM = (
    "Tu réécris une page d'un cycle poétique français contraint. "
    "Objectif: poésie française native, lyrique, littéraire — pas de répétition mécanique "
    "des mêmes 5-10 mots-clés (parchemin, chronique, épée, foi, langue, nombre, pari, complot, "
    "jeu, Maliette). Vocabulaire varié, images concrètes, syntaxe naturelle. "
    "Aucun terme computationnel. "
    "PRÉSERVE EXACTEMENT la structure formelle de l'original: même nombre de strophes/paragraphes, "
    "même forme dominante (alexandrin, sonnet, villanelle, rondeau, ballade, haïku, anaphore en prose). "
    "Si la page est en anglais, traduis-la en français natif sous la même forme. "
    "Garde le ton historique/médiéval (chroniques, serments, écriture, mémoire) mais SANS marteler les mêmes mots. "
    "Tu peux utiliser les mots-clés une ou deux fois par page maximum, jamais en couples figés. "
    "Retourne UNIQUEMENT le poème, sans préambule ni guillemets ni explication."
)


def detect_form_hint(text: str) -> str:
    """Return a short form hint based on the existing structure."""
    t = text.strip()
    if t.startswith("#") or t.startswith("*Anaphore") or "J'ai vu" in t[:200] or \
       "J'ai compté" in t[:200] or "J'ai entendu" in t[:200] or \
       "J'ai parié" in t[:200] or "J'ai été témoin" in t[:200] or "J'ai mesuré" in t[:200]:
        return "anaphore en prose poétique (paragraphes denses, refrain anaphorique en début de paragraphe)"
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    if not paras:
        return "vers libres"
    # haiku-like: tercets dominant
    tercet_like = sum(1 for p in paras if 2 <= len(p.splitlines()) <= 3)
    if tercet_like / max(1, len(paras)) > 0.7 and len(paras) >= 8:
        return "séquence de haïkus (tercets 5-7-5 approximatifs, images saisonnières, pas de rimes)"
    quatrain_like = sum(1 for p in paras if len(p.splitlines()) == 4)
    if quatrain_like >= 6:
        return "ballade en quatrains d'alexandrins rimés ABAB"
    if len(paras) <= 5:
        return "sonnet ou rondeau (alexandrins, rimes croisées ou embrassées)"
    return "ballade libre en strophes mêlées d'alexandrins"


def stanza_signature(text: str) -> str:
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    counts = [len(p.splitlines()) for p in paras]
    return f"{len(paras)} strophe(s), nombre de lignes par strophe: {counts}"


def main():
    client = anthropic.Anthropic()
    files = sorted(SRC.glob("page_*.txt"))
    print(f"[rewrite] {len(files)} pages found", flush=True)
    for i, fp in enumerate(files, 1):
        original = fp.read_text(encoding="utf-8")
        form = detect_form_hint(original)
        sig = stanza_signature(original)
        user_msg = (
            f"FORME ATTENDUE: {form}\n"
            f"STRUCTURE EXACTE À PRÉSERVER: {sig}\n\n"
            f"PAGE ORIGINALE:\n---\n{original}\n---\n\n"
            "Réécris cette page comme poésie française native sous la forme indiquée. "
            "Préserve la structure exacte (même nombre de strophes/paragraphes, mêmes longueurs). "
            "Garde l'univers thématique (mémoire, écriture, serments, voix anciennes) mais varie le vocabulaire. "
            "Retourne uniquement le poème."
        )
        for attempt in range(3):
            try:
                resp = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=4096,
                    system=SYSTEM,
                    messages=[{"role": "user", "content": user_msg}],
                )
                new_text = resp.content[0].text.strip()
                # strip code fences if any
                new_text = re.sub(r"^```[a-zA-Z]*\n?", "", new_text)
                new_text = re.sub(r"\n?```\s*$", "", new_text)
                # strip leading/trailing quotes that some models add
                new_text = new_text.strip().strip('"').strip()
                if not new_text:
                    raise RuntimeError("empty response")
                fp.write_text(new_text + "\n", encoding="utf-8")
                print(f"  [{i:2}/{len(files)}] {fp.name}: rewritten ({len(new_text)} chars)", flush=True)
                break
            except Exception as e:
                print(f"  [{i:2}/{len(files)}] {fp.name}: attempt {attempt+1} failed: {e}", flush=True)
                time.sleep(2 + attempt * 3)
        else:
            print(f"  [{i:2}/{len(files)}] {fp.name}: GAVE UP", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
