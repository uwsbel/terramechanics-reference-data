"""Column cuts through the band: for u in [u0, u1] step s, runs in v within +-W of a rough band centre.
Grid rows (horizontal grid lines) are marked: a run inside a grid interval is shown as [g a-b]; a run that
contains a grid interval and extends beyond it is shown as a-b* ."""
import sys
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
            return v0 + (v1 - v0) * (u - u0) / (u1 - u0) if u1 > u0 else v0
    return pts[0][1] if u < pts[0][0] else pts[-1][1]
u0, u1, s = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
Wd = int(sys.argv[4]) if len(sys.argv) > 4 else 45
for u in range(u0, u1 + 1, s):
    c = int(round(vc(u))); lo, hi = c - Wd, c + Wd
    col = g[lo:hi + 1, u]
    runs, st = [], None
    for i, d in enumerate(col):
        if d and st is None: st = i
        if not d and st is not None: runs.append((lo + st, lo + i - 1)); st = None
    if st is not None: runs.append((lo + st, hi))
    txt = []
    for a, b in runs:
        gi = [(x, y) for x, y in GRID if not (b < x - 1 or a > y + 1)]
        inside = any(x - 1 <= a and b <= y + 1 for x, y in gi)
        txt.append(f"[g{a}-{b}]" if inside else (f"{a}-{b}*" if gi else f"{a}-{b}"))
    print(f"{u}: " + " ".join(txt))
