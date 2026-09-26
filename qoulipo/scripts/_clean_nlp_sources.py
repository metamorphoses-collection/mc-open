#!/usr/bin/env python3
"""GPT-5.5 audit C1-C2: clean canonical-NLP source pages of metadata contamination.

For folders whose canonical graph is NLP-derived, the source text must be the
literary content only — no Threads:, Form:, semantic-coordinate, or
title-page lines. After cleaning, the NLP graph is rebuilt from the cleaned
source so the deposit is reproducible end-to-end.

  partition_du_texte          — strip per-page Threads:/Form: headers; rebuild k=8
  vita_nel_cubo               — move page_001 paratext intro to paratext/; rebuild k=8
  sonetti_dal_tesseratto      — strip semantic-coordinate header from each page; rebuild k=8

Designed-graph folders (jumeaux EN/FR, etc.) are not graph-rebuilt; their
title-pages are moved to paratext where they violate the literary contract.
"""
import json
import math
import re
import shutil
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent / "qoulipo"

PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "
EMBEDDER = "intfloat/multilingual-e5-large-instruct"


def strip_partition_headers(folder):
    """Remove the first 3 header lines (####PAGE / *Threads:* / *Form:*) from every source page."""
    src = ROOT / folder / "source"
    n_changed = 0
    for p in sorted(src.glob("*.txt")):
        text = p.read_text(encoding="utf-8")
        # Pattern: optional #### PAGE line + *Threads:* line + *Form:* line at the very top
        # Strip up to first blank line if matches.
        lines = text.split("\n")
        i = 0
        # Eat any leading lines that are markdown header / *Threads:* / *Form:*
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("####") or s.startswith("###") or s.startswith("##") or s.startswith("#"):
                i += 1; continue
            if s.startswith("*Threads:") or s.startswith("*Form:") or s.startswith("*Voice:") or s.startswith("*Role:"):
                i += 1; continue
            if s == "":
                i += 1; break
            break
        new_text = "\n".join(lines[i:]).lstrip()
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_changed += 1
    return n_changed


def move_intro_to_paratext(folder, page_filename):
    """Move a single source page to paratext/ as a frontispiece."""
    src = ROOT / folder / "source" / page_filename
    para = ROOT / folder / "paratext"
    para.mkdir(exist_ok=True)
    if src.exists():
        shutil.move(str(src), str(para / page_filename))
        return True
    return False


def strip_sonetti_header(folder):
    """Sonetti pages start with ## 0000 — Terra,... *"incipit"* then the sonnet body.
    Strip the ## semantic-coordinate header, keep the italic incipit + body."""
    src = ROOT / folder / "source"
    n_changed = 0
    for p in sorted(src.glob("*.txt")):
        text = p.read_text(encoding="utf-8")
        # Match the ## semantic-coord header pattern at start (with or without the rest on same line)
        m = re.match(r"^##\s+\d+\s+—\s+[^\n*]+\n?", text)
        if m:
            new_text = text[m.end():].lstrip()
            if new_text != text:
                p.write_text(new_text, encoding="utf-8")
                n_changed += 1
    return n_changed


def rebuild_k8_graph(folder, model):
    """Rebuild graph_k8.json from cleaned source/ at canonical embedder."""
    src = ROOT / folder / "source"
    files = sorted(src.glob("*.txt"))
    texts = [p.read_text(encoding="utf-8") for p in files]
    nodes = [p.stem for p in files]
    print(f"  Embedding {len(texts)} pages...", flush=True)
    emb = model.encode([PREFIX + t for t in texts], normalize_embeddings=True,
                       show_progress_bar=False, batch_size=8)
    sim = emb @ emb.T
    k = 8
    edges = set()
    for i in range(len(nodes)):
        order = np.argsort(-sim[i])
        for j in order[1:k+1]:
            a, b = sorted((int(i), int(j)))
            edges.add((a, b))
    edges_out = [{"source": nodes[a], "target": nodes[b]} for a, b in sorted(edges)]
    N = len(nodes)
    E = len(edges_out)
    d = round(2 * E / (N * (N - 1)), 4) if N > 1 else 0
    out = {
        "N": N, "E": E, "density": d, "k": k,
        "embedder": EMBEDDER,
        "source": "Rebuilt by _clean_nlp_sources.py from cleaned source/ pages.",
        "nodes": nodes,
        "edges": edges_out,
    }
    out_path = ROOT / folder / "graph_k8.json"
    out_path.write_text(json.dumps(out, indent=2))
    return N, E, d


def main():
    from sentence_transformers import SentenceTransformer

    print("[partition_du_texte] strip headers from canonical pages")
    n = strip_partition_headers("partition_du_texte")
    print(f"  stripped headers from {n} pages")

    print("\n[vita_nel_cubo] move paratext page_001 to paratext/")
    moved = move_intro_to_paratext("vita_nel_cubo", "page_001.txt")
    print(f"  moved: {moved}")

    print("\n[sonetti_dal_tesseratto] strip semantic-coordinate headers")
    n = strip_sonetti_header("sonetti_dal_tesseratto")
    print(f"  stripped headers from {n} pages")

    # Move jumeaux title pages to paratext (file is page_001.txt)
    print("\n[jumeaux_en] move title page_001 to paratext/")
    moved = move_intro_to_paratext("jumeaux_en", "page_001.txt")
    print(f"  moved: {moved}")
    print("[jumeaux_fr] move title page_001 to paratext/")
    moved = move_intro_to_paratext("jumeaux_fr", "page_001.txt")
    print(f"  moved: {moved}")

    # Now rebuild k=8 NLP graphs for the canonical-NLP folders
    print(f"\nLoading {EMBEDDER}…")
    model = SentenceTransformer(EMBEDDER)

    for folder in ("partition_du_texte", "vita_nel_cubo", "sonetti_dal_tesseratto"):
        print(f"\n[{folder}] rebuilding graph_k8.json")
        N, E, d = rebuild_k8_graph(folder, model)
        print(f"  ✓ N={N}, E={E}, d={d}")


if __name__ == "__main__":
    main()
