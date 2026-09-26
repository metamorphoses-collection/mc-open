#!/usr/bin/env python3
"""
Fine-tune E5-large with contrastive learning on thread-labeled OuLiPo pages.

Strategy:
  - Positive pairs: pages sharing ≥4 threads (designed edges)
  - Negative pairs: pages sharing ≤2 threads (designed non-edges)
  - Loss: CosineSimilarityLoss (regression: sim=1.0 for positive, sim=0.0 for negative)
  - Training data: ALL written OuLiPo texts (~400 pages with thread labels)
  - Epochs: 3-5 (small dataset, risk of overfitting)
  - Output: fine-tuned model saved locally

Usage:
    python finetune_embedder.py
    python finetune_embedder.py --validate  # validate rho=1.0 text with fine-tuned model
"""

import json
import re
import sys
import os
from pathlib import Path
from collections import defaultdict

import numpy as np
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader

BASE = Path(__file__).resolve().parent
THREADS_DIR = BASE / "threads"
TEXTS_DIR = BASE / "texts"
MODEL_NAME = "intfloat/multilingual-e5-large"
OUTPUT_MODEL = BASE / "models" / "e5-large-oulipo"


def parse_pages(text_path):
    """Parse markdown OuLiPo text into pages with threads."""
    text = Path(text_path).read_text(encoding="utf-8")
    pages = []
    parts = re.split(r"####\s+PAGE\s+(\d+)", text)
    for i in range(1, len(parts), 2):
        page_num = int(parts[i])
        body = parts[i + 1]
        thread_match = re.search(r"\*Threads?:\s*(.+?)\*", body)
        threads = []
        if thread_match:
            threads = [t.strip() for t in thread_match.group(1).split(",")]
        lines = body.strip().split("\n")
        text_lines = [l for l in lines if not l.startswith("*") and l.strip()]
        page_text = "\n".join(text_lines).strip()
        page_text = re.sub(r"\n---\s*$", "", page_text).strip()
        if page_text and threads:
            pages.append({
                "page": page_num,
                "threads": set(threads),
                "text": page_text,
                "source": text_path.stem,
            })
    return pages


def load_all_pages():
    """Load pages from all OuLiPo texts with thread labels."""
    all_pages = []
    text_files = [
        "livre_irremplacable.md",
        "livre_irremplacable_v2.md",
        "kaleidoscope.md",
        "carte_du_texte.md",
        "proces_de_nithard.md",
        "livre_fractal.md",
        "piege_du_lecteur.md",
        "partition_du_texte.md",
        "jumeaux_en.md",
        "jumeaux_fr.md",
    ]
    for tf in text_files:
        path = TEXTS_DIR / tf
        if path.exists():
            pages = parse_pages(path)
            all_pages.extend(pages)
            print(f"  {tf}: {len(pages)} pages")
    return all_pages


def build_training_pairs(pages, pos_overlap=4, neg_overlap=2):
    """Build contrastive training pairs from thread overlap."""
    examples = []
    n_pos = 0
    n_neg = 0

    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            overlap = len(pages[i]["threads"] & pages[j]["threads"])

            if overlap >= pos_overlap:
                # Positive pair: should be similar
                examples.append(InputExample(
                    texts=["passage: " + pages[i]["text"],
                           "passage: " + pages[j]["text"]],
                    label=1.0,
                ))
                n_pos += 1
            elif overlap <= neg_overlap:
                # Negative pair: should be dissimilar
                examples.append(InputExample(
                    texts=["passage: " + pages[i]["text"],
                           "passage: " + pages[j]["text"]],
                    label=0.0,
                ))
                n_neg += 1
            # Skip overlap 3 (ambiguous zone)

    print(f"  Training pairs: {n_pos} positive, {n_neg} negative, "
          f"{len(examples)} total")
    return examples


def build_eval_set(pages, n_eval=200):
    """Build evaluation set from held-out pairs."""
    import random
    rng = random.Random(42)

    sentences1 = []
    sentences2 = []
    scores = []

    pairs = []
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            overlap = len(pages[i]["threads"] & pages[j]["threads"])
            if overlap >= 4 or overlap <= 2:
                pairs.append((i, j, 1.0 if overlap >= 4 else 0.0))

    rng.shuffle(pairs)
    for i, j, score in pairs[:n_eval]:
        sentences1.append("passage: " + pages[i]["text"])
        sentences2.append("passage: " + pages[j]["text"])
        scores.append(score)

    return EmbeddingSimilarityEvaluator(
        sentences1, sentences2, scores,
        name="thread-overlap",
    )


def main():
    validate_only = "--validate" in sys.argv

    if validate_only and OUTPUT_MODEL.exists():
        print(f"Loading fine-tuned model from {OUTPUT_MODEL}...")
        model = SentenceTransformer(str(OUTPUT_MODEL))
        validate_with_model(model)
        return

    print("=" * 60)
    print("  FINE-TUNING E5-LARGE FOR THREAD DISCRIMINATION")
    print("=" * 60)

    # Load all pages
    print("\nLoading pages...")
    pages = load_all_pages()
    print(f"  Total: {len(pages)} pages from {len(set(p['source'] for p in pages))} texts")

    # Split: 80% train, 20% eval
    import random
    rng = random.Random(42)
    indices = list(range(len(pages)))
    rng.shuffle(indices)
    split = int(0.8 * len(pages))
    train_pages = [pages[i] for i in indices[:split]]
    eval_pages = [pages[i] for i in indices[split:]]
    print(f"  Train: {len(train_pages)}, Eval: {len(eval_pages)}")

    # Build training pairs
    print("\nBuilding training pairs...")
    train_examples = build_training_pairs(train_pages, pos_overlap=4, neg_overlap=2)

    # Also add pairs with different thresholds for texts with 5 threads/page
    train_examples_3 = build_training_pairs(train_pages, pos_overlap=3, neg_overlap=1)
    # Combine but limit negatives (they dominate)
    all_examples = train_examples + train_examples_3
    rng.shuffle(all_examples)

    # Limit to balanced set
    pos = [e for e in all_examples if e.label > 0.5]
    neg = [e for e in all_examples if e.label <= 0.5]
    # Upsample positives or downsample negatives
    max_neg = min(len(neg), len(pos) * 3)  # 3:1 ratio
    neg = neg[:max_neg]
    balanced = pos + neg
    rng.shuffle(balanced)
    print(f"  Balanced: {len(pos)} positive, {len(neg)} negative = {len(balanced)} total")

    # Build eval
    print("Building evaluator...")
    evaluator = build_eval_set(eval_pages, n_eval=min(500, len(eval_pages) * (len(eval_pages) - 1) // 2))

    # Load model
    print(f"\nLoading {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)

    # Training
    train_dataloader = DataLoader(balanced, shuffle=True, batch_size=4)
    train_loss = losses.CosineSimilarityLoss(model)

    OUTPUT_MODEL.parent.mkdir(parents=True, exist_ok=True)

    # Force CPU to avoid MPS OOM on Mac
    import torch
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    if hasattr(torch.backends, "mps"):
        os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
    model = model.to("cpu")

    print(f"\nTraining for 3 epochs (CPU, batch_size=4)...")
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        evaluator=evaluator,
        epochs=3,
        warmup_steps=int(0.1 * len(train_dataloader)),
        output_path=str(OUTPUT_MODEL),
        show_progress_bar=True,
        evaluation_steps=len(train_dataloader),  # eval each epoch
        use_amp=False,
    )

    print(f"\n✓ Fine-tuned model saved to {OUTPUT_MODEL}")

    # Validate
    print("\n" + "=" * 60)
    print("  VALIDATING WITH FINE-TUNED MODEL")
    print("=" * 60)
    validate_with_model(model)


def validate_with_model(model):
    """Validate rho=1.0 text with the given model."""
    from sklearn.metrics.pairwise import cosine_similarity

    # Parse rho=1.0 text
    pages = parse_pages(TEXTS_DIR / "livre_irremplacable.md")
    N = len(pages)
    print(f"\n  Validating livre_irremplacable.md: {N} pages")

    # Embed
    texts = ["passage: " + p["text"] for p in pages]
    embeddings = model.encode(texts, batch_size=32, normalize_embeddings=True,
                              show_progress_bar=False)

    sim_matrix = cosine_similarity(embeddings)
    np.fill_diagonal(sim_matrix, 0)
    upper = sim_matrix[np.triu_indices(N, k=1)]

    print(f"  Similarity: mean={np.mean(upper):.4f}, std={np.std(upper):.4f}")
    print(f"  Min={np.min(upper):.4f}, Max={np.max(upper):.4f}")
    print(f"  % > 0.78: {100*np.mean(upper > 0.78):.1f}%")
    print(f"  % > 0.85: {100*np.mean(upper > 0.85):.1f}%")

    # Thread overlap vs similarity
    page_threads = {p["page"]: p["threads"] for p in pages}
    by_overlap = defaultdict(list)
    for i in range(N):
        for j in range(i + 1, N):
            overlap = len(pages[i]["threads"] & pages[j]["threads"])
            by_overlap[overlap].append(sim_matrix[i][j])

    print("\n  Thread overlap vs similarity:")
    for ov in sorted(by_overlap.keys()):
        sims = by_overlap[ov]
        pct_above = 100 * np.mean(np.array(sims) > 0.78)
        print(f"    Overlap {ov}: n={len(sims):4d}, sim={np.mean(sims):.4f} ± {np.std(sims):.4f}, "
              f">{0.78}: {pct_above:.1f}%")

    # Build graph at k=8
    import networkx as nx
    from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD

    node_ids = [f"p{p['page']}" for p in pages]
    G = nx.Graph()
    G.add_nodes_from(node_ids)
    for i in range(N):
        sims = sim_matrix[i].copy()
        sims[i] = -1
        top_k = np.argsort(sims)[-8:]
        for j in top_k:
            if sims[j] >= 0.78:
                G.add_edge(node_ids[i], node_ids[j])

    # MIS
    prob = LpProblem("MIS", LpMaximize)
    x = {n: LpVariable(f"x_{n}", cat="Binary") for n in G.nodes()}
    prob += lpSum(x.values())
    for u, v in G.edges():
        prob += x[u] + x[v] <= 1
    prob.solve(PULP_CBC_CMD(msg=0))
    mis = sorted([n for n, v in x.items() if v.varValue > 0.5])

    # Enumerate
    solutions = []
    for it in range(50):
        prob = LpProblem(f"MIS_{it}", LpMaximize)
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

    essential = set.intersection(*[set(s) for s in solutions]) if solutions else set()
    rho = len(essential) / len(solutions[0]) if solutions else 0

    print(f"\n  Graph (k=8): E={G.number_of_edges()}, d={nx.density(G):.4f}")
    print(f"  MIS: {len(mis)} (ratio: {len(mis)/N:.3f})")
    print(f"  Solutions: {len(solutions)}")
    print(f"  Rigidity rho: {rho:.3f}")

    if len(solutions) == 1:
        print(f"  *** rho = 1.000 — TARGET ACHIEVED ***")
    else:
        print(f"  Target: rho=1.0, achieved: rho={rho:.3f}")

    # Also try different thresholds
    print("\n  Threshold sweep:")
    for thresh in [0.70, 0.75, 0.78, 0.80, 0.85, 0.90]:
        G_t = nx.Graph()
        G_t.add_nodes_from(node_ids)
        for i in range(N):
            sims = sim_matrix[i].copy()
            sims[i] = -1
            top_k = np.argsort(sims)[-8:]
            for j in top_k:
                if sims[j] >= thresh:
                    G_t.add_edge(node_ids[i], node_ids[j])

        prob = LpProblem("MIS", LpMaximize)
        x = {n: LpVariable(f"x_{n}", cat="Binary") for n in G_t.nodes()}
        prob += lpSum(x.values())
        for u, v in G_t.edges():
            prob += x[u] + x[v] <= 1
        prob.solve(PULP_CBC_CMD(msg=0))
        m = sorted([n for n, v in x.items() if v.varValue > 0.5])

        print(f"    thresh={thresh}: E={G_t.number_of_edges()}, MIS={len(m)}")


if __name__ == "__main__":
    main()
