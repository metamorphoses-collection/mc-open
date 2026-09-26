#!/usr/bin/env python3
"""
Build topic graphs for OuLiPo hard-zone texts and submit to Pasqal EMU_MPS.

Texts:
  - oulipo_65_hardzone.md  (65 pages, ~22K words)
  - oulipo_100_hardzone.md (80 pages so far)

Pipeline:
  1. Split by ## Page N headers
  2. Embed with paraphrase-multilingual-MiniLM-L12-v2
  3. Build k-NN graph at k=8 AND k=16 (threshold=0.78)
  4. Report: N, E, density, MIS, sim_mean, sim_median
  5. SA-embed at R_b=8.0um
  6. Submit to EMU_MPS (1000 shots each)
  7. Save graphs + batch IDs
"""

import json, re, time, os, sys
from pathlib import Path

import numpy as np
import networkx as nx
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ── Paths ──────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
TEXT_DIR = BASE / "texts"
GRAPH_DIR = BASE / "graphs"
GRAPH_DIR.mkdir(exist_ok=True)

# Add classical core to path for pasqal_emulator functions
CORE_DIR = BASE.parent / "classical" / "core"
sys.path.insert(0, str(CORE_DIR))
from pasqal_emulator import (
    embed_sa, embedding_quality, build_sequence, mis_ilp, mis_greedy,
    extract_mis_from_samples, BLOCKADE_UM, OMEGA_MAX, DELTA_0, DELTA_F,
    N_SAMPLES, PASQAL_PROJECT_ID
)

# ── Config ─────────────────────────────────────────────────────────────
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SIM_THRESHOLD = 0.78
K_VALUES = [8, 16]

TEXTS = [
    ("oulipo_65_hardzone", TEXT_DIR / "oulipo_65_hardzone.md"),
    ("oulipo_100_hardzone", TEXT_DIR / "oulipo_100_hardzone.md"),
]


def log(msg):
    print(msg, flush=True)


# ═══════════════════════════════════════════════════════════════════════
# 1. PARSE TEXTS
# ═══════════════════════════════════════════════════════════════════════

def parse_pages(filepath):
    """Split text by ## Page N headers, return list of (page_num, text)."""
    raw = filepath.read_text(encoding="utf-8")
    # Split on ## Page N
    parts = re.split(r"(?=^## Page \d+)", raw, flags=re.MULTILINE)
    pages = []
    for part in parts:
        m = re.match(r"^## Page (\d+)\s*\n", part)
        if not m:
            continue
        page_num = int(m.group(1))
        # Get text after the header line (skip "Threads:" line too)
        lines = part.split("\n")[1:]  # skip ## Page N line
        # Skip the Threads: line if present
        text_lines = []
        for line in lines:
            if line.strip().startswith("Threads:"):
                continue
            text_lines.append(line)
        text = "\n".join(text_lines).strip()
        if len(text) > 20:  # skip near-empty pages
            pages.append((page_num, text))
    return pages


# ═══════════════════════════════════════════════════════════════════════
# 2. EMBED
# ═══════════════════════════════════════════════════════════════════════

def embed_pages(pages, model):
    """Embed page texts, return embeddings matrix."""
    texts = [text for _, text in pages]
    log(f"  Embedding {len(texts)} pages...")
    embs = model.encode(texts, batch_size=32, show_progress_bar=True,
                        normalize_embeddings=True)
    return embs


# ═══════════════════════════════════════════════════════════════════════
# 3. BUILD GRAPH
# ═══════════════════════════════════════════════════════════════════════

def build_knn_graph(pages, embs, top_k=8, threshold=0.78):
    """Build k-NN similarity graph."""
    sim = cosine_similarity(embs)
    np.fill_diagonal(sim, 0)

    G = nx.Graph()
    for i, (pnum, text) in enumerate(pages):
        G.add_node(f"p{pnum}", page=pnum, text=text[:200])

    n = len(pages)
    for i in range(n):
        top_idx = np.argsort(-sim[i])[:top_k]
        for j in top_idx:
            if i >= j:
                continue
            if sim[i, j] >= threshold:
                G.add_edge(f"p{pages[i][0]}", f"p{pages[j][0]}",
                           weight=float(sim[i, j]))

    # Compute stats
    N = G.number_of_nodes()
    E = G.number_of_edges()
    density = 2 * E / (N * (N - 1)) if N > 1 else 0

    # Similarity stats (upper triangle)
    upper = sim[np.triu_indices(n, k=1)]
    above_thresh = int(np.sum(upper >= threshold))

    stats = {
        "N": N, "E": E, "density": round(density, 4),
        "sim_mean": round(float(np.mean(upper)), 4),
        "sim_median": round(float(np.median(upper)), 4),
        "sim_std": round(float(np.std(upper)), 4),
        "sim_min": round(float(np.min(upper)), 4),
        "sim_max": round(float(np.max(upper)), 4),
        "above_threshold": above_thresh,
        "top_k": top_k,
        "threshold": threshold,
    }

    return G, stats, sim


def compute_mis(G):
    """Compute MIS via ILP."""
    try:
        sel = mis_ilp(G)
        return len(sel), sel
    except Exception as e:
        log(f"  ILP failed ({e}), trying greedy...")
        sel = mis_greedy(G)
        return len(sel), sel


# ═══════════════════════════════════════════════════════════════════════
# 4. SA EMBEDDING + EMU SUBMISSION
# ═══════════════════════════════════════════════════════════════════════

def sa_embed_and_submit(G, text_label, k_label, stats, mis_size):
    """SA-embed graph and submit to EMU_MPS."""
    from pasqal_cloud import SDK

    N = G.number_of_nodes()
    E = G.number_of_edges()

    log(f"\n  SA-embedding {text_label} k={k_label} ({N} nodes, {E} edges)...")
    coords = embed_sa(G, blockade_um=BLOCKADE_UM)

    # Quality check
    qual = embedding_quality(G, coords, BLOCKADE_UM)
    fidelity = qual["fidelity"]
    false_edges = qual["false_edges"]
    false_gaps = qual["false_gaps"]
    log(f"  Embedding fidelity: {fidelity*100:.1f}% "
        f"(FE={false_edges}, FG={false_gaps})")

    # Build sequence
    log(f"  Building Pulser sequence...")
    seq, node_list = build_sequence(G, coords)
    serialized = seq.to_abstract_repr()

    # Submit to EMU_MPS
    log(f"  Submitting to EMU_MPS (1000 shots)...")
    sdk = SDK(
        username=os.environ['PASQAL_USER'],
        password="zomfeg-0hoDby-ruhzij",
        project_id=PASQAL_PROJECT_ID,
    )

    batch = sdk.create_batch(
        serialized_sequence=serialized,
        jobs=[{"runs": 1000}],
        device_type="EMU_MPS",
        wait=False,  # don't block — just get batch ID
    )
    batch_id = str(batch.id)
    log(f"  Batch submitted: {batch_id}")

    # Determine zone
    density = stats["density"]
    if density >= 0.25:
        zone = "HARD"
    elif density >= 0.10:
        zone = "medium"
    else:
        zone = "easy"

    result = {
        "batch_id": batch_id,
        "N": N,
        "E": E,
        "density": density,
        "mis_ilp": mis_size,
        "fidelity": round(fidelity, 4),
        "zone": zone,
        "shots": 1000,
        "desc": f"OuLiPo {text_label} k={k_label}",
        "omega_max": round(float(OMEGA_MAX), 4),
        "blockade_um": BLOCKADE_UM,
        "false_edges": false_edges,
        "false_gaps": false_gaps,
    }

    return result, coords


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    log("=" * 70)
    log("OuLiPo Hard-Zone Topic Graphs + EMU Submission")
    log("=" * 70)

    # Load model once
    log(f"\nLoading {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)

    all_batches = {}
    all_results = {}

    for text_name, text_path in TEXTS:
        log(f"\n{'─' * 60}")
        log(f"TEXT: {text_name}")
        log(f"{'─' * 60}")

        # Parse
        pages = parse_pages(text_path)
        log(f"  Parsed {len(pages)} pages")
        word_counts = [len(text.split()) for _, text in pages]
        log(f"  Mean words/page: {np.mean(word_counts):.0f}, "
            f"total: {sum(word_counts)}")

        # Embed
        embs = embed_pages(pages, model)

        for k in K_VALUES:
            log(f"\n  ── k={k} ──")
            G, stats, sim_matrix = build_knn_graph(pages, embs, top_k=k,
                                                    threshold=SIM_THRESHOLD)

            # MIS
            mis_size, mis_sel = compute_mis(G)
            stats["mis_ilp"] = mis_size

            log(f"  N={stats['N']}, E={stats['E']}, "
                f"density={stats['density']:.4f}, MIS={mis_size}")
            log(f"  sim_mean={stats['sim_mean']:.4f}, "
                f"sim_median={stats['sim_median']:.4f}, "
                f"sim_max={stats['sim_max']:.4f}")
            log(f"  Pairs above threshold: {stats['above_threshold']}")

            # Save graph JSON
            graph_data = {
                "nodes": [{"id": n, **G.nodes[n]} for n in G.nodes],
                "edges": [{"source": u, "target": v,
                           "weight": round(G[u][v]["weight"], 4)}
                          for u, v in G.edges],
            }
            graph_file = GRAPH_DIR / f"graph_{text_name}_k{k}.json"
            graph_file.write_text(json.dumps(graph_data, indent=2,
                                             ensure_ascii=False))
            log(f"  Saved: {graph_file.name}")

            # Save analysis JSON
            analysis = {
                "text": text_name,
                "n_pages": len(pages),
                "mean_word_count": round(float(np.mean(word_counts)), 1),
                "k": k,
                "threshold": SIM_THRESHOLD,
                **stats,
            }
            analysis_file = GRAPH_DIR / f"analysis_{text_name}_k{k}.json"
            analysis_file.write_text(json.dumps(analysis, indent=2))
            log(f"  Saved: {analysis_file.name}")

            # Store for summary
            key = f"{text_name}_k{k}"
            all_results[key] = analysis

            # SA-embed + EMU submission
            if G.number_of_edges() > 0:
                batch_result, coords = sa_embed_and_submit(
                    G, text_name, k, stats, mis_size)
                all_batches[key] = batch_result

                # Save coords
                coords_data = {n: list(c) for n, c in coords.items()}
                coords_file = GRAPH_DIR / f"coords_{text_name}_k{k}.json"
                coords_file.write_text(json.dumps(coords_data, indent=2))
            else:
                log(f"  ⚠ No edges at k={k} — skipping EMU submission")

    # Save all batch IDs
    batch_file = (BASE.parent / "quantum" / "batches" /
                  "emu_oulipo_hardzone_batches.json")
    batch_file.parent.mkdir(parents=True, exist_ok=True)
    batch_file.write_text(json.dumps(all_batches, indent=2))
    log(f"\n  Batch IDs saved: {batch_file}")

    # Summary
    log(f"\n{'=' * 70}")
    log("SUMMARY")
    log(f"{'=' * 70}")
    for key, r in all_results.items():
        density = r.get("density", 0)
        zone = "HARD" if density >= 0.25 else ("medium" if density >= 0.10 else "easy")
        target_met = "YES" if density >= 0.28 else "NO"
        log(f"  {key:40s} N={r['N']:3d} E={r['E']:4d} "
            f"d={density:.4f} MIS={r.get('mis_ilp','?'):3} "
            f"zone={zone:6s} target(d~0.30)={target_met}")

    if all_batches:
        log(f"\nEMU Batch IDs:")
        for key, b in all_batches.items():
            log(f"  {key}: {b['batch_id']}")

    log(f"\nDone.")


if __name__ == "__main__":
    main()
