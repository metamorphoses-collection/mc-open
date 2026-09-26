#!/usr/bin/env python3
"""GPT round-2 audit C5/C6: literary lift for the 4 pieces still showing
constraint terminology in the prose (irreplaceable_book, piege_du_lecteur,
jumeaux_en, jumeaux_fr).

Per-piece literary premise from GPT's audit:
  irreplaceable_book → bibliographic / archival vocabulary (catchwords,
                       wormholes, missing folios, marginalia, colophons).
                       NEVER 'graph', 'MIS', 'backbone', 'vertex', 'edge',
                       'double domination'.
  piege_du_lecteur   → trap pages must SEDUCE; truth pages quiet but
                       structurally necessary; narrator misleads.
                       NEVER 'graph', 'greedy', 'optimum', 'TRUTH page',
                       'TRAP page', 'narrator'.
  jumeaux_en/fr      → paired chronicles. Constraint becomes: every
                       English paragraph has a French shadow on the
                       same theme. Constraint is felt, not declared.
                       NEVER 'isomorphic', 'graph', 'thread', 'edge',
                       'identity', 'twin' as label (literary metaphor OK).

Strict guards: no banned terms allowed in output; paragraph count
preserved; length ±15%.
"""
import os
import re
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent / "qoulipo"

BANNED = {
    "common": [
        r"\bgraph\b", r"\bvertex\b", r"\bvertices\b", r"\bedge\b", r"\bedges\b",
        r"\bMIS\b", r"\bindependent set\b", r"\bbackbone\b", r"\bρ\b", r"\brho\b",
        r"\boptim(um|a)\b", r"\bgreedy\b", r"\bbenchmark\b",
        r"\bRydberg\b", r"\bblockade\b", r"\batom(s)?\b", r"\bregister\b",
        r"\bquantum (processor|computer)\b", r"\bUDG\b", r"\bunit[- ]disk\b",
        r"\bcosine similarity\b", r"\bk[- ]NN\b", r"\bnearest[- ]neighbour\b",
        r"\bthread( assignment)?\b", r"\brole\b\s*:", r"\bcoordinate\b\s*:",
        r"\bgrid\b\s*:", r"\bvoice\b\s*:",
    ],
    "irreplaceable": [r"\bdouble dominat", r"\bunique solution", r"\bremoval test\b"],
    "piege": [r"\bTRUTH (page|node)", r"\bTRAP (page|node)", r"\bNARRATOR\b\s*pages?\b"],
    "jumeaux": [r"\bisomorph", r"\bidentical (page|graph|edge)\b", r"\btwin (graph|page)\b"],
}

PER_FOLDER = {
    "irreplaceable_book": {
        "lang": "English",
        "premise": (
            "A bibliographic fable: a 50-leaf book whose seventeen central leaves "
            "cannot be removed without making the archive unreadable. Use only "
            "bibliographic and material vocabulary — quires, stitching, wormholes, "
            "marginalia, errata, colophons, catchwords, vellum, ink, missing folios. "
            "DO NOT use any computational or graph-theoretic terminology."
        ),
        "extra_banned": "irreplaceable",
    },
    "piege_du_lecteur": {
        "lang": "English",
        "premise": (
            "A book that seduces the reader toward gorgeous, vivid pages while "
            "the structurally necessary truths are quieter. The narrator is "
            "untrustworthy. Make the seductive pages quotable. Make the truth "
            "pages plain but felt. DO NOT label any page as TRUTH, TRAP, or "
            "NARRATOR; do not name the construction. Let the reader experience "
            "the failure of greedy reading WITHOUT being told it is happening."
        ),
        "extra_banned": "piege",
    },
    "jumeaux_en": {
        "lang": "English",
        "premise": (
            "An English chronicle paired with its French shadow: each English "
            "paragraph faces a French paragraph on the same theme on the facing "
            "page. The pairing is felt as resonance, not declared. DO NOT name "
            "the pairing as 'isomorphic', 'graph-twin', 'identical structure', or "
            "any computational analogue. Use literary mirror vocabulary instead."
        ),
        "extra_banned": "jumeaux",
    },
    "jumeaux_fr": {
        "lang": "French",
        "premise": (
            "Une chronique française accompagnée de son ombre anglaise: chaque "
            "paragraphe français est accompagné d'un paragraphe anglais qui le "
            "redouble dans la page d'en face. L'écho est ressenti, jamais déclaré. "
            "NE PAS nommer l'appariement comme 'isomorphe', 'graphe-jumeau', "
            "'structure identique' ou tout équivalent computationnel. Utiliser "
            "plutôt un vocabulaire littéraire de miroir et de gémellité fabuleuse."
        ),
        "extra_banned": "jumeaux",
    },
}

SYSTEM = """You are a literary editor. Rewrite the page below to embody a
constrained literary premise WITHOUT any computational, graph-theoretic, or
benchmark vocabulary in the prose.

Premise for this piece: {premise}

HARD CONSTRAINTS (any violation → reject):
1. Do NOT use any of these terms or close cognates: graph, vertex, edge, MIS,
   independent set, backbone, ρ, rho, optimum, greedy, benchmark, atom, register,
   Rydberg, blockade, quantum processor, UDG, unit-disk, cosine similarity,
   k-NN, nearest-neighbour, thread (as a graph thread), role, coordinate, grid,
   voice (as a label header).
2. Do NOT add a header line like '#### PAGE N', '*Threads:*', '*Voice:*',
   '*Role:*', '*Form:*', '*Grid:*'. Return only literary prose.
3. Preserve the language ({lang}) and approximate length (±15%).
4. Preserve paragraph count.
5. Preserve named characters, place names, dates, historical references.

Return ONLY the rewritten prose. No preamble, no fences."""


def violates(text, lang_extra_banned):
    pats = BANNED["common"] + BANNED.get(lang_extra_banned, [])
    text_lo = text.lower()
    for p in pats:
        if re.search(p, text_lo, re.IGNORECASE):
            return True
    return False


def rewrite_one(client, system_prompt, text, banned_key, model="claude-sonnet-4-5", max_retries=2):
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
            # Guard: paragraph count
            n_p_in = len(re.split(r"\n\s*\n", text.strip()))
            n_p_out = len(re.split(r"\n\s*\n", out))
            if abs(n_p_out - n_p_in) > 1:
                if attempt < max_retries: continue
                return None, resp.usage
            # Guard: length
            ratio = len(out) / max(1, len(text))
            if ratio < 0.6 or ratio > 1.6:
                if attempt < max_retries: continue
                return None, resp.usage
            # Guard: banned terms
            if violates(out, banned_key):
                if attempt < max_retries: continue
                return None, resp.usage
            return out, resp.usage
        except Exception as e:
            if attempt < max_retries:
                continue
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
        ban = cfg["extra_banned"]
        print(f"\n[{folder}] {cfg['lang']} / {len(files)} files", flush=True)
        for p in files:
            text = p.read_text(encoding="utf-8")
            out, usage = rewrite_one(client, sys_p, text, ban)
            if out is None:
                n_fail += 1
                continue
            p.write_text(out, encoding="utf-8")
            if usage:
                total_in += usage.input_tokens
                total_out += usage.output_tokens
            n_ok += 1
            if n_ok % 10 == 0:
                print(f"  ✓ {n_ok} pages rewritten", flush=True)
    cost = (total_in * 3 + total_out * 15) / 1_000_000
    print(f"\nTotals: {n_ok} ok, {n_fail} failed.")
    print(f"Tokens: {total_in:,} in, {total_out:,} out, ~${cost:.2f}")


if __name__ == "__main__":
    main()
