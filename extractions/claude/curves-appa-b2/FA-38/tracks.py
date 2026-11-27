"""Reader helper: non-grid ink runs along every page row near the curves, to see the three curves' tracks.
Grid rows and columns are those dark over more than `thr` of a wide deskewed window outside the table.
Writes tracks.csv (v, u_start, u_end, centre, width, grid_row) and tracks.png (centre - c(v) against v)."""
import sys, csv
import numpy as np
from PIL import Image
img = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
g = np.asarray(Image.open(img).convert("L")) < 128
SH, SV = -0.0045, 0.0064
TABLE = (1335, 1252, 1940, 2742)
KV = [1250, 1300, 1340, 1420, 1500, 1580, 1660, 1740, 1820, 1900, 1980, 2100, 2220, 2340, 2460, 2580, 2700, 2780, 2860, 2940, 3020, 3100, 3180, 3240]
KU = [670, 690, 706, 724, 770, 822, 875, 912, 955, 995, 1022, 1050, 1080, 1110, 1145, 1178, 1213, 1246, 1274, 1308, 1345, 1383, 1420, 1450]
def c(v): return float(np.interp(v, KV, KU))
def in_table(u, v): return (TABLE[0] <= u) & (u <= TABLE[2]) & (TABLE[1] <= v) & (v <= TABLE[3])
V0, V1 = 1180, 3230
rowfrac = {}
for v in range(V0, V1):
    cc = c(v)
    us = np.concatenate([np.arange(max(700, int(cc) - 300), int(cc) - 70), np.arange(int(cc) + 70, min(2140, int(cc) + 300))])
    vv = np.round(v + SH * (us - cc)).astype(int)
    ok = ~in_table(us, vv)
    rowfrac[v] = g[vv[ok], us[ok]].mean() if ok.sum() > 50 else 0.0
colfrac = {}
def colf(u, v):
    key = (u, v // 50)
    if key not in colfrac:
        vs = np.arange(v - 300, v + 300)
        vs = vs[(vs > 1130) & (vs < 3740)]
        uu = np.round(u + SV * (vs - v)).astype(int)
        ok = ~in_table(uu, vs)
        colfrac[key] = g[vs[ok], uu[ok]].mean() if ok.sum() > 50 else 0.0
    return colfrac[key]
rows = []
for v in range(V0, V1):
    cc = int(c(v)); a, b = max(cc - 70, 698), cc + 70
    gridrow = any(rowfrac.get(v + d, 0) > thr for d in (-1, 0, 1))
    line = g[v, a:b].copy()
    for i in range(len(line)):
        u = a + i
        if any(colf(u + d, v) > thr for d in (-1, 0, 1)):
            line[i] = False
    s = None
    for i, dk in enumerate(list(line) + [False]):
        if dk and s is None: s = i
        if not dk and s is not None:
            rows.append((v, a + s, a + i - 1, (2 * a + s + i - 1) / 2, i - s, int(gridrow))); s = None
with open("tracks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["v", "u_start", "u_end", "centre", "width", "grid_row"]); w.writerows(rows)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = np.array(rows, float)
fig, axs = plt.subplots(1, 8, figsize=(32, 18))
segs = [(1250 + 250 * k, 1500 + 250 * k) for k in range(8)]
for ax, (lo, hi) in zip(axs, segs):
    m = (R[:, 0] >= lo) & (R[:, 0] < hi) & (R[:, 5] == 0)
    ax.scatter(R[m, 3] - np.array([c(v) for v in R[m, 0]]), R[m, 0], s=np.clip(R[m, 4], 1, 30), c="k")
    ax.set_ylim(hi, lo); ax.set_xlim(-72, 72); ax.grid(True, alpha=0.4); ax.set_yticks(range(lo, hi + 1, 10)); ax.tick_params(labelsize=6)
    ax.set_xlabel("u - c(v)")
fig.tight_layout(); fig.savefig("tracks.png", dpi=60)
print(len(rows), "runs")
