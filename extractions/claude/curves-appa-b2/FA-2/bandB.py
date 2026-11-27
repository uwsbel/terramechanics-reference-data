"""Column-mode envelopes of the merged band on the shallow stretch (u 770..1200) and the crossings of
the derived lower (top edge + half extent), upper (bottom edge - half extent) and middle lines with the
sampling lines. Reading aid; see merged.py for the rule."""
import json, math, sys
import numpy as np
import track as TR, band as B, fa2_tools as T

seeds = json.load(open("bandB_seeds.json"))
U0, U1, WIN = 770, 1200, 10
cols = {}
for u in range(U0 - WIN, U1 + WIN + 1):
    c, s = TR.interp_seeds(seeds, u, "u")
    cols[u] = (c, s, B.band_at(TR.DARK[:, u], 1580, 1760, c, TR.grid_rows_at(u), gap=1))
lines = {}
for u in range(U0, U1 + 1):
    c, s, _ = cols[u]
    tops, bots = [], []
    for uu in range(u - WIN, u + WIN + 1):
        r = cols[uu][2]
        if r is None or r[1] - r[0] > 70:
            continue
        if not r[2]:
            tops.append(r[0] - s * (uu - u))
        if not r[3]:
            bots.append(r[1] - s * (uu - u))
    if not tops or not bots:
        continue
    h2 = 5.0 * math.sqrt(1 + s * s)
    top, bot = min(tops), max(bots)
    lines[u] = (top + h2 - 0.5, bot - h2 + 0.5, 0.5 * (top + bot), top, bot)
json.dump({str(k): v for k, v in lines.items()}, open("bandB_lines.json", "w"))

def cross(fn, target):
    res = {}
    for i, name in enumerate(("lower", "upper", "average")):
        us = sorted(lines)
        hits = []
        for a, b in zip(us, us[1:]):
            fa = fn(a, lines[a][i]) - target
            fb = fn(b, lines[b][i]) - target
            if fa * fb <= 0 and fa != fb:
                w = fa / (fa - fb)
                hits.append((round(a + w, 1), round(lines[a][i] + w * (lines[b][i] - lines[a][i]), 1)))
        res[name] = hits
    return res

for k in (9, 8, 7):
    print("k", k, cross(lambda u, v: math.log10(T.X.value(u, v)[0]), 0.05 * k))
for p in (95, 90, 85, 80, 75, 70, 65, 60):
    print("pct", p, cross(lambda u, v: T.Y.value(u, v)[0], p))
