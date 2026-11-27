import json
import numpy as np
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
GRID = [(1157,1168),(1207,1215),(1264,1272),(1304,1315),(1330,1336),(1408,1417),(1438,1444),(1504,1513),(1562,1566),(1580,1590),(1625,1636),(1703,1710),(1730,1741),(1796,1810),(1878,1885),(1919,1930),(2015,2026),(2051,2053),(2090,2101),(2133,2140),(2165,2176),(2184,2191),(2240,2249)]
def grid_at(v, u):
    dv = -0.004 * (u - 1450)
    return any(a - 1 + dv <= v <= b + 1 + dv for a, b in GRID)
_k = json.load(open(HERE / "center_knots.json"))
_ku = np.array([a for a, b in _k], float); _kv = np.array([b for a, b in _k], float)
# light smoothing of the knots
_kvs = np.convolve(np.pad(_kv, 1, mode="edge"), np.ones(3) / 3, mode="valid")
def vc(u):
    return float(np.interp(u, _ku, _kvs))
def runs_col(u, lo, hi):
    col = g[lo:hi + 1, u]; out = []; st = None
    for i, d in enumerate(col):
        if d and st is None: st = i
        if not d and st is not None: out.append((lo + st, lo + i - 1)); st = None
    if st is not None: out.append((lo + st, hi))
    return out
def runs_row(v, lo, hi):
    line = g[v, lo:hi + 1]; out = []; st = None
    for i, d in enumerate(line):
        if d and st is None: st = i
        if not d and st is not None: out.append((lo + st, lo + i - 1)); st = None
    if st is not None: out.append((lo + st, hi))
    return out
