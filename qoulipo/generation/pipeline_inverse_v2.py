#!/usr/bin/env python3
"""
Pipeline-inverse v2: adds table-format thread parsing, parent-inheritance
for language variants with missing annotations, natural-text mode, and
a unified database output.

Supports three text formats:
  A. `#### PAGE n` + `*Threads: X, Y*` (livre_irremplacable, kaleidoscope ...)
  B. `## Page n` + `Threads: X, Y`     (nithards_wager_65p, oulipo_100_hardzone ...)
  C. table format: `| P01 | ... | X, Y, Z |` + chapters delimited differently
     (carte_du_texte)

Plus parent-inheritance: if a FR text has no thread annotations of its
own, inherit them from its EN parent by page number. This works for
jumeaux_fr ← jumeaux_en, oulipo_v2b_100pages_fr ← oulipo_v2_100pages, etc.
"""

import json
import re
from itertools import combinations
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
TEXTS = BASE / "texts"
OUT = BASE / "pipeline_inverse_db.json"

MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
INSTRUCTION = "Retrieve semantically similar passages from the same constrained literary text."
THREAD_OVERLAP_THRESHOLD = 4


# ── Corpus config ──────────────────────────────────────────────────────

ENGINEERED_CORPUS = [
    # format: (filename, lang, parent_for_threads_or_None)
    ("kaleidoscope.md", "EN", None),
    ("livre_irremplacable.md", "FR", None),
    ("livre_irremplacable_v2.md", "FR", None),
    ("piege_du_lecteur.md", "FR", None),
    ("livre_fractal.md", "EN", None),
    ("proces_de_nithard.md", "FR", None),
    ("partition_du_texte.md", "FR", None),
    ("oulipo_nithard_pascal_v1_original.md", "EN", None),
    ("oulipo_nithard_pascal.md", "EN", None),
    ("incarnate_graph_50_en.md", "EN", None),
    ("incarnate_graph_50p_en.md", "EN", None),
    ("oulipo_udg_50pages.md", "FR", None),
    ("oulipo_udg_50pages_en.md", "EN", None),
    ("oulipo_udg65_text.md", "EN", None),
    ("nithards_wager_65p_en.md", "EN", None),
    ("oulipo_65_hardzone.md", "FR", None),
    ("oulipo_65_hardzone_en.md", "EN", None),
    ("oulipo_65_hardzone_en_v2.md", "EN", None),
    ("nithards_wager_100p_en.md", "EN", None),
    ("oulipo_100_hardzone.md", "FR", None),
    ("oulipo_v2_100pages.md", "EN", None),
    ("oulipo_v2_100pages_revised.md", "EN", None),
    ("jumeaux_en.md", "EN", None),
    # Language inheritance: FR version borrows threads from EN parent
    ("jumeaux_fr.md", "FR", "jumeaux_en.md"),
    ("oulipo_v2b_100pages_fr.md", "FR", "oulipo_v2_100pages.md"),
    ("oulipo_v2b_100pages_fr_revised.md", "FR", "oulipo_v2_100pages_revised.md"),
    # Table-format threads
    ("carte_du_texte.md", "FR", "_TABLE_"),  # sentinel for table-format parser
]


NATURAL_CORPUS_GRAPHS = [
    # (display_name, lang, N, graph_file)
    ("augustine_conf13 (LA) N=22 k=8", "LA", 22,
     "3_MIS/classical/graphs/augustine/graph_Augustine_Conf13.json"),
    ("lactantius_demort (LA) N=52 k=8", "LA", 52,
     "3_MIS/classical/graphs/lactantius/graph_lactantius_demort_k8.json"),
    ("lactantius_demort (LA) N=52 k=16", "LA", 52,
     "3_MIS/classical/graphs/lactantius/graph_Lactantius_DeMort_k16.json"),
    ("giambullari_65 (IT) N=65 k=8", "IT", 65,
     "3_MIS/classical/graphs/giambullari/graph_giambullari_65.json"),
    ("galileo_65 (IT) N=65 k=8", "IT", 65,
     "3_MIS/classical/graphs/galileo/graph_galileo_65_k8.json"),
    ("galileo_65 (IT) N=65 k=16", "IT", 65,
     "3_MIS/classical/graphs/galileo/graph_galileo_65.json"),
    ("galileo_dialogo (IT) N=74 k=8", "IT", 74,
     "3_MIS/classical/graphs/galileo/graph_Galileo_Dialogo.json"),
    ("galileo_dialogo (IT) N=74 k=12", "IT", 74,
     "3_MIS/classical/graphs/galileo/graph_Galileo_Dialogo_k12.json"),
    ("galileo_dialogo (IT) N=74 k=16", "IT", 74,
     "3_MIS/classical/graphs/galileo/graph_Galileo_Dialogo_k16.json"),
    ("heptameron (FR) N=72 k=8", "FR", 72,
     "3_MIS/classical/graphs/heptameron/graph_heptameron_1559_k8.json"),
    ("heptameron (FR) N=72 k=16", "FR", 72,
     "3_MIS/classical/graphs/heptameron/graph_heptameron_1559_k16.json"),
    ("boethius_consolatio (LA) N=72 k=8", "LA", 72,
     "3_MIS/classical/graphs/boethius/graph_boethius_consolatio_k8.json"),
    ("boethius_consolatio (LA) N=72 k=16", "LA", 72,
     "3_MIS/classical/graphs/boethius/graph_boethius_consolatio_k16.json"),
    ("dante_commedia (IT) N=59 k=8", "IT", 59,
     "3_MIS/classical/graphs/dante/graph_dante_59_k8.json"),
    ("montaigne_essais (FR) N=65 k=8", "FR", 65,
     "3_MIS/classical/graphs/montaigne/graph_montaigne_65_k8.json"),
    ("montaigne_essais (FR) N=65 k=16", "FR", 65,
     "3_MIS/classical/graphs/montaigne/graph_montaigne_65_k16.json"),
    ("augustine_conf7_13 (LA) N=132 k=8", "LA", 132,
     "3_MIS/classical/graphs/augustine/graph_Augustine_Conf7_13.json"),
]


# ── Parsers ────────────────────────────────────────────────────────────

def _split_pages(text):
    """Return list of (page_num, body) pairs. Supports #### PAGE and ## Page."""
    parts_a = re.split(r"(?m)^####\s+PAGE\s+(\d+)", text)
    pages_a = [(int(parts_a[i]), parts_a[i + 1]) for i in range(1, len(parts_a), 2)]
    parts_b = re.split(r"(?im)^##\s+PAGE\s+(\d+)", text)
    pages_b = [(int(parts_b[i]), parts_b[i + 1]) for i in range(1, len(parts_b), 2)]
    return pages_a if len(pages_a) >= len(pages_b) else pages_b


def parse_pages_std(text_path, inherited_threads=None):
    """Standard parser: pages with explicit Threads: lines, or inherited."""
    text = Path(text_path).read_text(encoding="utf-8")
    pages = []
    for page_num, body in _split_pages(text):
        body = re.split(r"(?m)^(?:####\s+PAGE|\s*---\s*$)", body)[0]
        # Grab threads from body if present
        thread_match = re.search(r"(?im)^\s*\*?\s*Threads?:\s*(.+?)\s*\*?\s*$", body)
        threads = []
        if thread_match:
            threads = [t.strip() for t in thread_match.group(1).split(",") if t.strip()]
        # If no threads here, try inherited by page number
        if not threads and inherited_threads is not None:
            threads = list(inherited_threads.get(page_num, []))
        # Strip metadata / annotations from body
        lines = body.strip().split("\n")
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
                continue
            text_lines.append(stripped)
        page_text = "\n".join(text_lines).strip()
        if page_text and threads:
            pages.append({"page": page_num, "threads": set(threads), "text": page_text})
    return pages


def parse_pages_table(text_path):
    """carte_du_texte format: threads in a table, pages delimited by '### Page P01' or similar.
    We first extract the table, then pair each row with its chapter body."""
    text = Path(text_path).read_text(encoding="utf-8")

    # Extract thread table: rows look like "| P06 | r0c6 | --- | BONE, NUMBER, ... |"
    table_threads = {}
    for line in text.split("\n"):
        m = re.match(r"^\|\s*P(\d+)\s*\|.*?\|\s*([A-Z][A-Z, ]+)\s*\|", line)
        if m:
            page_num = int(m.group(1))
            threads = [t.strip() for t in m.group(2).split(",") if t.strip()]
            if threads:
                table_threads[page_num] = set(threads)

    # Now split text into pages. Try both heading patterns.
    # carte_du_texte uses `### Page P01 — ...`
    parts = re.split(r"(?im)^###\s+Page\s+P(\d+)", text)
    pages = []
    for i in range(1, len(parts), 2):
        page_num = int(parts[i])
        body = parts[i + 1]
        body = re.split(r"(?im)^###\s+Page\s+P", body)[0]
        lines = body.strip().split("\n")
        text_lines = [l.strip() for l in lines
                      if l.strip() and not l.strip().startswith("|")
                      and not l.strip().startswith("#")]
        page_text = "\n".join(text_lines).strip()
        if page_text and page_num in table_threads:
            pages.append({
                "page": page_num,
                "threads": table_threads[page_num],
                "text": page_text,
            })
    return pages


def extract_threads_by_page(text_path):
    """Parse text and return {page_num: set(threads)}, for parent inheritance."""
    pages = parse_pages_std(text_path)
    return {p["page"]: p["threads"] for p in pages}


def parse_pages(text_path, parent_path=None):
    """Dispatch parser: try std first, then std+inherit, then table."""
    if parent_path == "_TABLE_":
        return parse_pages_table(text_path)
    inherited = None
    if parent_path:
        parent_file = TEXTS / parent_path
        if parent_file.exists():
            inherited = extract_threads_by_page(parent_file)
    return parse_pages_std(text_path, inherited_threads=inherited)


# ── Pipeline ───────────────────────────────────────────────────────────

def build_designed_adjacency(pages, overlap_threshold):
    N = len(pages)
    edges = set()
    for i, j in combinations(range(N), 2):
        if len(pages[i]["threads"] & pages[j]["threads"]) >= overlap_threshold:
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
    return {
        "recovered": len(recovered), "tp": tp, "fp": fp, "fn": fn,
        "recall": round(recall, 3), "precision": round(precision, 3),
        "f1": round(f1, 3), "jaccard": round(jaccard, 3),
    }


# ── Engineered runner ──────────────────────────────────────────────────

def run_engineered(filename, lang, parent, k_values=(8, 16, 24)):
    path = TEXTS / filename
    if not path.exists():
        return None
    pages = parse_pages(path, parent_path=parent)
    if len(pages) < 4:
        return None
    N = len(pages)
    designed = build_designed_adjacency(pages, THREAD_OVERLAP_THRESHOLD)
    if not designed:
        return None

    avg_degree = 2 * len(designed) / N
    k_star = max(2, round(avg_degree))
    slug = filename.replace(".md", "")
    display = f"{slug} ({lang}) N={N} k={k_star}"
    density = len(designed) / (N * (N - 1) // 2)

    print(f"  {display}  d={density:.3f} edges={len(designed)} "
          f"avg_deg={avg_degree:.1f}")

    texts = [p["text"] for p in pages]
    embeddings = embed_pages(texts)

    results = {}
    for k in sorted(set(list(k_values) + [k_star])):
        recovered = build_knn(embeddings, k=k)
        m = metrics(recovered, designed, N)
        tag = "*" if k == k_star else ""
        results[f"k={k}{tag}"] = m

    best_f1 = max(r["f1"] for r in results.values())
    return {
        "type": "engineered",
        "file": filename,
        "display": display,
        "lang": lang,
        "N": N,
        "density": round(density, 4),
        "designed_edges": len(designed),
        "avg_degree": round(avg_degree, 2),
        "k_star": k_star,
        "best_f1": best_f1,
        "k_results": results,
        "parent": parent,
    }


# ── Natural-text runner ────────────────────────────────────────────────

def run_natural(display, lang, N, graph_file, k_values=(8, 16, 24)):
    """
    For natural texts we have the k-NN graph already (built by the classical
    pipeline). The "pipeline-inverse" experiment for natural texts is a
    sanity check: re-embed the chapter texts with e5-instruct and compare
    the recovered k-NN graph to the stored one. High F1 means the stored
    graph is reproducible.

    If the graph file has text content on the nodes (topic graph style),
    we use that text directly. Otherwise we skip the sanity check and
    just record the stored graph's invariants for the database.
    """
    path = Path(graph_file)
    if not path.exists():
        return None
    g = json.loads(path.read_text())
    nodes = g.get("nodes", [])
    edges = g.get("edges", g.get("links", []))
    if not nodes:
        return None
    # Try to extract per-node text. Accept `nodes` as dicts with 'text'/'text_full'/'preview'
    # or as plain strings with no body.
    node_texts = []
    if isinstance(nodes[0], dict):
        node_ids = [n["id"] if isinstance(n, dict) else n for n in nodes]
        for n in nodes:
            txt = (n.get("text_full") or n.get("text") or n.get("preview") or "").strip()
            node_texts.append(txt)
    else:
        node_ids = nodes
        node_texts = [""] * len(nodes)

    N_actual = len(node_ids)
    density = (len(edges) * 2) / (N_actual * (N_actual - 1)) if N_actual > 1 else 0
    result = {
        "type": "natural",
        "file": str(graph_file),
        "display": display,
        "lang": lang,
        "N": N_actual,
        "density": round(density, 4),
        "stored_edges": len(edges),
        "has_text": any(t for t in node_texts),
    }

    if any(len(t) > 30 for t in node_texts):
        # Re-embed with e5-instruct and compute recovery F1 against stored graph
        # Convert stored edges to integer pairs
        idx = {n: i for i, n in enumerate(node_ids)}
        stored_set = set()
        for e in edges:
            if isinstance(e, dict):
                u, v = e["source"], e["target"]
            else:
                u, v = e[0], e[1]
            if u in idx and v in idx:
                ii, jj = idx[u], idx[v]
                stored_set.add((min(ii, jj), max(ii, jj)))

        texts = [t for t in node_texts]
        embeddings = embed_pages(texts)
        avg_deg = 2 * len(stored_set) / N_actual
        k_star = max(2, round(avg_deg))
        k_results = {}
        for k in sorted(set(list(k_values) + [k_star])):
            recovered = build_knn(embeddings, k=k)
            m = metrics(recovered, stored_set, N_actual)
            tag = "*" if k == k_star else ""
            k_results[f"k={k}{tag}"] = m
        result["avg_degree"] = round(avg_deg, 2)
        result["k_star"] = k_star
        result["k_results"] = k_results
        result["best_f1"] = max(r["f1"] for r in k_results.values())
    else:
        result["note"] = "graph file has no inline text; only invariants recorded"
    return result


# ── Main ────────────────────────────────────────────────────────────────

def main():
    engineered = []
    natural = []

    print("\n=== ENGINEERED CORPUS ===")
    for filename, lang, parent in ENGINEERED_CORPUS:
        try:
            r = run_engineered(filename, lang, parent)
            if r is not None:
                engineered.append(r)
        except Exception as e:
            print(f"  ERROR {filename}: {e}")

    print("\n=== NATURAL CORPUS ===")
    for display, lang, N, graph_file in NATURAL_CORPUS_GRAPHS:
        try:
            r = run_natural(display, lang, N, graph_file)
            if r is not None:
                natural.append(r)
                info = f"d={r['density']:.3f} edges={r['stored_edges']}"
                if "best_f1" in r:
                    info += f" best_F1={r['best_f1']:.3f}"
                print(f"  {display}: {info}")
        except Exception as e:
            print(f"  ERROR {display}: {e}")

    db = {
        "model": MODEL_NAME,
        "overlap_threshold": THREAD_OVERLAP_THRESHOLD,
        "engineered": engineered,
        "natural": natural,
        "summary": {
            "n_engineered": len(engineered),
            "n_natural": len(natural),
            "mean_engineered_f1": round(
                float(np.mean([e["best_f1"] for e in engineered])), 3
            ) if engineered else 0,
            "mean_natural_f1": round(
                float(np.mean([n["best_f1"] for n in natural if "best_f1" in n])), 3
            ) if any("best_f1" in n for n in natural) else None,
        },
    }
    OUT.write_text(json.dumps(db, indent=2))

    print("\n\n========== ENGINEERED ==========")
    print(f"{'display':<52} {'d':>6} {'best_F1':>9}")
    for e in sorted(engineered, key=lambda r: -r["best_f1"]):
        print(f"{e['display']:<52} {e['density']:>6.3f} {e['best_f1']:>9.3f}")

    print("\n========== NATURAL ==========")
    print(f"{'display':<48} {'d':>6} {'N':>4} {'edges':>6} {'F1':>7}")
    for n in natural:
        f1 = n.get("best_f1", "—")
        f1s = f"{f1:.3f}" if isinstance(f1, float) else f1
        print(f"{n['display']:<48} {n['density']:>6.3f} {n['N']:>4} "
              f"{n['stored_edges']:>6} {f1s:>7}")

    print(f"\nSaved → {OUT}")
    print(f"Engineered: {len(engineered)}  Natural: {len(natural)}")
    print(f"Mean engineered F1: {db['summary']['mean_engineered_f1']}")
    if db['summary']['mean_natural_f1'] is not None:
        print(f"Mean natural F1: {db['summary']['mean_natural_f1']}")


if __name__ == "__main__":
    main()
