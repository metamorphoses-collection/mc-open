#!/usr/bin/env python3
"""
Validate an OuLiPo constrained text: embed, build graph, compute MIS, check constraints.

Usage:
    python validate_text.py <text_file> [--k 8] [--threshold 0.78]
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np
import networkx as nx
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "intfloat/multilingual-e5-large"


def parse_pages(text_path):
    """Parse markdown OuLiPo text into pages."""
    text = Path(text_path).read_text(encoding="utf-8")
    pages = []
    # Split on #### PAGE N
    parts = re.split(r"####\s+PAGE\s+(\d+)", text)
    for i in range(1, len(parts), 2):
        page_num = int(parts[i])
        body = parts[i + 1]
        # Extract threads
        thread_match = re.search(r"\*Threads?:\s*(.+?)\*", body)
        threads = []
        if thread_match:
            threads = [t.strip() for t in thread_match.group(1).split(",")]
        # Extract role
        role_match = re.search(r"\*Role:\s*(.+?)\*", body)
        role = role_match.group(1).strip() if role_match else "unknown"
        # Extract text (everything after the metadata lines)
        lines = body.strip().split("\n")
        text_lines = []
        past_meta = False
        for line in lines:
            if past_meta:
                text_lines.append(line)
            elif line.strip() == "" and not past_meta:
                continue
            elif not line.startswith("*"):
                past_meta = True
                text_lines.append(line)
        page_text = "\n".join(text_lines).strip()
        # Remove trailing ---
        page_text = re.sub(r"\n---\s*$", "", page_text).strip()

        pages.append({
            "page": page_num,
            "threads": threads,
            "role": role,
            "text": page_text,
            "word_count": len(page_text.split()),
        })
    return pages


def mis_ilp(G):
    from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD
    prob = LpProblem("MIS", LpMaximize)
    x = {n: LpVariable(f"x_{n}", cat="Binary") for n in G.nodes()}
    prob += lpSum(x.values())
    for u, v in G.edges():
        prob += x[u] + x[v] <= 1
    prob.solve(PULP_CBC_CMD(msg=0))
    return sorted([n for n, v in x.items() if v.varValue > 0.5])


def enumerate_mis(G, max_solutions=200):
    from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD
    solutions = []
    for i in range(max_solutions + 50):
        prob = LpProblem(f"MIS_{i}", LpMaximize)
        x = {n: LpVariable(f"x_{n}", cat="Binary") for n in G.nodes()}
        prob += lpSum(x.values())
        for u, v in G.edges():
            prob += x[u] + x[v] <= 1
        for prev in solutions:
            prob += lpSum(x[n] for n in prev) <= len(prev) - 1
        prob.solve(PULP_CBC_CMD(msg=0))
        sol = sorted([n for n, v in x.items() if v.varValue > 0.5])
        if not sol or (solutions and len(sol) < len(solutions[0])):
            break
        solutions.append(sol)
        if len(solutions) >= max_solutions:
            break
    return solutions


def main():
    text_path = sys.argv[1] if len(sys.argv) > 1 else "texts/livre_irremplacable.md"
    k_values = [8, 12, 16]
    threshold = 0.78

    print("=" * 70)
    print(f"  VALIDATING: {Path(text_path).name}")
    print("=" * 70)

    # Parse
    pages = parse_pages(text_path)
    N = len(pages)
    print(f"\n  Parsed {N} pages")
    print(f"  Word counts: min={min(p['word_count'] for p in pages)}, "
          f"max={max(p['word_count'] for p in pages)}, "
          f"mean={np.mean([p['word_count'] for p in pages]):.0f}")

    # Thread stats
    all_threads = set()
    for p in pages:
        all_threads.update(p["threads"])
    print(f"  Threads: {len(all_threads)} unique: {sorted(all_threads)}")
    threads_per_page = [len(p["threads"]) for p in pages]
    print(f"  Threads/page: min={min(threads_per_page)}, max={max(threads_per_page)}, "
          f"mean={np.mean(threads_per_page):.1f}")

    # Thread balance
    thread_counts = defaultdict(int)
    for p in pages:
        for t in p["threads"]:
            thread_counts[t] += 1
    print(f"  Thread balance: {dict(sorted(thread_counts.items(), key=lambda x: x[1]))}")

    # MIS/backbone pages
    mis_pages = [p["page"] for p in pages if "MIS" in p["role"] or "backbone" in p["role"].lower()]
    buttress_pages = [p["page"] for p in pages if p["page"] not in mis_pages]
    print(f"  Designed MIS: {len(mis_pages)} pages, Buttress: {len(buttress_pages)} pages")

    # Embed
    print("\n  Embedding with E5-large...")
    model = SentenceTransformer(MODEL_NAME)
    texts = ["passage: " + p["text"] for p in pages]
    embeddings = model.encode(texts, batch_size=32, normalize_embeddings=True,
                              show_progress_bar=False)
    print(f"  Embeddings: {embeddings.shape}")

    # Pairwise similarity
    sim_matrix = cosine_similarity(embeddings)
    np.fill_diagonal(sim_matrix, 0)

    # Similarity stats
    upper = sim_matrix[np.triu_indices(N, k=1)]
    print(f"\n  Similarity stats:")
    print(f"    Mean: {np.mean(upper):.4f}")
    print(f"    Std:  {np.std(upper):.4f}")
    print(f"    Min:  {np.min(upper):.4f}")
    print(f"    Max:  {np.max(upper):.4f}")
    print(f"    % > 0.78: {100 * np.mean(upper > 0.78):.1f}%")
    print(f"    % > 0.85: {100 * np.mean(upper > 0.85):.1f}%")

    # Check designed edge/non-edge separation
    print("\n  Thread overlap vs similarity:")
    node_ids = [f"p{p['page']}" for p in pages]
    page_threads = {p["page"]: set(p["threads"]) for p in pages}

    overlaps_sims = []
    for i in range(N):
        for j in range(i + 1, N):
            pi, pj = pages[i]["page"], pages[j]["page"]
            overlap = len(page_threads[pi] & page_threads[pj])
            sim = sim_matrix[i][j]
            overlaps_sims.append((overlap, sim))

    # Group by overlap
    by_overlap = defaultdict(list)
    for overlap, sim in overlaps_sims:
        by_overlap[overlap].append(sim)

    for ov in sorted(by_overlap.keys()):
        sims = by_overlap[ov]
        print(f"    Overlap {ov}: n={len(sims):4d}, sim={np.mean(sims):.4f} ± {np.std(sims):.4f}, "
              f">{threshold}: {100*np.mean(np.array(sims) > threshold):.1f}%")

    # Build graphs at different k
    results = {}
    for k in k_values:
        print(f"\n  --- Graph at k={k}, threshold={threshold} ---")
        G = nx.Graph()
        G.add_nodes_from(node_ids)
        for i in range(N):
            sims = sim_matrix[i].copy()
            sims[i] = -1
            top_indices = np.argsort(sims)[-k:]
            for j in top_indices:
                if sims[j] >= threshold:
                    G.add_edge(node_ids[i], node_ids[j], weight=float(sims[j]))

        density = nx.density(G)
        n_edges = G.number_of_edges()
        print(f"    Nodes: {G.number_of_nodes()}, Edges: {n_edges}, Density: {density:.4f}")

        # Solve MIS
        mis = mis_ilp(G)
        print(f"    MIS size: {len(mis)} (ratio: {len(mis)/N:.3f})")
        print(f"    MIS pages: {mis}")

        # Check if designed MIS matches
        designed_mis_ids = set(f"p{p}" for p in mis_pages)
        actual_mis_ids = set(mis)
        overlap_with_designed = len(designed_mis_ids & actual_mis_ids)
        print(f"    Overlap with designed MIS: {overlap_with_designed}/{len(designed_mis_ids)}")

        # Enumerate solutions
        print(f"    Enumerating MIS solutions...")
        solutions = enumerate_mis(G, max_solutions=100)
        print(f"    Found {len(solutions)} optimal MIS solutions")

        # Rigidity
        all_mis_nodes = set()
        node_counts = defaultdict(int)
        for sol in solutions:
            all_mis_nodes.update(sol)
            for n in sol:
                node_counts[n] += 1
        essential = [n for n in all_mis_nodes if node_counts[n] == len(solutions)]
        rigidity = len(essential) / len(solutions[0]) if solutions else 0
        print(f"    Essential nodes: {len(essential)}")
        print(f"    Rigidity rho: {rigidity:.3f}")

        # Double domination check (for rho=1.0 texts)
        if len(solutions) == 1:
            print(f"    *** UNIQUE MIS — rho = 1.000 ***")
            mis_set = set(solutions[0])
            non_mis = [n for n in node_ids if n not in mis_set]
            min_mis_neighbors = float("inf")
            for n in non_mis:
                mis_neighbors = len(set(G.neighbors(n)) & mis_set)
                min_mis_neighbors = min(min_mis_neighbors, mis_neighbors)
            print(f"    Min MIS neighbors of non-MIS node: {min_mis_neighbors}")
            if min_mis_neighbors >= 2:
                print(f"    *** DOUBLE DOMINATION VERIFIED ***")

        results[f"k={k}"] = {
            "edges": n_edges,
            "density": round(density, 4),
            "mis_size": len(mis),
            "mis_ratio": round(len(mis) / N, 3),
            "n_solutions": len(solutions),
            "rigidity": round(rigidity, 3),
            "essential": len(essential),
        }

    # Save results
    out_path = Path(text_path).with_suffix(".validation.json")
    with open(out_path, "w") as f:
        json.dump({
            "text": Path(text_path).name,
            "N": N,
            "word_stats": {
                "min": min(p["word_count"] for p in pages),
                "max": max(p["word_count"] for p in pages),
                "mean": round(np.mean([p["word_count"] for p in pages]), 1),
                "total": sum(p["word_count"] for p in pages),
            },
            "sim_stats": {
                "mean": round(float(np.mean(upper)), 4),
                "std": round(float(np.std(upper)), 4),
                "pct_above_078": round(float(100 * np.mean(upper > 0.78)), 1),
            },
            "results": results,
        }, f, indent=2)
    print(f"\n  Saved to {out_path}")


if __name__ == "__main__":
    main()
