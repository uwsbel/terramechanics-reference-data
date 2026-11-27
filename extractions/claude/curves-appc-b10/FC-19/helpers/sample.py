"""Trace samples, features and markers of Fig. C-19 (FC-19), Claude reader, panel 1.

Uses the per-column centerlines written by centerline.py. In every column only "clean" ink counts:
a run not touching a masked grid line, no longer than 11 px, and within 3 px of a robust quadratic
fit of its own dash (or of a 120 px window of the solid curve). The line's v at a column u is a
local linear fit over the clean columns within 12 px of u, on the same dash, so a sample at a
vertical grid line (where the curve's ink is merged with the grid line's) is the drawn line's
position through the grid line, read from the ink on both sides of it.

Dr targets 0.05 k are placed with the piecewise x map of cal-p1 (tools/calibrate_axes.py, imported
read-only). A dashed-curve target falling in a gap between dashes moves to the nearest dash end,
on the ink (rule 7). The dash extents and the curve ends were read on pixel dumps and zoomed crops
(see notes.md); they are listed here, not detected.
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import calibrate_axes as ca  # noqa: E402  (read-only use of the tool's piecewise map)

IMG = ROOT / "packet" / "p0155.png"

# Extents of ink (first and last column of each dash, or of the solid curve), read on pixel dumps.
DASHES = {
    "upper": [(966, 1103), (1161, 1316), (1367, 1523), (1560, 1728), (1788, 1929), (1976, 2133),
              (2173, 2323), (2378, 2515)],
    "lower": [(969, 1145), (1193, 1354), (1398, 1572), (1641, 1811), (1868, 1993), (2032, 2166),
              (2213, 2347), (2378, 2522)],
    "mean": [(990, 2503)],     # clean ink right of the circle ring up to the x = 1.0 grid line
}

# Curve ends read by eye on pixel dumps (u, v, u_bound, v_bound, note).
ENDS = {
    "upper": {
        "first": (961.0, 2118.0, 3.0, 4.5,
                  "first point: left end of the first dash; its ink merges with the x = 0 grid line "
                  "(grid line ink u 959 to 962), no ink left of the grid line; u bound covers the grid line"),
        "last": (2514.0, 1360.0, 2.0, 4.0,
                 "last point: right end of the last dash, which crosses the x = 1.0 grid line and ends "
                 "about 5 px right of it; also the maximum of the trace"),
    },
    "lower": {
        "first": (963.5, 2325.5, 3.0, 4.5,
                  "first point: left end of the first dash; its ink merges with the x = 0 grid line "
                  "(grid line ink u 962 to 965), no ink left of the grid line; u bound covers the grid line"),
        "last": (2521.0, 1529.0, 2.0, 4.0,
                 "last point: right end of the last dash, which crosses the x = 1.0 grid line and ends "
                 "about 10 px right of it; also the maximum of the trace"),
    },
    "mean": {
        "first": (965.0, 2223.5, 4.0, 5.0,
                  "first point: the line's ink is visible inside the left circle (lower half of its hole, "
                  "from u 969) and is merged with the circle's ring and the x = 0 grid line further left; "
                  "its start lies between the grid line (u about 961) and u 969, bound covers that"),
        "last": (2507.5, 1439.0, 3.0, 5.0,
                 "last point: the line runs into the x = 1.0 grid line (grid ink u 2507 to 2510) and no "
                 "ink appears right of it; the end is hidden in the grid line, bound covers it; also the "
                 "maximum of the trace"),
    },
}

STEP = 0.05


def load_centerline(name):
    rows = []
    with (HERE / f"centerline-{name}.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["v_center"] == "" or r["flag"] != "" or int(r["run_px"]) > 11:
                continue
            rows.append((int(r["u"]), float(r["v_center"]), int(r["run_px"])))
    return rows


def clean_by_segment(rows, segs, window=None):
    """Keep the columns inside each segment that lie within 3 px of a robust quadratic fit of it."""
    keep = []
    for (a, b) in segs:
        pts = np.array([(u, v, w) for (u, v, w) in rows if a <= u <= b], float)
        if window:
            chunks = [(lo, min(lo + window, b)) for lo in range(a, b + 1, window)]
        else:
            chunks = [(a, b)]
        for lo, hi in chunks:
            sel = pts[(pts[:, 0] >= lo - 20) & (pts[:, 0] <= hi + 20)]
            if len(sel) < 5:
                continue
            for _ in range(3):
                c = np.polyfit(sel[:, 0], sel[:, 1], 2)
                res = sel[:, 1] - np.polyval(c, sel[:, 0])
                ok = np.abs(res) <= 3.0
                if ok.all():
                    break
                sel = sel[ok]
            inside = sel[(sel[:, 0] >= lo) & (sel[:, 0] < hi + (1 if hi == b else 0))]
            keep.extend((int(u), float(v), int(w), (a, b)) for u, v, w in inside)
    keep.sort()
    return keep


def v_at(clean, seg, u, half=12):
    pts = np.array([(uu, vv) for (uu, vv, _, s) in clean if s == seg and abs(uu - u) <= half], float)
    if len(pts) < 4:
        pts = np.array([(uu, vv) for (uu, vv, _, s) in clean if s == seg and abs(uu - u) <= 2 * half], float)
    c = np.polyfit(pts[:, 0], pts[:, 1], 1)
    return float(np.polyval(c, u)), float(c[0])


def seg_of(segs, u):
    for s in segs:
        if s[0] <= u <= s[1]:
            return s
    return None


def solve_u(X, clean, segs, target, u_lo, u_hi):
    """u where the curve (continued straight across gaps) crosses the line of constant Dr = target."""
    def f(u):
        s = seg_of(segs, u) or min(segs, key=lambda s: min(abs(u - s[0]), abs(u - s[1])))
        v, _ = v_at(clean, s, min(max(u, s[0]), s[1]))
        if not (s[0] <= u <= s[1]):
            v2, k = v_at(clean, s, min(max(u, s[0]), s[1]))
            v = v2 + k * (u - min(max(u, s[0]), s[1]))
        return X.value(u, v)[0] - target, v
    a, b = u_lo, u_hi
    fa, _ = f(a)
    for _ in range(60):
        m = 0.5 * (a + b)
        fm, _ = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def main():
    cal, X, Y = ca.piecewise_maps(str(OUT / "cal-p1"), str(IMG))
    rows_out = []
    thickness = {}
    for name in ("mean", "upper", "lower"):
        segs = DASHES[name]
        raw = load_centerline(name)
        clean = clean_by_segment(raw, segs, window=120 if name == "mean" else None)
        runs = np.array([w for (_, _, w, _) in clean], float)
        slopes = [v_at(clean, s, 0.5 * (s[0] + s[1]), half=40)[1] for s in segs]
        cosang = np.cos(np.arctan(np.median(np.abs(slopes))))
        perp = float(np.median(runs)) * cosang
        half_t = np.ceil(perp / 2 * 2) / 2          # half the line thickness, rounded up to 0.5 px
        thickness[name] = (float(np.median(runs)), perp, half_t)
        first, last = ENDS[name]["first"], ENDS[name]["last"]
        u_first, u_last = first[0], last[0]
        x_first = X.value(u_first, first[1])[0]
        x_last = X.value(u_last, last[1])[0]
        samples = [(u_first, first[1], first[2], first[3], "left end of the trace (" + first[4].split(":")[0] + ")")]
        k0 = int(np.ceil(x_first / STEP - 1e-9))
        used = set()
        for k in range(k0, int(np.floor(x_last / STEP + 1e-9)) + 1):
            t = round(k * STEP, 2)
            u = solve_u(X, clean, segs, t, segs[0][0] - 40, segs[-1][1] + 40)
            if abs(u - u_first) <= 3 or abs(u - u_last) <= 3:
                continue          # the curve's end is this sample
            s = seg_of(segs, u)
            if s is None:
                # in a gap: move to the nearest dash end, on the ink
                cands = [(abs(u - e), e, ss) for ss in segs for e in ss]
                _, e, ss = min(cands)
                key = (ss, e)
                if key in used:
                    continue
                used.add(key)
                ue = e - 1.5 if e == ss[1] else e + 1.5
                v, _ = v_at(clean, ss, ue)
                side = "right" if e == ss[1] else "left"
                note = f"Dr {t:.2f} falls in a gap between dashes; moved to the nearest dash end ({side} end of the dash u {ss[0]} to {ss[1]})"
                samples.append((ue, v, half_t, half_t, note))
            else:
                v, _ = v_at(clean, s, u)
                gridline = abs(t * 10 - round(t * 10)) < 1e-6
                note = f"Dr {t:.2f}"
                if gridline:
                    note += "; on a vertical grid line, line position read from its ink on both sides"
                samples.append((u, v, half_t, half_t, note))
        samples.append((u_last, last[1], last[2], last[3], "right end of the trace (" + last[4].split(":")[0] + ")"))
        samples.sort(key=lambda s: s[0])   # drawing order = left to right for these monotone curves
        for i, (u, v, bu, bv, note) in enumerate(samples, 1):
            rows_out.append({"series_id": name, "point_kind": "trace", "sequence": i, "pixel_u": round(u, 1),
                             "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv, "symbol": "",
                             "note": note})
        for i, (tag, e) in enumerate((("first", first), ("last", last)), 1):
            rows_out.append({"series_id": name, "point_kind": "feature", "sequence": i, "pixel_u": e[0],
                             "pixel_v": e[1], "u_bound_px": e[2], "v_bound_px": e[3], "symbol": "",
                             "note": e[4]})
    # markers, read on pixel dumps (centers from the outer extents of the rings)
    markers = [
        (971.0, 2214.0, 3.0, 3.0,
         "single; open circle (outer ring u 953 to 989, v 2195 to 2233, center from the outer extents); "
         "the x = 0 grid line runs through its left part and the solid curve through the lower half of "
         "its hole, so the hole cannot be used and the bound is widened to 3 px"),
        (2433.0, 1428.5, 2.0, 2.0,
         "single; open circle (outer ring u 2415 to 2452, v 1409 to 1447, hole center 2432.5, 1428.5); "
         "clean, touches no line"),
    ]
    for i, (u, v, bu, bv, note) in enumerate(markers, 1):
        rows_out.append({"series_id": "data", "point_kind": "marker", "sequence": i, "pixel_u": u, "pixel_v": v,
                         "u_bound_px": bu, "v_bound_px": bv, "symbol": "circle", "note": note})
    order = {"data": 0, "mean": 1, "upper": 2, "lower": 3}
    kind = {"marker": 0, "trace": 1, "feature": 2}
    rows_out.sort(key=lambda r: (order[r["series_id"]], kind[r["point_kind"]], r["sequence"]))
    cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px",
            "v_bound_px", "symbol", "note"]
    with (OUT / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows_out:
            w.writerow({"figure_id": "FC-19", "panel": 1, **r})
    for k, (run, perp, h) in thickness.items():
        print(f"{k}: median vertical run {run:.1f} px, perpendicular thickness {perp:.1f} px, bound {h} px")
    from collections import Counter
    print(Counter((r["series_id"], r["point_kind"]) for r in rows_out))


if __name__ == "__main__":
    sys.exit(main())
