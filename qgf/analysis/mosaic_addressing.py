"""Local-addressing simulation on a 20-atom triangular patch: a detuning is applied to one interior site and the occupation response is compared with the same detuning applied uniformly."""
from pathlib import Path
import sys
import json, sys, numpy as np, torch
dev = "cuda" if torch.cuda.is_available() else "cpu"
R, C = 4, 5
PATCHES = {
    "L-shape": dict(fig=[(0, 1), (1, 1), (2, 1), (2, 2), (2, 3)], hole=(3, 4)),
    "diamond": dict(fig=[(0, 2), (1, 1), (1, 2), (1, 3), (2, 2)], hole=(3, 0)),
    "bar":     dict(fig=[(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 2)], hole=(0, 4)),
    "blob":    dict(fig=[(1, 2), (1, 3), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4)], hole=(0, 0)),
    "top-edge":    dict(fig=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)], hole=(3, 2)),
    "left-edge":   dict(fig=[(0, 0), (1, 0), (2, 0), (3, 0), (2, 1)], hole=(1, 3)),
    "corner":      dict(fig=[(2, 3), (2, 4), (3, 2), (3, 3), (3, 4)], hole=(0, 1)),
    "edge-strip":  dict(fig=[(3, 0), (3, 1), (3, 2), (3, 3), (2, 0)], hole=(0, 3)),
}
def run(pos, det, Om=0.3, T=40.0, dt=0.025):
    N = len(pos); X = np.array(pos, float); D = np.linalg.norm(X[:, None] - X[None], axis=-1); np.fill_diagonal(D, np.inf); V = D ** -6.0
    idx = torch.arange(2 ** N, device=dev); bits = ((idx[:, None] >> (N - 1 - torch.arange(N, device=dev))) & 1).double()
    diag = (-(bits * torch.tensor(det, device=dev)).sum(1) + ((bits @ torch.tensor(np.triu(V, 1), device=dev)) * bits).sum(1)).to(torch.complex128)
    flips = [idx ^ (1 << (N - 1 - i)) for i in range(N)]
    def Hp(p):
        o = diag * p
        for f in flips: o = o + (Om / 2) * p[f]
        return o
    psi = torch.zeros(2 ** N, dtype=torch.complex128, device=dev); psi[0] = 1
    for _ in range(int(T / dt)):
        k1 = -1j * Hp(psi); k2 = -1j * Hp(psi + 0.5 * dt * k1); k3 = -1j * Hp(psi + 0.5 * dt * k2); k4 = -1j * Hp(psi + dt * k3); psi = psi + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    p = (psi.abs() ** 2).real; return (bits * p[:, None]).sum(0).cpu().numpy(), (V.sum(1))
out = {}
for name, P in PATCHES.items():
    cells = [(r, c) for r in range(R) for c in range(C) if (r, c) != P["hole"]]; pos = [(c, r) for r, c in cells]
    col = np.array([1.0 if k in P["fig"] else 0.0 for k in cells])
    outline = np.array([1.0 if (k in P["fig"] and any((k[0] + dr, k[1] + dc) in cells and (k[0] + dr, k[1] + dc) not in P["fig"] for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))) else 0.0 for k in cells])
    nG, F = run(pos, np.zeros(len(cells))); nL, _ = run(pos, 1.0 * col)
    cc = lambda a, b: float(np.corrcoef(a, b)[0, 1])
    def partial(n, F, col):                           # correlation of <n> with colour after removing what the static field explains
        A = np.c_[F, np.ones_like(F)]; res = n - A @ np.linalg.lstsq(A, n, rcond=None)[0]; return float(np.corrcoef(res, col)[0, 1])
    out[name] = dict(cells=cells, colour=col.tolist(), outline=outline.tolist(), n_global=nG.tolist(), n_local=nL.tolist(), field=F.tolist(),
                     corr=dict(global_vs_figure=cc(nG, col), local_vs_figure=cc(nL, col), global_vs_outline=cc(nG, outline), local_vs_outline=cc(nL, outline), field_vs_figure=cc(F, col), global_vs_figure_given_field=partial(nG, F, col), local_vs_figure_given_field=partial(nL, F, col)))
    print(name, {k: round(v, 2) for k, v in out[name]["corr"].items()}, flush=True)
out_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1] / 'data/mosaic/addressing.json')
json.dump(out, open(out_path, "w")); print('wrote', out_path)
