#!/usr/bin/env python3
"""Diagnose v2 embedding: similarity distribution TP vs FP, per-threshold
graph, and mutual-kNN vs union-kNN comparison."""
import json
from itertools import combinations
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

HERE = Path(__file__).resolve().parent
FRIAR = HERE.parent
SOURCE = FRIAR / "source"
DESIGNED = FRIAR / "graph_designed.json"

MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
INSTRUCT_PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "


def load_pages():
    out = []
    for i in range(1, 21):
        raw = (SOURCE / f"page_{i:03d}.txt").read_text().strip()
        lines = raw.splitlines()
        if lines and lines[-1].startswith("[v2 motifs:"):
            lines = lines[:-1]
            while lines and not lines[-1].strip():
                lines.pop()
        out.append("\n".join(lines))
    return out


def mis_brute(N, edges):
    adj = [[False]*N for _ in range(N)]
    for a,b in edges:
        adj[a][b]=adj[b][a]=True
    best=0; all_max=[]
    for mask in range(1<<N):
        if bin(mask).count("1")<best: continue
        bits=[i for i in range(N) if mask>>i&1]
        ok=all(not adj[i][j] for i,j in combinations(bits,2))
        if not ok: continue
        s=len(bits)
        if s>best: best=s; all_max=[tuple(bits)]
        elif s==best: all_max.append(tuple(bits))
    if all_max:
        common=set(all_max[0])
        for x in all_max[1:]: common&=set(x)
        rho=len(common)/best if best else 0.0
    else:
        rho=0.0
    return best, len(all_max), rho


def main():
    texts = [INSTRUCT_PREFIX + t for t in load_pages()]
    model = SentenceTransformer(MODEL_NAME)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=False, batch_size=8)
    sim = cosine_similarity(emb)

    designed = json.loads(DESIGNED.read_text())
    dedges = {tuple(sorted((int(e["source"][5:])-1, int(e["target"][5:])-1))) for e in designed["edges"]}

    # TP vs FP similarity distributions (over all C(20,2) = 190 pairs)
    tp_sims, fp_sims = [], []
    for i,j in combinations(range(20), 2):
        s = sim[i,j]
        if (i,j) in dedges:
            tp_sims.append(s)
        else:
            fp_sims.append(s)
    tp_sims = np.array(tp_sims); fp_sims = np.array(fp_sims)
    print(f"TP (adjacent, n=30):     min={tp_sims.min():.3f}  p25={np.percentile(tp_sims,25):.3f}  med={np.median(tp_sims):.3f}  p75={np.percentile(tp_sims,75):.3f}  max={tp_sims.max():.3f}  mean={tp_sims.mean():.3f}")
    print(f"FP (non-adj, n=160):     min={fp_sims.min():.3f}  p25={np.percentile(fp_sims,25):.3f}  med={np.median(fp_sims):.3f}  p75={np.percentile(fp_sims,75):.3f}  max={fp_sims.max():.3f}  mean={fp_sims.mean():.3f}")
    gap = tp_sims.mean() - fp_sims.mean()
    print(f"mean gap: {gap:.4f}")

    # Per-threshold sweep (edge = any pair with sim >= t)
    print()
    print("Threshold sweep (edge = sim >= t, no k restriction):")
    print(f"{'t':>5}  {'E':>4}  {'TP':>3}  {'FP':>3}  {'FN':>3}  {'prec':>5}  {'rec':>5}  {'MIS':>3}  {'#opt':>5}  {'ρ':>5}")
    for t in [0.78, 0.80, 0.82, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90]:
        edges = set()
        for i,j in combinations(range(20), 2):
            if sim[i,j] >= t:
                edges.add((i,j))
        tp = len(edges & dedges); fp = len(edges - dedges); fn = len(dedges - edges)
        if edges:
            mis_s, n_opt, rho = mis_brute(20, list(edges))
        else:
            mis_s, n_opt, rho = 20, 1, 1.0
        prec = tp/(tp+fp) if tp+fp else 0.0
        rec = tp/(tp+fn) if tp+fn else 0.0
        print(f"{t:>5.2f}  {len(edges):>4}  {tp:>3}  {fp:>3}  {fn:>3}  {prec:>5.3f}  {rec:>5.3f}  {mis_s:>3}  {n_opt:>5}  {rho:>5.3f}")

    # Mutual kNN (intersection) at k=3..8
    print()
    print("Mutual-kNN (both-directions, intersection) sweep:")
    print(f"{'k':>3}  {'E':>4}  {'TP':>3}  {'FP':>3}  {'FN':>3}  {'prec':>5}  {'rec':>5}  {'MIS':>3}  {'#opt':>5}  {'ρ':>5}")
    s_nod = sim.copy(); np.fill_diagonal(s_nod, -1.0)
    for k in [3,4,5,6,7,8]:
        topk = [set(np.argsort(-s_nod[i])[:k]) for i in range(20)]
        edges = set()
        for i,j in combinations(range(20), 2):
            if j in topk[i] and i in topk[j]:
                edges.add((i,j))
        tp = len(edges & dedges); fp = len(edges - dedges); fn = len(dedges - edges)
        mis_s, n_opt, rho = mis_brute(20, list(edges)) if edges else (20,1,1.0)
        prec = tp/(tp+fp) if tp+fp else 0.0
        rec = tp/(tp+fn) if tp+fn else 0.0
        print(f"{k:>3}  {len(edges):>4}  {tp:>3}  {fp:>3}  {fn:>3}  {prec:>5.3f}  {rec:>5.3f}  {mis_s:>3}  {n_opt:>5}  {rho:>5.3f}")

    # Top-8 false positives by similarity
    print()
    print("Worst false positives (highest sim among non-designed-adjacent pairs):")
    fps = [((i,j), sim[i,j]) for i,j in combinations(range(20), 2) if (i,j) not in dedges]
    fps.sort(key=lambda x:-x[1])
    for (i,j), s in fps[:10]:
        print(f"  p{i+1:02d}-p{j+1:02d}  sim={s:.4f}")

    # Top missed adjacencies (lowest sim among designed-adjacent pairs)
    print()
    print("Weakest true positives (lowest sim among designed-adjacent pairs):")
    tps = [((i,j), sim[i,j]) for i,j in dedges]
    tps.sort(key=lambda x:x[1])
    for (i,j), s in tps[:8]:
        print(f"  p{i+1:02d}-p{j+1:02d}  sim={s:.4f}")


if __name__ == "__main__":
    main()
