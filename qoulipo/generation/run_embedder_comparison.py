#!/usr/bin/env python3
"""Compare sentence embedders on French OuLiPo 100 text.

For each embedder, compute mean cosine similarity for page-pairs
sharing >=3 threads vs <=1 thread. The winning embedder maximises
the gap and pushes the connected-pair mean above 0.78.
"""

import json, re, time, warnings
import numpy as np
from itertools import combinations
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore")

BASE = "generation"

# ---------- load text ----------
with open(f"{BASE}/texts/oulipo_100_hardzone.md", encoding="utf-8") as f:
    raw = f.read()

# Split on "## Page N" headers
pages_raw = re.split(r'\n## Page \d+\n', raw)[1:]  # drop preamble
N_PAGES = 20
pages_text = []
for p in pages_raw[:N_PAGES]:
    # Strip the "Threads: ..." line
    lines = p.strip().split('\n')
    body = '\n'.join(l for l in lines if not l.startswith('Threads:'))
    pages_text.append(body.strip())

print(f"Loaded {len(pages_text)} pages, avg {np.mean([len(t) for t in pages_text]):.0f} chars")

# ---------- load thread assignments ----------
with open(f"{BASE}/threads/oulipo_100_hardzone_threads.json", encoding="utf-8") as f:
    tdata = json.load(f)

page_threads = {}
for pid_str, info in tdata["assignments"].items():
    pid = int(pid_str)
    if pid < N_PAGES:
        page_threads[pid] = set(info["threads"])

# ---------- precompute shared-thread counts ----------
pair_shared = {}
for i, j in combinations(range(N_PAGES), 2):
    shared = len(page_threads[i] & page_threads[j])
    pair_shared[(i, j)] = shared

connected = [(i, j) for (i, j), s in pair_shared.items() if s >= 3]
disconnected = [(i, j) for (i, j), s in pair_shared.items() if s <= 1]
print(f"Pairs: {len(connected)} connected (>=3 threads), {len(disconnected)} disconnected (<=1 thread)")

# ---------- embedders ----------
EMBEDDERS = [
    ("paraphrase-multilingual-MiniLM-L12-v2", None),
    ("paraphrase-multilingual-mpnet-base-v2", None),
    ("distiluse-base-multilingual-cased-v2", None),
    ("sentence-transformers/LaBSE", None),
    ("intfloat/multilingual-e5-large", "query: "),  # E5 needs prefix
]

results = {}

for model_name, prefix in EMBEDDERS:
    print(f"\n{'='*60}")
    print(f"Model: {model_name}")
    t0 = time.time()

    model = SentenceTransformer(model_name)

    # Prepare texts (E5 needs "query: " prefix)
    if prefix:
        texts = [prefix + t for t in pages_text]
    else:
        texts = pages_text

    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    dt = time.time() - t0

    # Cosine similarity matrix (embeddings already L2-normalised)
    sim_matrix = embeddings @ embeddings.T

    # Gather sims
    conn_sims = [float(sim_matrix[i, j]) for i, j in connected]
    disc_sims = [float(sim_matrix[i, j]) for i, j in disconnected]

    conn_mean = np.mean(conn_sims)
    disc_mean = np.mean(disc_sims)
    gap = conn_mean - disc_mean

    # Also compute overall stats
    all_sims = [float(sim_matrix[i, j]) for i, j in combinations(range(N_PAGES), 2)]

    rec = {
        "model": model_name,
        "embed_time_s": round(dt, 1),
        "dim": int(embeddings.shape[1]),
        "sim_all_mean": round(np.mean(all_sims), 4),
        "sim_all_std": round(np.std(all_sims), 4),
        "sim_connected_mean": round(conn_mean, 4),
        "sim_connected_std": round(np.std(conn_sims), 4),
        "sim_disconnected_mean": round(disc_mean, 4),
        "sim_disconnected_std": round(np.std(disc_sims), 4),
        "gap": round(gap, 4),
        "n_connected_pairs": len(connected),
        "n_disconnected_pairs": len(disconnected),
        "connected_above_078": sum(1 for s in conn_sims if s > 0.78),
        "connected_above_078_pct": round(100 * sum(1 for s in conn_sims if s > 0.78) / len(conn_sims), 1),
    }
    results[model_name] = rec

    print(f"  dim={rec['dim']}  time={rec['embed_time_s']}s")
    print(f"  connected (>=3 threads): mean={rec['sim_connected_mean']:.4f}  std={rec['sim_connected_std']:.4f}")
    print(f"  disconnected (<=1 thread): mean={rec['sim_disconnected_mean']:.4f}  std={rec['sim_disconnected_std']:.4f}")
    print(f"  GAP = {rec['gap']:.4f}")
    print(f"  connected pairs > 0.78: {rec['connected_above_078']}/{len(connected)} ({rec['connected_above_078_pct']}%)")

# ---------- summary ----------
print("\n" + "="*60)
print("SUMMARY (sorted by gap)")
print(f"{'Model':<50} {'Conn':>6} {'Disc':>6} {'Gap':>6} {'>0.78':>6}")
for name in sorted(results, key=lambda n: results[n]["gap"], reverse=True):
    r = results[name]
    print(f"{name:<50} {r['sim_connected_mean']:>6.4f} {r['sim_disconnected_mean']:>6.4f} {r['gap']:>6.4f} {r['connected_above_078_pct']:>5.1f}%")

# ---------- save ----------
out_path = f"{BASE}/embedder_comparison.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({
        "description": "Embedder comparison on French OuLiPo 100 text (first 20 pages)",
        "n_pages": N_PAGES,
        "threshold": 0.78,
        "n_connected_pairs": len(connected),
        "n_disconnected_pairs": len(disconnected),
        "results": results,
    }, f, indent=2, ensure_ascii=False)
print(f"\nSaved to {out_path}")
