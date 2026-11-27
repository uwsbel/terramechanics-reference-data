"""Writes out/F2-48/points-p1-prev.csv (the first reading; out/F2-48/finalize_points.py turns it into points-p1.csv) from the solid centerline (solid-centerline.csv) and the dot chain
(dots.csv), plus the features read by eye from the page (listed below with their evidence).

Trace samples every 0.25 in of penetration, in drawing order (penetration 0 first):
  lpt87 (solid): the centerline point where the constant-penetration line crosses the trace. On a
    penetration grid line (whole inches) the sample is taken 7 px below it (0.023 in less), so that
    it sits on the trace's own ink and not on the grid line's; a sample whose center falls within
    8 px of a load grid line is moved along the trace to the nearest row clear of it. Bound: half
    the line's thickness across itself, t = H V / sqrt(H^2 + V^2) from the horizontal and vertical
    runs, median over +-6 rows.
  lpt85 (dotted): the center of the dot nearest that penetration, skipping dots that touch grid
    ink (cut by the grid mask). Bound: an ellipse with half the local dot spacing along the line and
    half the dot diameter across it, projected on u and v.
"""
import csv
import math
import numpy as np
from trace_lib import x_of, y_of, v_at_x, near_v_grid, near_h_grid

FIG, PANEL = "F2-48", 1
rows = []


def add(series, kind, u, v, bu, bv, note):
    rows.append(dict(figure_id=FIG, panel=PANEL, series_id=series, point_kind=kind, pixel_u=f"{u:.1f}",
                     pixel_v=f"{v:.1f}", u_bound_px=f"{bu:.1f}", v_bound_px=f"{bv:.1f}", symbol="", note=note))


# ------------------------------------------------------------------ solid trace, lpt87
cl = [d for d in csv.DictReader(open("out/F2-48/solid-centerline.csv")) if d["flag"] == "" and d["u"] and d["v"]]
P = np.array([[float(d["u"]), float(d["v"])] for d in cl])
T = np.array([float(d["t_perp"]) if d["t_perp"] else np.nan for d in cl])
X = np.array([x_of(u, v) for u, v in P])
Y = np.array([y_of(u, v) for u, v in P])


def half_thickness(i):
    lo, hi = max(0, i - 6), min(len(T), i + 7)
    t = np.nanmedian(T[lo:hi])
    return max(2.5, round(t / 2 * 2) / 2)       # to 0.5 px


def first_crossing(xt, start=0):
    for i in range(start, len(X) - 1):
        if (X[i] - xt) * (X[i + 1] - xt) <= 0 and X[i + 1] >= X[i] - 0.05:
            return i if abs(X[i] - xt) <= abs(X[i + 1] - xt) else i + 1
    return None


solid = []   # (x for ordering, row)
# features read by eye (see notes.md): first point, toe knee, end of initial rise, plateau maximum,
# plateau minimum, peak and last point
feat_solid = [
    (2245.0, 3758.0, 5.0, 4.0, "first: the solid line's ink comes out of the bottom frame line (penetration 0) "
     "here; the lowest dots of lpt85 merge with it (the traces run together below about 0.13 in), so its upper "
     "edge is hidden and the bound is widened; whether it continues inside the frame to the corner cannot be seen"),
    (2218.0, 3738.0, 3.5, 3.5, "knee (toe): the initial rise steepens here, about 250 lb/in below and 550 lb/in "
     "above; just clear of the lpt85 dots"),
    (2031.5, 3668.0, 3.5, 3.5, "knee: end of the initial steep rise, the trace turns onto the plateau"),
    (2026.5, 3648.0, 3.0, 10.0, "knee: local maximum of the plateau (flat between about 0.46 and 0.57 in; "
     "x is not an observation, v bound covers the flat top)"),
    (2044.5, 3502.0, 3.0, 4.0, "knee: lowest load of the plateau, after which the second rise begins"),
    (982.0, 1351.0, 3.0, 3.0, "peak: the maximum load of the trace is at its end (the same ink as the last point)"),
    (982.0, 1351.0, 3.0, 3.0, "last: the solid line ends 9 px above the x = 8 in grid line (extrapolated beyond "
     "the last labelled line)"),
]
for u, v, bu, bv, note in feat_solid:
    solid.append((x_of(u, v), ("feature", u, v, bu, bv, note)))

i0 = 0
for k in range(1, 33):
    xt = 0.25 * k
    on_grid = abs(xt - round(xt)) < 1e-9
    target = xt - (7.0 / 307.0 if on_grid else 0.0)
    i = first_crossing(target, i0)
    if i is None:
        continue
    note = []
    if on_grid:
        note.append(f"sampled 7 px below the x = {int(round(xt))} in grid line, on the trace's own ink")
    u, v = P[i]
    L = near_v_grid(u, v, 4.5)
    if L is not None:
        # move along the trace to the nearest clean row clear of the load grid line
        best = None
        for j in range(max(0, i - 40), min(len(P), i + 41)):
            uj, vj = P[j]
            if near_v_grid(uj, vj, 4.5) is None and near_h_grid(uj, vj, 3) is None:
                if best is None or abs(j - i) < abs(best - i):
                    best = j
        dv = P[best][1] - v
        note.append(f"moved {abs(dv):.0f} px along the trace off the y = {L['y_value']:.0f} lb grid line")
        i = best
        u, v = P[i]
    h = half_thickness(i)
    note.insert(0, f"trace sample near x = {xt:.2f} in")
    solid.append((X[i] + 1e-6, ("trace", u, v, h, h, "; ".join(note))))
    i0 = i

# drawing order: by position along the trace; the trace never doubles back by more than a pixel
# here, so the order of the centerline (and of x for the features) is the drawing order
solid.sort(key=lambda t: t[0])
seq = 0
for _, (kind, u, v, bu, bv, note) in solid:
    add("lpt87", kind, u, v, bu, bv, note)

# ------------------------------------------------------------------ dotted trace, lpt85
dots = list(csv.DictReader(open("out/F2-48/dots.csv")))
D = np.array([[float(d["u"]), float(d["v"])] for d in dots])
DX = np.array([float(d["x"]) for d in dots])
area = np.array([float(d["area"]) for d in dots])
ext_ok = np.array([int(d["du"]) >= 10 and int(d["dv"]) >= 10 for d in dots])
# a dot is usable for a sample when it is whole: untouched by grid ink, or touching it but still of
# full size (area 85 px or more, both extents 10 px or more) with its center 6 px or more from the
# grid line (so the grid mask did not cut it and its center is on the dot's own ink)
clean = np.array([(d["flag"] == "") or (a >= 85 and e and near_v_grid(u, v, 2.5) is None
                  and near_h_grid(u, v, 2) is None)
                  for d, a, e, (u, v) in zip(dots, area, ext_ok, D)])


def dot_bounds(i):
    a = []
    if i > 0:
        a.append(np.hypot(*(D[i] - D[i - 1])))
    if i < len(D) - 1:
        a.append(np.hypot(*(D[i + 1] - D[i])))
    along = np.mean(a) / 2
    j0, j1 = max(0, i - 1), min(len(D) - 1, i + 1)
    d = D[j1] - D[j0]
    cu, cv = d / np.hypot(*d)
    diam = 2 * math.sqrt(area[i] / math.pi)
    across = diam / 2
    bu = math.sqrt((along * cu) ** 2 + (across * cv) ** 2)
    bv = math.sqrt((along * cv) ** 2 + (across * cu) ** 2)
    return round(bu * 2) / 2, round(bv * 2) / 2


dotted = []
feat_dotted = [
    (2252.0, 3752.0, 8.0, 8.0, "first: the lowest dot visible above the bottom frame line; it and the two dots "
     "above it touch the solid line (the traces run together below about 0.15 in), so the bound is widened; a "
     "dot nearer the corner would be hidden in the frame line"),
]
ix_knee1 = int(np.argmin(np.abs(D[:, 0] - 2136.0) + np.abs(D[:, 1] - 3599.5)))
ix_knee2 = int(np.argmin(np.abs(D[:, 0] - 2122.0) + np.abs(D[:, 1] - 3447.2)))
for i, note in ((ix_knee1, "knee: end of the initial rise, the dots turn onto the plateau (on a dot)"),
                (ix_knee2, "knee: the second rise begins, slope up from about 20 to 75 lb/in (on a dot)")):
    bu, bv = dot_bounds(i)
    feat_dotted.append((D[i, 0], D[i, 1], bu, bv, note))
bu, bv = dot_bounds(len(D) - 1)
for note in ("peak: the maximum load of the trace is at its last dot",
             "last: the last dot, just below the x = 8 in grid line (the line is broken here; the 6 px fragment "
             "on it at u 1124-1129 is grid-line ink, the height of the line, not a dot)"):
    feat_dotted.append((D[-1, 0], D[-1, 1], bu, bv, note))
for u, v, bu, bv, note in feat_dotted:
    dotted.append((x_of(u, v), ("feature", u, v, bu, bv, note)))

used = set()
for k in range(1, 32):
    xt = 0.25 * k
    order = np.argsort(np.abs(DX - xt))
    i = next(j for j in order if clean[j] and j not in used)
    if abs(DX[i] - xt) > 0.08:
        continue
    used.add(i)
    note = f"trace sample near x = {xt:.2f} in, on the dot center"
    if not clean[order[0]]:
        note += "; the nearest dot is cut by a grid line, the next whole dot is used"
    elif dots[i]["flag"]:
        note += "; the dot touches a grid line but is whole"
    bu, bv = dot_bounds(i)
    dotted.append((DX[i] + 1e-6, ("trace", D[i, 0], D[i, 1], bu, bv, note)))

dotted.sort(key=lambda t: t[0])
for _, (kind, u, v, bu, bv, note) in dotted:
    add("lpt85", kind, u, v, bu, bv, note)

# sequence per series in drawing order
cnt = {}
for r in rows:
    cnt[r["series_id"]] = cnt.get(r["series_id"], 0) + 1
    r["sequence"] = cnt[r["series_id"]]
cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px",
        "v_bound_px", "symbol", "note"]
with open("out/F2-48/points-p1-prev.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for s in ("lpt87", "lpt85"):
    print(s, {k: sum(1 for r in rows if r["series_id"] == s and r["point_kind"] == k) for k in ("trace", "feature")})
