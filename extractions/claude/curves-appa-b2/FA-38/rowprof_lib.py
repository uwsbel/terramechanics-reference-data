import numpy as np
from PIL import Image
from calmap import c, IMAGE
G = np.asarray(Image.open(IMAGE).convert("L")) < 128
SH, SV = -0.0045, 0.0064
TABLE = (1335, 1252, 1940, 2742)
THR = 0.5
def in_table(u, v): return (TABLE[0] <= u) & (u <= TABLE[2]) & (TABLE[1] <= v) & (v <= TABLE[3])
def rowfrac(v):
    cc = c(v)
    us = np.concatenate([np.arange(max(700, int(cc) - 300), int(cc) - 70), np.arange(int(cc) + 70, min(2140, int(cc) + 300))])
    vv = np.round(v + SH * (us - cc)).astype(int)
    ok = ~in_table(us, vv)
    return float(G[vv[ok], us[ok]].mean())
def is_gridrow(v): return rowfrac(v) > THR
def colfrac(u, v):
    vs = np.arange(v - 300, v + 300); vs = vs[(vs > 1130) & (vs < 3740)]
    uu = np.round(u + SV * (vs - v)).astype(int)
    ok = ~in_table(uu, vs)
    return float(G[vs[ok], uu[ok]].mean())
def gridcols(a, b, v):
    m = [colfrac(u, v) > THR for u in range(a, b)]
    out, s = [], None
    for i, d in enumerate(m + [False]):
        if d and s is None: s = i
        if not d and s is not None: out.append((a + s, a + i - 1)); s = None
    return out
