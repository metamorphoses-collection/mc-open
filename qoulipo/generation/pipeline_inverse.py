#!/usr/bin/env python3
"""
Pipeline-inverse experiment: does the NLP+k-NN pipeline recover
the designed graph of an engineered text?

For each (text_file, designed_graph) pair:
  1. Split the text into chapters (one per markdown heading)
  2. Embed each chapter with e5-large (passage: prefix)
  3. Build the k-NN graph at several k values
  4. Compare the recovered graph to the designed adjacency
  5. Report edge recall, edge precision, F1, and Jaccard

Produces a compact summary JSON per text.
"""

import argparse
import json
import re
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent


def parse_chapters_md(text_path, heading_regex=r"^###\s+(.+?)$"):
    """
    Parse a markdown file into chapters. Each `## ...` heading is a
    chapter; the chapter body is the text until the next heading or
    end of file. Returns list of dicts with {id, title, body}.
    """
    content = Path(text_path).read_text(encoding="utf-8")
    lines = content.split("\n")
    chapters = []
    current = None
    for line in lines:
        m = re.match(heading_regex, line)
        if m:
            if current is not None:
                chapters.append(current)
            current = {"title": m.group(1).strip(), "body": []}
        elif current is not None:
            current["body"].append(line)
    if current is not None:
        chapters.append(current)
    for i, ch in enumerate(chapters):
        ch["id"] = i
        ch["body_text"] = "\n".join(ch["body"]).strip()
    return chapters


def extract_vertex_label(title, mapping):
    """Given chapter title, find which designed-graph vertex it maps to.

    mapping is a list of (substring, vertex_label) pairs; the first
    substring found in the title determines the mapping.
    """
    for sub, lbl in mapping:
        if sub in title:
            return lbl
    return None


def embed_chapters(chapter_texts, model_name="intfloat/multilingual-e5-large-instruct"):
    """
    Embed chapter texts with the instruct variant of multilingual-e5-large.
    Project default per feedback_always_e5_instruct.md.
    """
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    task = "Retrieve semantically similar passages from the same constrained literary text."
    queries = [f"Instruct: {task}\nQuery: {t}" for t in chapter_texts]
    return model.encode(queries, batch_size=8, normalize_embeddings=True,
                        show_progress_bar=False)


def build_knn_graph(embeddings, k):
    N = len(embeddings)
    sim = embeddings @ embeddings.T
    np.fill_diagonal(sim, -1.0)
    # For each node, pick top-k neighbours
    edges = set()
    for i in range(N):
        top = np.argsort(-sim[i])[:k]
        for j in top:
            e = tuple(sorted([int(i), int(j)]))
            edges.add(e)
    return edges


def compare_graphs(recovered_edges, designed_edges, N):
    designed = set(tuple(sorted(e)) for e in designed_edges)
    tp = len(recovered_edges & designed)
    fp = len(recovered_edges - designed)
    fn = len(designed - recovered_edges)
    total_pairs = N * (N - 1) // 2
    tn = total_pairs - tp - fp - fn
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = 2 * precision * recall / max(1e-9, precision + recall)
    jaccard = tp / max(1, tp + fp + fn)
    return {
        "N": N,
        "designed_edges": len(designed),
        "recovered_edges": len(recovered_edges),
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "recall": round(recall, 3),
        "precision": round(precision, 3),
        "f1": round(f1, 3),
        "jaccard": round(jaccard, 3),
    }


def run_experiment(text_file, designed_nodes, designed_edges,
                   vertex_mapping, k_values=(3, 8, 16, 24),
                   model="intfloat/multilingual-e5-large-instruct"):
    """
    vertex_mapping: list of (chapter-title-substring, designed-vertex-label).
    Chapters are matched to designed vertices by substring search.
    """
    chapters = parse_chapters_md(text_file)
    # Keep chapters whose title maps to a designed vertex
    mapped = []
    for ch in chapters:
        lbl = extract_vertex_label(ch["title"], vertex_mapping)
        if lbl is not None:
            mapped.append({"chapter_id": ch["id"], "title": ch["title"],
                           "designed_label": lbl, "body": ch["body_text"]})

    # Order by designed_label to match designed_nodes order
    label_to_chapter = {c["designed_label"]: c for c in mapped}
    ordered_chapters = []
    for label in designed_nodes:
        if label not in label_to_chapter:
            raise RuntimeError(f"No chapter found for designed vertex {label}")
        ordered_chapters.append(label_to_chapter[label])

    print(f"  parsed {len(chapters)} chapters, matched {len(ordered_chapters)} "
          f"to designed graph ({len(designed_nodes)} vertices)")
    for c in ordered_chapters[:3]:
        print(f"    '{c['title'][:60]}' → {c['designed_label']} "
              f"({len(c['body'])} chars)")

    # Embed chapter bodies
    texts = [c["body"] for c in ordered_chapters]
    print(f"  embedding {len(texts)} chapters with {model} ...")
    embeddings = embed_chapters(texts, model_name=model)
    print(f"  embeddings shape: {embeddings.shape}")

    # Convert designed edges to integer-indexed pairs
    label_to_idx = {label: i for i, label in enumerate(designed_nodes)}
    designed_int = [(label_to_idx[a], label_to_idx[b]) for a, b in designed_edges]

    results = {}
    for k in k_values:
        recovered = build_knn_graph(embeddings, k=k)
        metrics = compare_graphs(recovered, designed_int, N=len(designed_nodes))
        results[f"k={k}"] = metrics
        print(f"  k={k}: recall={metrics['recall']} "
              f"precision={metrics['precision']} "
              f"f1={metrics['f1']} "
              f"jaccard={metrics['jaccard']}")

    return {
        "text_file": str(text_file),
        "N": len(designed_nodes),
        "designed_edges": len(designed_edges),
        "model": model,
        "k_values": list(k_values),
        "results": results,
        "chapter_titles": [c["title"] for c in ordered_chapters],
        "chapter_labels": [c["designed_label"] for c in ordered_chapters],
    }


def main():
    OUT = BASE / "oulipo" / "pipeline_inverse_results.json"

    results = {}

    # ── Il quadrato dei re (2D 4×4 king, N=16) ──
    print("\n=== Il quadrato dei re (4×4 king) ===")
    king_data = json.loads((BASE / "quantum/arxiv_paper").parent.parent.joinpath(
        "oulipo/graphs/showcase_2d_2L_3d.json").read_text())["2D_4x4x1_king"]
    # designed nodes in the graph are labels like "v000", "v010", ..., "v330"
    # The text uses chapter headings like "### (0,0) — ..."
    designed_nodes_king = king_data["nodes"]  # v000, v010, v020, ...
    designed_edges_king = king_data["edges"]
    # Chapter titles use "(i,j)" so map substring "(i,j)" → v{i}{j}{0}
    king_mapping = []
    for node in designed_nodes_king:
        # node format "vijk" — i=row, j=col, k=layer(always 0)
        i, j = node[1], node[2]
        king_mapping.append((f"({i},{j})", node))
    results["il_quadrato_dei_re"] = run_experiment(
        text_file=BASE / "oulipo/texts/il_quadrato_dei_re.md",
        designed_nodes=designed_nodes_king,
        designed_edges=designed_edges_king,
        vertex_mapping=king_mapping,
    )

    # ── Le otto dimore (2L Q_3, N=8) ──
    print("\n=== Le otto dimore (Q_3 bi-layer) ===")
    q3_data = json.loads((BASE / "oulipo/graphs/graph_q3_bilayer_showcase.json").read_text())
    designed_nodes_q3 = q3_data["graph"]["nodes"]  # "000", "001", ..., "111"
    designed_edges_q3 = q3_data["graph"]["edges"]
    q3_mapping = [(f"`{n}`", n) for n in designed_nodes_q3]
    results["le_otto_dimore"] = run_experiment(
        text_file=BASE / "oulipo/texts/le_otto_dimore.md",
        designed_nodes=designed_nodes_q3,
        designed_edges=designed_edges_q3,
        vertex_mapping=q3_mapping,
    )

    OUT.write_text(json.dumps(results, indent=2))
    print(f"\n✓ saved {OUT}")


if __name__ == "__main__":
    main()
