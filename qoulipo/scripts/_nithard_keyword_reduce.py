#!/usr/bin/env python3
"""Claude API Nithard-series keyword-stuffing reduction.

The Nithard texts (nithards_wager_en/fr, pari_de_nithard_II/III) repeat
their thread keywords ('wager', 'faith', 'sword', 'parchment', 'game' /
'pari', 'foi', 'épée', 'parchemin', 'jeu') at 2-5%% of word count, which
makes them read like SEO copy. The asserted designed graph does NOT
depend on the literary text (it's constructed from explicit thread
allocations, not NLP), so the literary text can be revised without
breaking the compute instance.

This script asks Claude (sonnet) to rewrite each page replacing direct
keyword repetitions with lexical-field alternatives, while preserving:
  - the Threads: header line (verbatim, since the asserted graph reads it)
  - the Role: header line (verbatim)
  - the page number and title line
  - the narrative voice and overall meaning

Each thread is allowed ONE direct mention per page; further mentions must
use synonyms, periphrases, or anaphoric reference.

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 corpus/_nithard_keyword_reduce.py            # all 4 folders
  python3 corpus/_nithard_keyword_reduce.py nithards_wager_en  # one folder
  python3 corpus/_nithard_keyword_reduce.py --dry-run  # cost only
"""
import argparse
import os
import re
import sys
import time
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Install: pip install anthropic", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent / "qoulipo"

FOLDERS = {
    "nithards_wager_en":   ("English", ["wager", "faith", "sword", "parchment", "game",
                                         "chronicle", "conspiracy", "tongue", "number",
                                         "ink", "maliette", "mirror"]),
    "nithards_wager_fr":   ("French",  ["pari", "foi", "épée", "epee", "parchemin", "jeu",
                                         "chronique", "conspiration", "langue", "nombre",
                                         "encre", "maliette", "miroir"]),
    "pari_de_nithard_II":  ("French",  ["pari", "foi", "épée", "epee", "parchemin", "jeu",
                                         "chronique", "conspiration", "langue", "nombre",
                                         "encre", "maliette", "miroir"]),
    "pari_de_nithard_III": ("French",  ["pari", "foi", "épée", "epee", "parchemin", "jeu",
                                         "chronique", "conspiration", "langue", "nombre",
                                         "encre", "maliette", "miroir"]),
}

SYSTEM = """You are a literary editor revising a constrained-OuLiPo text to reduce keyword stuffing.

CRITICAL CONSTRAINTS — violating any of these breaks the corpus design:
1. The first 3 header lines MUST be returned VERBATIM, character-for-character.
   These are typically:
       #### PAGE N -- Title
       *Threads: KEYWORD1, KEYWORD2, ...*
       *Voice: NAME*  (or *Role: ...*)
   Do not change them in any way.
2. The narrative content (paragraphs after the header) should be revised to
   reduce direct repetition of the thread keywords. Specifically:
   - For each thread keyword in the 'Threads:' header, allow AT MOST ONE
     direct mention in the body.
   - Replace further occurrences with synonyms, periphrases, anaphora, or
     pronouns. Use the lexical field, not the exact word.
   - Example: instead of repeating 'wager' five times, vary with 'bet',
     'gamble', 'stake', 'chance', 'risk', 'hazard', 'tossed against fate'.
3. PRESERVE the narrative voice, the named characters (Nithard, Pascal,
   Charlemagne, Lothar, etc.), the proper nouns, and the overall meaning of
   each paragraph.
4. PRESERVE markdown formatting (italics *like this*, bold **like this**,
   line breaks, blockquotes).
5. Match the language of the input ({lang}). Do not translate.
6. The thread keywords for THIS text are: {keywords}.
7. Return ONLY the revised page, no preamble, no explanation, no fences."""


def split_header(text):
    """Split a page into (header_lines, body) where header is the first 3 non-empty lines
    that look like markdown header + threads + voice/role."""
    lines = text.split("\n")
    head_idx = 0
    seen_thread = seen_voice = False
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        if s.startswith("####") or s.startswith("###") or s.startswith("##"):
            head_idx = i + 1
            continue
        if s.startswith("*Threads:") or s.startswith("*Threads :") or s.startswith("*Fils :"):
            seen_thread = True
            head_idx = i + 1
            continue
        if s.startswith("*Voice:") or s.startswith("*Role:") or s.startswith("*Voix:"):
            seen_voice = True
            head_idx = i + 1
            continue
        if seen_thread or seen_voice:
            break
        # First non-empty, non-markdown line — assume header is over
        break
    return "\n".join(lines[:head_idx]), "\n".join(lines[head_idx:])


def revise_one(client, lang, keywords, text, model="claude-sonnet-4-5", max_retries=2):
    sys_prompt = SYSTEM.format(lang=lang, keywords=", ".join(keywords))
    for attempt in range(max_retries + 1):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=4096,
                system=sys_prompt,
                messages=[{"role": "user", "content": text}],
            )
            out = resp.content[0].text.strip()
            # Strict header check
            head_in, _ = split_header(text)
            head_out, _ = split_header(out)
            if head_in.strip() != head_out.strip():
                if attempt < max_retries:
                    continue
                return None, resp.usage, "header-mismatch"
            return out, resp.usage, None
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2)
                continue
            raise


def keyword_density(text, keywords):
    text_lo = text.lower()
    n_words = max(1, len(text_lo.split()))
    n_kw = sum(len(re.findall(r"\b" + re.escape(k) + r"s?\b", text_lo)) for k in keywords)
    return n_kw / n_words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default="claude-sonnet-4-5")
    args = ap.parse_args()

    target = args.folders or list(FOLDERS.keys())
    if args.dry_run:
        n_files = 0
        n_chars = 0
        for f in target:
            files = sorted((ROOT / f / "source").glob("*.txt"))
            n_files += len(files)
            n_chars += sum(p.stat().st_size for p in files)
        tokens = n_chars / 3
        # Output expected to be similar size; sonnet ~$3/M in + $15/M out
        cost = (tokens / 1_000_000) * (3 + 15)
        print(f"Dry run: {n_files} files, ~{n_chars:,} chars, ~{int(tokens):,} tokens.")
        print(f"Estimated cost: ${cost:.2f} on {args.model}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(2)

    client = anthropic.Anthropic()
    total_in = total_out = 0
    for f in target:
        if f not in FOLDERS:
            print(f"SKIP unknown folder: {f}")
            continue
        lang, keywords = FOLDERS[f]
        files = sorted((ROOT / f / "source").glob("*.txt"))
        print(f"\n[{f}] {lang}, {len(files)} files, keywords={keywords[:5]}…")
        for p in files:
            text = p.read_text(encoding="utf-8")
            density_before = keyword_density(text, keywords)
            if density_before < 0.02:
                print(f"  - {p.name}: skipped (density {density_before*100:.1f}% already low)")
                continue
            out, usage, err = revise_one(client, lang, keywords, text, model=args.model)
            if out is None:
                print(f"  ! {p.name}: {err}; original kept")
                continue
            p.write_text(out, encoding="utf-8")
            density_after = keyword_density(out, keywords)
            total_in += usage.input_tokens
            total_out += usage.output_tokens
            print(f"  ✓ {p.name}: density {density_before*100:.1f}% → {density_after*100:.1f}% "
                  f"(in={usage.input_tokens}, out={usage.output_tokens})")
    cost = (total_in * 3 + total_out * 15) / 1_000_000
    print(f"\nTotals: {total_in:,} in + {total_out:,} out tokens ≈ ${cost:.2f}")


if __name__ == "__main__":
    main()
