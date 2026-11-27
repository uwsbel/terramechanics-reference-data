"""Assemble points-p1.csv of FB-4 (Fig. B-4) from the measurements of the helpers:
markers (ring-model or hole centres, ringfit.py / clean_circles.py), the fitted segment centre lines
(segments.json), the piecewise x map of cal-p1 (to place the trace samples at whole psi), and the
ink of the page (to find where each drawn line's ink starts and ends at a symbol outline).

usage: build_points.py <tools dir> <page png> <segments.json> <cal dir> <out csv>"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca  # noqa: E402  (imported, not modified)

page, segf, cal_dir, out = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
D = np.asarray(Image.open(page).convert("L")) < 128
S = json.load(open(segf))
cal, X, Y = ca.piecewise_maps(cal_dir, page)
R_OUT = 20.77      # outer radius of the circle symbols (ringfit.py, median of six isolated circles)
R_IN = 12.75

# ---- markers: (series, u, v, bound_u, bound_v, note) -------------------------------------------
M = [
    ("dr22", 770.50, 3210.20, 2, 2, "isolated circle; the loose line ends on its outline (first point of dr22)"),
    ("dr86", 943.88, 2526.25, 3, 3, "upper of two overlapping circles at sigma3 ~2.5 (dense); centre from a two-ring model fit, hole partly covered by the other ring; the dense line ends on this pair's outline"),
    ("dr86", 943.12, 2541.62, 3, 3, "lower of two overlapping circles at sigma3 ~2.5 (dense); centre from a two-ring model fit"),
    ("dr86", 957.40, 2579.20, 2, 2, "circle just below the overlapping pair; its hole is clean; nearest drawn line is the dense line (13 px from its extension, 107 px from the loose line), so dense; with the pair it makes three dense tests at ~2.5 psi as the loose group has three"),
    ("dr22", 953.38, 2757.25, 3, 3, "top of three overlapping circles at sigma3 ~2.5 (loose); centre from a three-ring model fit; the loose line's hidden vertex lies at its centre"),
    ("dr22", 944.25, 2777.75, 3, 3, "middle of three overlapping circles at sigma3 ~2.5 (loose); three-ring model fit (a two-ring model leaves 2.7x the misfit)"),
    ("dr22", 944.25, 2793.12, 3, 3, "bottom of three overlapping circles at sigma3 ~2.5 (loose); three-ring model fit"),
    ("dr86", 1284.50, 1833.10, 2, 2, "isolated circle above the dense line at sigma3 ~5"),
    ("dr86", 1285.30, 1900.40, 2, 2, "circle below the dense vertex at sigma3 ~5; the dense line crosses its upper left outline; centre = mean of hole centroid and outer-edge fit (0.6 px apart)"),
    ("dr22", 1300.00, 2154.80, 2, 2, "isolated circle between the two lines at sigma3 ~5; nearer the loose line (157 px) than the dense line (293 px), and the loose vertex sits midway between it and the circle below; assigned dr22"),
    ("dr22", 1294.95, 2475.60, 2, 2, "isolated circle below the loose line at sigma3 ~5"),
    ("dr86", 1973.62, 1330.62, 3, 3, "upper of two overlapping circles at sigma3 ~9.8 (dense, printed as a double circle); two-ring model fit (one ring leaves 3.5x the misfit); the ink spans v 1310 to 1364, which an edge reading puts at 1330.3 and 1343.2, hence the 3 px bound"),
    ("dr86", 1974.12, 1341.50, 3, 3, "lower of two overlapping circles at sigma3 ~9.8 (dense); two-ring model fit; edge reading gives v 1343.2"),
    ("dr22", 1947.22, 1841.60, 2, 2, "isolated circle above the loose line's right end at sigma3 ~9.7; far below the dense line"),
    ("dr22", 1948.28, 2062.03, 2, 2, "isolated circle below the loose line's right end at sigma3 ~9.7"),
]
circles = [(u, v) for _, u, v, *_ in M]


def seg_point(name, t):
    s = S[name]
    return (s["c0"] + s["k"] * t, t) if s["steep"] else (t, s["c0"] + s["k"] * t)


def seg_t(name, u, v):
    return v if S[name]["steep"] else u


def intersect(a, b):
    """intersection of two fitted segments, by bisection-free algebra on the general line form"""
    def coef(name):
        s = S[name]
        # steep: u - k v - c0 = 0 ; shallow: v - k u - c0 = 0  -> A u + B v = C
        return (1.0, -s["k"], s["c0"]) if s["steep"] else (-s["k"], 1.0, s["c0"])
    A1, B1, C1 = coef(a)
    A2, B2, C2 = coef(b)
    det = A1 * B2 - A2 * B1
    return ((C1 * B2 - C2 * B1) / det, (A1 * C2 - A2 * C1) / det)


def march_to_circle(name, t_start, step, cands):
    """walk along a segment's centre line from t_start in steps of `step` until within R_OUT of a
    candidate circle centre: where the line's ink meets that symbol's outline"""
    t = t_start
    last_ink = None
    for _ in range(20000):
        u, v = seg_point(name, t)
        if D[int(round(v)), int(round(u))]:
            last_ink = (u, v)
        d = min(np.hypot(u - cu, v - cv) for cu, cv in cands)
        if d <= R_OUT:
            # the last centre-line pixel with ink before the outline (a white notch where line and
            # ring meet is not ink, rule 7)
            return (u, v) if D[int(round(v)), int(round(u))] else last_ink
        t += step
    raise RuntimeError(name)


def free_end(name, t_from, t_to):
    """last position along the centre line (from t_from towards t_to) whose pixel is ink"""
    last = None
    for t in np.arange(t_from, t_to, 0.25 if t_to > t_from else -0.25):
        u, v = seg_point(name, t)
        ui, vi = int(round(u)), int(round(v))
        if D[vi, ui]:
            last = (u, v)
        else:
            break
    return last


def x_of(u, v):
    return X.value(u, v)[0]


def at_x(name, target, t0, t1):
    """point on segment centre line where the piecewise x equals target (bisection in t)"""
    f0 = x_of(*seg_point(name, t0)) - target
    for _ in range(80):
        tm = 0.5 * (t0 + t1)
        fm = x_of(*seg_point(name, tm)) - target
        if (fm < 0) == (f0 < 0):
            t0, f0 = tm, fm
        else:
            t1 = tm
    return seg_point(name, 0.5 * (t0 + t1))


def half(name):
    return round(S[name]["thickness"] / 2, 1)


def ink(u, v):
    return bool(D[int(round(v)), int(round(u))])


rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append({"figure_id": "FB-4", "panel": 1, "series_id": series, "point_kind": kind, "sequence": seq,
                 "pixel_u": round(u, 2), "pixel_v": round(v, 2), "u_bound_px": bu, "v_bound_px": bv,
                 "symbol": symbol, "note": note})


# ---- markers, left to right per series --------------------------------------------------------
for sid in ("dr86", "dr22"):
    ms = sorted([m for m in M if m[0] == sid], key=lambda m: (round(m[1] / 30), m[2]))
    for i, (_, u, v, bu, bv, note) in enumerate(ms, 1):
        add(sid, "marker", i, u, v, bu, bv, "circle", note)

# ---- dense polyline dr86: s1 (from the overlapping pair at ~2.5 psi) and s2 ---------------------
A_pair = [(943.88, 2526.25), (943.12, 2541.62), (957.40, 2579.20)]
C_pair = [(1973.62, 1330.62), (1974.12, 1341.50)]
d_first = march_to_circle("dr86_s1", 2480.0, +0.05, A_pair)          # walking down the line towards the pair
d_v1 = intersect("dr86_s1", "dr86_s2")
d_last = march_to_circle("dr86_s2", 1900.0, +0.05, C_pair)           # walking right towards the double circle
print("dense first", d_first, "ink", ink(*d_first), " vertex", d_v1, "ink", ink(*d_v1), " last", d_last, "ink", ink(*d_last))
tr = [(d_first, "dr86_s1", "first point: the line's ink meets the outline of the overlapping circles at ~2.5 psi (it may continue under them)")]
for x in range(3, 5):
    tr.append((at_x("dr86_s1", x, seg_t("dr86_s1", *d_first), seg_t("dr86_s1", *d_v1)), "dr86_s1", f"sigma3 = {x} psi"))
tr.append((d_v1, "dr86_s1+s2", "vertex: intersection of the two fitted segments, on the ink of the drawn corner; the line touches the circle at (1285.3, 1900.4)"))
for x in range(5, 10):
    tr.append((at_x("dr86_s2", x, seg_t("dr86_s2", *d_v1), seg_t("dr86_s2", *d_last)), "dr86_s2", f"sigma3 = {x} psi"))
tr.append((d_last, "dr86_s2", "last point: the line's ink meets the outline of the double circle at ~9.8 psi"))
for i, ((u, v), seg, note) in enumerate(tr, 1):
    b = max(half("dr86_s1"), half("dr86_s2")) if "+" in seg else half(seg)
    assert ink(u, v), (u, v, note)
    add("dr86", "trace", i, u, v, b, b, "", note)

# ---- loose polyline dr22: s1, (hidden vertex in the top circle at ~2.5 psi), s2, s3 ------------
B_trip = [(953.38, 2757.25), (944.25, 2777.75), (944.25, 2793.12)]
l_first = march_to_circle("dr22_s1", 3150.0, +0.05, [(770.50, 3210.20)])  # walking down towards the first circle
l_q1 = march_to_circle("dr22_s1", 2900.0, -0.05, B_trip)             # walking up towards the triple
l_vb = intersect("dr22_s1", "dr22_s2")
l_q2 = march_to_circle("dr22_s2", 2690.0, +0.05, B_trip)             # walking down towards the triple
l_v2 = intersect("dr22_s2", "dr22_s3")
s3 = S["dr22_s3"]
l_last = free_end("dr22_s3", 1930.0, 1975.0)
print("loose first", l_first, ink(*l_first), " q1", l_q1, ink(*l_q1), " hidden vertex", l_vb, "ink", ink(*l_vb),
      " q2", l_q2, ink(*l_q2), " v2", l_v2, ink(*l_v2), " last", l_last, ink(*l_last))
dmin = min(np.hypot(l_vb[0] - cu, l_vb[1] - cv) for cu, cv in B_trip)
print("hidden vertex distance from nearest circle centre", round(dmin, 2))
tr = [(l_first, "dr22_s1", "first point: the line's ink meets the outline of the circle at ~1.3 psi")]
tr.append((at_x("dr22_s1", 2, seg_t("dr22_s1", *l_first), seg_t("dr22_s1", *l_q1)), "dr22_s1", "sigma3 = 2 psi"))
tr.append((l_q1, "dr22_s1", "the line's ink meets the outline of the three overlapping circles at ~2.5 psi; the drawn line is hidden by them from here to the next sample (its vertex is inside the top circle's hole, not on ink)"))
tr.append((l_q2, "dr22_s2", "the line's ink leaves the outline of the top circle of the three at ~2.5 psi"))
# the corner sits at sigma3 = 4.999 psi (0.12 px from the 5 psi line): the vertex stands for the 5 psi
# sample, which would otherwise duplicate it
assert abs(x_of(*l_v2) - 5) < 0.02
for x in range(3, 5):
    tr.append((at_x("dr22_s2", x, seg_t("dr22_s2", *l_q2), seg_t("dr22_s2", *l_v2)), "dr22_s2", f"sigma3 = {x} psi"))
tr.append((l_v2, "dr22_s2+s3", "vertex: intersection of the two fitted segments, on the ink of the drawn corner; at sigma3 = 5.00 psi, so it is also the 5 psi sample"))
for x in range(6, 10):
    tr.append((at_x("dr22_s3", x, seg_t("dr22_s3", *l_v2), seg_t("dr22_s3", *l_last)), "dr22_s3", f"sigma3 = {x} psi"))
tr.append((l_last, "dr22_s3", "last point: free end of the line's ink"))
for i, ((u, v), seg, note) in enumerate(tr, 1):
    b = max(half("dr22_s2"), half("dr22_s3")) if "+" in seg else half(seg)
    assert ink(u, v), (u, v, note)
    add("dr22", "trace", i, u, v, b, b, "", note)

# ---- features ------------------------------------------------------------------------------------
F = [
    ("dr86", d_first, half("dr86_s1"), "first point (ink start at the outline of the overlapping circles at ~2.5 psi)"),
    ("dr86", d_v1, max(half("dr86_s1"), half("dr86_s2")), "vertex"),
    ("dr86", d_last, half("dr86_s2"), "last point (ink end at the outline of the double circle at ~9.8 psi); also the maximum of the trace"),
    ("dr86", (2202.5, 1380.0), 10, "label: Dense D_r = 0.86 (two lines, ink block u 2045-2360, v 1313-1447); right of the upper polyline's end"),
    ("dr22", l_first, half("dr22_s1"), "first point (ink start at the outline of the circle at ~1.3 psi)"),
    ("dr22", l_vb, 5, "vertex, hidden: intersection of the two fitted segments, inside the hole of the top circle of the three at ~2.5 psi (white there; the drawn ink stops at the outlines), so not a trace sample"),
    ("dr22", l_v2, max(half("dr22_s2"), half("dr22_s3")), "vertex"),
    ("dr22", l_last, half("dr22_s3"), "last point (free end of the ink); also the maximum of the trace"),
    ("dr22", (2200.5, 1963.5), 10, "label: Loose D_r = 0.22 (two lines, ink block u 2044-2357, v 1900-2027); right of the lower polyline's end"),
]
seqs = {}
for sid, (u, v), b, note in F:
    seqs[sid] = seqs.get(sid, 0) + 1
    add(sid, "feature", seqs[sid], u, v, b, b, "", note)

cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("wrote", out, len(rows), "rows")
from collections import Counter
print(Counter((r["series_id"], r["point_kind"]) for r in rows))
