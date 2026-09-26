#!/usr/bin/env python3
"""
Build topic graphs for Montaigne, Dante, Manetti at k=8 and k=16,
take top-65 by degree, SA-embed, and submit to EMU_MPS.
"""

import json, math, os, re, sys, time
import numpy as np
import networkx as nx
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, PULP_CBC_CMD, value

BASE = Path(__file__).resolve().parent
REF_TEXTS = BASE / "classical" / "reference_texts"
GRAPHS_DIR = BASE / "classical" / "graphs"
BATCHES_DIR = BASE / "quantum" / "batches"

SIM_THRESHOLD = 0.78
MIN_CHUNK_CHARS = 40
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# FRESNEL physics
C6_FRESNEL = 865723
BLOCKADE_UM = 8.0
OMEGA_MAX = C6_FRESNEL / (BLOCKADE_UM ** 6)  # 3.303 rad/µs
DELTA_0 = -3 * OMEGA_MAX
DELTA_F = +3 * OMEGA_MAX
T_NS = 4000
SHOTS = 1000

PASQAL_PROJECT_ID = "9311685e-cc0c-43b2-8db6-6e11d352878a"

TEXTS = {
    "montaigne": {
        "file": REF_TEXTS / "montaigne_essais_gutenberg.txt",
        "title": "Montaigne Essais",
        "lang": "FR",
    },
    "dante": {
        "file": REF_TEXTS / "dante_inferno_gutenberg.txt",
        "title": "Dante Commedia (Inferno)",
        "lang": "IT",
    },
    "manetti": {
        "file": REF_TEXTS / "manetti_dialogo_archive.txt",
        "title": "Manetti Dialogo",
        "lang": "IT",
    },
}


def log(msg):
    print(msg, flush=True)


# === TEXT CHUNKING ===

def chunk_text(filepath, target_words=300):
    """Split text into ~300-word paragraphs."""
    raw = filepath.read_text(encoding="utf-8", errors="replace")

    # Split on double newlines first
    paragraphs = re.split(r"\n\s*\n", raw)

    # Merge short paragraphs, split long ones
    chunks = []
    current = []
    current_words = 0

    for para in paragraphs:
        para = para.strip()
        if not para or len(para) < MIN_CHUNK_CHARS:
            continue
        # Skip pure-numeric lines (page numbers)
        para = re.sub(r"^\s*\d+\s*$", "", para, flags=re.MULTILINE).strip()
        if len(para) < MIN_CHUNK_CHARS:
            continue

        words = para.split()
        if current_words + len(words) > target_words * 1.5 and current:
            chunks.append(" ".join(current))
            current = words
            current_words = len(words)
        else:
            current.extend(words)
            current_words += len(words)

        if current_words >= target_words:
            chunks.append(" ".join(current))
            current = []
            current_words = 0

    if current and current_words >= MIN_CHUNK_CHARS // 5:
        chunks.append(" ".join(current))

    return chunks


# === EMBEDDING + GRAPH BUILDING ===

def embed_texts(chunks, model):
    """Embed chunks with sentence-transformer."""
    texts = [c for c in chunks]
    embs = model.encode(texts, batch_size=32, show_progress_bar=True,
                        normalize_embeddings=True)
    return embs


def build_knn_graph(chunks, embs, top_k):
    """Build symmetric k-NN graph with sim >= threshold."""
    sim = cosine_similarity(embs)
    np.fill_diagonal(sim, 0)
    N = len(chunks)

    G = nx.Graph()
    for i in range(N):
        G.add_node(f"p{i}")

    for i in range(N):
        top_idx = np.argsort(-sim[i])[:top_k]
        for j in top_idx:
            if sim[i, j] >= SIM_THRESHOLD:
                # Symmetric: add edge if either direction qualifies
                G.add_edge(f"p{i}", f"p{j}", weight=float(sim[i, j]))

    # Remove isolated nodes
    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)

    return G


def top_k_subgraph(G, k):
    """Take top-k nodes by degree."""
    if G.number_of_nodes() <= k:
        return G.copy()
    top = sorted(G.nodes, key=lambda n: -G.degree(n))[:k]
    return G.subgraph(top).copy()


def mis_ilp(G):
    """Solve MIS via ILP."""
    prob = LpProblem("MIS", LpMaximize)
    x = {n: LpVariable(f"x_{n}", cat=LpBinary) for n in G.nodes}
    prob += sum(x.values())
    for u, v in G.edges():
        prob += x[u] + x[v] <= 1
    prob.solve(PULP_CBC_CMD(msg=0, timeLimit=30))
    return sum(1 for n in G.nodes if value(x[n]) > 0.5)


# === SA EMBEDDING ===

def embed_sa(G, blockade_um=BLOCKADE_UM, spacing=5.5, seed_base=42):
    """SA embedding with FRESNEL constraints."""
    import random as rmod

    nodes = list(G.nodes)
    N = len(nodes)
    node_idx = {n: i for i, n in enumerate(nodes)}

    # Adaptive parameters
    if N > 60:
        n_iter, n_restarts = 16000, 10
    elif N > 30:
        n_iter, n_restarts = 12000, 8
    else:
        n_iter, n_restarts = 8000, 6

    MAX_RADIUS = 46.0
    MIN_DIST = 5.0
    sites = []
    rows = int(2 * MAX_RADIUS / (spacing * math.sqrt(3) / 2)) + 2
    cols = int(2 * MAX_RADIUS / spacing) + 2
    for row in range(-rows, rows + 1):
        for col in range(-cols, cols + 1):
            x = col * spacing + (row % 2) * spacing / 2
            y = row * spacing * math.sqrt(3) / 2
            if math.hypot(x, y) <= MAX_RADIUS:
                sites.append((x, y))
    sites.sort(key=lambda p: math.hypot(*p))

    if len(sites) < N:
        raise ValueError(f"Only {len(sites)} lattice sites for {N} atoms")

    adj_target = np.zeros((N, N), dtype=int)
    for u, v in G.edges():
        i, j = node_idx[u], node_idx[v]
        adj_target[i][j] = 1
        adj_target[j][i] = 1

    def violations(assign):
        v = 0
        for i in range(N):
            for j in range(i + 1, N):
                d = math.hypot(sites[assign[i]][0] - sites[assign[j]][0],
                               sites[assign[i]][1] - sites[assign[j]][1])
                within = d <= blockade_um
                edge = adj_target[i][j]
                if within != edge:
                    v += 1
        return v

    best_assign = None
    best_viol = float('inf')

    for restart in range(n_restarts):
        rng = rmod.Random(seed_base + restart)
        pos = nx.spring_layout(G, seed=seed_base + restart)
        scale = MAX_RADIUS * 0.7
        scaled = {n: (pos[n][0] * scale, pos[n][1] * scale) for n in nodes}

        used = set()
        assign = [0] * N
        for i, n in enumerate(nodes):
            best_s = min((s for s in range(len(sites)) if s not in used),
                         key=lambda s: math.hypot(sites[s][0] - scaled[n][0],
                                                  sites[s][1] - scaled[n][1]))
            assign[i] = best_s
            used.add(best_s)

        cur_v = violations(assign)
        best_local = assign[:]
        best_local_v = cur_v

        T0, T1 = 4.0, 0.02
        for step in range(n_iter):
            T = T0 * (T1 / T0) ** (step / n_iter)

            if rng.random() < 0.5:
                atom = rng.randint(0, N - 1)
                free = [s for s in range(min(len(sites), N * 3)) if s not in set(assign)]
                if not free:
                    continue
                new_site = rng.choice(free)
                old_site = assign[atom]
                assign[atom] = new_site
                new_v = violations(assign)
                delta = new_v - cur_v
                if delta < 0 or rng.random() < math.exp(-delta / max(T, 1e-10)):
                    cur_v = new_v
                    if cur_v < best_local_v:
                        best_local_v = cur_v
                        best_local = assign[:]
                else:
                    assign[atom] = old_site
            else:
                a, b = rng.sample(range(N), 2)
                assign[a], assign[b] = assign[b], assign[a]
                new_v = violations(assign)
                delta = new_v - cur_v
                if delta < 0 or rng.random() < math.exp(-delta / max(T, 1e-10)):
                    cur_v = new_v
                    if cur_v < best_local_v:
                        best_local_v = cur_v
                        best_local = assign[:]
                else:
                    assign[a], assign[b] = assign[b], assign[a]

        if best_local_v < best_viol:
            best_viol = best_local_v
            best_assign = best_local[:]

        log(f"    SA restart {restart+1}/{n_restarts}: violations={best_local_v}")

    coords = {}
    for i, n in enumerate(nodes):
        coords[n] = sites[best_assign[i]]

    positions = list(coords.values())
    min_dist = min(math.hypot(positions[i][0] - positions[j][0],
                              positions[i][1] - positions[j][1])
                   for i in range(N) for j in range(i + 1, N))
    max_r = max(math.hypot(*p) for p in positions)

    return coords, best_viol, min_dist, max_r


def embedding_quality(G, coords, blockade_um=BLOCKADE_UM):
    nodes = list(G.nodes)
    correct = false_edges = false_gaps = 0
    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            d = math.hypot(coords[u][0] - coords[v][0], coords[u][1] - coords[v][1])
            within = d <= blockade_um
            has_edge = G.has_edge(u, v)
            if within == has_edge:
                correct += 1
            elif within and not has_edge:
                false_edges += 1
            else:
                false_gaps += 1
    total = correct + false_edges + false_gaps
    fidelity = correct / total if total > 0 else 0
    return fidelity, false_edges, false_gaps


# === SEQUENCE + EMU ===

def build_emu_sequence(coords_dict):
    """Build adiabatic pulse for EMU_MPS."""
    from pulser import Register, Pulse, Sequence
    from pulser.waveforms import InterpolatedWaveform
    from pulser.devices import DigitalAnalogDevice

    qubits = {f"q{i}": (x, y) for i, (_, (x, y)) in enumerate(
        sorted(coords_dict.items()))}
    reg = Register(qubits)

    seq = Sequence(reg, DigitalAnalogDevice)
    seq.declare_channel("ising", "rydberg_global")

    sweep = Pulse(
        InterpolatedWaveform(T_NS, [1e-9, OMEGA_MAX, 1e-9]),
        InterpolatedWaveform(T_NS, [DELTA_0, 0, DELTA_F]),
        0,
    )
    seq.add(sweep, "ising")
    return seq


def save_graph_json(G, name, title, top_k, out_path):
    """Save graph in standard format."""
    nodes = sorted(G.nodes())
    edges = [[u, v] for u, v in G.edges()]
    N = G.number_of_nodes()
    E = G.number_of_edges()
    d = nx.density(G)

    data = {
        "book_id": f"{name}_top{N}_k{top_k}",
        "title": title,
        "N": N,
        "E": E,
        "density": round(d, 4),
        "top_k": top_k,
        "nodes": nodes,
        "edges": edges,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    log(f"  Saved {out_path.name}")
    return data


# === MAIN ===

def main():
    log("=" * 70)
    log("EXTRA TEXTS — Topic Graph + SA Embed + EMU Submit")
    log("=" * 70)

    # Load model once
    log(f"\nLoading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    all_results = {}  # name -> {graph, coords, metrics}
    all_graphs = {}   # name -> graph_data

    for text_name, info in TEXTS.items():
        log(f"\n{'='*60}")
        log(f"TEXT: {info['title']} ({text_name})")
        log(f"{'='*60}")

        # 1. Chunk
        chunks = chunk_text(info["file"])
        log(f"  Chunked into {len(chunks)} paragraphs (~300 words each)")

        # 2. Embed
        log(f"  Embedding {len(chunks)} chunks...")
        embs = embed_texts(chunks, model)

        for top_k in [8, 16]:
            log(f"\n  --- k={top_k} ---")

            # 3. Build k-NN graph
            G_full = build_knn_graph(chunks, embs, top_k)
            N_full = G_full.number_of_nodes()
            E_full = G_full.number_of_edges()
            log(f"  Full graph: N={N_full}, E={E_full}")

            # 4. Top-65
            if N_full > 65:
                G65 = top_k_subgraph(G_full, 65)
                log(f"  Top-65 subgraph: N={G65.number_of_nodes()}, E={G65.number_of_edges()}")
            else:
                G65 = G_full.copy()
                log(f"  N={N_full} <= 65, using full graph")

            N = G65.number_of_nodes()
            E = G65.number_of_edges()
            d = nx.density(G65)
            mis = mis_ilp(G65)
            log(f"  N={N}, E={E}, density={d:.4f}, MIS={mis}")

            # 5. Save graph JSON
            graph_dir = GRAPHS_DIR / text_name
            out_path = graph_dir / f"graph_{text_name}_{N}_k{top_k}.json"
            gdata = save_graph_json(G65, text_name, info["title"], top_k, out_path)

            # 6. SA embed
            log(f"  SA embedding (R_b={BLOCKADE_UM}um)...")
            coords, viol, min_dist, max_r = embed_sa(G65)
            fidelity, false_edges, false_gaps = embedding_quality(G65, coords)
            log(f"  SA: fidelity={fidelity:.4f}, violations={viol}, "
                f"false_edges={false_edges}, false_gaps={false_gaps}")
            log(f"  FRESNEL: min_dist={min_dist:.2f}um, max_r={max_r:.2f}um")

            key = f"{text_name}_k{top_k}"
            all_results[key] = {
                'G': G65,
                'coords': coords,
                'N': N, 'E': E, 'density': round(d, 4),
                'mis_ilp': mis,
                'fidelity': round(fidelity, 4),
                'false_edges': false_edges,
                'false_gaps': false_gaps,
                'min_dist': round(min_dist, 2),
                'max_r': round(max_r, 2),
                'desc': f"{info['title']} top-{N} k={top_k}",
                'zone': "HARD" if 0.3 <= d <= 0.7 else "easy",
            }
            all_graphs[key] = gdata

    # === SUMMARY ===
    log(f"\n{'='*70}")
    log("SUMMARY")
    log(f"{'='*70}")
    log(f"{'Name':<25} {'N':>3} {'E':>4} {'d':>7} {'Zone':<5} {'MIS':>3} {'Fid':>6} {'FE':>3} {'FG':>3}")
    log("-" * 65)
    for key, r in all_results.items():
        log(f"{key:<25} {r['N']:>3} {r['E']:>4} {r['density']:>7.4f} "
            f"{r['zone']:<5} {r['mis_ilp']:>3} {r['fidelity']:>6.4f} "
            f"{r['false_edges']:>3} {r['false_gaps']:>3}")

    # === EMU SUBMISSION ===
    log(f"\n{'='*70}")
    log("EMU_MPS SUBMISSION")
    log(f"{'='*70}")

    from pasqal_cloud import SDK

    sdk = SDK(
        project_id=PASQAL_PROJECT_ID,
        username=os.environ['PASQAL_USER'],
        password='zomfeg-0hoDby-ruhzij',
    )

    batches = {}
    for key, r in all_results.items():
        log(f"\n  Submitting {key}...")
        try:
            seq = build_emu_sequence(r['coords'])
            serialized = seq.to_abstract_repr()

            batch = sdk.create_batch(
                serialized_sequence=serialized,
                jobs=[{"runs": SHOTS}],
                emulator="EMU_MPS",
            )
            bid = batch.id
            log(f"  -> Batch {bid}")

            batches[key] = {
                'batch_id': bid,
                'N': r['N'], 'E': r['E'], 'density': r['density'],
                'mis_ilp': r['mis_ilp'], 'fidelity': r['fidelity'],
                'zone': r['zone'], 'shots': SHOTS,
                'desc': r['desc'],
                'omega_max': round(OMEGA_MAX, 4),
                'blockade_um': BLOCKADE_UM,
                'false_edges': r['false_edges'],
                'false_gaps': r['false_gaps'],
            }
        except Exception as e:
            log(f"  ERROR: {e}")
            import traceback; traceback.print_exc()
            batches[key] = {'error': str(e)}

    # Save batches
    BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    batches_file = BATCHES_DIR / "emu_extra_texts_batches.json"
    with open(batches_file, 'w') as f:
        json.dump(batches, f, indent=2)
    log(f"\nSaved batch metadata to {batches_file}")

    # Final report
    log(f"\n{'='*70}")
    log("FINAL REPORT")
    log(f"{'='*70}")
    for key, b in batches.items():
        if 'error' in b:
            log(f"  {key}: ERROR - {b['error']}")
        else:
            log(f"  {key}: batch={b['batch_id']}, N={b['N']}, d={b['density']}, MIS={b['mis_ilp']}, fid={b['fidelity']}")


if __name__ == '__main__':
    main()
