"""Reader helper: curve ink along page rows around each sample row. Grid columns (dark over more than
`thr` of a 600 px deskewed window outside the table) are removed and refilled where ink lies on both
sides (a stroke continues under a grid line); rows lying on a horizontal grid line are marked G.
usage: rowprof.py k_lo k_hi [half_rows] [thr]"""
import sys
import numpy as np
from PIL import Image
from calmap import c, v_of_g, IMAGE
g = np.asarray(Image.open(IMAGE).convert("L")) < 128
SH, SV = -0.0045, 0.0064
TABLE = (1335, 1252, 1940, 2742)
k0, k1 = int(sys.argv[1]), int(sys.argv[2]); hr = int(sys.argv[3]) if len(sys.argv) > 3 else 8
thr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
def in_table(u, v): return (TABLE[0] <= u) & (u <= TABLE[2]) & (TABLE[1] <= v) & (v <= TABLE[3])
def rowfrac(v):
    cc = c(v)
    us = np.concatenate([np.arange(max(700, int(cc) - 300), int(cc) - 70), np.arange(int(cc) + 70, min(2140, int(cc) + 300))])
    vv = np.round(v + SH * (us - cc)).astype(int)
    ok = ~in_table(us, vv)
    return g[vv[ok], us[ok]].mean()
def colfrac(u, v):
    vs = np.arange(v - 300, v + 300); vs = vs[(vs > 1130) & (vs < 3740)]
    uu = np.round(u + SV * (vs - v)).astype(int)
    ok = ~in_table(uu, vs)
    return g[vs[ok], uu[ok]].mean()
def runs(mask, a):
    out, s = [], None
    for i, d in enumerate(list(mask) + [False]):
        if d and s is None: s = i
        if not d and s is not None: out.append((a + s, a + i - 1)); s = None
    return out
for k in range(k0, k1 + 1):
    gs = 10 ** (0.05 * k)
    v = 2000.0
    for _ in range(5): v = v_of_g(gs, c(v))
    vt = int(round(v)); cc = int(round(c(v))); a, b = cc - 60, cc + 60
    gc = np.array([max(colfrac(u + d, vt) for d in (-1, 0, 1)) > thr for u in range(a, b)])
    print(f"== k {k} g {gs:.4f} v_target {v:.1f}  window u {a}..{b}  grid cols: " + " ".join(f"{p}-{q}" for p, q in runs(gc, a)))
    for vv in range(vt - hr, vt + hr + 1):
        ink = g[vv, a:b].copy()
        m = ink & ~gc
        # refill grid columns between ink on both sides
        filled = m.copy()
        for p, q in runs(gc, 0):
            if p > 0 and q < len(m) - 1 and m[p - 1] and m[q + 1]:
                filled[p:q + 1] = True
        gr = rowfrac(vv) > thr
        print(f"  v {vv} {'G' if gr else ' '} " + " ".join(f"{p}-{q}({q - p + 1})" for p, q in runs(filled, a)))
