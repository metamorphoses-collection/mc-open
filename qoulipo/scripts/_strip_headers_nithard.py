#!/usr/bin/env python3
"""Strip *Threads:*, *Voice:*, *Role:*, *Form:* header lines from Nithard
source pages. Capture the per-page thread allocation in
metadata.json[threads_per_page] so the design intent is preserved."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "qoulipo"
FOLDERS = ["nithards_wager_en", "nithards_wager_fr",
           "pari_de_nithard_II", "pari_de_nithard_III"]


def parse_threads(line):
    s = line.strip().lstrip("*").rstrip("*").strip()
    s = re.sub(r"^(threads|fils)\s*:?\s*", "", s, flags=re.IGNORECASE)
    return [t.strip() for t in re.split(r"[,;]", s) if t.strip()]


def strip_one_page(text):
    lines = text.split("\n")
    threads = []
    voice = None
    role = None
    form = None
    title = None
    i = 0
    consumed_any = False
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            if consumed_any:
                i += 1
                break
            i += 1
            continue
        if s.startswith("####") or s.startswith("###") or s.startswith("##") or s.startswith("#"):
            title = s
            i += 1
            consumed_any = True
            continue
        m = re.match(r"^\*?(?:threads|fils)\s*:?\s*(.+?)\*?$", s, re.IGNORECASE)
        if m:
            threads = parse_threads(s)
            i += 1
            consumed_any = True
            continue
        m = re.match(r"^\*?voice\s*:?\s*(.+?)\*?$", s, re.IGNORECASE)
        if m:
            voice = m.group(1).strip().rstrip("*").strip()
            i += 1
            consumed_any = True
            continue
        m = re.match(r"^\*?role\s*:?\s*(.+?)\*?$", s, re.IGNORECASE)
        if m:
            role = m.group(1).strip().rstrip("*").strip()
            i += 1
            consumed_any = True
            continue
        m = re.match(r"^\*?form\s*:?\s*(.+?)\*?$", s, re.IGNORECASE)
        if m:
            form = m.group(1).strip().rstrip("*").strip()
            i += 1
            consumed_any = True
            continue
        if consumed_any:
            break
        break
    body = "\n".join(lines[i:]).lstrip()
    return body, {"title": title, "threads": threads, "voice": voice, "role": role, "form": form}


def main():
    for folder in FOLDERS:
        src = ROOT / folder / "source"
        files = sorted(src.glob("*.txt"))
        per_page = {}
        n_changed = 0
        for p in files:
            text = p.read_text(encoding="utf-8")
            body, head = strip_one_page(text)
            if body.strip() and body != text:
                p.write_text(body, encoding="utf-8")
                n_changed += 1
                per_page[p.stem] = {k: v for k, v in head.items() if v}
        meta_path = ROOT / folder / "metadata.json"
        meta = json.loads(meta_path.read_text())
        meta["threads_per_page"] = per_page
        meta["literary_status"] = ("Source pages contain literary content only; per-page thread "
                                    "allocations and voice/role/form metadata are recorded above "
                                    "in threads_per_page (not in source/).")
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        print(f"[{folder}] stripped {n_changed}/{len(files)} pages; threads_per_page recorded in metadata.")


if __name__ == "__main__":
    main()
