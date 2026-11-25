"""SYN-1 generator: matched unicyclic windows on a triangular slot grid, label = parity of the unique cycle (29 Oct 2026).

Design (PREREG_SYN1_CYCLE_PARITY_20261029.md): each window is one induced cycle of length L on the triangular lattice (pitch 1 =
nearest-neighbour distance) plus k pendant atoms, each attached to a distinct ring site and adjacent to nothing else, so the
occupied-slot graph is unicyclic: E = N, mean degree 2 exactly, degree set {1,2,3}. Even class L in {8,10,12}, odd class L in
{9,11,13}; target N drawn uniformly in [N_MIN, N_MAX] for BOTH classes, k = N - L, so N carries no label information.
Usage: python3 gen_cycles.py out.jsonl [n_per_class] [seed]
"""
import json, math, random, sys

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]          # axial neighbours, triangular lattice
EVEN_L, ODD_L = (8, 10, 12, 14), (9, 11, 13)
N_MIN, N_MAX, K_MAX = 10, 18, 4   # v3: N_MIN 10 (was 12) so small odd cycles are not rejected
# v2 (29 Oct 2026, after gate-1 v1 failed rule A): windows are built in MATCHED PAIRS. Each pair draws k once and an odd L, and the
# even partner takes L +/- 1 at random, so both classes share the k distribution exactly and the L means (11 vs 11) and N within 1.
# v1 (even {8,10,12} vs odd {9,11,13}, independent N) leaked the label through the pendant fraction (local AUROC 0.84).


def hexdist(a, b):
    dq, dr = a[0] - b[0], a[1] - b[1]
    return max(abs(dq), abs(dr), abs(dq + dr))


def adjacent(a, b):
    return (b[0] - a[0], b[1] - a[1]) in DIRS


def induced_cycle(L, rng, max_tries=20000):
    """Random self-avoiding closed lattice walk of length L with no chords (an induced cycle)."""
    for _ in range(max_tries):
        path = [(0, 0)]
        ok = True
        for s in range(1, L):
            cands = [(path[-1][0] + d[0], path[-1][1] + d[1]) for d in DIRS]
            rng.shuffle(cands)
            nxt = None
            for c in cands:
                if c in path:
                    continue
                if hexdist(c, (0, 0)) > L - s:          # must still be able to close
                    continue
                if s == L - 1 and not adjacent(c, (0, 0)):
                    continue
                # chord check against all earlier non-consecutive vertices
                if any(adjacent(c, p) for p in path[:-1] if not (s == L - 1 and p == (0, 0))):
                    continue
                nxt = c
                break
            if nxt is None:
                ok = False
                break
            path.append(nxt)
        if ok and adjacent(path[-1], (0, 0)) and len(path) == L:
            return path
    raise RuntimeError(f"no induced cycle of length {L}")


def add_pendants(ring, k, rng, max_tries=500):
    for _ in range(max_tries):
        occ = set(ring)
        pend, parents = [], []
        sites = rng.sample(range(len(ring)), k)
        good = True
        for i in sites:
            p = ring[i]
            cands = [(p[0] + d[0], p[1] + d[1]) for d in DIRS]
            rng.shuffle(cands)
            placed = False
            for c in cands:
                if c in occ:
                    continue
                if any(adjacent(c, o) for o in occ if o != p):
                    continue
                occ.add(c); pend.append(c); parents.append(i); placed = True
                break
            if not placed:
                good = False
                break
        if good:
            return pend, parents
    return None, None


def to_xy(p):
    return (p[0] + 0.5 * p[1], p[1] * math.sqrt(3) / 2)


def make_window(L, N, rng, wid):
    k = N - L
    assert 0 <= k <= max(K_MAX, 64)
    for _ in range(50):
        ring = induced_cycle(L, rng)
        pend, parents = add_pendants(ring, k, rng)
        if pend is not None:
            break
    else:
        raise RuntimeError(f"could not place {k} pendants on L={L}")
    axial = ring + pend
    xy = [to_xy(p) for p in axial]
    cx = sum(x for x, _ in xy) / len(xy); cy = sum(y for _, y in xy) / len(xy)
    coords = [[round(x - cx, 6), round(y - cy, 6)] for x, y in xy]
    edges = [[i, (i + 1) % L] for i in range(L)] + [[L + j, parents[j]] for j in range(k)]
    # sanity: every NN pair at distance 1 is an edge and vice versa (unicyclic, induced)
    nn = {tuple(sorted((i, j))) for i in range(N) for j in range(i + 1, N)
          if abs(math.dist(coords[i], coords[j]) - 1.0) < 1e-6}
    assert nn == {tuple(sorted(e)) for e in edges}, "graph is not the intended unicyclic graph"
    return dict(id=wid, N=N, L=L, k=k, parity=L % 2, label=int(L % 2 == 1), coords=coords, edges=edges,
                ring=list(range(L)), pendants=list(range(L, N)))


def main():
    out = sys.argv[1]; n_per = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20261029
    rng = random.Random(seed)
    rows = []
    wid = 0
    while len(rows) < 2 * n_per:
        L_odd = rng.choice(ODD_L)
        L_even = L_odd + (1 if (wid // 2) % 2 == 0 else -1)   # v3: direction balanced exactly, alternating per pair
        k = rng.randint(0, K_MAX)
        if not (N_MIN <= L_odd + k <= N_MAX and N_MIN <= L_even + k <= N_MAX):
            continue
        pair = wid // 2
        for L in (L_even, L_odd):
            w = make_window(L, L + k, rng, wid); w["pair"] = pair; rows.append(w); wid += 1
    with open(out, "w") as fp:
        for r in rows:
            fp.write(json.dumps(r) + "\n")
    import collections
    byN = collections.Counter((r["label"], r["N"]) for r in rows)
    print(f"{len(rows)} windows -> {out}")
    for lab in (0, 1):
        print(" label", lab, {n: byN[(lab, n)] for n in range(N_MIN, N_MAX + 1)})


if __name__ == "__main__":
    main()
