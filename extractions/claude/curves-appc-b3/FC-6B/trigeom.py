"""Geometric reading of triangle symbols: apex and base from the ink along the symbol's axis,
horizontal center from the outer edges of the two sides. Prints, per triangle, the apex, the
base edge, the measured height, the centroid from the base (base - H/3 for an up-triangle) and
from the apex (apex + 2H/3 with the nominal H), and the u center from several rows, so that the
reader can accept or override each one after looking at the check sheet.

python trigeom.py <image> <matched.csv> [--prefix p1-n4695-]
"""
import argparse
import csv

import numpy as np
from PIL import Image

HNOM = 29.5


def runs(mask, off):
    idx = np.where(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((int(s + off), int(p + off)))
            s = i
        p = i
    out.append((int(s + off), int(p + off)))
    return out


ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("points")
ap.add_argument("--prefix", default="")
a = ap.parse_args()
g = np.asarray(Image.open(a.image).convert("L")) < 128
rows = list(csv.DictReader(open(a.points, encoding="utf-8")))
print("key,sym,u_fit,v_fit,apex,base_edge,H,v_from_base,v_from_apex,u_rows")
for r in rows:
    if not r["symbol"].startswith("triangle"):
        continue
    if a.prefix and not r["key"].startswith(a.prefix):
        continue
    up = r["symbol"] == "triangle-up"
    uc, vc = int(round(float(r["u_fit"]))), int(round(float(r["v_fit"])))
    col = g[vc - 30:vc + 31, uc - 2:uc + 3].any(1)
    rr = runs(col, vc - 30)
    if up:
        # apex run: the run whose start is the topmost within [vc-26, vc-12]
        ap_runs = [x for x in rr if vc - 26 <= x[0] <= vc - 12]
        apex = ap_runs[0][0] if ap_runs else None
        b_runs = [x for x in rr if x[0] <= vc + 12 and x[1] >= vc + 6]
        base = b_runs[-1][1] if b_runs else None
    else:
        ap_runs = [x for x in rr if vc + 12 <= x[1] <= vc + 26]
        apex = ap_runs[-1][1] if ap_runs else None
        b_runs = [x for x in rr if x[1] >= vc - 12 and x[0] <= vc - 6]
        base = b_runs[0][0] if b_runs else None
    H = (base - apex) if (up and apex is not None and base is not None) else ((apex - base) if (apex is not None and base is not None) else None)
    if up:
        vb = base - (H if H else HNOM) / 3 if base is not None else None
        va = apex + 2 * HNOM / 3 if apex is not None else None
    else:
        vb = base + (H if H else HNOM) / 3 if base is not None else None
        va = apex - 2 * HNOM / 3 if apex is not None else None
    # u center from rows at the centroid level and 4 px either side (outer edges of the sides)
    us = []
    for dv in (-4, 0, 4):
        row = g[vc + dv, uc - 26:uc + 27]
        rw = runs(row, uc - 26)
        left = [x for x in rw if x[1] < uc]
        right = [x for x in rw if x[0] > uc]
        if left and right:
            # the side runs nearest the axis
            L = max(left, key=lambda x: x[1])
            Rr = min(right, key=lambda x: x[0])
            us.append(((L[0] + Rr[1]) / 2, L, Rr))
    ustr = "; ".join(f"{m:.1f} [{L[0]}-{L[1]}|{Rr[0]}-{Rr[1]}]" for m, L, Rr in us)
    print(f"{r['key']},{r['symbol']},{r['u_fit']},{r['v_fit']},{apex},{base},{H},"
          f"{vb if vb is None else round(vb, 1)},{va if va is None else round(va, 1)},{ustr}  runs={rr}")
