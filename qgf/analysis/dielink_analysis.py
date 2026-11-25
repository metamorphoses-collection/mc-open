from pathlib import Path
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DIE = ROOT / 'data/die'
# PREFLIGHT-EXEMPT: read-only scoring of a saved Ruby result file against the die-link register; builds and submits nothing.
"""PREREG_DIELINK_A (31 Oct 2026). Usage: python3 dielink_analysis.py results_ruby_dielink/ruby_diag_job_328.json [more files]
Scores each shot as an independent set of the die graph (which IS the register graph): valid fraction, approximation ratio (mean valid
set size / 33), raw P(opt), optimum fraction after the standard completion (drop highest-conflict atom until valid, then greedy
extend by ascending degree), distinct optima, and the per-combination membership frequency across optimal shots. Compares with the
emulated prediction (Ruby noise: ratio 0.846, repaired-opt 0.910; noiseless: 0.9998, 1.000)."""
import json, sys, os, collections, numpy as np
R = json.load(open(str(DIE / "qgf_dielink_a.json")))
A = np.array(R["adj"]); N = len(A); OPT = 33; deg = A.sum(1)
def valid(x): return not np.any(np.outer(x, x) * A)
def repair(x):
    x = x.copy()
    while not valid(x):
        conf = (A @ x) * x; x[int(np.argmax(conf))] = 0
    for i in np.argsort(deg):
        if x[i] == 0 and not np.any(A[i] * x): x[i] = 1
    return x
rows = []; pooled = collections.Counter()
for f in sys.argv[1:]:
    d = json.load(open(f)); order = d["qubit_order"]; idx = [int(q[1:]) for q in order]
    cnt = d["results"] if isinstance(d["results"], dict) else collections.Counter(d["results"])
    tot = sum(cnt.values())
    for b, c in cnt.items():
        x = np.zeros(N, int); x[idx] = [int(ch) for ch in b]; pooled[tuple(x)] += c
    rows.append((d["job_idx"], d.get("batch_id"), tot))
tot = sum(pooled.values()); vals = []; sizes = []; nopt = 0; nrep = 0; optima = collections.Counter(); member = np.zeros(N)
for x, c in pooled.items():
    x = np.array(x); v = valid(x); vals.append(c if v else 0)
    if v:
        sizes.append((x.sum(), c))
        if x.sum() == OPT: nopt += c; optima[tuple(x)] += c; member += c * x
    y = repair(x); nrep += c * (y.sum() == OPT)
valid_frac = sum(vals) / tot; ratio = sum(s * c for s, c in sizes) / max(1, sum(c for _, c in sizes)) / OPT
res = dict(rows=rows, shots=tot, valid=round(valid_frac, 4), ratio=round(ratio, 4), p_opt_raw=round(nopt / tot, 4), repaired_opt=round(nrep / tot, 4),
           distinct_optima=len(optima), excited_per_shot=round(float(sum(np.array(x).sum() * c for x, c in pooled.items())) / tot, 2),
           membership_freq={R["labels"][i]: round(float(member[i] / nopt), 3) for i in range(N)} if nopt else None,
           emulated=dict(ruby_noise=dict(ratio=0.846, repaired_opt=0.910, valid=0.021), noiseless=dict(ratio=0.9998, repaired_opt=1.0, p_opt_raw=0.905)))
res["verdict"] = ("PREDICTION REPRODUCED" if abs(ratio - 0.846) <= 0.05 and nrep / tot >= 0.80 else "PREDICTION NOT REPRODUCED")
print(json.dumps(res, indent=1)); json.dump(res, open(str(DIE / "dielink_result.json"), "w"), indent=1)
