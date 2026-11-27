"""Assemble points-p1.csv for Fig. 4-20 from the automatic trace samples (helpers/auto.csv) and the
samples and features read by hand on zoomed crops (below). Rows are ordered per series in drawing
order by their arc length along the series' dense trace (helpers/dense.csv).

usage: build_points.py <auto.csv> <dense.csv> <out points-p1.csv>
"""
import csv
import sys

import numpy as np

STYLE = {"run4": "solid", "run10": "dotted", "run12": "dashed"}

FIRST_NOTE = ("first: the three traces start together in the ink at the origin corner, merged with each other "
              "and with the frame (displacement 0 and force 0 lines); the first point is where that merged ink meets "
              "the force = 0 frame line, about 6 px of trace ink above the frame; the same point for the three series, "
              "not separable by series; wide bound")

# auto rows removed (series, pixel_u, pixel_v) -> reason
DROP = {
    ("run10", 2001.3, 3762.1): "the automatic F = 100 lb sample of Run 10 landed on the Run 4 line where the two run together; replaced by a hand reading",
    ("run4", 1952.7, 2628.1): "the automatic x = 1.9 in sample of Run 4 took in the 100 lb grid line merged on its right; replaced by a hand reading",
}

# hand readings: series, kind, u, v, bu, bv, arc (drawing-order position), note
MANUAL = [
    # Run No. 12, long dashes
    ("run12", "feature", 2276, 3793, 7, 7, 1, FIRST_NOTE),
    ("run12", "trace", 2276, 3793, 7, 7, 1, "trace start, at the first point (merged ink at the origin corner; see the first feature)"),
    ("run12", "trace", 2122, 3791, 10, 5, 152, "sample for F = 50 lb; the dash lies on the frame line and Run 4 and Run 10 touch it from above; "
     "centre between the dash's upper edge (v 3784) plus half a dash width and the frame's upper edge (v 3797.5) less half a dash width; "
     "the dash gaps at u 2086 to 2110 and 2152 to 2168 show the frame alone; bound widened along the line to half the gap"),
    ("run12", "feature", 455, 3578, 5, 6, 1846, "peak: the apex where the loading dash and the unloading dash meet (largest force of the run); "
     "centre half a line width inside the ink's leftmost edge (u 451)"),
    ("run12", "trace", 2252.5, 3283, 5, 5, 3685, "added at the turn from unloading to the rebound (bottom of the near-vertical stroke), so the trace keeps its shape"),
    ("run12", "feature", 2252, 3268, 5, 18, 3700, "knee, minimum: the force is flat at its minimum along the near-vertical stroke from v 3250 to 3286 "
     "(its location along x is not an observation); the trace turns here from unloading to the rebound"),
    ("run12", "feature", 2083.7, 3055.5, 5, 5, 3998, "peak: second local maximum of the force, at the left end of the hook, before the force falls at the largest displacement"),
    ("run12", "feature", 2204, 3023, 4, 5, 4125, "last: right end of the last dash (end of the trace; the force has fallen at the largest displacement)"),
    ("run12", "trace", 2204, 3023, 4, 5, 4125, "trace end, at the last point (right end of the last dash)"),
    # Run No. 10, dotted
    ("run10", "feature", 2276, 3793, 7, 7, 1, FIRST_NOTE),
    ("run10", "trace", 2276, 3793, 7, 7, 1, "trace start, at the first point (merged ink at the origin corner; see the first feature)"),
    ("run10", "trace", 2100, 3779, 6, 7.5, 170, "sample for F = 50 lb (about 60 lb, the nearest clean ink: at the 50 lb line Run 12 and the grid line merge in); Run 4 and Run 10 run together here (one band of ink, v 3772 to 3786, "
     "between u about 2050 and the origin) and cannot be told apart; centre of the band, bound covering the whole band; the same pixel as Run 4's sample"),
    ("run10", "trace", 1959, 3763.5, 8, 6, 316, "sample for F = 100 lb (about 105 lb); the dot merges with the Run 4 line above it; centre taken "
     "half a dot (5 px) above the dot's lower edge (v 3768.5); bound widened along the line to half the gap"),
    ("run10", "feature", 1406.9, 3616.4, 5, 6, 888, "peak: the corner dot at the end of loading (largest force of the run); "
     "the dots then rise nearly at constant force to the next corner"),
    ("run10", "feature", 1430.7, 3521.3, 5, 5, 986, "knee: corner dot where the near-constant-force stretch turns into the unloading branch"),
    ("run10", "feature", 1857, 3126, 5, 5, 1581, "knee: kink in the unloading branch at the lower end of a short stretch of closely spaced dots; "
     "the slope on the page changes from about -2.6 to -1.25"),
    ("run10", "feature", 2087.9, 2862.4, 5, 8, 1933, "knee, minimum: corner dot where the trace turns to nearly constant force; the force is lowest here "
     "and rises slightly (by about 6 lb) to the second peak"),
    ("run10", "trace", 2085.0, 2813.8, 5, 5, 1977, "last dot before the scan dropout (no ink, grid lines included, from about x 1.6 to 1.96 in); "
     "x = 1.7, 1.8 and 1.9 in cannot be read"),
    ("run10", "trace", 2064.0, 2609.0, 5, 5, 2986, "first dot after the scan dropout; a stray thin stroke (u 2069 to 2081, v 2608 to 2610) to its right is not part of the trace"),
    ("run10", "feature", 2064.0, 2594.0, 5, 9, 2996, "peak: second local maximum of the force (the two dots at u 2064, v 2594 and 2609, are equally far left), "
     "before the force falls at the largest displacement along the x = 2.0 in grid line"),
    ("run10", "trace", 2064.0, 2594.0, 5, 5, 2996, "added at the second peak (dot centre), so the trace keeps its shape"),
    ("run10", "trace", 2088.9, 2575.9, 5, 5, 3028, "added at the bend where the trace turns to run along the x = 2.0 in grid line (dot centre)"),
    ("run10", "feature", 2187.2, 2557.7, 5, 6, 3124, "last: the last dot, partly on the x = 2.0 in grid line (end of the trace)"),
    ("run10", "trace", 2187.2, 2557.7, 5, 6, 3124, "trace end, at the last point (last dot)"),
    # Run No. 4, solid
    ("run4", "feature", 2276, 3793, 7, 7, 1, FIRST_NOTE),
    ("run4", "trace", 2276, 3793, 7, 7, 1, "trace start, at the first point (merged ink at the origin corner; see the first feature)"),
    ("run4", "trace", 2100, 3779, 6, 7.5, 170, "sample for F = 50 lb (about 60 lb, the nearest clean ink: at the 50 lb line Run 12 and the grid line merge in); Run 4 and Run 10 run together here (one band of ink, v 3772 to 3786, "
     "between u about 2050 and the origin) and cannot be told apart; centre of the band, bound covering the whole band; the same pixel as Run 10's sample"),
    ("run4", "trace", 1968, 3753, 6.5, 6.5, 308, "sample for F = 100 lb (about 102 lb), 7 px left of the 100 lb grid line, where the line's own ink is clear "
     "(a Run 10 dot touches it at u 1954 to 1964)"),
    ("run4", "feature", 1903.5, 3653, 6, 7, 435, "peak: first local maximum of the force; the line is at its leftmost over v 3646 to 3660"),
    ("run4", "feature", 2053.7, 3187, 5, 23, 930, "knee, minimum: the force is flat at its minimum over v 3164 to 3210 (location along x not an observation)"),
    ("run4", "trace", 1971.5, 2763, 6, 6, 1365, "sample for x = 1.7 in (about 1.68 in): between v 2700 and 2758 the line runs into the 100 lb grid line "
     "on its left; sampled just below, where its own ink is clear"),
    ("run4", "trace", 1959.5, 2700, 6, 6, 1425, "last ink before the scan dropout (no ink, grid lines included, from v 2666 to 2697); x = 1.8 in falls in it and cannot be read"),
    ("run4", "trace", 1954.5, 2661, 6, 6, 2436, "first ink after the scan dropout"),
    ("run4", "trace", 1951.5, 2628, 6.5, 6.5, 2466, "sample for x = 1.9 in; the 100 lb grid line merges with the right side of the line here; "
     "centre from the clear left edge (u 1945.5) plus half the line width"),
    ("run4", "feature", 1819.5, 1300, 5, 15, 3801, "peak: second local maximum of the force; the line is at its leftmost over v 1285 to 1316"),
    ("run4", "feature", 1830, 1250, 5, 5, 3853, "knee: rounded corner where the trace stops penetrating and the force starts to fall at the largest displacement"),
    ("run4", "feature", 2141, 1229.5, 5, 5, 4167, "knee: kink where the falling-force stroke turns down-right into a short diagonal (displacement decreasing slightly)"),
    ("run4", "trace", 2141, 1229.5, 5, 5, 4167, "added at the kink, so the trace keeps its shape"),
    ("run4", "feature", 2189, 1252, 5, 5, 4220, "knee, minimum: tip of the end hook, the lowest force after the second peak; the diagonal and the return stroke merge here"),
    ("run4", "trace", 2189, 1252, 5, 5, 4220, "added at the tip of the end hook, so the trace keeps its shape (diagonal and return stroke merged)"),
    ("run4", "feature", 2110, 1252.5, 4, 6, 4294, "last: left end of the return stroke of the end hook; the force rises again from about 20 to about 45 lb "
     "at nearly constant displacement (drawn so; it may be the footpad settling on the soil)"),
    ("run4", "trace", 2110, 1252.5, 4, 6, 4294, "trace end, at the last point (left end of the return stroke)"),
]


def main():
    auto = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    rows = []
    for r in auto:
        key = (r["series_id"], float(r["pixel_u"]), float(r["pixel_v"]))
        if key in DROP:
            continue
        rows.append({"series_id": r["series_id"], "point_kind": "trace", "pixel_u": float(r["pixel_u"]),
                     "pixel_v": float(r["pixel_v"]), "u_bound_px": float(r["u_bound_px"]), "v_bound_px": float(r["v_bound_px"]),
                     "arc": float(r["arc"]) + (0 if r["segment"] == "1" else 0), "note": r["note"]})
    for sid, kind, u, v, bu, bv, arc, note in MANUAL:
        rows.append({"series_id": sid, "point_kind": kind, "pixel_u": u, "pixel_v": v, "u_bound_px": bu, "v_bound_px": bv,
                     "arc": float(arc) + (0.01 if kind == "trace" else 0), "note": note})
    out = []
    for sid in ("run4", "run10", "run12"):
        rs = sorted([r for r in rows if r["series_id"] == sid], key=lambda r: r["arc"])
        for k, r in enumerate(rs, 1):
            out.append({"figure_id": "F4-20", "panel": 1, "series_id": sid, "point_kind": r["point_kind"], "sequence": k,
                        "pixel_u": round(r["pixel_u"], 1), "pixel_v": round(r["pixel_v"], 1),
                        "u_bound_px": round(r["u_bound_px"], 1), "v_bound_px": round(r["v_bound_px"], 1),
                        "symbol": STYLE[sid], "note": r["note"]})
    with open(sys.argv[3], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(Counter((r["series_id"], r["point_kind"]) for r in out))
    for d in DROP.values():
        print("dropped:", d)


if __name__ == "__main__":
    main()
