"""Reader helper: per page row, the curve ink runs near the curves with grid columns removed and refilled
where ink lies on both sides; rows on a horizontal grid line flagged. Cached to rowink.npz-like JSON."""
import sys, json
import numpy as np
from PIL import Image
from calmap import c, IMAGE
g = np.asarray(Image.open(IMAGE).convert("L")) < 128
SH, SV = -0.0045, 0.0064
TABLE = (1335, 1252, 1940, 2742)
THR = 0.5
def in_table(u, v): return (TABLE[0] <= u) & (u <= TABLE[2]) & (TABLE[1] <= v) & (v <= TABLE[3])
def rowfrac(v):
    cc = c(v)
    us = np.concatenate([np.arange(max(700, int(cc) - 300), int(cc) - 70), np.arange(int(cc) + 70, min(2140, int(cc) + 300))])
    vv = np.round(v + SH * (us - cc)).astype(int)
    ok = ~in_table(us, vv)
    return float(g[vv[ok], us[ok]].mean())
_cf = {}
def colfrac(u, v):
    key = (u, v // 25)
    if key not in _cf:
        vs = np.arange(v - 300, v + 300); vs = vs[(vs > 1130) & (vs < 3740)]
        uu = np.round(u + SV * (vs - v)).astype(int)
        ok = ~in_table(uu, vs)
        _cf[key] = float(g[vs[ok], uu[ok]].mean())
    return _cf[key]
def runs(mask, a):
    out, s = [], None
    for i, d in enumerate(list(mask) + [False]):
        if d and s is None: s = i
        if not d and s is not None: out.append((a + s, a + i - 1)); s = None
    return out
out = {}
for v in range(1260, 3215):
    cc = int(round(c(v))); a, b = max(cc - 70, 699), cc + 70
    gc = np.array([max(colfrac(u + d, v) for d in (-1, 0, 1)) > THR for u in range(a, b)])
    ink = g[v, a:b]
    m = ink & ~gc
    filled = m.copy()
    for p, q in runs(gc, 0):
        if p > 0 and q < len(m) - 1 and m[p - 1] and m[q + 1]:
            filled[p:q + 1] = True
    out[v] = {"grid_row": rowfrac(v) > THR, "runs": runs(filled, a), "gridcols": runs(gc, a), "a": a, "b": b}
json.dump(out, open("rowink.json", "w"))
print("rows", len(out))
