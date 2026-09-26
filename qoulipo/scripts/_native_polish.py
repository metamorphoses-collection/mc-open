#!/usr/bin/env python3
"""Native-speaker literary polish pass for FR / IT QOuLiPo texts.

Run AFTER accent restoration is complete. Each text gets passed through
a native-speaker literary-editor prompt that improves register, idiom,
flow, and naturalness, while:
  - PRESERVING paragraph structure and named characters
  - PRESERVING the language (FR stays FR, IT stays IT)
  - PRESERVING any first-line markdown header (# / ##)
  - NOT lengthening or shortening the page significantly

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 corpus/_native_polish.py            # all FR + IT folders
  python3 corpus/_native_polish.py castello_49_destini  # one folder
  python3 corpus/_native_polish.py --dry-run
"""
import argparse
import os
import re
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent / "qoulipo"

FOLDERS = {
    "jumeaux_fr":               ("French",  "literary"),
    "partition_du_texte":       ("French",  "poetic"),  # Alexandrines, sonnets etc.
    "pascal_apocryphe":         ("French",  "novelistic"),
    "pascal_apocryphe_scholia": ("French",  "scholarly"),
    "pari_de_nithard_II":       ("French",  "chronicler"),
    "pari_de_nithard_III":      ("French",  "chronicler"),
    "castello_49_destini":      ("Italian", "Calvinian"),
    "vita_nel_cubo":            ("Italian", "lyrical"),
    "sonetti_dal_tesseratto":   ("Italian", "sonnets"),
    "venticinque_stanze":       ("Italian", "novella-king-grid"),
}

SYSTEM = """You are a native-{lang}-speaking literary editor.

Your task is to polish the page below to native literary quality. The
register is {register}. Improve:
  - Idiomatic phrasing — replace stiff or translated-sounding constructions
    with natural {lang} alternatives
  - Sentence rhythm — break up monotonous strings, vary clause length
  - Lexical precision — replace generic words with the precise {lang} term
  - Punctuation per {lang} typographic conventions

PRESERVE:
  - All named characters, dates, places, and historical references
  - The narrative voice and viewpoint
  - The number of paragraphs (do not merge or split)
  - The length of the page (within ±10%)
  - Any markdown header on the first line (# / ## / #### …)
  - The language: {lang} stays {lang}; do not translate

DO NOT:
  - Add a translator's note, preamble, explanation, or fences
  - Add or remove proper nouns
  - Significantly change the meaning of any sentence

Return ONLY the polished page. No commentary, no fences, no preface."""


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
            # Sanity: paragraph count similar; length within reason
            n_p_in = len(re.split(r"\n\s*\n", text.strip()))
            n_p_out = len(re.split(r"\n\s*\n", out))
            if abs(n_p_out - n_p_in) > 1:
                if attempt < max_retries:
                    continue
                return None, resp.usage
            len_ratio = len(out) / max(1, len(text))
            if len_ratio < 0.7 or len_ratio > 1.4:
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
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default="claude-sonnet-4-5")
    args = ap.parse_args()

    target = args.folders or list(FOLDERS.keys())
    if args.dry_run:
        n_files = 0; n_chars = 0
        for f in target:
            files = sorted((ROOT / f / "source").glob("*.txt"))
            n_files += len(files)
            n_chars += sum(p.stat().st_size for p in files)
        tokens = n_chars / 3
        cost = (tokens / 1_000_000) * (3 + 15)
        print(f"Dry run: {n_files} files, ~{n_chars:,} chars, ~{int(tokens):,} tokens, ~${cost:.2f}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr); sys.exit(2)
    client = anthropic.Anthropic()
    total_in = total_out = 0
    n_ok = n_fail = 0
    for folder in target:
        if folder not in FOLDERS:
            print(f"SKIP unknown {folder}"); continue
        lang, register = FOLDERS[folder]
        files = sorted((ROOT / folder / "source").glob("*.txt"))
        sys_p = SYSTEM.format(lang=lang, register=register)
        print(f"\n[{folder}] {lang} / {register} / {len(files)} files", flush=True)
        for p in files:
            text = p.read_text(encoding="utf-8")
            out, usage = rewrite_one(client, sys_p, text)
            if out is None:
                n_fail += 1
                print(f"  ! {p.name}: rewrite failed", flush=True)
                continue
            p.write_text(out, encoding="utf-8")
            if usage:
                total_in += usage.input_tokens
                total_out += usage.output_tokens
            n_ok += 1
            if n_ok % 20 == 0:
                print(f"  ✓ {n_ok} pages polished so far", flush=True)
    cost = (total_in * 3 + total_out * 15) / 1_000_000
    print(f"\nTotals: {n_ok} ok, {n_fail} failed.")
    print(f"Tokens: {total_in:,} in, {total_out:,} out, ~${cost:.2f}")


if __name__ == "__main__":
    main()
