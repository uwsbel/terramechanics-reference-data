"""Trace samples of FC-22 on the ink. Ink intervals (u) of each curve were read on zoomed crops
(crops/w1..w6, e_*, circle*, jog) and refined with dashends.py; v at any u is a local straight-line fit
to the column-wise ink centre (centerline.py) within the same ink interval, +-20 px. Target Dr found
with this reader's piecewise x map. A target in a gap (between dashes, inside a circle) moves to the
nearest interval end (rule 7).

usage: sample.py <tools dir> <cal dir> <page png> <centerline.json> <out points csv>"""
import sys, json, csv
import numpy as np
sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(sys.argv[2], sys.argv[3])
cl = json.load(open(sys.argv[4]))
out = sys.argv[5]
CIRCLES = [(1688.9, 2014.65), (2341.8, 1584.6)]
# ink intervals (u_start, u_end): each end is the centre of the line's end cap, read on the crops
SEGS = {
    "mean": [(855, 1668), (1712, 2073), (2079, 2319), (2365, 2412)],
    "upper": [(859, 943), (967, 1071), (1108, 1244), (1283, 1407), (1448, 1612), (1659, 1764),
              (1827, 1975), (2008, 2147), (2179, 2297), (2338, 2404.5)],
    "lower": [(853, 999), (1045, 1184), (1219, 1398), (1448, 1611), (1655, 1746), (1799, 1927),
              (1986, 2135), (2182, 2306), (2354, 2404.5)],
}
GAP_WHY = {
    ("mean", 1668): "where the solid line is interrupted by circle 1",
    ("mean", 1712): "where the solid line is interrupted by circle 1",
    ("mean", 2319): "where the solid line is interrupted by circle 2",
    ("mean", 2365): "where the solid line is interrupted by circle 2",
    ("mean", 2073): "in a small break of the solid line",
    ("mean", 2079): "in a small break of the solid line",
}
VL = [(l["x_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
HL = [(l["y_value"], l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]


def clean(name):
    rows = [r for r in cl[name] if (r[3] - r[2]) < 14 and not r[4] and not r[5]]
    if name == "mean":
        rows = [r for r in rows if all(abs(r[0] - cu) > 24 for cu, _ in CIRCLES)]
    A = np.array([[r[0], r[1]] for r in rows])
    p = np.polyfit(A[:, 0], A[:, 1], 3)        # a cubic only to pick the curve's run in each column
    by = {}
    for r in rows:
        d = abs(r[1] - np.polyval(p, r[0]))
        if d < 10 and (r[0] not in by or d < by[r[0]][0]):
            by[r[0]] = (d, r[1])
    U = np.array(sorted(by), float)
    V = np.array([by[int(u)][1] for u in U])
    return U, V


def vfit(U, V, u, lo, hi, w=20):
    for ww in (w, 30, 45):
        a, b = max(lo, u - ww), min(hi, u + ww)
        if b - a < 2 * ww:     # near an interval end: keep the window inside the interval
            a, b = (lo, min(hi, lo + 2 * ww)) if u - lo < hi - u else (max(lo, hi - 2 * ww), hi)
        m = (U >= a) & (U <= b)
        if m.sum() >= 10:
            p = np.polyfit(U[m], V[m], 1)
            r = V[m] - np.polyval(p, U[m])
            return float(np.polyval(p, u)), float(np.sqrt(np.mean(r ** 2))), int(m.sum())
    raise SystemExit(f"no ink near u={u}")


def xval(u, v):
    return X.value(u, v)[0]


def find_u(U, V, segs, dr):
    u = 860 + dr * 1550
    for _ in range(40):
        seg = min(segs, key=lambda s: 0 if s[0] <= u <= s[1] else min(abs(u - s[0]), abs(u - s[1])))
        lo, hi = seg
        v, _, _ = vfit(U, V, min(max(u, lo), hi), lo, hi)
        du = (dr - xval(u, v)) / 0.000645
        u += du
        if abs(du) < 0.01:
            break
    return u


rows = []
for k, (cu, cv) in enumerate(CIRCLES, 1):
    note = ("single; open circle on the solid curve, cut by the phi = 45 grid line; centre from circle fits to the "
            "inner and outer ring edges (rays on the grid line dropped); bound widened from 2 px for the overlaps") if k == 1 else \
           ("single; open circle on the solid curve near its right end; centre from circle fits to the inner and outer "
            "ring edges; bound widened from 2 px for the overlap with the curve")
    rows.append(dict(series_id="data", point_kind="marker", sequence=k, pixel_u=round(cu, 1), pixel_v=round(cv, 1),
                     u_bound_px=3, v_bound_px=3, symbol="circle", note=note))

LNOTE = {"mean": "left end: the solid line's ink starts just left of the Dr = 0 grid line",
         "upper": "left end: the first dash starts at the Dr = 0 grid line (ink first seen at its right edge; the end may be under the line, the u bound covers the line width)",
         "lower": "left end: the first dash's ink starts just left of the Dr = 0 grid line"}
RNOTE = {"mean": "right end: the solid line's ink ends just right of the Dr = 1.0 grid line",
         "upper": "right end: the last dash ends at the Dr = 1.0 grid line (no ink right of it; the end may be under the line, the u bound covers the line width)",
         "lower": "right end: the last dash ends at the Dr = 1.0 grid line (no ink right of it; the end may be under the line, the u bound covers the line width)"}
for name in ("mean", "upper", "lower"):
    U, V = clean(name)
    segs = SEGS[name]
    first, last = segs[0], segs[-1]
    pts = []
    v0, _, _ = vfit(U, V, first[0], *first)
    pts.append((first[0], v0, 4 if name == "upper" else 3, 4, LNOTE[name]))
    for k in range(0, 21):
        dr = round(0.05 * k, 2)
        u = find_u(U, V, segs, dr)
        if u > last[1] + 0.5:
            break
        if u < first[0] or abs(u - first[0]) <= (4 if name == "upper" else 3):
            continue   # before the left end, or the left end itself (within its u bound): the end sample stands for it
        inside = [s for s in segs if s[0] <= u <= s[1]]
        if inside:
            lo, hi = inside[0]
            end_ub = 3 if name == "mean" else 4
            if abs(u - last[1]) <= end_ub:
                continue   # this Dr is the right end itself (within the end's u bound): the end sample stands for it
            v, rms, n = vfit(U, V, u, lo, hi)
            note = f"Dr {dr:.2f}"
            for xv, i0, sl in VL:
                if abs(u - (i0 + sl * v)) <= 6:
                    note += f"; at the crossing with the Dr = {xv:g} grid line, centre from the ink either side"
            for yv, i0, sl in HL:
                if abs(v - (i0 + sl * u)) <= 7:
                    note += f"; at the crossing with the phi = {yv:g} grid line, centre from the ink either side"
            pts.append((u, v, 2, 4, note))
        else:
            d, e, s = min((abs(u - e), e, s) for s in segs for e in s)
            v, _, _ = vfit(U, V, e, *s)
            why = GAP_WHY.get((name, e), "in a gap between dashes")
            pts.append((e, v, 3, 4, f"Dr {dr:.2f} falls {why} (u {u:.0f}); moved to the nearest line end on the ink, {d:.0f} px away (rule 7)"))
    ve, _, _ = vfit(U, V, last[1], *last)
    pts.append((last[1], ve, 3 if name == "mean" else 4, 4, RNOTE[name]))
    for i, (u, v, ub, vb, note) in enumerate(pts, 1):
        rows.append(dict(series_id=name, point_kind="trace", sequence=i, pixel_u=round(u, 1), pixel_v=round(v, 1),
                         u_bound_px=ub, v_bound_px=vb, symbol="", note=note))
    rows.append(dict(series_id=name, point_kind="feature", sequence=1, pixel_u=round(pts[0][0], 1), pixel_v=round(pts[0][1], 1),
                     u_bound_px=pts[0][2], v_bound_px=4, symbol="", note="first point (left end of the trace)"))
    rows.append(dict(series_id=name, point_kind="feature", sequence=2, pixel_u=round(pts[-1][0], 1), pixel_v=round(pts[-1][1], 1),
                     u_bound_px=pts[-1][2], v_bound_px=4, symbol="",
                     note="last point (right end of the trace; also its maximum, the curve rises monotonically; no knee: the slope changes gradually)"))
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
                                      "u_bound_px", "v_bound_px", "symbol", "note"], lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({"figure_id": "FC-22", "panel": 1, **r})
print(len(rows), "rows")
