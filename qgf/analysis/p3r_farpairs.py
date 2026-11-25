# PREFLIGHT-EXEMPT: reads saved result files only; builds nothing, submits nothing.
"""Control for the residual across-cut S in split blocks: a global shot-to-shot fluctuation (drive or detuning) correlates every pair, near or
far, while the r^-6 tail falls as the sixth power of distance. S (noise-subtracted mean C^2) over across-cut pairs at Manhattan slot distance
2-3 (the test's pairs) against 4-6 (far pairs), pooled 3000 shots, per split block and per whole block. Writes p3r_farpairs.json."""
import json, numpy as np, p3_analysis as P, p3r_analysis as R
def S_over(res, reg, dmin, dmax):
    S = np.array([[q["slot"], q["line"]] for q in reg["nodes"]], float); side = np.array(reg["side"]); A = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            d = abs(S[i, 0] - S[j, 0]) + abs(S[i, 1] - S[j, 1])
            if dmin <= d <= dmax and side[i] >= 0 and side[j] >= 0 and side[i] != side[j]: A.append((i, j))
    A = np.array(A); B, c = R.to_Bc(res); n = c.sum(); s0, _ = P.S_stat(c[None, :], B, A, n); lo, hi = P.null_interval(B, c, A, n, draws=400)
    return float(s0[0]), len(A), float(lo), float(hi)
out = []
for k in R.K:
    r = P.rows[k]; reg = P.regs[r["register"]]; res = R.pool(R.pool(R.R1[k], R.R2[k]), R.R3[k])
    near = S_over(res, reg, 2, 3); far = S_over(res, reg, 4, 6)
    out.append(dict(pair=reg["pair"] + 1, role=reg["role"], S_near=near[0], n_near=near[1], null_near=[near[2], near[3]], S_far=far[0], n_far=far[1], null_far=[far[2], far[3]]))
    print(f"pair {reg['pair']+1:2d} {reg['role']:5s} near {near[0]:+.2e} ({near[1]:3d} pairs, null hi {near[3]:+.1e}) | far {far[0]:+.2e} ({far[1]:3d} pairs, null hi {far[3]:+.1e})")
sp = [x for x in out if x["role"] == "split"]; wh = [x for x in out if x["role"] == "whole"]
summ = dict(split_median_near=float(np.median([x["S_near"] for x in sp])), split_median_far=float(np.median([x["S_far"] for x in sp])),
            split_far_inside_null=sum(x["null_far"][0] <= x["S_far"] <= x["null_far"][1] for x in sp), whole_median_near=float(np.median([x["S_near"] for x in wh])), whole_median_far=float(np.median([x["S_far"] for x in wh])))
print(summ); json.dump(dict(summary=summ, blocks=out), open("p3r_farpairs.json", "w"), indent=1)
