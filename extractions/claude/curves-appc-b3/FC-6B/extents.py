"""Print the ink runs along the vertical through a proposed triangle center and along the rows
near its base, to read the apex, the base and the base corners of a triangle symbol.

python extents.py <image> <matched.csv> --keys k1,k2 | --prefix p1-n4695-
"""
import argparse
import csv

import numpy as np
from PIL import Image


def runs(mask, off):
    idx = np.where(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s + off, p + off))
            s = i
        p = i
    out.append((s + off, p + off))
    return out


ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("points")
ap.add_argument("--keys", default="")
ap.add_argument("--prefix", default="")
a = ap.parse_args()
g = np.asarray(Image.open(a.image).convert("L")) < 128
rows = list(csv.DictReader(open(a.points, encoding="utf-8")))
keys = [k for k in a.keys.split(",") if k]
for r in rows:
    if keys and r["key"] not in keys:
        continue
    if a.prefix and not r["key"].startswith(a.prefix):
        continue
    uc, vc = int(round(float(r["u_fit"]))), int(round(float(r["v_fit"])))
    col = g[vc - 26:vc + 27, uc - 1:uc + 2].any(1)
    print(r["key"], r["symbol"], "fit", r["u_fit"], r["v_fit"])
    print("   column runs (v):", runs(col, vc - 26))
    for dv in (-12, -6, 0, 6, 10, 12, 14):
        row = g[vc + dv, uc - 26:uc + 27]
        print(f"   row v={vc + dv}:", runs(row, uc - 26))
