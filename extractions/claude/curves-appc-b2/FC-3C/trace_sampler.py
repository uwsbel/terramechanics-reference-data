"""Trace and feature sampling of the upper-panel curves of FC-3C.

Each series' markers (markers-p1.csv) are the backbone: at every sampling column the curve's
expected v is interpolated between the neighbouring markers and the dark run (plot_grid.py
scan logic: columns u-1..u+1 combined) nearest that expectation is taken as the drawn line.
Columns are every 25 px (about 4.3 thousandths), moved off vertical gridlines and off the
series' own markers, and moved by a few px when they fall in a gap of the dashed line.
Steep first segments (first to second marker) are sampled along rows instead, where the
horizontal run is short and the line center is well determined.

Bounds: half the run thickness in the scanned direction (the line center is known to within
half its width), 2 px in the sampling direction. A run thicker than 1.6 times the series'
median line thickness is flagged (merged with a gridline, a marker, or a steep segment) and
keeps its honest half-thickness bound.

Features: first point (start of the drawn line, from a fine scan near the first marker), the
peak (minimum v of the drawn line, with u bound spanning the flat top), the last point (end
of the drawn line at the right).
"""
import csv, os, sys, json
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "..", "packet", "p0125.png")
CAL = json.load(open(os.path.join(HERE, "cal-p1", "calibration.json")))
G = np.array(Image.open(IMG).convert("L"))
DARK = 128

# vertical gridlines: u = u0 + slope*v
VLINES = [(l["u_at_v0"], l["slope_du_dv"]) for l in CAL["vertical_lines"]]
# horizontal gridlines: v = v0 + slope*u
HLINES = [(l["v_at_u0"], l["slope_dv_du"]) for l in CAL["horizontal_lines"]] if "horizontal_lines" in CAL else []


def runs(mask):
    idx = np.nonzero(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    start = prev = idx[0]
    for i in idx[1:]:
        if i != prev + 1:
            out.append((start, prev))
            start = i
        prev = i
    out.append((start, prev))
    return [((a + b) / 2.0, b - a + 1) for a, b in out]


def col_runs(u, v0, v1, hw=1):
    col = G[v0:v1, u - hw:u + hw + 1].min(axis=1) < DARK
    return [(c + v0, t) for c, t in runs(col)]


def row_runs(v, u0, u1, hw=1):
    row = G[v - hw:v + hw + 1, u0:u1].min(axis=0) < DARK
    return [(c + u0, t) for c, t in runs(row)]


def near_vline(u, v, tol=9):
    return any(abs(u - (a + b * v)) < tol for a, b in VLINES)


def interp_v(markers, u):
    us = [m[0] for m in markers]
    vs = [m[1] for m in markers]
    return float(np.interp(u, us, vs))


def pick(rs, vexp, tol=30, min_t=7):
    best = None
    for c, t in rs:
        if t < min_t:
            continue
        d = abs(c - vexp)
        if d < tol and (best is None or d < best[0]):
            best = (d, c, t)
    return best


def sample_series(sid, markers, step=14):
    markers = sorted(markers)
    pts = []  # (u, v, ub, vb, note, kind)
    u_first, v_first = markers[0]
    u_second, v_second = markers[1]
    u_last = markers[-1][0]
    # --- steep first segment: rows every 25 px between first and second marker
    v_top = min(v_first, v_second) + 18
    v_bot = max(v_first, v_second) - 18
    rows = list(range(int(v_bot), int(v_top), -step))
    for v in rows:
        rs = row_runs(v, int(u_first) - 15, int(u_second) + 15)
        uexp = float(np.interp(v, [v_second, v_first], [u_second, u_first]))
        best = None
        for c, t in rs:
            if t < 6:
                continue
            d = abs(c - uexp)
            if d < 35 and (best is None or d < best[0]):
                best = (d, c, t)
        if best is None:
            continue
        _, c, t = best
        pts.append((c, float(v), max(2.0, t / 2.0), 2.0, "row sample on the steep first segment", "trace"))
    # --- columns from just after the second marker's left side to the last marker
    u = int(u_second) - 16 if rows else int(u_first) + 12
    cols = []
    while u <= u_last - 4:
        cols.append(u)
        u += step
    def select(cols, excl, med_est):
        """columns moved off vertical gridlines and off the series' own markers (closer than
        `excl` px to a marker center); within 20 px of a marker a run is accepted only if its
        thickness is at most med_est + 5, so marker ink does not enter a sample."""
        thick, recs = [], []
        for u in cols:
            shifts = [0, 3, -3, 6, -6, 9, -9, 12, -12, 15, -15, 18, -18]
            chosen = None
            for s in shifts:
                uu = u + s
                vexp = interp_v(markers, uu)
                if near_vline(uu, vexp):
                    continue
                dm = min(abs(uu - mu) for mu, _ in markers)
                if dm < excl:
                    continue
                rs = col_runs(uu, int(vexp) - 60, int(vexp) + 60)
                best = pick(rs, vexp)
                if best is None:
                    continue
                if dm < 20 and med_est is not None and best[2] > med_est + 5:
                    continue
                chosen = (uu, best[1], best[2], s)
                break
            recs.append((u, chosen))
            if chosen is not None:
                thick.append(chosen[2])
        return recs, (float(np.median(thick)) if thick else 12.0)
    recs, med = select(cols, 20, None)          # pass 1: median line thickness
    recs, _ = select(cols, 14, med)              # pass 2: closer to markers, thickness-checked
    gaps = []
    for u, ch in recs:
        if ch is None:
            gaps.append(u)
            continue
        uu, c, t, s = ch
        note = ""
        vb = max(2.0, t / 2.0)
        if t > 1.6 * med:
            # merged with a horizontal gridline, marker, or steep: honest half-thickness bound
            note = "run %d px thick (median %d): merged with a gridline or steep here; bound is half the run" % (t, med)
        elif s:
            note = "column moved %+d px off a gridline, marker or dash gap" % s
        pts.append((float(uu), c, 2.0, vb, note, "trace"))
    pts.sort(key=lambda p: p[0])
    # drop near-duplicate columns produced by the shifts (within 4 px of the previous sample)
    kept = []
    for p in pts:
        if kept and abs(p[0] - kept[-1][0]) < 4 and p[5] == kept[-1][5]:
            continue
        kept.append(p)
    pts = kept
    # a run whose extent reaches a horizontal gridline may include the gridline's ink
    HL = [(l["y_value"], l["v_at_u0"], l["slope_dv_du"]) for l in CAL["horizontal_lines"]]
    out = []
    for (u, v, ub, vb, note, kind) in pts:
        if kind == "trace" and note.startswith("row sample") is False:
            for y, v0, sl in HL:
                vg = v0 + sl * u
                if abs(vg - v) < vb + 5:
                    note = (note + "; " if note else "") + "run touches the %d psf gridline (fitted v=%.1f), may include its ink" % (y, vg)
                    vb = max(vb, 5.0)
                    break
        out.append((u, v, ub, vb, note, kind))
    return out, med, gaps


def features(sid, markers, med):
    markers = sorted(markers)
    out = []
    u_first, v_first = markers[0]
    # first point: leftmost column where a curve run exists near the first marker's v,
    # scanning columns left of the first marker
    start = None
    for u in range(int(u_first) - 30, int(u_first) + 30):
        rs = col_runs(u, int(v_first) - 80, int(v_first) + 40)
        if any(t >= 6 for _, t in rs):
            start = u
            break
    out.append((u_first, v_first, 4.0, 4.0, "first point: the drawn line begins at the first marker (checked on the zoom-3 tiles)", "feature"))
    # peak: fine column scan from second marker to last marker
    best = None
    rows = []
    for u in range(int(markers[1][0]) - 10, int(markers[-1][0]), 2):
        vexp = interp_v(markers, u)
        if near_vline(u, vexp, tol=7) or any(abs(u - mu) < 20 for mu, _ in markers):
            continue
        rs = col_runs(u, int(vexp) - 60, int(vexp) + 60)
        b = pick(rs, vexp, tol=30, min_t=7)
        if b is None or b[2] > 1.6 * med:
            continue
        rows.append((u, b[1], b[2]))
    vs = np.array([r[1] for r in rows])
    us = np.array([r[0] for r in rows])
    vmin = vs.min()
    sel = vs <= vmin + 4.0
    flat = us[sel]
    u_pk = float(flat.mean())
    v_pk = float(np.median(vs[sel]))
    ub = max(2.0, (flat.max() - flat.min()) / 2.0)
    print(sid, "peak scan: vmin %.1f at u=%d; flat (<= vmin+4) u %d..%d, n=%d, median v %.1f" % (vmin, us[vs.argmin()], flat.min(), flat.max(), sel.sum(), v_pk))
    out.append((u_pk, v_pk, ub, max(2.0, med / 2.0) + 2.0, "peak of the drawn line (dashed, so the top is read as the region within 4 px of the minimum v, u %d to %d; u bound spans it, v is the median there)" % (flat.min(), flat.max()), "feature"))
    # last point: rightmost ink of the line at the right end, scanning columns to the right of the last marker
    u_last, v_last = markers[-1]
    end = None
    for u in range(int(u_last) + 40, int(u_last) - 30, -1):
        if near_vline(u, v_last, tol=8):
            continue
        rs = col_runs(u, int(v_last) - 30, int(v_last) + 30)
        if any(t >= 6 for _, t in rs):
            end = u
            break
    out.append((u_last, v_last, 4.0, 4.0, "last point: the drawn line ends at the last marker at x=250 (rightmost line ink at u=%s; the legend symbol sits here too)" % end, "feature"))
    return out


def main():
    mk = list(csv.DictReader(open(os.path.join(HERE, "markers-p1.csv"), newline="", encoding="utf-8")))
    series = {}
    for r in mk:
        series.setdefault((r["series_id"], r["symbol"]), []).append((float(r["pixel_u"]), float(r["pixel_v"])))
    out = []
    for (sid, sym), markers in series.items():
        pts, med, gaps = sample_series(sid, markers)
        print(sid, "trace samples", len(pts), "median thickness", med, "columns with no line ink within +-18 px (dropped):", gaps)
        for i, (u, v, ub, vb, note, kind) in enumerate(pts, 1):
            k = "trace"
            out.append(["FC-3C", 1, sid, k, i, "%.1f" % u, "%.1f" % v, "%.1f" % ub, "%.1f" % vb, "", note])
        for i, (u, v, ub, vb, note, kind) in enumerate(features(sid, markers, med), 1):
            out.append(["FC-3C", 1, sid, "feature", i, "%.1f" % u, "%.1f" % v, "%.1f" % ub, "%.1f" % vb, "", note])
    with open(os.path.join(HERE, "traces-p1.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"])
        w.writerows(out)
    # points-p1.csv = markers (markers-p1.csv) followed by traces and features
    with open(os.path.join(HERE, "points-p1.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"])
        for r in mk:
            w.writerow([r[k] for k in ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]])
        w.writerows(out)


if __name__ == "__main__":
    main()
