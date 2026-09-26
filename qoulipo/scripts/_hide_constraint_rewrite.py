#!/usr/bin/env python3
"""GPT-5.5 audit C5/C6: literary rewrite to hide the constraint.

Two passes:
  1. nithards_wager_en + pari_de_nithard_II + pari_de_nithard_III
     — replace explicit graph terminology (vertex, edge, graph, network,
       enumeration of cabals, etc.) with literary equivalents; preserve
       narrative voice and character continuity.
  2. incarnate_graph/source/page_001.txt
     — completely rewrite the didactic preamble as the first literary page
       (introducing the three narrators in narrative form, no overt
       constraint declaration). All other pages get a constraint-hiding
       pass that replaces 'graph', 'atoms', 'register', 'pages', 'fifty',
       'sixty-five', 'UDG', 'blockade', 'Rydberg', 'quantum processor'
       with literary equivalents.

Strict guard: paragraph count preserved, page header (if any) preserved,
narrative voice preserved.
"""
import os
import re
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent / "qoulipo"

NITHARD_FOLDERS = ["nithards_wager_en", "pari_de_nithard_II", "pari_de_nithard_III"]

NITHARD_SYS = """You are a literary editor tightening a historical-philosophical novel.

The narrator is a Carolingian chronicler (Nithard of Saint-Riquier). The
text was written under a graph-theoretic constraint, but the constraint
SHOULD NOT be visible to the reader. Currently several pages contain
explicit graph terminology that breaks the spell: 'vertex', 'edge',
'graph', 'network', 'enumeration', 'combinatorial', 'fabrication of the
graph', 'cabals', etc.

Rewrite the page below so that:
1. ALL explicit graph terminology is replaced with literary equivalents.
   - 'vertex' → 'figure', 'name', 'face', 'witness', or character-specific
   - 'edge' / 'link' → 'tie', 'bond', 'thread', 'connection of blood or oath'
   - 'graph' / 'network' → 'web', 'tapestry', 'lineage', 'fabric of
     allegiances', 'chain of names'
   - 'enumeration' / 'combinatorics' → 'tally', 'reckoning', 'inventory of
     names', 'accounting of treacheries'
2. Each thread keyword in the original ({keywords}) appears at most once
   per paragraph. Use lexical-field synonyms for further mentions.
3. The narrator's voice (first-person Nithard / third-person chronicler /
   Pascal / the Professor with the maliette) is preserved.
4. Character names, dates, place names, historical references are preserved
   verbatim (Lothar, Pepin, Fontenoy, Strasbourg, Charlemagne, etc.).
5. Paragraph structure (number of paragraphs) is preserved.
6. The text remains in {lang}.

Return ONLY the revised page. No preamble, no explanation, no fences."""

INCARNATE_SYS = """You are a literary editor revising a constrained-OuLiPo novel cycle.

The text is built on three narrative voices — Nithard the Carolingian
chronicler, Pascal the geometer, the Professor (le Porteur de Maliettes) —
and a constraint that the reader should NOT have to see explicitly. Currently
some pages mention 'the graph', 'the atoms', 'the register', 'sixty-five
pages', 'the UDG', 'the constraint', etc. These are constraint-declarations
that break the literary spell.

Rewrite the page below so that:
1. ALL meta-references to the graph / atoms / register / quantum / UDG /
   blockade / Rydberg / 'this book is a quantum processor' / page count
   are removed or rewritten as literary metaphors that do NOT name the
   technical object. Substitute:
     - 'graph' → 'tapestry', 'lineage', 'web of names'
     - 'atom' → 'page', 'leaf', 'witness', 'fragment'
     - 'register' / 'lattice' → 'manuscript', 'codex', 'ledger'
     - 'sixty-five pages' → 'this book' or 'the work' or omit count
     - explicit numbers like 65, 24.25 um, 8.0 um → drop them
     - 'unit disk graph' / 'UDG' / 'Rydberg' / 'quantum processor' / 'Pasqal' / 'Fresnel' → drop or replace with neutral words
2. The three voices are preserved (Nithard / Pascal / Professor).
3. Paragraph structure (number of paragraphs) is preserved.
4. The narrative meaning is preserved — the page still does what it did
   literarily, but without naming the constraint.
5. Match the input language ({lang}).

Return ONLY the revised page. No preamble, no explanation, no fences."""


# Patterns that indicate constraint contamination (rough — used to decide if rewrite needed)
GRAPH_TERMS_RE = re.compile(
    r"\b(vertex|vertices|edge|edges|graph|network|combinatori|enumeration|UDG|"
    r"unit[- ]disk|Rydberg|blockade|atom|atomic register|quantum processor|"
    r"Pasqal|Fresnel|optical lattice|cosine similarity|sommet|arête|arete|"
    r"graphe|réseau|reseau|combinatoire|énumération|enumeration)\b",
    re.IGNORECASE,
)


def needs_rewrite(text):
    return bool(GRAPH_TERMS_RE.search(text))


def rewrite_one(client, system_prompt, text, model="claude-sonnet-4-5", max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            resp = client.messages.create(
                model=model, max_tokens=4096, system=system_prompt,
                messages=[{"role": "user", "content": text}],
            )
            if not resp.content:
                if attempt < max_retries:
                    continue
                return None, resp.usage
            out = resp.content[0].text.strip()
            # Sanity: paragraph count similar
            n_p_in = len(re.split(r"\n\s*\n", text.strip()))
            n_p_out = len(re.split(r"\n\s*\n", out))
            if abs(n_p_out - n_p_in) > 1:
                if attempt < max_retries:
                    continue
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

    NITHARD_KEYS = {
        "nithards_wager_en":   ["wager","faith","sword","parchment","game","chronicle","conspiracy","tongue","number","ink","maliette","mirror"],
        "pari_de_nithard_II":  ["pari","foi","épée","epee","parchemin","jeu","chronique","conspiration","langue","nombre","encre","maliette","miroir"],
        "pari_de_nithard_III": ["pari","foi","épée","epee","parchemin","jeu","chronique","conspiration","langue","nombre","encre","maliette","miroir"],
    }
    LANG = {"nithards_wager_en": "English", "pari_de_nithard_II": "French", "pari_de_nithard_III": "French"}

    # 1. Nithard sweep — only pages that contain graph terminology
    for folder in NITHARD_FOLDERS:
        files = sorted((ROOT / folder / "source").glob("*.txt"))
        targets = [p for p in files if needs_rewrite(p.read_text(encoding="utf-8"))]
        if not targets:
            print(f"[{folder}] no pages need rewrite (clean)")
            continue
        print(f"\n[{folder}] rewriting {len(targets)} pages with graph terminology")
        sys_p = NITHARD_SYS.format(keywords=", ".join(NITHARD_KEYS[folder]), lang=LANG[folder])
        for p in targets:
            text = p.read_text(encoding="utf-8")
            out, usage = rewrite_one(client, sys_p, text)
            if out is None:
                n_fail += 1
                print(f"  ! {p.name}: rewrite failed (empty/guard)")
                continue
            p.write_text(out, encoding="utf-8")
            if usage:
                total_in += usage.input_tokens
                total_out += usage.output_tokens
            n_ok += 1
            if n_ok % 10 == 0:
                print(f"  ✓ {n_ok} pages rewritten so far")

    # 2. Incarnate Graph — every page (rewrites needed are widespread)
    print("\n[incarnate_graph] full constraint-hiding rewrite (65 pages)")
    files = sorted((ROOT / "incarnate_graph" / "source").glob("*.txt"))
    sys_p = INCARNATE_SYS.format(lang="English")
    for p in files:
        text = p.read_text(encoding="utf-8")
        out, usage = rewrite_one(client, sys_p, text)
        if out is None:
            n_fail += 1
            print(f"  ! {p.name}: paragraph-count guard failed")
            continue
        p.write_text(out, encoding="utf-8")
        total_in += usage.input_tokens
        total_out += usage.output_tokens
        n_ok += 1
        if n_ok % 15 == 0:
            print(f"  ✓ {n_ok} total pages rewritten")

    cost = (total_in * 3 + total_out * 15) / 1_000_000
    print(f"\nTotals: {n_ok} ok, {n_fail} failed.")
    print(f"Tokens: {total_in:,} in, {total_out:,} out, ~${cost:.2f}")


if __name__ == "__main__":
    main()
