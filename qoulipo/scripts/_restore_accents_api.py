#!/usr/bin/env python3
"""Claude API accent restoration. Strict preservation: add only diacritics.

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 corpus/_restore_accents_api.py            # all 5 folders
  python3 corpus/_restore_accents_api.py castello_49_destini   # one folder
  python3 corpus/_restore_accents_api.py --dry-run  # estimate cost only

Behavior:
  - Reads each .txt file in folder/source/
  - Sends to Claude (sonnet) with a system prompt that forbids any change other
    than adding French/Italian diacritics
  - Writes the response back if (and only if) it parses as a strict superset
    diacritic edit (same length on stripped form, same characters modulo accents)
  - Skips files that already pass the diacritic-density check (>= 0.5%)
"""
import argparse
import os
import sys
import time
import unicodedata
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Install: pip install anthropic", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent / "qoulipo"

FOLDERS = {
    "jumeaux_fr":               ("French",  "*.txt"),
    "partition_du_texte":       ("French",  "*.txt"),
    "pascal_apocryphe":         ("French",  "*.txt"),
    "pascal_apocryphe_scholia": ("French",  "*.txt"),
    "castello_49_destini":      ("Italian", "*.txt"),
}

SYSTEM = (
    "You are a strict orthographic restoration tool for {lang} text.\n"
    "Task: add missing diacritics (accents) to the text below. Do NOT change "
    "any word, do NOT add or remove punctuation, do NOT reflow lines, do NOT "
    "alter capitalisation except where adding an accent (e.g. 'E' → 'É'). "
    "Only diacritic-adding edits are allowed.\n"
    "Preserve all whitespace, line breaks, markdown headers (####), and "
    "italics/bold marks (* and **) verbatim.\n"
    "Return ONLY the corrected text, no preamble, no explanation, no fences."
)


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def is_strict_diacritic_edit(orig, restored):
    """True iff restored differs from orig only by adding diacritics."""
    return strip_accents(restored) == strip_accents(orig)


def diacritic_density(text):
    if not text:
        return 0.0
    n_acc = sum(1 for c in text if unicodedata.category(c) == "Mn"
                or c in "àáâäéèêëíîïóôöúùûüçÀÉÈÊÇñÑáàèéêëîïôöùûüçœŒæÆ")
    return n_acc / max(1, len(text.split()))


def restore_one(client, lang, text, model="claude-sonnet-4-5", max_retries=2):
    sys_prompt = SYSTEM.format(lang=lang)
    for attempt in range(max_retries + 1):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=4096,
                system=sys_prompt,
                messages=[{"role": "user", "content": text}],
            )
            out = resp.content[0].text
            if is_strict_diacritic_edit(text, out):
                return out, resp.usage
            else:
                # If model added/removed words, retry once with stricter prompt
                if attempt < max_retries:
                    continue
                return None, resp.usage
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2)
                continue
            raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default="claude-sonnet-4-5")
    args = ap.parse_args()

    target_folders = args.folders or list(FOLDERS.keys())
    if args.dry_run:
        n_files = 0
        n_chars = 0
        for f in target_folders:
            src = ROOT / f / "source"
            files = sorted(src.glob(FOLDERS[f][1]))
            n_files += len(files)
            n_chars += sum(p.stat().st_size for p in files)
        # Sonnet pricing (~$3/M input + $15/M output, very rough): assume input≈output
        tokens = n_chars / 3  # ~3 chars per token
        cost = (tokens / 1_000_000) * (3 + 15)
        print(f"Dry run: {n_files} files, ~{n_chars:,} chars, ~{int(tokens):,} tokens.")
        print(f"Estimated cost: ${cost:.2f} on {args.model}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(2)

    client = anthropic.Anthropic()
    total_in = total_out = 0
    for f in target_folders:
        if f not in FOLDERS:
            print(f"SKIP unknown folder: {f}")
            continue
        lang, pattern = FOLDERS[f]
        src = ROOT / f / "source"
        files = sorted(src.glob(pattern))
        print(f"\n[{f}] {lang}, {len(files)} files")
        for p in files:
            text = p.read_text(encoding="utf-8")
            density_before = diacritic_density(text)
            if density_before > 0.05:
                print(f"  - {p.name}: skipped (density {density_before:.3f} suggests already accented)")
                continue
            out, usage = restore_one(client, lang, text, model=args.model)
            if out is None:
                print(f"  ! {p.name}: model output rejected (non-diacritic edits)")
                continue
            p.write_text(out, encoding="utf-8")
            total_in += usage.input_tokens
            total_out += usage.output_tokens
            density_after = diacritic_density(out)
            print(f"  ✓ {p.name}: density {density_before:.3f} → {density_after:.3f} "
                  f"(in={usage.input_tokens}, out={usage.output_tokens})")
    cost = (total_in * 3 + total_out * 15) / 1_000_000
    print(f"\nTotals: {total_in:,} in + {total_out:,} out tokens ≈ ${cost:.2f}")


if __name__ == "__main__":
    main()
