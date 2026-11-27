"""Follow one drawn curve column by column, as an aid to sampling it on the ink.

Starting from a seed (u, v) that the reader has checked on a zoomed crop, step to the next column
and take the dark run (threshold 128, columns u-1..u+1 combined as in plot_grid scan) whose center
is closest to the position extrapolated from the last two accepted samples, within `tol` px.
Columns within `gap` px of a vertical gridline (from the calibration file) and columns inside any
marker box (marker center +- `mbox` px, from a points CSV of markers) are skipped; a column with no
run in tolerance, or with a run thicker than `maxthick` (a marker or a crossing), is reported as
a gap and not used; a run within reach of a horizontal gridline is flagged hgrid-merge (not used for
tracking or sampling) and a run thinner than 5 px is flagged thin (a speck or a dash tip). Output: u, v_center, thickness, status. The reader reviews every row on the
crops and the overlay; this script only proposes.

usage: trace.py <image> <calibration.json> <markers.csv> u_seed v_seed u_end step [tol=6] [gap=9] [mbox=15] [maxthick=16] [u_seed2 v_seed2]

A second seed (u_seed2, v_seed2), also checked on the crop, gives the initial slope on steep parts.
Across a skipped stretch (gridline, marker, gap) the prediction keeps the slope measured over the
last 20 px or more of accepted samples.
"""
import csv
import json
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
cal = json.load(open(sys.argv[2], encoding="utf-8"))
markers = []
with open(sys.argv[3], encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        if r["point_kind"] == "marker":
            markers.append((float(r["pixel_u"]), float(r["pixel_v"])))
u, v, u_end, step = int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
tol = float(sys.argv[8]) if len(sys.argv) > 8 else 6
gap = float(sys.argv[9]) if len(sys.argv) > 9 else 9
mbox = float(sys.argv[10]) if len(sys.argv) > 10 else 15
maxthick = float(sys.argv[11]) if len(sys.argv) > 11 else 16
vlines = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
hlines = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]


def runs(col):
    idx = np.where(col)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append(((s + p) / 2, p - s + 1))
            s = i
        p = i
    out.append(((s + p) / 2, p - s + 1))
    return out


hist = [(u, v)]
if len(sys.argv) > 13:
    hist = [(float(sys.argv[12]), float(sys.argv[13])), (u, v)] if float(sys.argv[12]) < u else [(u, v), (float(sys.argv[12]), float(sys.argv[13]))]
    if float(sys.argv[12]) > u:
        hist = [(2 * u - float(sys.argv[12]), 2 * v - float(sys.argv[13])), (u, v)]
print("u,v_center,thickness,status")
direction = 1 if u_end >= u else -1
cu = u
while (cu - u_end) * direction <= 0:
    if len(hist) >= 2:
        ub, vb = hist[-1]
        # slope over a baseline of at least 20 px (fewer pixels make it noisy)
        ua, va = next(((a, b) for a, b in reversed(hist[:-1]) if abs(ub - a) >= 20), hist[0])
        pred = vb + (vb - va) / (ub - ua) * (cu - ub) if ub != ua else vb
    else:
        pred = hist[-1][1]
    near_grid = any(abs(cu - (i0 + s * pred)) <= gap for i0, s in vlines)
    in_marker = any(abs(cu - mu) <= mbox and abs(pred - mv) <= mbox + 6 for mu, mv in markers)
    if near_grid:
        print(f"{cu},,,skip-gridline")
    elif in_marker:
        print(f"{cu},,,skip-marker")
    else:
        v0 = int(pred - tol - 15)
        col = g[v0:int(pred + tol + 15) + 1, cu - 1:cu + 2].min(axis=1) < 128
        cand = [(abs(c + v0 - pred), c + v0, w) for c, w in runs(col) if abs(c + v0 - pred) <= tol]
        if not cand:
            print(f"{cu},,,gap")
        else:
            d, c, w = min(cand)
            on_hgrid = any(abs(c - (i0 + s * cu)) <= w / 2 + 4 for i0, s in hlines)
            if w > maxthick:
                print(f"{cu},{c:.1f},{w},too-thick")
            elif on_hgrid:
                print(f"{cu},{c:.1f},{w},hgrid-merge")
            elif w < 5:
                print(f"{cu},{c:.1f},{w},thin")
            else:
                print(f"{cu},{c:.1f},{w},ok")
                hist.append((cu, c))
    cu += step * direction
