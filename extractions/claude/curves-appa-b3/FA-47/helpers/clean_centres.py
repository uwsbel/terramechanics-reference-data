"""Clean centres of a plotted line: in each column, the dark run through the line's predicted centre
(v = a + b (u - uref)) when it is a lone stroke (thickness 5 to 11 px) that touches no grid pixel
(runs >= 45 horizontal or >= 30 vertical, dilated 1) and no other dark run within 2 px; its
midpoint is the line's centre there. Prints the residual (centre minus prediction) per bin of
`bin` px, then a straight-line refit through all clean centres, and writes them to <out.csv>.
Usage: clean_centres.py <image> uref a b ua ub bin out.csv"""
import sys
import numpy as np
from PIL import Image

img = sys.argv[1]
uref, a, b, ua, ub, binw = map(float, sys.argv[2:8])
outp = sys.argv[8]
G = np.asarray(Image.open(img).convert("L")) < 128
vlo = int(min(a + b * (ua - uref), a + b * (ub - uref))) - 60
vhi = int(max(a + b * (ua - uref), a + b * (ub - uref))) + 60
ulo, uhi = int(ua) - 60, int(ub) + 60
sub = G[vlo:vhi, ulo:uhi]


def long_runs(mask, L):
    out = np.zeros_like(mask)
    for i in range(mask.shape[0]):
        d = np.diff(np.concatenate([[0], mask[i].astype(int), [0]]))
        for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0]):
            if e - s >= L:
                out[i, s:e] = True
    return out


gr = long_runs(sub, 45) | long_runs(sub.T, 30).T
gm = gr.copy()
gm[1:, :] |= gr[:-1, :]; gm[:-1, :] |= gr[1:, :]; gm[:, 1:] |= gr[:, :-1]; gm[:, :-1] |= gr[:, 1:]
GM = np.zeros_like(G); GM[vlo:vhi, ulo:uhi] = gm
rows = []
for u in range(int(ua), int(ub) + 1):
    p = a + b * (u - uref)
    c = int(round(p))
    # nearest dark pixel within 3 px of the prediction
    cand = [c + d for d in (0, 1, -1, 2, -2, 3, -3) if G[c + d, u]]
    if not cand:
        continue
    lo = hi = cand[0]
    while G[lo - 1, u]:
        lo -= 1
    while G[hi + 1, u]:
        hi += 1
    t = hi - lo + 1
    if not 5 <= t <= 11:
        continue
    if GM[lo - 1:hi + 2, u].any():
        continue
    if G[lo - 3:lo - 1, u].any() or G[hi + 2:hi + 4, u].any():
        continue
    rows.append((u, (lo + hi) / 2, t, (lo + hi) / 2 - p))
R = np.array(rows)
with open(outp, "w", encoding="utf-8") as f:
    f.write("u,centre_v,thickness,resid\n")
    for r in rows:
        f.write(f"{r[0]},{r[1]:.1f},{r[2]},{r[3]:.2f}\n")
print(f"{len(R)} clean columns; thickness median {np.median(R[:, 2]):.1f}; residual mean {R[:, 3].mean():.2f} rms {np.sqrt((R[:, 3]**2).mean()):.2f}")
edges = np.arange(ua, ub + binw, binw)
for e0, e1 in zip(edges, edges[1:]):
    s = (R[:, 0] >= e0) & (R[:, 0] < e1)
    if s.sum():
        print(f"  u {e0:6.0f}-{e1:6.0f}: n {s.sum():3d}  resid median {np.median(R[s, 3]):+.2f}  thick {np.median(R[s, 2]):.1f}")
bb, aa = np.polyfit(R[:, 0] - uref, R[:, 1], 1)
res = R[:, 1] - (aa + bb * (R[:, 0] - uref))
print(f"refit: a {aa:.2f} b {bb:.5f}  rms {np.sqrt((res**2).mean()):.2f}, max {np.abs(res).max():.2f}")
