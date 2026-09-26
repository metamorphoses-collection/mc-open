#!/usr/bin/env python3
"""
Fine-tune E5-large for OuLiPo thread discrimination.
Run on RunPod or GCP with GPU (A100/T4/L4).

Setup:
    pip install sentence-transformers datasets accelerate torch

Usage:
    python finetune_colab.py                    # train + validate
    python finetune_colab.py --validate-only    # validate with saved model

Output:
    models/e5-large-oulipo/    — fine-tuned model
    finetune_results.json      — validation metrics
"""

import json, re, os, sys, random
from pathlib import Path
from collections import defaultdict
import numpy as np

# ─── Parse pages ──────────────────────────────────────────────────────────
def parse_pages(text_path):
    text = Path(text_path).read_text(encoding="utf-8")
    pages = []
    parts = re.split(r"####\s+PAGE\s+(\d+)", text)
    for i in range(1, len(parts), 2):
        page_num = int(parts[i])
        body = parts[i + 1]
        thread_match = re.search(r"\*Threads?:\s*(.+?)\*", body)
        threads = [t.strip() for t in thread_match.group(1).split(",")] if thread_match else []
        lines = body.strip().split("\n")
        text_lines = [l for l in lines if not l.startswith("*") and l.strip()]
        page_text = re.sub(r"\n---\s*$", "", "\n".join(text_lines).strip()).strip()
        if page_text and threads:
            pages.append({"page": page_num, "threads": set(threads),
                         "text": page_text, "source": Path(text_path).stem})
    return pages

# ─── Main ─────────────────────────────────────────────────────────────────
def main():
    from sentence_transformers import SentenceTransformer, InputExample, losses
    from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
    from torch.utils.data import DataLoader
    from sklearn.metrics.pairwise import cosine_similarity
    import networkx as nx

    BASE = Path(".")
    TEXTS_DIR = BASE / "texts"
    OUTPUT_MODEL = BASE / "models" / "e5-large-oulipo"

    validate_only = "--validate-only" in sys.argv

    # ─── Load all texts ───────────────────────────────────────────────────
    text_files = [f for f in TEXTS_DIR.glob("*.md")
                  if not f.name.startswith("oulipo") and f.name != "parity_sweep.md"
                  and f.name != "topic_clusters.md"]

    all_pages = []
    for tf in sorted(text_files):
        pages = parse_pages(tf)
        if pages:
            all_pages.extend(pages)
            print(f"  {tf.name}: {len(pages)} pages")

    print(f"\n  Total: {len(all_pages)} pages from {len(set(p['source'] for p in all_pages))} texts")

    if validate_only and OUTPUT_MODEL.exists():
        model = SentenceTransformer(str(OUTPUT_MODEL))
        validate(model, all_pages)
        return

    # ─── Build training pairs ─────────────────────────────────────────────
    rng = random.Random(42)
    indices = list(range(len(all_pages)))
    rng.shuffle(indices)
    split = int(0.85 * len(all_pages))
    train_pages = [all_pages[i] for i in indices[:split]]
    eval_pages = [all_pages[i] for i in indices[split:]]

    print(f"\n  Train: {len(train_pages)}, Eval: {len(eval_pages)}")

    # Build pairs with multiple overlap thresholds
    examples = []
    for pos_ov, neg_ov in [(4, 2), (3, 1), (5, 2)]:
        for i in range(len(train_pages)):
            for j in range(i + 1, len(train_pages)):
                overlap = len(train_pages[i]["threads"] & train_pages[j]["threads"])
                if overlap >= pos_ov:
                    examples.append(InputExample(
                        texts=["passage: " + train_pages[i]["text"],
                               "passage: " + train_pages[j]["text"]],
                        label=1.0))
                elif overlap <= neg_ov:
                    examples.append(InputExample(
                        texts=["passage: " + train_pages[i]["text"],
                               "passage: " + train_pages[j]["text"]],
                        label=0.0))

    pos = [e for e in examples if e.label > 0.5]
    neg = [e for e in examples if e.label <= 0.5]
    # Balance: 1:2 ratio (pos:neg)
    max_neg = min(len(neg), len(pos) * 2)
    neg = neg[:max_neg]
    balanced = pos + neg
    rng.shuffle(balanced)
    print(f"  Pairs: {len(pos)} pos, {len(neg)} neg = {len(balanced)} total")

    # Eval set
    eval_s1, eval_s2, eval_scores = [], [], []
    for i in range(len(eval_pages)):
        for j in range(i + 1, len(eval_pages)):
            ov = len(eval_pages[i]["threads"] & eval_pages[j]["threads"])
            if ov >= 4 or ov <= 2:
                eval_s1.append("passage: " + eval_pages[i]["text"])
                eval_s2.append("passage: " + eval_pages[j]["text"])
                eval_scores.append(1.0 if ov >= 4 else 0.0)
    evaluator = EmbeddingSimilarityEvaluator(eval_s1[:1000], eval_s2[:1000], eval_scores[:1000],
                                              name="thread-overlap")

    # ─── Train ────────────────────────────────────────────────────────────
    print(f"\n  Loading intfloat/multilingual-e5-large...")
    model = SentenceTransformer("intfloat/multilingual-e5-large")

    train_dl = DataLoader(balanced, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model)
    OUTPUT_MODEL.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Training for 5 epochs (batch_size=16, GPU)...")
    model.fit(
        train_objectives=[(train_dl, train_loss)],
        evaluator=evaluator,
        epochs=5,
        warmup_steps=int(0.1 * len(train_dl)),
        output_path=str(OUTPUT_MODEL),
        show_progress_bar=True,
        evaluation_steps=len(train_dl),
    )
    print(f"\n  ✓ Model saved to {OUTPUT_MODEL}")

    # ─── Validate ─────────────────────────────────────────────────────────
    validate(model, all_pages)


def validate(model, all_pages):
    from sklearn.metrics.pairwise import cosine_similarity
    import networkx as nx
    from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD

    # Test on rho=1.0 text specifically
    rho1_pages = [p for p in all_pages if p["source"] == "livre_irremplacable"]
    if not rho1_pages:
        print("  No livre_irremplacable pages found for validation")
        return

    N = len(rho1_pages)
    print(f"\n  Validating on livre_irremplacable ({N} pages)...")

    texts = ["passage: " + p["text"] for p in rho1_pages]
    embs = model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)
    sim = cosine_similarity(embs)
    np.fill_diagonal(sim, 0)
    upper = sim[np.triu_indices(N, k=1)]

    print(f"  Sim: mean={np.mean(upper):.4f}, std={np.std(upper):.4f}, "
          f"min={np.min(upper):.4f}, max={np.max(upper):.4f}")
    print(f"  % > 0.78: {100*np.mean(upper > 0.78):.1f}%, "
          f"% > 0.85: {100*np.mean(upper > 0.85):.1f}%")

    # Thread overlap vs similarity
    by_ov = defaultdict(list)
    for i in range(N):
        for j in range(i+1, N):
            ov = len(rho1_pages[i]["threads"] & rho1_pages[j]["threads"])
            by_ov[ov].append(sim[i][j])

    print(f"\n  Overlap vs similarity (fine-tuned):")
    for ov in sorted(by_ov):
        s = by_ov[ov]
        pct = 100 * np.mean(np.array(s) > 0.78)
        print(f"    Overlap {ov}: n={len(s):4d}, sim={np.mean(s):.4f} ± {np.std(s):.4f}, >0.78: {pct:.1f}%")

    # Build graph + MIS at k=8
    node_ids = [f"p{p['page']}" for p in rho1_pages]
    for thresh in [0.50, 0.60, 0.70, 0.78, 0.85, 0.90]:
        G = nx.Graph()
        G.add_nodes_from(node_ids)
        for i in range(N):
            sims = sim[i].copy(); sims[i] = -1
            top_k = np.argsort(sims)[-8:]
            for j in top_k:
                if sims[j] >= thresh:
                    G.add_edge(node_ids[i], node_ids[j])

        prob = LpProblem("MIS", LpMaximize)
        x = {n: LpVariable(f"x_{n}", cat="Binary") for n in G.nodes()}
        prob += lpSum(x.values())
        for u, v in G.edges():
            prob += x[u] + x[v] <= 1
        prob.solve(PULP_CBC_CMD(msg=0))
        mis = [n for n, v in x.items() if v.varValue > 0.5]

        # Quick enumerate
        sols = []
        for it in range(20):
            prob = LpProblem(f"E_{it}", LpMaximize)
            x = {n: LpVariable(f"x_{n}", cat="Binary") for n in G.nodes()}
            prob += lpSum(x.values())
            for u, v in G.edges():
                prob += x[u] + x[v] <= 1
            for prev in sols:
                prob += lpSum(x[n] for n in prev) <= len(prev) - 1
            prob.solve(PULP_CBC_CMD(msg=0))
            sol = sorted([n for n, v in x.items() if v.varValue > 0.5])
            if not sol or (sols and len(sol) < len(sols[0])): break
            sols.append(sol)

        ess = set.intersection(*[set(s) for s in sols]) if sols else set()
        rho = len(ess) / len(sols[0]) if sols else 0
        print(f"  thresh={thresh}: E={G.number_of_edges()}, MIS={len(mis)}, "
              f"sols={len(sols)}, rho={rho:.3f}")

    # Save results
    results = {
        "sim_mean": float(np.mean(upper)),
        "sim_std": float(np.std(upper)),
        "overlap_sims": {str(ov): {"mean": float(np.mean(s)), "std": float(np.std(s))}
                        for ov, s in by_ov.items()},
    }
    with open("finetune_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  ✓ Saved to finetune_results.json")


if __name__ == "__main__":
    main()
