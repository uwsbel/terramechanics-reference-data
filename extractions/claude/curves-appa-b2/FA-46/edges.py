"""Band envelope per column: top edge T, bottom edge Bt (grid rows masked), runs inside. Writes edges.csv"""
import csv
import numpy as np
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
GRID = [(1157,1168),(1207,1215),(1264,1272),(1304,1315),(1330,1336),(1408,1417),(1438,1444),(1504,1513),(1562,1566),(1580,1590),(1625,1636),(1703,1710),(1730,1741),(1796,1810),(1878,1885),(1919,1930),(2015,2026),(2051,2053),(2090,2101),(2133,2140),(2165,2176),(2184,2191),(2240,2249)]
CEN = [(2130,2130),(2120,2120),(2000,1965),(1960,1945),(1900,1910),(1800,1863),(1700,1833),(1600,1800),(1500,1777),(1400,1767),(1300,1745),(1200,1730),(1100,1720),(1000,1710),(900,1690),(800,1660),(740,1560)]
def vc(u):
    pts = sorted(CEN)
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        if u0 <= u <= u1:
            return v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return pts[0][1] if u < pts[0][0] else pts[-1][1]
def grid_at(v, u):
    # horizontal grid intervals are given at u ~ 1450; tilt about -0.004 px per px of u
    dv = -0.004 * (u - 1450)
    return any(a - 1 + dv <= v <= b + 1 + dv for a, b in GRID)
rows = []
for u in range(740, 2131):
    c = int(round(vc(u))); lo, hi = c - 45, c + 45
    col = g[lo:hi + 1, u]
    if col.mean() > 0.8:
        rows.append({"u": u, "vgrid": 1}); continue
    runs, st = [], None
    for i, d in enumerate(col):
        if d and st is None: st = i
        if not d and st is not None: runs.append((lo + st, lo + i - 1)); st = None
    if st is not None: runs.append((lo + st, hi))
    # remove runs entirely within grid rows
    band = []
    for a, b in runs:
        if all(grid_at(v, u) for v in range(a, b + 1)):
            continue
        if b - a < 2:   # dots
            continue
        band.append((a, b))
    if not band:
        rows.append({"u": u, "vgrid": 0}); continue
    T, Bt = band[0][0], band[-1][1]
    Tg = int(grid_at(T - 1, u)); Bg = int(grid_at(Bt + 1, u))
    rows.append({"u": u, "vgrid": 0, "T": T, "Bt": Bt, "Tg": Tg, "Bg": Bg, "runs": " ".join(f"{a}-{b}" for a, b in band)})
with open(HERE / "edges.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["u", "vgrid", "T", "Bt", "Tg", "Bg", "runs"]); w.writeheader(); w.writerows(rows)
print("ok", len(rows))
