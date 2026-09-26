#!/usr/bin/env python3
"""
Pipeline-inverse on ALL thread-annotated QOuLiPo texts.

For each text:
  1. Parse pages via `#### PAGE n` heading + `*Threads: ...*` annotation
  2. Build designed adjacency: pages share ≥ 4 threads (the same
     threshold used by the contrastive fine-tune in finetune_embedder.py)
  3. Embed page bodies with intfloat/multilingual-e5-large-instruct
  4. Build k-NN graph at k = 8, 16, 24
  5. Report recall/precision/F1/Jaccard vs designed adjacency

The goal is to measure, across the entire engineered corpus, how well
the pipeline's NLP embedding step recovers the hidden designed graph.
"""

import json
import re
from itertools import combinations
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
TEXTS = BASE / "texts"
OUT = BASE / "pipeline_inverse_all_results.json"

MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
INSTRUCTION = "Retrieve semantically similar passages from the same constrained literary text."
THREAD_OVERLAP_THRESHOLD = 4  # matches finetune_embedder.py positive-pair rule


THREAD_TEXTS = [
    # 50-page books (proven)
    "kaleidoscope.md",
    "livre_irremplacable.md",
    "livre_irremplacable_v2.md",
    "piege_du_lecteur.md",
    "livre_fractal.md",
    "proces_de_nithard.md",
    "partition_du_texte.md",
    "oulipo_nithard_pascal_v1_original.md",
    "incarnate_graph_50_en.md",
    "incarnate_graph_50p_en.md",
    "oulipo_udg_50pages.md",
    "oulipo_udg_50pages_en.md",
    # 65-page hard-zone books
    "nithards_wager_65p_en.md",
    "oulipo_65_hardzone.md",
    "oulipo_65_hardzone_en.md",
    "oulipo_65_hardzone_en_v2.md",
    "oulipo_nithard_pascal.md",
    "oulipo_udg65_text.md",
    # 100-page books
    "nithards_wager_100p_en.md",
    "oulipo_100_hardzone.md",
    "oulipo_v2_100pages.md",
    "oulipo_v2_100pages_revised.md",
    # smaller
    "jumeaux_en.md",
]


def _split_pages(text):
    """Return a list of (page_num, body_text) pairs.

    Supports BOTH page-delimiter styles:
      - `#### PAGE 1 — title` (used by livre_irremplacable, kaleidoscope, ...)
      - `## Page 1` or `## PAGE 1` (used by nithards_wager_65p, oulipo_100_hardzone, ...)
    Whichever produces more pages wins.
    """
    # Style A: #### PAGE n
    parts_a = re.split(r"(?m)^####\s+PAGE\s+(\d+)", text)
    pages_a = []
    for i in range(1, len(parts_a), 2):
        pages_a.append((int(parts_a[i]), parts_a[i + 1]))

    # Style B: ## Page n  (case-insensitive on "page")
    parts_b = re.split(r"(?im)^##\s+PAGE\s+(\d+)", text)
    pages_b = []
    for i in range(1, len(parts_b), 2):
        pages_b.append((int(parts_b[i]), parts_b[i + 1]))

    return pages_a if len(pages_a) >= len(pages_b) else pages_b


def parse_pages(text_path):
    text = Path(text_path).read_text(encoding="utf-8")
    pages = []
    for page_num, body in _split_pages(text):
        # Stop the body at the next page separator if present
        body = re.split(r"(?m)^(?:####\s+PAGE|\s*---\s*$)", body)[0]
        # Accept both `*Threads: A, B*` and plain `Threads: A, B`
        thread_match = re.search(r"(?im)^\s*\*?\s*Threads?:\s*(.+?)\s*\*?\s*$", body)
        threads = []
        if thread_match:
            threads = [t.strip() for t in thread_match.group(1).split(",")]
            threads = [t for t in threads if t]  # drop empties
        lines = body.strip().split("\n")
        # Keep prose; drop any line that is itself a thread annotation,
        # heading, or metadata marker.
        text_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r"^\*?\s*Threads?:", stripped, re.I):
                continue
            if stripped.startswith("#"):
                continue
            if stripped.startswith("*") and stripped.endswith("*") and len(stripped) < 80:
                continue  # metadata lines like *Voice: Professor*
            text_lines.append(stripped)
        page_text = "\n".join(text_lines).strip()
        if page_text and threads:
            pages.append({
                "page": page_num,
                "threads": set(threads),
                "text": page_text,
            })
    return pages


def build_designed_adjacency(pages, overlap_threshold):
    N = len(pages)
    edges = set()
    for i, j in combinations(range(N), 2):
        shared = len(pages[i]["threads"] & pages[j]["threads"])
        if shared >= overlap_threshold:
            edges.add((i, j))
    return edges


def embed_pages(chapter_texts, model_name=MODEL_NAME):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    queries = [f"Instruct: {INSTRUCTION}\nQuery: {t}" for t in chapter_texts]
    return model.encode(queries, batch_size=8, normalize_embeddings=True,
                        show_progress_bar=False)


def build_knn(embeddings, k):
    N = len(embeddings)
    sim = embeddings @ embeddings.T
    np.fill_diagonal(sim, -1.0)
    edges = set()
    for i in range(N):
        top = np.argsort(-sim[i])[:k]
        for j in top:
            e = (min(int(i), int(j)), max(int(i), int(j)))
            edges.add(e)
    return edges


def metrics(recovered, designed, N):
    tp = len(recovered & designed)
    fp = len(recovered - designed)
    fn = len(designed - recovered)
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = 2 * precision * recall / max(1e-9, precision + recall)
    jaccard = tp / max(1, tp + fp + fn)
    density = len(designed) / max(1, N * (N - 1) // 2)
    return {
        "N": N,
        "designed_edges": len(designed),
        "recovered_edges": len(recovered),
        "density": round(density, 4),
        "tp": tp, "fp": fp, "fn": fn,
        "recall": round(recall, 3),
        "precision": round(precision, 3),
        "f1": round(f1, 3),
        "jaccard": round(jaccard, 3),
    }


LANGUAGE_HINTS = {
    "kaleidoscope.md": "EN",
    "livre_irremplacable.md": "FR",
    "livre_irremplacable_v2.md": "FR",
    "piege_du_lecteur.md": "FR",
    "livre_fractal.md": "EN",
    "proces_de_nithard.md": "FR",
    "partition_du_texte.md": "FR",
    "oulipo_nithard_pascal.md": "EN",
    "oulipo_nithard_pascal_v1_original.md": "EN",
    "oulipo_65_hardzone.md": "FR",
    "oulipo_65_hardzone_en.md": "EN",
    "oulipo_65_hardzone_en_v2.md": "EN",
    "nithards_wager_65p_en.md": "EN",
    "nithards_wager_100p_en.md": "EN",
    "oulipo_100_hardzone.md": "FR",
    "oulipo_v2_100pages.md": "EN",
    "oulipo_v2_100pages_revised.md": "EN",
    "oulipo_udg_50pages.md": "FR",
    "oulipo_udg_50pages_en.md": "EN",
    "oulipo_udg65_text.md": "EN",
    "incarnate_graph_50_en.md": "EN",
    "incarnate_graph_50p_en.md": "EN",
    "jumeaux_en.md": "EN",
    "jumeaux_fr.md": "FR",
    "il_quadrato_dei_re.md": "IT",
    "le_otto_dimore.md": "IT",
    "sonetti_dal_tesseratto.md": "IT",
    "la_vita_nel_cubo.md": "IT",
}


def run_one(text_name, k_values=(8, 16, 24)):
    path = TEXTS / text_name
    if not path.exists():
        print(f"  SKIP {text_name}: not found")
        return None
    pages = parse_pages(path)
    if len(pages) < 4:
        print(f"  SKIP {text_name}: only {len(pages)} pages with threads")
        return None
    N = len(pages)
    designed = build_designed_adjacency(pages, THREAD_OVERLAP_THRESHOLD)
    if not designed:
        print(f"  SKIP {text_name}: no designed edges at overlap≥{THREAD_OVERLAP_THRESHOLD}")
        return None

    avg_degree = 2 * len(designed) / N
    k_adaptive = max(2, round(avg_degree))

    lang = LANGUAGE_HINTS.get(text_name, "??")
    slug = text_name.replace(".md", "")
    display_title = f"{slug} ({lang}) N={N} k={k_adaptive}"
    print(f"\n=== {display_title}  [d={len(designed)/(N*(N-1)/2):.3f}, "
          f"edges={len(designed)}, avg_deg={avg_degree:.1f}] ===")
    texts = [p["text"] for p in pages]
    embeddings = embed_pages(texts)

    results = {}
    # Always include the adaptive-k point (matched to avg designed degree)
    k_values_aug = tuple(sorted(set(list(k_values) + [k_adaptive])))
    for k in k_values_aug:
        recovered = build_knn(embeddings, k=k)
        m = metrics(recovered, designed, N)
        tag = "*" if k == k_adaptive else " "
        results[f"k={k}"] = m
        print(f"  k={k:2d}{tag}: recall={m['recall']:.3f} precision={m['precision']:.3f} "
              f"f1={m['f1']:.3f} jaccard={m['jaccard']:.3f}")

    return {
        "text": text_name,
        "display_title": display_title,
        "lang": lang,
        "N": N,
        "n_pages_with_threads": N,
        "overlap_threshold": THREAD_OVERLAP_THRESHOLD,
        "designed_edges": len(designed),
        "avg_degree": round(avg_degree, 2),
        "k_adaptive": k_adaptive,
        "density": round(len(designed) / (N * (N - 1) // 2), 4),
        "model": MODEL_NAME,
        "k_values": list(k_values_aug),
        "results": results,
        "thread_universe": sorted(set().union(*(p["threads"] for p in pages))),
        "avg_threads_per_page": round(np.mean([len(p["threads"]) for p in pages]), 2),
    }


def main():
    print(f"Pipeline-inverse on all thread-annotated QOuLiPo texts")
    print(f"Model: {MODEL_NAME}")
    print(f"Thread-overlap threshold for designed edges: ≥ {THREAD_OVERLAP_THRESHOLD}")

    all_results = {}
    for text in THREAD_TEXTS:
        try:
            r = run_one(text)
            if r is not None:
                all_results[text] = r
        except Exception as e:
            print(f"  ERROR {text}: {e}")

    # Summary table
    print("\n\n========== SUMMARY ==========")
    print(f"{'text (lang) N k*':<48} {'d':>6} {'F1@8':>7} {'F1@16':>7} {'F1@24':>7} "
          f"{'F1@k*':>7} {'best':>7}")
    rows = []
    for name, r in all_results.items():
        rr = r["results"]
        f1_8 = rr.get("k=8", {}).get("f1", 0)
        f1_16 = rr.get("k=16", {}).get("f1", 0)
        f1_24 = rr.get("k=24", {}).get("f1", 0)
        f1_adaptive = rr.get(f"k={r['k_adaptive']}", {}).get("f1", 0)
        best = max(f1_8, f1_16, f1_24, f1_adaptive)
        rows.append((r["display_title"], r["N"], r["density"], f1_8, f1_16, f1_24, f1_adaptive, best))
        print(f"{r['display_title']:<48} {r['density']:>6.3f} "
              f"{f1_8:>7.3f} {f1_16:>7.3f} {f1_24:>7.3f} {f1_adaptive:>7.3f} {best:>7.3f}")
    if rows:
        mean_best = np.mean([r[-1] for r in rows])
        print(f"\nMean best F1 across {len(rows)} texts: {mean_best:.3f}")

    OUT.write_text(json.dumps(all_results, indent=2))
    print(f"\n✓ saved {OUT}")


if __name__ == "__main__":
    main()
