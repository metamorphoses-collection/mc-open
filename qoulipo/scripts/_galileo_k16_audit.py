#!/usr/bin/env python3
"""Build Galileo k=16 graph at the canonical e5-large-instruct embedder.

This produces the current-embedder analogue of the Galileo k=16 graph used
in the QPU campaign with the pre-pivot (paraphrase-multilingual-MiniLM)
embedder. The asterisk on Galileo in Tables 7 and 11 marks that the
*QPU run itself* was on the pre-pivot embedder — re-submitting the QPU
batch on this current-embedder graph is a future task.

Output:
  corpus/natural/galileo_dialogo/graph_k16.json
"""
import json
import re
from pathlib import Path
from itertools import combinations

import numpy as np

ROOT = Path(__file__).resolve().parent / "natural" / "galileo_dialogo"
SOURCE = ROOT / "source" / "galileo_dialogo_full.txt"
OUT = ROOT / "graph_k16.json"

PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "
MODEL = "intfloat/multilingual-e5-large-instruct"
TARGET_N = 65        # match existing graph_k8.json
WORDS_PER_CHUNK = 400


def chunk_400_words(text, target_n):
    words = text.split()
    chunk_size = max(1, len(words) // target_n)
    chunks = []
    for i in range(target_n):
        chunks.append(" ".join(words[i * chunk_size:(i + 1) * chunk_size]))
    return chunks


def main():
    print(f"Loading {MODEL}...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL)
    text = SOURCE.read_text(encoding="utf-8")
    chunks = chunk_400_words(text, TARGET_N)
    print(f"Galileo: {TARGET_N} chunks of ~{WORDS_PER_CHUNK} words each.")

    embeddings = model.encode([PREFIX + c for c in chunks],
                              normalize_embeddings=True, show_progress_bar=True,
                              batch_size=8)
    sim = embeddings @ embeddings.T

    k = 16
    edges = set()
    for i in range(TARGET_N):
        order = np.argsort(-sim[i])
        # k nearest neighbours, skipping self
        for j in order[1:k+1]:
            a, b = sorted((int(i), int(j)))
            edges.add((a, b))

    nodes = [f"chunk_{i:03d}" for i in range(TARGET_N)]
    edges_out = [{"source": nodes[a], "target": nodes[b]} for a, b in sorted(edges)]
    N = TARGET_N
    E = len(edges_out)
    d = round(2 * E / (N * (N - 1)), 4)
    out = {
        "N": N, "E": E, "density": d, "k": k,
        "embedder": MODEL,
        "chunking": f"linear {WORDS_PER_CHUNK}-word window, {TARGET_N} chunks",
        "source": "Built by corpus/_galileo_k16_audit.py from galileo_dialogo_full.txt.",
        "nodes": nodes,
        "edges": edges_out,
    }
    OUT.write_text(json.dumps(out, indent=2))
    print(f"\n✓ {OUT}: N={N}, E={E}, d={d}")


if __name__ == "__main__":
    main()
