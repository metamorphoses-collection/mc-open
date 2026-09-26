#!/usr/bin/env python3
"""
Repair Procès de Nithard: retry recovery with fine-tuned e5-large-oulipo.

Also try overlap threshold ≥ 3 instead of ≥ 4, in case the designed
graph is too sparse at the standard threshold for the bipartite trick
to be captured.
"""

import json
import re
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_inverse_v2 import parse_pages_std, metrics, build_knn, build_designed_adjacency

BASE = Path(__file__).resolve().parent
TEXT = BASE / "texts" / "proces_de_nithard.md"
FINETUNED_DIR = BASE / "models" / "e5-large-oulipo" / "e5-large-oulipo"

MODELS = [
    ("e5-large-instruct", "intfloat/multilingual-e5-large-instruct"),
    ("e5-large-plain", "intfloat/multilingual-e5-large"),
    ("e5-large-oulipo-finetuned", str(FINETUNED_DIR)),
]

THRESHOLDS = [3, 4]


def embed(texts, model_name):
    from sentence_transformers import SentenceTransformer
    print(f"    loading {model_name}...")
    m = SentenceTransformer(model_name)
    if "instruct" in model_name.lower():
        task = "Retrieve semantically similar passages from the same constrained literary text."
        queries = [f"Instruct: {task}\nQuery: {t}" for t in texts]
    else:
        queries = [f"passage: {t}" for t in texts]
    return m.encode(queries, batch_size=8, normalize_embeddings=True,
                    show_progress_bar=False)


def main():
    if not TEXT.exists():
        print(f"missing {TEXT}")
        return
    if not FINETUNED_DIR.exists():
        print(f"no fine-tuned model at {FINETUNED_DIR}")
        MODELS.pop()

    pages = parse_pages_std(TEXT)
    N = len(pages)
    print(f"Proces de Nithard: {N} pages")

    results = {"N": N, "runs": {}}
    for threshold in THRESHOLDS:
        designed = build_designed_adjacency(pages, threshold)
        density = len(designed) / (N * (N - 1) // 2) if N > 1 else 0
        avg_deg = 2 * len(designed) / N if N > 0 else 0
        k_star = max(2, round(avg_deg))
        print(f"\n--- overlap threshold ≥ {threshold}: "
              f"{len(designed)} edges, density={density:.3f}, avg_deg={avg_deg:.1f}, "
              f"k*={k_star} ---")

        texts = [p["text"] for p in pages]
        for label, model_name in MODELS:
            try:
                embs = embed(texts, model_name)
            except Exception as e:
                print(f"  {label}: LOAD FAILED  {str(e)[:150]}")
                continue
            run_results = {}
            for k in sorted(set([4, 8, k_star])):
                recovered = build_knn(embs, k=k)
                m = metrics(recovered, designed, N)
                run_results[f"k={k}"] = m
            best_f1 = max(r["f1"] for r in run_results.values())
            print(f"  {label}:")
            for ktag, m in run_results.items():
                print(f"    {ktag}: recall={m['recall']:.3f} "
                      f"prec={m['precision']:.3f} f1={m['f1']:.3f}")
            print(f"    best F1 = {best_f1:.3f}")
            results["runs"][f"threshold={threshold}/{label}"] = {
                "threshold": threshold,
                "designed_edges": len(designed),
                "density": round(density, 4),
                "k_star": k_star,
                "model": model_name,
                "k_results": run_results,
                "best_f1": best_f1,
            }

    out = BASE / "proces_repair_results.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\n✓ saved {out}")

    print("\n========== SUMMARY ==========")
    print(f"{'run':<50} {'best_F1':>9}")
    for name, r in results["runs"].items():
        print(f"{name:<50} {r['best_f1']:>9.3f}")


if __name__ == "__main__":
    main()
