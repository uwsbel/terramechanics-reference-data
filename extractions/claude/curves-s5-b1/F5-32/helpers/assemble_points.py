"""Assemble points-p<n>.csv (the reader's file: pixels, bounds, notes) from the trace samples
(trace-p<n>.csv, written by sample_trace.py) and the features read by eye on the centre line and the
page (listed below, each placed at a point of the centre line or at a measured end of the ink).

Role words (the first word of each feature note) follow the curve as drawn upright: `peak` is a local
maximum of the plotted curve and `knee, minimum` a local minimum, where up is the direction in which the
panel's printed labels grow in magnitude (compression on panels 1 and 3, whose labels run 0, -20, -40 ...
upwards; tension on panel 2, labels 0, +20, +40 upwards). On panels 1 and 3 a `peak` is therefore a local
minimum of the signed value as the scale gives it (the most negative), and a `knee, minimum` a local
maximum of it; each note gives the signed value too.

usage: assemble_points.py <helpers_dir> <out_dir>
"""
import csv
import sys
from pathlib import Path

import numpy as np

FEATURES = {
    1: ("strut3", [
        ((1357.0, 3500.0), None, "first: the trace's ink meets the bottom frame (t = 0) at the 0 lb line; the last 15 px before the frame run over the 0 lb grid line"),
        ((1277.5, 3406.0), None, "peak: sharp vertex of the first compression pulse, about -18 lb at t about 0.0057 s"),
        ((1374.5, 3298.0), None, "knee, minimum: the trace dips below the 0 lb line (about +5 lb as the scale gives it) at t about 0.012 s"),
        ((1334.5, 3205.0), None, "peak: small rounded maximum of compression, about -4.5 lb at t about 0.017 s"),
        ((1342.5, 3052.0), None, "knee, minimum: shallow, about -2 lb at t about 0.026 s"),
        ((1333.0, 2944.0), None, "peak: shallow, about -4 lb at t about 0.033 s"),
        ((1348.0, 2682.0), None, "knee, minimum: flat stretch on the 0 lb grid line from t about 0.043 to 0.055 s (trace merged with the grid line, its centre known to about 1.5 px); value about 0 lb, t of the minimum ill defined"),
        ((1228.0, 1885.0), None, "peak: rounded maximum of compression, about -26.5 lb at t about 0.095 s (beyond the last verified time line 0.09: extrapolated in t)"),
        ((1237.5, 1745.5), None, "last: top of the trace's ink, t about 0.103 s, beyond the printed 0.10 (extrapolated in t)"),
    ]),
    2: ("strut2", [
        ((1781.0, 3494.5), None, "first: the trace's ink meets the bottom frame (t = 0) at the 0 lb line; the last 15 px before the frame run over the 0 lb grid line"),
        ((1639.5, 3356.0), None, "peak: first tension maximum, about +32.6 lb at t about 0.0084 s"),
        ((1685.5, 3262.0), None, "knee, minimum: about +21.7 lb at t about 0.014 s"),
        ((1569.5, 2220.0), None, "peak: broad, nearly flat top, about +46.5 lb; the trace stays within 1 lb of it from t about 0.054 to 0.086 s, so its t is ill defined"),
        ((1573.0, 1954.0), None, "knee, minimum: shallow dip, about +45.0 lb at t about 0.091 s, before the final rise (1.4 lb below the broad top, about 6 px across the grid)"),
        ((1548.0, 1745.5), None, "last: top of the trace's ink, t about 0.103 s, beyond the printed 0.10 (extrapolated in t)"),
    ]),
    3: ("strut1", [
        ((2270.0, 3495.0), (18.0, 3.0), "first: the trace's ink runs into the bottom frame at u about 2252 and is hidden in the frame line from there to the corner with the 0 lb line (u 2288); it reaches t = 0 somewhere on that stretch (between about -8 lb and 0 lb), hence the wide u bound"),
        ((2123.5, 3434.0), None, "knee: end of the initial steep rise, where the trace turns onto the -40 lb grid line, about -39 lb at t about 0.0037 s (trace over the grid line)"),
        ((2105.5, 3307.0), None, "peak: about -43.0 lb at t about 0.011 s"),
        ((2128.0, 3135.0), None, "knee, minimum: about -37.3 lb at t about 0.021 s"),
        ((2020.5, 2274.0), None, "peak: broad flat top on the -60 lb grid line, about -60.5 lb; the trace stays within 0.5 lb of it from t about 0.063 to 0.079 s (merged with the grid line), so its t is ill defined"),
        ((2057.5, 1741.5), None, "last: top of the trace's ink, t about 0.103 s, beyond the printed 0.10 (extrapolated in t)"),
    ]),
}

COLS = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px",
        "v_bound_px", "symbol", "note"]


def main():
    hd, od = Path(sys.argv[1]), Path(sys.argv[2])
    for pn, (sid, feats) in FEATURES.items():
        with (hd / f"trace-p{pn}.csv").open(encoding="utf-8") as f:
            trace = list(csv.DictReader(f))
        with (hd / f"trace-p{pn}-polyline.csv").open(encoding="utf-8") as f:
            poly = list(csv.DictReader(f))
        P = np.array([[float(r["u"]), float(r["v"])] for r in poly])
        rows = []
        for r in trace:
            rows.append({k: r[k] for k in COLS})
        for k, ((u, v), bnd, note) in enumerate(feats, 1):
            if bnd is None:
                # half the trace's thickness across the line near the feature (clean centre-line points within 15)
                i = int(np.argmin(np.hypot(P[:, 0] - u, P[:, 1] - v)))
                near = [float(poly[j]["wp"]) for j in range(max(0, i - 15), min(len(poly), i + 16))
                        if poly[j]["wp"] not in ("", None) and poly[j]["flag"] == ""]
                b = (np.median(near) / 2 if near else 2.5)
                if "merged" in note or "over the grid line" in note or "over the 0 lb grid line" in note:
                    b += 1.0
                bu = bv = round(float(b), 1)
            else:
                bu, bv = bnd
            rows.append({"figure_id": "F5-32", "panel": pn, "series_id": sid, "point_kind": "feature", "sequence": k,
                         "pixel_u": u, "pixel_v": v, "u_bound_px": bu, "v_bound_px": bv, "symbol": "", "note": note})
        with (od / f"points-p{pn}.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"panel {pn}: {len(trace)} trace, {len(feats)} feature rows -> points-p{pn}.csv")


if __name__ == "__main__":
    main()
