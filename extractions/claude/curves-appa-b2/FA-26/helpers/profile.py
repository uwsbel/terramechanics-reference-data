"""Band profile across the three curves, column by column (cols) or row by row (rows), on the page ink with
the printed grid greyed out (clean2.py). For each line: the band's two edges, its height, the white gaps
inside it, and a flag where an edge lies on a grid line (the edge is then uncertain by that line's width).
Writes profile_<mode>.csv; prints a compact table.
usage: profile.py cols u0 u1 | profile.py rows v0 v1"""
import csv, json, sys
from pathlib import Path
import numpy as np
from PIL import Image
base = Path(__file__).resolve().parents[1]
g = np.array(Image.open(base.parents[1] / "packet" / "p0054.png").convert("L")) < 128
U0, V0 = 520, 2050
gm = np.load(base / "helpers" / "gridmask.npy")
grid = np.zeros_like(g); grid[V0:V0 + gm.shape[0], U0:U0 + gm.shape[1]] = gm
curve = g & ~grid
gb = json.loads((base / "helpers" / "gridbands.json").read_text())
GUIDE = np.array([(552, 2236), (575, 2262), (600, 2320), (650, 2370), (700, 2395), (800, 2425), (900, 2445), (1000, 2460),
                  (1100, 2475), (1200, 2490), (1300, 2502), (1400, 2520), (1500, 2545), (1600, 2565),
                  (1700, 2598), (1800, 2640), (1850, 2672), (1900, 2705), (1950, 2765), (1990, 2830),
                  (2010, 2890), (2025, 2960), (2026, 2985)], float)
def runs(line, off):
    idx = np.where(line)[0]; out = []
    if len(idx):
        s = p = idx[0]
        for i in list(idx[1:]) + [None]:
            if i is None or i != p + 1:
                out.append((int(s + off), int(p + off))); s = i
            p = i if i is not None else p
    return out
def in_band(x, bl):
    return next((f"{a}-{b}" for a, b in bl if a - 1 <= x <= b + 1), "")
mode, a0, a1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
W = 45
skip = gb["cols"] if mode == "cols" else gb["rows"]
across = gb["rows"] if mode == "cols" else gb["cols"]
out = []
for a in range(a0, a1 + 1):
    if any(s - 1 <= a <= e + 1 for s, e in skip):
        continue
    if mode == "cols":
        c = float(np.interp(a, GUIDE[:, 0], GUIDE[:, 1])); lo, hi = int(c - W), int(c + W)
        rr = runs(curve[lo:hi + 1, a], lo)
    else:
        c = float(np.interp(a, GUIDE[:, 1], GUIDE[:, 0])); lo, hi = int(c - W), int(c + W)
        rr = runs(curve[a, lo:hi + 1], lo)
    rr = [r for r in rr if r[1] - r[0] >= 1]
    if not rr:
        continue
    # the cluster of runs around the run nearest the guide, joined across gaps of up to 5 px
    k = min(range(len(rr)), key=lambda i: 0 if rr[i][0] <= c <= rr[i][1] else min(abs(rr[i][0] - c), abs(rr[i][1] - c)))
    i0 = i1 = k
    while i0 > 0 and rr[i0][0] - rr[i0 - 1][1] - 1 <= 5: i0 -= 1
    while i1 < len(rr) - 1 and rr[i1 + 1][0] - rr[i1][1] - 1 <= 5: i1 += 1
    cl = rr[i0:i1 + 1]
    T, B = cl[0][0], cl[-1][1]
    gaps = [f"{p[1]+1}-{q[0]-1}" for p, q in zip(cl, cl[1:])]
    out.append({"pos": a, "lo_edge": T, "hi_edge": B, "height": B - T + 1, "gaps": " ".join(gaps),
                "lo_on_grid": in_band(T, across), "hi_on_grid": in_band(B, across),
                "others": " ".join(f"{s}-{e}" for s, e in rr[:i0] + rr[i1 + 1:])})
with (base / "helpers" / f"profile_{mode}_{a0}_{a1}.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
for r in out:
    print(f"{r['pos']}: {r['lo_edge']}-{r['hi_edge']} h{r['height']} gaps[{r['gaps']}] "
          f"{'LOg' + r['lo_on_grid'] if r['lo_on_grid'] else ''} {'HIg' + r['hi_on_grid'] if r['hi_on_grid'] else ''}")
