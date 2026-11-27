"""Band profile: for each column u (or row v), the curve-ink runs near a guide position, after the grid is
greyed out (clean2.py). Prints top edge, bottom edge and internal white gaps of the band.
usage: band.py cols u0 u1 step   |   band.py rows v0 v1 step
The guide is a rough centreline of the band through hand-picked points; runs within +-40 px of it count."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
base = Path(__file__).resolve().parents[1]
g = np.array(Image.open(base.parents[1] / "packet" / "p0054.png").convert("L")) < 128
U0, V0 = 520, 2050
gm = np.load(base / "helpers" / "gridmask.npy")
grid = np.zeros_like(g); grid[V0:V0 + gm.shape[0], U0:U0 + gm.shape[1]] = gm
curve = g & ~grid
# rough band centreline (u, v), from the overview
GUIDE = np.array([(560, 2245), (600, 2320), (650, 2370), (700, 2395), (800, 2425), (900, 2445), (1000, 2460),
                  (1100, 2475), (1200, 2490), (1300, 2502), (1400, 2520), (1500, 2545), (1600, 2565),
                  (1700, 2598), (1800, 2632), (1850, 2665), (1900, 2700), (1950, 2760), (1990, 2830),
                  (2010, 2890), (2025, 2960)], float)
def runs(line, off):
    idx = np.where(line)[0]
    out = []
    if len(idx):
        s = p = idx[0]
        for i in list(idx[1:]) + [None]:
            if i is None or i != p + 1:
                out.append((s + off, p + off)); s = i
            p = i if i is not None else p
    return out
mode, a0, a1, st = sys.argv[1], *map(int, sys.argv[2:5])
W = int(sys.argv[5]) if len(sys.argv) > 5 else 40
for a in range(a0, a1 + 1, st):
    if mode == "cols":
        c = float(np.interp(a, GUIDE[:, 0], GUIDE[:, 1]))
        lo, hi = int(c - W), int(c + W)
        rr = runs(curve[lo:hi + 1, a], lo)
    else:
        c = float(np.interp(a, GUIDE[:, 1], GUIDE[:, 0]))
        lo, hi = int(c - W), int(c + W)
        rr = runs(curve[a, lo:hi + 1], lo)
    rr = [r for r in rr if r[1] - r[0] >= 2]
    if not rr:
        print(f"{a}: -"); continue
    print(f"{a}: band {rr[0][0]}-{rr[-1][1]} ({rr[-1][1]-rr[0][0]+1})  runs " + " ".join(f"{s}-{e}" for s, e in rr))
