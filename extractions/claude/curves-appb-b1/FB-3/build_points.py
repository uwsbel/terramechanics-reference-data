"""Points of FB-3 (p0109.png), panel 1, from the measurements of circles.py / ringfit.py (symbol centres)
and trace.py (segments.json: each drawn straight segment fitted to its ink).

Markers: clean circles at the centroid of their enclosed white hole (circles.py); the overlapping
symbols (the dense pair at 4.9 psi, the upper two loose symbols at 4 psi) at the centres of the ring
model (ringfit.py, annulus 12.5 to 21 px).
Trace: per segment, the line's ink end next to a symbol is the last position, walking along the fitted
centreline towards the symbol, where the ink run across the line is still the line alone (merge_ends.py:
no wider than the line + 3 px, centred within 2 px); the free end of the loose line at the last ink on
its centreline; integer-psi samples where the x = k line of the piecewise
map crosses the drawn line, at the centre of the ink run cut along that x line.
Vertices are hidden under symbols: they are features (the intersection of the two fitted segments),
not trace samples.

Usage: python build_points.py <image> <cal_dir> <tools_dir> <segments.json> <out.csv>
"""
import csv
import json
import sys

import numpy as np
from PIL import Image

IMG, CAL, TOOLS, SEG, OUT = sys.argv[1:6]
sys.path.insert(0, TOOLS)
import calibrate_axes as ca  # noqa: E402

g = np.asarray(Image.open(IMG).convert("L"), dtype=float)
cal, X, Y = ca.piecewise_maps(CAL)
S = json.load(open(SEG))
R_END = 22.5

# symbol centres (u, v) with bounds and notes
M = {
    "d23u": (875.33, 2971.57), "d23l": (862.70, 3124.83),
    "dbu": (1235.25, 1987.00), "dbl": (1236.00, 1996.25),
    "d99u": (1938.45, 889.49), "d99l": (1936.17, 931.50),
    "lA": (1103.75, 3770.50), "lB": (1094.00, 3789.75), "lC": (1105.62, 3852.80),
    "l6": (1384.09, 3232.61), "l136u": (2443.37, 2203.57), "l136l": (2444.36, 2285.47),
}
rows = []


def add(series, kind, u, v, bu, bv, symbol, note):
    rows.append({"figure_id": "FB-3", "panel": 1, "series_id": series, "point_kind": kind, "sequence": 0,
                 "pixel_u": round(float(u), 1), "pixel_v": round(float(v), 1), "u_bound_px": bu, "v_bound_px": bv,
                 "symbol": symbol, "note": note})


clean = "clean open circle; centre = centroid of its enclosed white hole"
# ---- markers, left to right
add("dr99", "marker", *M["d23l"], 2, 2, "circle", clean + "; the dense line's left end touches its top")
add("dr99", "marker", *M["d23u"], 2, 2, "circle", clean + "; the dense line passes close to its right side")
add("dr99", "marker", *M["dbu"], 4, 5, "circle",
    "upper of two overlapping circles (one double-outlined blob, centres 9 px apart vertically); centre from a two-ring model fit "
    "(mismatch 4.3 % of pixels, against 21.6 % for one ring); bound widened; the dense polyline's vertex is under this pair")
add("dr99", "marker", *M["dbl"], 4, 5, "circle",
    "lower of two overlapping circles (see the upper one); centre from the two-ring model fit; bound widened")
add("dr99", "marker", *M["d99l"], 2, 2, "circle", clean + "; touches the circle above it; the dense line ends at its lower left")
add("dr99", "marker", *M["d99u"], 2, 2, "circle", clean + "; touches the circle below it")
add("dr30", "marker", *M["lB"], 4, 4, "circle",
    "left of the two overlapping circles above the lowest loose symbol at 4 psi; its ring crosses the hole of the upper one and the loose line "
    "runs over its right side; centre from a two-ring model fit (mismatch 6.1 %); bound widened")
add("dr30", "marker", *M["lA"], 4, 4, "circle",
    "upper of the two overlapping circles at 4 psi; the loose line runs over its right side; centre from the two-ring model fit; bound widened")
add("dr30", "marker", *M["lC"], 2, 2, "circle", clean + "; lowest loose symbol; the loose line's left end touches its top")
add("dr30", "marker", *M["l6"], 2, 2, "circle", clean + "; the loose polyline's vertex is under it")
add("dr30", "marker", *M["l136l"], 2, 2, "circle", clean + "; the loose line runs over the upper left of its outline")
add("dr30", "marker", *M["l136u"], 2, 2, "circle", clean + "; above the loose line's right end, not touched by it")


def seg(name):
    s = S[name]
    return np.array(s["point"]), np.array(s["dir"])


def circle_exit(name, centre, towards):
    """the point of segment `name`'s centreline at R_END from `centre`, on the side of point `towards`"""
    p, e = seg(name)
    c = np.array(centre)
    # |p + t e - c|^2 = R^2
    b = e @ (p - c)
    disc = b * b - ((p - c) @ (p - c) - R_END ** 2)
    ts = [-b - np.sqrt(disc), -b + np.sqrt(disc)]
    pts = [p + t * e for t in ts]
    return min(pts, key=lambda q: np.linalg.norm(q - np.array(towards)))


def intersect(a, b):
    p, d = seg(a)
    q, e = seg(b)
    t = np.linalg.solve(np.c_[d, -e], q - p)
    return p + t[0] * d


def xval(u, v):
    return X.value(u, v)[0]


def on_line_at_x(name, k):
    """centreline point where x = k (bisection along the fitted centreline)"""
    p, e = seg(name)
    lo, hi = -3000.0, 3000.0
    f = lambda t: xval(*(p + t * e)) - k
    flo = f(lo)
    for _ in range(80):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return p + lo * e


def ink_cut_at_x(name, k, half=45):
    """centre of the ink run where the x = k line of the map crosses the drawn line: walk along the x = k
    line (direction of X's lines near there) through the predicted crossing, 0.25 px steps"""
    q = on_line_at_x(name, k)
    # direction of the iso-x line: perpendicular to X's local gradient (finite differences)
    h = 1.0
    gx = np.array([xval(q[0] + h, q[1]) - xval(q[0] - h, q[1]), xval(q[0], q[1] + h) - xval(q[0], q[1] - h)])
    t_dir = np.array([-gx[1], gx[0]]) / np.hypot(*gx)
    ss = np.arange(-half, half + 0.001, 0.25)
    pts = [q + s * t_dir for s in ss]
    vals = []
    for (u, v) in pts:
        u0, v0 = int(np.floor(u)), int(np.floor(v))
        fu, fv = u - u0, v - v0
        vals.append(g[v0, u0] * (1 - fu) * (1 - fv) + g[v0, u0 + 1] * fu * (1 - fv) + g[v0 + 1, u0] * (1 - fu) * fv + g[v0 + 1, u0 + 1] * fu * fv)
    dark = np.array(vals) < 128
    idx = np.where(dark)[0]
    runs, st = [], idx[0]
    for a, b in zip(idx, idx[1:]):
        if b != a + 1:
            runs.append((st, a)); st = b
    runs.append((st, idx[-1]))
    a, b = min(runs, key=lambda r: abs((ss[r[0]] + ss[r[1]]) / 2))
    if a == 0 or b == len(ss) - 1:
        raise SystemExit(f"{name} x={k}: ink run reaches the end of the cut (symbol?)")
    c = (ss[a] + ss[b]) / 2
    return q + c * t_dir, ss[b] - ss[a] + 0.25


def free_end(name, start_t=0.0, step=0.25):
    """the last ink on the fitted centreline walking forward (increasing t along dir)"""
    p, e = seg(name)
    t = start_t
    last = None
    miss = 0
    while miss < 12:   # 3 px of white ends the line
        u, v = p + t * e
        if g[int(round(v)), int(round(u))] < 128:
            last, miss = t, 0
        else:
            miss += 1
        t += step
    return p + last * e


half = {"dense_S1": 4.1, "dense_S2": 4.8, "loose_S1": 4.5, "loose_S2": 4.6}
trace = {"dr99": [], "dr30": []}


def tr(series, segname, P, note):
    hb = half[segname]
    trace[series].append((P, hb, note))


# ---- dense polyline: S1 from the 2.3 psi lower circle to the 4.9 psi pair, S2 from the pair to the 9.9 psi lower circle
# merge points measured by merge_ends.py (last clean ink before the symbol's ring)
d_start = np.array([857.3, 3099.3])
d_s1_end = np.array([1235.5, 2018.0])
d_s2_start = np.array([1255.9, 1973.3])
d_end = np.array([1919.2, 945.5])
d_vertex = intersect("dense_S1", "dense_S2")
l_start = np.array([1094.8, 3827.7])
l_s1_end = np.array([1382.3, 3255.5])
l_s2_start = np.array([1404.8, 3220.7])
p2, e2 = seg("loose_S2")
l_end = free_end("loose_S2", start_t=float((np.array([2470.0, 2235.0]) - p2) @ e2))
d_vertex_l = intersect("loose_S1", "loose_S2")

for name, P in (("dense start", d_start), ("dense S1 end", d_s1_end), ("dense S2 start", d_s2_start), ("dense end", d_end),
                ("dense vertex", d_vertex), ("loose start", l_start), ("loose S1 end", l_s1_end), ("loose S2 start", l_s2_start),
                ("loose end", l_end), ("loose vertex", d_vertex_l)):
    print(f"{name:15s} ({P[0]:.1f}, {P[1]:.1f})  x {xval(*P):.3f}  y {Y.value(*P)[0]:.3f}")


def samples(series, segname, P0, P1, first_note, last_note, skip=()):
    x0, x1 = xval(*P0), xval(*P1)
    tr(series, segname, P0, first_note)
    for k in range(int(np.floor(x0)) + 1, int(np.ceil(x1))):
        if k in skip:
            print(f"  {segname}: x = {k} skipped ({skip[k]})")
            continue
        P, w = ink_cut_at_x(segname, k)
        print(f"  {segname}: x = {k} at ({P[0]:.1f}, {P[1]:.1f}), cut run {w:.1f} px")
        tr(series, segname, P, f"every 1 psi: on the line's ink at x = {k}")
    tr(series, segname, P1, last_note)


samples("dr99", "dense_S1", d_start, d_s1_end,
        "left end: the line's ink starts at the top outline of the lower circle at 2.3 psi (last clean ink before the ring)",
        "the line's ink meets the outline of the overlapping pair at 4.9 psi (last clean ink before the ring); the vertex is hidden under the pair")
samples("dr99", "dense_S2", d_s2_start, d_end,
        "the line's ink leaves the outline of the overlapping pair at 4.9 psi (last clean ink before the ring)",
        "right end: the line's ink ends at the lower-left outline of the lower circle at 9.9 psi (last clean ink before the ring)")
# loose S1: x = 4 lies where the line runs over the ring of the left overlapping circle; check it
samples("dr30", "loose_S1", l_start, l_s1_end,
        "left end: the line's ink starts where it meets the upper left outline of the lowest circle at 4 psi (last clean ink before the ring; the line, extended, would graze the ring, 20.8 px from the centre)",
        "the line's ink meets the outline of the circle at 6 psi (last clean ink before the ring); the vertex is hidden under it",
        skip={4: "the line runs over the rings of the two overlapping circles from v 3814 to 3762; x = 4 falls at v 3807, on a ring"})
samples("dr30", "loose_S2", l_s2_start, l_end,
        "the line's ink leaves the outline of the circle at 6 psi (last clean ink before the ring)",
        "right end: the last ink of the line's rounded tip on its centreline, short of the right frame; no symbol there")

for series in ("dr99", "dr30"):
    for P, hb, note in trace[series]:
        add(series, "trace", P[0], P[1], hb, hb, "", note)

# ---- features: first point, vertex, last point (the maximum of a rising trace), label centres
add("dr99", "feature", *trace["dr99"][0][0], half["dense_S1"], half["dense_S1"], "", "first point of the polyline (its left end)")
add("dr99", "feature", *d_vertex, 4.5, 5, "",
    "vertex: hidden under the overlapping pair at 4.9 psi; intersection of the two segments fitted to their ink (angle 13.4 deg); "
    "about 11 px right of the pair's centres")
add("dr99", "feature", *trace["dr99"][-1][0], half["dense_S2"], half["dense_S2"], "", "last point of the polyline (its right end; also the trace's maximum)")
add("dr30", "feature", *trace["dr30"][0][0], half["loose_S1"], half["loose_S1"], "", "first point of the polyline (its left end)")
add("dr30", "feature", *d_vertex_l, 4.5, 4.5, "",
    "vertex: hidden under the circle at 6 psi (inside its white hole, where no line ink is drawn); intersection of the two segments "
    "fitted to their ink (angle 20.4 deg); about 10 px right of the circle's centre")
add("dr30", "feature", *trace["dr30"][-1][0], half["loose_S2"], half["loose_S2"], "", "last point of the polyline (its right end; also the trace's maximum)")

LABELS = json.load(open(sys.argv[6])) if len(sys.argv) > 6 else {}
for series, (u, v, bu, bv, text) in LABELS.items():
    add(series, "feature", u, v, bu, bv, "", f"label: {text}")

seq = {}
for r in rows:
    k = (r["series_id"], r["point_kind"])
    seq[k] = seq.get(k, 0) + 1
    r["sequence"] = seq[k]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("wrote", OUT, len(rows), "rows;", {k: v for k, v in seq.items()})
