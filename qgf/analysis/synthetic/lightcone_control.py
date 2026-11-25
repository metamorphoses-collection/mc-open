"""SYN-1 light-cone-truncated control (amendment 3, rule E). For every window and every truncation radius r, each site i is
simulated EXACTLY inside its own cluster = {j : graph distance d(i,j) <= r}, with all r^-6 couplings inside the cluster and nothing
outside. Site features: <n_i> from cluster(i); C_ij for d(i,j) <= r as the mean of the readings in cluster(i) and cluster(j); C_ij is
undefined (NaN) beyond r. Same integrator, working point and readouts as exact_quench.py. If features built from these truncated
readings separate the classes as well as the full-window quench, the information is local and no many-body reading survives.
Usage: python3 lightcone_control.py windows.jsonl out.jsonl r1,r2,... [--centres M] [--procs P]
  --centres M : simulate only M randomly chosen centre sites per window (gate 2, where every site is too costly); seed = window id."""
import json, sys, time, argparse, random, numpy as np, networkx as nx
from multiprocessing import Pool
from exact_quench import evolve, JT_SAVE, OMEGA, DELTA


def clusters(w, r, centres):
    G = nx.Graph(); G.add_nodes_from(range(w["N"])); G.add_edges_from([tuple(e) for e in w["edges"]])
    return {i: sorted(nx.single_source_shortest_path_length(G, i, cutoff=r)) for i in centres}


def one(args):
    w, r, centres, dt = args
    N = w["N"]; X = np.array(w["coords"], float); t0 = time.time()
    cl = clusters(w, r, centres)
    n = np.full((len(JT_SAVE), N), np.nan); C = np.full((len(JT_SAVE), N, N), np.nan); cnt = np.zeros((N, N))
    cache = {}
    for i, sites in cl.items():
        key = tuple(sites)
        if key not in cache:
            cache[key] = evolve(X[sites], dt=dt)
        res = cache[key]; pos = sites.index(i)
        for t, rd in enumerate(res):
            n[t, i] = rd["n"][pos]
            Cc = np.array(rd["C"])
            for a, j in enumerate(sites):
                v = Cc[pos, a]
                if np.isnan(C[t, i, j]): C[t, i, j] = 0.0
                C[t, i, j] += v
        for j in sites: cnt[i, j] += 1
    # symmetrise: mean of the two readings where both centres were simulated
    Cs = np.full_like(C, np.nan)
    for t in range(len(JT_SAVE)):
        A = np.nan_to_num(C[t]); M = cnt + cnt.T
        with np.errstate(invalid="ignore", divide="ignore"):
            Cs[t] = np.where(M > 0, (A + A.T) / np.maximum(M, 1), np.nan)
    worst = max(abs(rd["norm"] - 1) for res in cache.values() for rd in res)
    size = max(len(s) for s in cl.values())
    return dict(id=w["id"], N=N, L=w["L"], label=w["label"], r=r, centres=sorted(centres), max_cluster=size, n_clusters=len(cache),
                dt=dt, omega=OMEGA, delta=DELTA, norm_err=worst, seconds=time.time() - t0,
                readouts=[dict(Jt=JT_SAVE[t], n=n[t].tolist(), C=Cs[t].tolist()) for t in range(len(JT_SAVE))])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst"); ap.add_argument("radii")
    ap.add_argument("--centres", type=int, default=0); ap.add_argument("--procs", type=int, default=12); ap.add_argument("--dt", type=float, default=0.05)
    a = ap.parse_args(); radii = [int(x) for x in a.radii.split(",")]
    done = set()
    try:
        for l in open(a.dst): d = json.loads(l); done.add((d["id"], d["r"]))
    except FileNotFoundError: pass
    rows = [json.loads(l) for l in open(a.src)]; jobs = []
    for w in rows:
        centres = list(range(w["N"])) if a.centres <= 0 else sorted(random.Random(w["id"]).sample(range(w["N"]), min(a.centres, w["N"])))
        for r in radii:
            if (w["id"], r) not in done: jobs.append((w, r, centres, a.dt))
    print(f"{len(jobs)} jobs on {a.procs} procs", flush=True)
    with Pool(a.procs) as pool, open(a.dst, "a") as fp:
        for res in pool.imap_unordered(one, jobs):
            fp.write(json.dumps(res) + "\n"); fp.flush()
            print(f"id {res['id']:3d} r {res['r']} N {res['N']} max_cluster {res['max_cluster']:2d} clusters {res['n_clusters']:2d} "
                  f"norm_err {res['norm_err']:.1e} {res['seconds']:.0f}s", flush=True)


if __name__ == "__main__":
    main()
