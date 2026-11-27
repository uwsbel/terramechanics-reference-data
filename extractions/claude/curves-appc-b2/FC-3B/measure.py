"""Outer-outline extents of a marker around an approximate center: column scan at u_c (+-1) and
row scan at v_c (+-1) within +-24 px; prints extents, outer-bbox center, hole center for comparison.
python measure.py cand.csv"""
import sys, csv
import numpy as np
from PIL import Image
g = np.array(Image.open("packet/p0124.png").convert("L")) < 128
def extent(line, c, r=24):
    lo, hi = c - r, c + r
    seg = line[lo:hi+1]
    idx = np.where(seg)[0]
    if len(idx) == 0: return None
    # take the ink run cluster containing/nearest the center, allowing gaps <= 3 px
    pos = idx + lo
    groups = [[pos[0]]]
    for p in pos[1:]:
        if p - groups[-1][-1] <= 3: groups[-1].append(p)
        else: groups.append([p])
    # merge groups into the symbol: those within the window that are within 30 px overall span around c
    best = min(groups, key=lambda gr: abs((gr[0]+gr[-1])/2 - c))
    lo_g, hi_g = best[0], best[-1]
    # extend with neighbouring groups if the hollow interior separates stroke runs (hollow symbol)
    for gr in groups:
        if gr is best: continue
        if (abs(gr[0] - hi_g) <= 26 and gr[0] > hi_g and gr[-1] - lo_g <= 36): hi_g = gr[-1]
        if (abs(lo_g - gr[-1]) <= 26 and gr[-1] < lo_g and hi_g - gr[0] <= 36): lo_g = gr[0]
    return lo_g, hi_g
with open(sys.argv[1], newline="") as f:
    for r in csv.DictReader(f):
        u, v = int(round(float(r["u"]))), int(round(float(r["v"])))
        col = g[:, u-1:u+2].max(axis=1); row = g[v-1:v+2, :].max(axis=0)
        ev = extent(col, v); eu = extent(row, u)
        cv = (ev[0]+ev[1])/2 if ev else None; cu = (eu[0]+eu[1])/2 if eu else None
        print(f"{r['label']:3s} hole=({r['u']},{r['v']}) outer_u={eu} outer_v={ev} outer_center=({cu},{cv}) "
              f"du={None if cu is None else round(cu-float(r['u']),1)} dv={None if cv is None else round(cv-float(r['v']),1)}")
