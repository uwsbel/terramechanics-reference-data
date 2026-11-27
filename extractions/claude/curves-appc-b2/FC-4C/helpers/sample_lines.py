"""Sample the drawn lines of the upper panel at chosen columns, guided by each series' markers.

    python sample_lines.py <image> <calibration.json> <markers.csv> <out.csv> [--tol 15]

For each series a guide polyline is built through its marker centres plus the extra guide points
listed in GUIDE (places where the drawn line leaves the marker interpolation, read off the zoomed
crops). At each sample column (x = 7.5, 12.5, ... thousandths, never on a vertical gridline) the
dark runs of the column (dark in all of u-1..u+1) are listed and the run nearest the guide within
`tol` px is the line; if none (dash gap) the column is shifted by up to 8 px. Dense columns every
2 px give the first point, the peak (smallest v) and the last point of each line. Rows carry notes
where another series' guide is within 20 px (possible shared ink) or where the run is thick (the
line crosses a symbol, a gridline or another line). The overlay is then checked by eye.
"""
import argparse
import csv
import json

import numpy as np
from PIL import Image

FIG = "FC-4C"
SERIES = ["n4695", "n3815", "n2934", "n1761", "n741"]
# extra guide points (u, v) read off the zoom-3 crops where the line departs from the markers
GUIDE = {
    "n4695": [(1010, 1432), (1033, 1422), (1060, 1430)],
    "n3815": [(1000, 1455)],
    "n2934": [(1085, 1655)],
    "n1761": [],
    "n741": [(1015, 2105)],
}
# where the line starts and ends (u range to search), from the crops. n4695: no line is drawn
# between its first plus (807,1776) and its second (864,1690); the only ink there is the n3815
# dash (zoom-5 crop p1-start-lines.png), so the n4695 line is taken to begin at the second plus.
RANGE = {"n4695": (878, 2240), "n3815": (800, 2240), "n2934": (800, 2240), "n1761": (805, 2240), "n741": (805, 2240)}
# markers left out of the guide polyline (the drawn line does not pass through them)
NO_GUIDE = {"n4695": [(806.5, 1775.5)]}
GRID_U = [747.3, 1039.9, 1334.9, 1624.1, 1916.6, 2201.4]  # u at v=0 of the vertical gridlines (cal-p1), slope 0.0085


def grid_u_at(v):
    return [g + 0.0085 * v for g in GRID_U]


def runs(dark, v0):
    idx = np.where(dark)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append(((s + p) / 2 + v0, p - s + 1))
            s = i
        p = i
    out.append(((s + p) / 2 + v0, p - s + 1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("calibration")
    ap.add_argument("markers")
    ap.add_argument("out")
    ap.add_argument("--tol", type=float, default=15)
    ap.add_argument("--vband", type=int, nargs=2, default=[1300, 2500])
    a = ap.parse_args()
    g = np.asarray(Image.open(a.image).convert("L"))
    cal = json.load(open(a.calibration, encoding="utf-8"))
    ax = cal["ax"]
    mk = {s: [] for s in SERIES}
    for r in csv.DictReader(open(a.markers, encoding="utf-8-sig", newline="")):
        if r["point_kind"] == "marker":
            mk[r["series_id"]].append((float(r["pixel_u"]), float(r["pixel_v"])))
    guide = {}
    for s in SERIES:
        pts = sorted([p for p in mk[s] if p not in NO_GUIDE.get(s, [])] + GUIDE[s])
        guide[s] = (np.array([p[0] for p in pts]), np.array([p[1] for p in pts]))

    def gv(s, u):
        gu, gvv = guide[s]
        # linear interpolation; held at the end values outside the marker range (no extrapolation:
        # the steep extrapolation at the start ran into horizontal gridlines)
        return float(np.interp(u, gu, gvv))

    HGRID = [(1326.6, -0.0038), (1617.5, -0.0040), (1913.0, -0.0038), (2199.0, -0.0036), (2492.7, -0.0033)]

    def on_hgrid(u, c, t):
        return t <= 9 and any(abs(c - (i + sl * u)) <= 4 for i, sl in HGRID)

    def in_marker(s, u, r=12):
        return any(abs(u - mu) <= r for mu, mv in mk[s])

    def column_runs(u):
        ui = int(round(u))
        col = g[a.vband[0]:a.vband[1], ui - 1:ui + 2] < 128
        return runs(col.all(axis=1), a.vband[0])

    def pick(s, u, tol):
        exp = gv(s, u)
        best = None
        for c, t in column_runs(u):
            if on_hgrid(u, c, t):
                continue
            if 3 <= t <= 60 and abs(c - exp) <= tol and (best is None or abs(c - exp) < abs(best[0] - exp)):
                best = (c, t)
        return best

    def near_grid(u, v):
        return any(abs(u - gu) <= 7 for gu in grid_u_at(v))

    rows = []
    report = []
    for s in SERIES:
        u_lo, u_hi = RANGE[s]
        # dense scan for features
        dense = []
        u_lo = max(u_lo, int(min(guide[s][0])) + 15)  # the line begins at the first symbol it passes through
        for u in range(u_lo, u_hi + 1, 2):
            if in_marker(s, u, 14) or near_grid(u, gv(s, u)):
                continue
            b = pick(s, u, a.tol)
            if b:
                dense.append((u, b[0], b[1]))
        first, last = dense[0], dense[-1]
        peak = min(dense, key=lambda d: d[1])
        # samples every 5 thousandths at x = 7.5, 12.5, ...
        seq = 0
        x = 7.5
        missing = []
        while True:
            u = (x - ax[1] * gv(s, 1900) - ax[2]) / ax[0]
            u = (x - ax[1] * gv(s, u) - ax[2]) / ax[0]
            if u > last[0] + 3:
                break
            if u < first[0] - 3:
                x += 5
                continue
            chosen = None
            tainted = None
            for du in [0, -2, 2, -4, 4, -6, 6, -8, 8, -10, 10, -12, 12, -14, 14]:
                uu = u + du
                if in_marker(s, uu, 14):
                    continue
                b = pick(s, uu, a.tol)
                if b:
                    # a run that touches a horizontal gridline is the line crossing the gridline:
                    # its centre is biased toward the gridline, so prefer a clean column nearby
                    if any(abs(b[0] - (i + sl * uu)) <= b[1] / 2 + 1 for i, sl in HGRID) and b[1] <= 24:
                        if tainted is None:
                            tainted = (uu, b[0], b[1])
                        continue
                    chosen = (uu, b[0], b[1])
                    break
            crosses = False
            if chosen is None and tainted is not None:
                chosen, crosses = tainted, True
            if chosen is None:
                missing.append(x)
                x += 5
                continue
            uu, c, t = chosen
            seq += 1
            bound = max(2, int(np.ceil(t / 2)))
            note = f"drawn line sampled near x={x:g}"
            others = [o for o in SERIES if o != s and abs(gv(o, uu) - c) <= 20]
            if others:
                note += "; within 20 px of the " + ",".join(others) + " line (shared or adjacent ink possible)"
                bound = max(bound, int(np.ceil(t)))
            if crosses:
                note += "; line crossing a horizontal gridline here (run merged with the gridline, bound widened)"
                bound = max(bound, int(np.ceil(t)))
            if t >= 16:
                note += f"; thick run ({t:g} px: steep segment, or line over a symbol or gridline)"
            rows.append(dict(figure_id=FIG, panel=1, series_id=s, point_kind="trace", sequence=seq,
                             pixel_u=f"{uu:.1f}", pixel_v=f"{c:.1f}", u_bound_px=2, v_bound_px=bound, symbol="", note=note))
            x += 5
        for k, (d, what) in enumerate([(first, "first point of the drawn line (first ink column outside the first symbol)"),
                                       (peak, "peak of the drawn line (highest ink column outside symbols)"),
                                       (last, "last point of the drawn line (last ink column before the right end)")], 1):
            bound = max(2, int(np.ceil(d[2] / 2)))
            rows.append(dict(figure_id=FIG, panel=1, series_id=s, point_kind="feature", sequence=k,
                             pixel_u=f"{d[0]:.1f}", pixel_v=f"{d[1]:.1f}", u_bound_px=3, v_bound_px=bound, symbol="", note=what))
        report.append(f"{s}: {seq} trace samples; first ({first[0]},{first[1]:.1f}) peak ({peak[0]},{peak[1]:.1f}) last ({last[0]},{last[1]:.1f}); missing x={missing}")
    cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("\n".join(report))


main()
