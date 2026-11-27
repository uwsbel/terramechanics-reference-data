"""Assemble out/FC-18/points-p1.csv from the circle readings, the sampled traces and the end points read on
the page (FC-18 blind reading helper). Run from the workspace root.
"""
import csv
from pathlib import Path

OUT = Path("out/FC-18")
FIG = "FC-18"
rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append({"figure_id": FIG, "panel": 1, "series_id": series, "point_kind": kind, "sequence": seq,
                 "pixel_u": u, "pixel_v": v, "u_bound_px": bu, "v_bound_px": bv, "symbol": symbol, "note": note})


# circles, in order of Dr; centres from the ring (outer and inner edges on 8x to 10x crops, checked against
# fit_circle.py), see notes.md
circles = [
    (891.5, 2418.0, 3, 3, "pair 1 left; on the x = 0 grid line, the joining line leaves it to the right and the "
                          "first dash of the upper dashed curve meets its ring at the upper right"),
    (927.5, 2538.5, 3, 3, "single; overlaps the circle above-right of it (sequence 4) and touches the solid curve "
                          "at its upper left"),
    (931.5, 2616.0, 3, 3, "single; the first dash of the lower dashed curve passes through it"),
    (946.5, 2515.5, 4, 4, "single; the solid curve passes across its top and it overlaps the circle below-left of "
                          "it (sequence 2); ring drawn slightly wider than tall"),
    (1110.0, 2413.0, 3, 3, "pair 1 right; the solid curve passes through it and the joining line enters it from "
                           "the left"),
    (2447.5, 1727.0, 2, 3, "single; the x = 1.0 grid line passes through its centre; ring slightly taller (42 px) "
                           "than wide (37 px)"),
]
for i, (u, v, bu, bv, note) in enumerate(circles, 1):
    add("data", "marker", i, u, v, bu, bv, "circle", note)

ends = {
    "upper": {
        "first": (905.0, 2398.0, 3.0, 4.5, "left end: the first dash's ink emerges from the ring of the pair 1 left "
                                           "circle at its upper right (it may continue under the ring)"),
        "last": (2594.0, 1605.0, 3.0, 4.5, "right end: the last dash runs into the right frame (inner edge u 2595)"),
    },
    "mean": {
        "first": (897.0, 2526.5, 4.0, 4.5, "left end: the ink meets the right edge of the x = 0 grid line (it may "
                                           "begin under the grid line, centre u 892)"),
        "last": (2596.0, 1737.5, 3.0, 5.0, "right end: the curve runs into the right frame (inner edge u 2597); the "
                                           "line is slightly thicker over its last 25 px"),
    },
    "lower": {
        "first": (898.5, 2638.5, 4.0, 4.5, "left end: the ink meets the right edge of the x = 0 grid line (it may "
                                           "begin under the grid line, centre u 893.5)"),
        "last": (2597.0, 1884.5, 3.0, 5.0, "right end: the last dash merges with the y = 45 grid line from about u "
                                           "2560 to the right frame (inner edge u 2598); centre from the dash's own "
                                           "line and its ink showing above the grid line (v 1880 to 1883)"),
    },
}
overrides = {
    ("upper", 0.65): (1917.5, 1882.5, 3.7, 4.0,
                      "Dr 0.65 (u 1900.7) falls in the gap around the y = 45 grid line (dash ends u 1872, next dash "
                      "starts u 1917); moved to the nearest dash start, read on the page (ink v 1880.6 to 1885.6), "
                      "just above the grid line"),
    ("lower", 0.45): (1611.5, 2284.0, 4.0, 4.5,
                      "Dr 0.45 (u 1591.9) falls in a gap (dash ends u 1567, next dash starts u 1610 on the y = 40 grid "
                      "line); moved to the nearest dash start, read on the page: its tip shows below the grid line "
                      "(v 2280 to 2288)"),
}
vgrid_dr = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0}
hcross = {("upper", 0.15): "on the crossing with the y = 40 grid line; centre from the dash on the left of the crossing",
          ("mean", 0.30): "on the crossings with the x = 0.3 and y = 40 grid lines; centre from the line on both sides",
          ("mean", 0.85): "next to the crossing with the y = 45 grid line (u 2167 to 2211); centre from the line on both sides"}
features = []
for name in ("upper", "mean", "lower"):
    seq = 1
    f, l = ends[name]["first"], ends[name]["last"]
    add(name, "trace", seq, f[0], f[1], f[2], f[3], "", f[4]); seq += 1
    with (OUT / "work" / f"samp_{name}.csv").open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = round(float(r["target_dr"]), 2)
            if (name, d) in overrides:
                u, v, bu, bv, note = overrides[(name, d)]
            else:
                u, v, bu, bv, note = float(r["u"]), float(r["v"]), float(r["u_bound"]), float(r["v_bound"]), r["note"]
                extra = []
                if not note and d in vgrid_dr:
                    extra.append(f"Dr {d:.2f}: on the x = {d:g} grid line; centre from the line on both sides of it")
                elif not note:
                    extra.append(f"Dr {d:.2f}")
                if (name, d) in hcross:
                    extra.append(hcross[(name, d)])
                if name == "mean" and d == 0.05:
                    extra.append("just right of the circle the solid curve crosses (u 927 to 966)")
                if d > 1.0:
                    extra.append("beyond the x = 1.0 grid line (extrapolated)")
                note = "; ".join([note] + extra if note else extra)
            add(name, "trace", seq, u, v, bu, bv, "", note); seq += 1
    add(name, "trace", seq, l[0], l[1], l[2], l[3], "", l[4] + "; beyond the x = 1.0 grid line (extrapolated)")
    features.append((name, f, l))
for name, f, l in features:
    add(name, "feature", 1, f[0], f[1], f[2], f[3], "", "first point of the trace")
    add(name, "feature", 2, l[0], l[1], l[2], l[3], "", "last point of the trace, at the right frame; also its maximum "
                                                       "(the curve rises monotonically, no knee)")
with (OUT / "points-p1.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
from collections import Counter
print(Counter((r["series_id"], r["point_kind"]) for r in rows))
