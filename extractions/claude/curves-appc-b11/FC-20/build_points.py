"""Assemble points-p1.csv for FC-20 (reader's helper).

Markers: circle centres from fit_circles.py (ray-cast ring midpoints, least-squares circle).
Traces: ends read on zoom-5/6 crops and column scans; the Dr 0.00 samples on the x = 0 grid line,
where the curves' ink is merged with the grid line, interpolated between the columns of ink on
either side of it; the samples at 0.05 to 0.95 from sample_curves.py (samples-<curve>.csv).
Features: first and last point of each trace (no knee on any of the three curves).
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VL = [(l["u_at_v0"], l["slope_du_dv"]) for l in json.loads((HERE / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))["vertical_lines"]]


def vgrid_between(u0, u1, v):
    return any(u0 < a + b * v < u1 for a, b in VL)
FIG = "FC-20"
HALF = 4  # half the line thickness, rounded up (median thickness 7.4 to 7.6 px on the three curves)

rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append({"figure_id": FIG, "panel": 1, "series_id": series, "point_kind": kind, "sequence": seq,
                 "pixel_u": u, "pixel_v": v, "u_bound_px": bu, "v_bound_px": bv, "symbol": symbol, "note": note})


markers = [
    (825.3, 3228.9, 3, "single; ring touches the Dr 0 grid line on its left; solid curve passes about 8 px below"),
    (827.5, 3280.5, 3, "pair 1 left; the solid curve runs over the top of the ring and the joining line meets its right side; bound widened"),
    (1009.2, 3280.3, 2, "pair 1 right; the joining line meets its left side; the lower dashed curve has a gap just below it"),
    (1264.1, 2964.0, 3, "single; the Dr 0.3 grid line passes through the circle near its centre; bound widened"),
    (1531.4, 2671.5, 3, "single; ring printed broken (gaps at upper right and lower left); the upper dashed curve passes about 6 px from its upper left, there printed as fragments; bound widened"),
    (1994.2, 2318.4, 2, "single; the upper dashed curve passes about 10 px above it"),
    (2341.2, 2320.9, 3, "single; the Dr 1.0 grid line passes through it near its centre; the solid curve ends on its left side; bound widened"),
]
for i, (u, v, b, n) in enumerate(markers, 1):
    add("data", "marker", i, u, v, b, b, "circle", n)

ENDS = {
    "mean": {
        "left": (797.5, 3266.5, HALF, HALF, "left end: ink starts about 7 px left of the centre of the Dr 0 grid line"),
        "zero": (804.5, 3265.8, HALF, 6, "Dr 0.00 on the Dr 0 grid line; curve merged with the grid line, the pair 1 left circle just right of it; v bound widened"),
        "right": (2321.5, 2321.0, HALF, HALF, "right end: ink ends where it meets the outline of the circle at Dr 0.99 (it does not enter the ring)"),
    },
    "upper": {
        "left": (799.5, 3171.0, HALF, HALF, "left end: ink starts at the left edge of the Dr 0 grid line"),
        "zero": (802.5, 3170.1, HALF, 5, "Dr 0.00 on the Dr 0 grid line; curve merged with the grid line; v bound widened"),
        "right": (2335.5, 2165.5, HALF, HALF, "right end: last dash runs into the Dr 1.0 grid line; no ink right of it"),
    },
    "lower": {
        "left": (803.5, 3383.0, HALF, HALF, "left end: ink starts about 3 px left of the Dr 0 grid line"),
        "zero": (806.9, 3382.7, HALF, 5, "Dr 0.00 on the Dr 0 grid line; curve merged with the grid line; v bound widened"),
        "right": (2339.5, 2396.5, HALF, HALF, "right end: last dash runs into the Dr 1.0 grid line; no ink right of it"),
    },
}

for name in ("mean", "upper", "lower"):
    e = ENDS[name]
    seq = 1
    u, v, bu, bv, n = e["left"]
    add(name, "trace", seq, u, v, bu, bv, "", n)
    seq += 1
    u, v, bu, bv, n = e["zero"]
    add(name, "trace", seq, u, v, bu, bv, "", n)
    for r in csv.DictReader((HERE / f"samples-{name}.csv").open(encoding="utf-8")):
        seq += 1
        d, how = float(r["dr_target"]), r["how"]
        bu = bv = HALF
        note = f"Dr {d:.2f}"
        if how.startswith("gap"):
            note += "; in a gap between dashes: moved to the nearest dash end, on the ink"
        if "hgrid" in how:
            bv = 5
            note += "; curve merged with a horizontal grid line: centre half a line width from its free edge; v bound widened"
        if how.startswith("interp") and vgrid_between(*(int(x) for x in how.split()[1].split("-")), float(r["v"])):
            note += "; on a vertical grid line: centre interpolated between the ink either side of it"
        if name == "upper" and abs(d - 0.95) < 1e-9:
            bv = 8
            note += ("; the dash ends in a thin flat tail (u 2239 to 2261) that lies up to 8 px below the path of the stroke (the next dash, from u 2284, continues that path);"
                     " sample on the tail's ink, v bound widened to take in the stroke's path")
        if name == "upper" and abs(d - 0.45) < 1e-9:
            note += "; this stretch of the dashed curve is printed as fragments next to the circle at Dr 0.46"
        add(name, "trace", seq, float(r["u"]), float(r["v"]), bu, bv, "", note)
    seq += 1
    u, v, bu, bv, n = e["right"]
    add(name, "trace", seq, u, v, bu, bv, "", n)
    # features: first and last point of the trace
    u, v, bu, bv, _ = e["left"]
    add(name, "feature", 1, u, v, bu, bv, "", "first point (left end of the ink)")
    u, v, bu, bv, _ = e["right"]
    add(name, "feature", 2, u, v, bu, bv, "", "last point (right end of the ink); also the maximum of the trace; no knee on this curve")

with (HERE / "points-p1.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"wrote points-p1.csv: {len(rows)} rows")
