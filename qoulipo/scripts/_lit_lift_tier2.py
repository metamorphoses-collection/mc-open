#!/usr/bin/env python3
"""Tier-2 literary lift for the medium-revision pieces per GPT audit:
  proces_de_nithard       (English)
  carte_du_texte          (English)
  kaleidoscope            (English)
  twenty_five_rooms       (English)
  livre_fractal           (English)
  pari_de_nithard_II      (French)  — second pass
  pari_de_nithard_III     (French)  — second pass

Per-piece literary premise:
  proces  → real trial dossier; charges/testimonies/marginalia; bipartite
            structure becomes prosecution/defense rhetoric, never declared.
  carte   → 5x10 grid as cartographic map of a town/region; each page a
            location with directions to its grid neighbours felt as roads,
            not coordinates.
  kaleido → 17 events each in 3 incompatible voices: witness, analyst,
            fabulist. No 'voice' label; voices distinguished by style.
  rooms   → 25 prehistoric/environmental tableaux walking a 5x5 cave;
            constraint is felt as adjacency through scent/sound/light.
  fractal → coastline/measurement obsession; the measurer keeps failing,
            the ruler shrinks, the coast escapes. Never declared as fractal.

Strict guards: no graph terms, paragraph count preserved, length ±15%.
"""
import os
import re
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent / "qoulipo"

BANNED_COMMON = [
    r"\bgraph\b", r"\bvertex\b", r"\bvertices\b", r"\bedge\b", r"\bedges\b",
    r"\bMIS\b", r"\bindependent set\b", r"\bbackbone\b", r"\boptim(um|a)\b",
    r"\bgreedy\b", r"\bbenchmark\b", r"\bRydberg\b", r"\bblockade\b",
    r"\batom(s)?\b", r"\bregister\b", r"\bquantum (processor|computer)\b",
    r"\bUDG\b", r"\bunit[- ]disk\b", r"\bcosine similarity\b", r"\bk[- ]NN\b",
    r"\bnearest[- ]neighbour\b", r"\bthread( assignment)?\b", r"\brole\b\s*:",
    r"\bcoordinate\b\s*:", r"\bgrid\b\s*:", r"\bvoice\b\s*:",
]

PER_FOLDER = {
    "proces_de_nithard": {
        "lang": "English",
        "premise": (
            "A trial dossier: charges, testimonies, marginal notes, exhibits, "
            "contradictions. Twenty-five accusers and twenty-five defenders. "
            "Each prosecution voice answers a defense voice — the bipartite "
            "structure is felt as adversarial rhetoric, never declared. "
            "DO NOT use 'bipartite', 'graph', or any computational term. Make "
            "the prosecution pages thunderous; the defense pages quiet, "
            "forensic, careful. The trial concerns the legacy of Nithard."
        ),
    },
    "carte_du_texte": {
        "lang": "English",
        "premise": (
            "A topographic prose map of an imagined town arranged 5×10. Each "
            "page is one place — forge, mill, cloister, harbour, ridge, "
            "watchtower. Adjacent places are felt as walkable; non-adjacent "
            "places are days apart. DO NOT use 'grid', 'coordinate', "
            "'planar', 'r0c0' etc. Make the map readable as terrain, not "
            "lattice. Each page should have one weather, one trade, one "
            "smell, and at most one named figure."
        ),
    },
    "kaleidoscope": {
        "lang": "English",
        "premise": (
            "Seventeen events told in three incompatible voices: a witness "
            "(sensory, first-person, breathless), an analyst (austere, "
            "Pascalian, second-person), a fabulist (third-person fairy-tale, "
            "nursery cadence). The three are distinguished by STYLE only, "
            "never by labels. Each event-triad should feel like the same "
            "moment seen by three minds whose vocabularies barely overlap."
        ),
    },
    "twenty_five_rooms": {
        "lang": "English",
        "premise": (
            "Twenty-five tableaux of a single multi-chambered cavern, walked "
            "in order. Each tableau is one chamber: ochre walls, fossil "
            "ferns, glacial drip, mammoth ivory, flint shards, brackish pool. "
            "Adjacency is felt as scent, sound, draft; non-adjacency as "
            "geological distance. Do NOT use 'room', 'cell', 'king', "
            "'coordinate'; use cavern, gallery, alcove, niche, threshold. "
            "Reader should feel the walk."
        ),
    },
    "livre_fractal": {
        "lang": "English",
        "premise": (
            "A measurer's obsession with a coastline that refuses to be "
            "measured. Each page: a tide, a ruler shrinking, a stone, a "
            "wave, a notation that fails to close. The measurer is a real "
            "human (Mandelbrot in cameo, perhaps); the failure is felt as "
            "narrative, not declared as fractality. NO mathematical "
            "terminology in the prose; the recursion is dramatised through "
            "obsession, not named."
        ),
    },
    "pari_de_nithard_II": {
        "lang": "French",
        "premise": (
            "Deuxième volume du cycle de Nithard, en français littéraire. "
            "Préserver les noms propres et le récit chronicle, mais varier "
            "le vocabulaire des fils thématiques (pari, foi, épée, parchemin) "
            "par champs lexicaux : hasard/gageure, vœu/grâce, lame/acier, "
            "vélin/folio. Pas de terminologie computationnelle."
        ),
    },
    "pari_de_nithard_III": {
        "lang": "French",
        "premise": (
            "Troisième volume du cycle de Nithard, en français littéraire. "
            "Mêmes principes que le volume II : préserver le récit, varier "
            "le vocabulaire des fils thématiques par champs lexicaux. Pas de "
            "terminologie computationnelle, pas de 'graphe', 'sommet', etc."
        ),
    },
}

SYSTEM = """You are a literary editor. Rewrite the page below to embody the
piece's literary premise, with NO computational, graph-theoretic, or benchmark
vocabulary in the prose.

Premise: {premise}

HARD CONSTRAINTS (any violation → reject):
1. Banned terms (close cognates also banned): graph, vertex, edge, MIS,
   independent set, backbone, ρ, rho, optimum, greedy, benchmark, atom,
   register, Rydberg, blockade, quantum processor, UDG, unit-disk, cosine
   similarity, k-NN, nearest-neighbour, thread (as a graph thread), role
   header, coordinate header, grid header, voice header.
2. NO header lines like '#### PAGE N', '*Threads:*', '*Voice:*', '*Role:*',
   '*Form:*', '*Grid:*'. Return only literary prose.
3. Preserve the language ({lang}) and approximate length (±15%).
4. Preserve paragraph count.
5. Preserve named characters, place names, dates, historical references.

Return ONLY the rewritten prose. No preamble, no fences."""


def violates(text):
    text_lo = text.lower()
    for p in BANNED_COMMON:
        if re.search(p, text_lo, re.IGNORECASE):
            return True
    return False


def rewrite_one(client, system_prompt, text, model="claude-sonnet-4-5", max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            resp = client.messages.create(
                model=model, max_tokens=4096, system=system_prompt,
                messages=[{"role": "user", "content": text}],
            )
            if not resp.content:
                if attempt < max_retries: continue
                return None, resp.usage
            out = resp.content[0].text.strip()
            n_p_in = len(re.split(r"\n\s*\n", text.strip()))
            n_p_out = len(re.split(r"\n\s*\n", out))
            if abs(n_p_out - n_p_in) > 1:
                if attempt < max_retries: continue
                return None, resp.usage
            ratio = len(out) / max(1, len(text))
            if ratio < 0.6 or ratio > 1.6:
                if attempt < max_retries: continue
                return None, resp.usage
            if violates(out):
                if attempt < max_retries: continue
                return None, resp.usage
            return out, resp.usage
        except Exception as e:
            if attempt < max_retries: continue
            print(f"  ! API error: {e}")
            return None, None


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr); sys.exit(2)
    client = anthropic.Anthropic()
    total_in = total_out = 0
    n_ok = n_fail = 0
    for folder, cfg in PER_FOLDER.items():
        files = sorted((ROOT / folder / "source").glob("*.txt"))
        sys_p = SYSTEM.format(premise=cfg["premise"], lang=cfg["lang"])
        print(f"\n[{folder}] {cfg['lang']} / {len(files)} files", flush=True)
        for p in files:
            text = p.read_text(encoding="utf-8")
            if not text.strip():
                continue
            out, usage = rewrite_one(client, sys_p, text)
            if out is None:
                n_fail += 1
                continue
            p.write_text(out, encoding="utf-8")
            if usage:
                total_in += usage.input_tokens
                total_out += usage.output_tokens
            n_ok += 1
            if n_ok % 20 == 0:
                print(f"  ✓ {n_ok} pages rewritten", flush=True)
    cost = (total_in * 3 + total_out * 15) / 1_000_000
    print(f"\nTotals: {n_ok} ok, {n_fail} failed.")
    print(f"Tokens: {total_in:,} in, {total_out:,} out, ~${cost:.2f}")


if __name__ == "__main__":
    main()
