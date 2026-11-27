"""Assemble points-p1.csv from the marker list and the reviewed tracker output.

Trace samples: from each tracker file, rows with status ok and a run thickness inside the given
limits; the rows are split into dashes (a break wherever the tracker skipped a column or found no
ink), and each dash contributes its first row, its last row and interior rows at least 15 px
apart. Manual samples (read with plot_grid scan where the tracker cannot work: the ink ends and
the start of the 147 psf curve, which rests on the bottom frame) are added with their notes.
Bounds: u 0 (a trace column is a sampling location), v half the run thickness. Features (first
point, peak of the drawn line, last point) are listed by hand below.

usage: python assemble_p1.py   (run from out/FC-6D)
"""
import csv
from collections import Counter

FIG = "FC-6D"
rows = []
with open("helpers/markers_p1.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append(r)


def dashes(path, tmin, tmax, umin=None, umax=None):
    out, cur = [], []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            u = int(r["u"])
            if (umin is not None and u < umin) or (umax is not None and u > umax):
                continue
            ok = r["status"] == "ok" and tmin <= float(r["thickness"]) <= tmax
            if ok:
                cur.append((u, float(r["v_center"]), float(r["thickness"])))
            elif cur:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return out


def pick(dash):
    sel = [dash[0]]
    for p in dash[1:-1]:
        if p[0] - sel[-1][0] >= 15 and dash[-1][0] - p[0] >= 10:
            sel.append(p)
    if len(dash) > 1:
        sel.append(dash[-1])
    return sel


def steep_note(t):
    return "steep part of the line: the column run is long and the v bound is half of it" if t >= 17 else ""


traces = {
    "n4695": [("helpers/tr4695_raw.csv", 7, 28, 828, 2198)],
    "n3814": [("helpers/tr3814_raw.csv", 7, 28, 831, 2201)],
    "n2934": [("helpers/tr2934_raw.csv", 7, 28, 839, 1296), ("helpers/tr2934b_raw.csv", 7, 28, 1350, 2207)],
    "n1761": [("helpers/tr1761_raw.csv", 7, 28, 829, 2207)],
    "n147": [("helpers/tr147_raw.csv", 7, 13, 1020, 2191)],
}
XING = "crossing of the {g} gridline: the gridline lies inside the line band, so the run is the line band"
manual = {
    "n4695": [(826, 1732.5, 9, "first ink of the drawn line: its lower-left tip, just above the right arm of the first plus"),
              (885, 1632.5, 13, XING.format(g=2000)), (1115, 1337.5, 10, XING.format(g=3000)), (1480, 1038.0, 7.5, XING.format(g=4000)),
              (1645, 946.5, 6, "short dash between the 150 gridline and the plus at u 1663 (below its left arm)")],
    "n3814": [(830, 1819.5, 9, "first ink of the drawn line, just above where it runs into the top-right corner of the first triangle"),
              (975, 1629.0, 10.5, XING.format(g=2000)), (1285, 1334.5, 8, XING.format(g=3000))],
    "n2934": [(838, 1977.5, 8, "first ink of the drawn line, just above the top-right corner of the first square"),
              (897, 1925.5, 9, XING.format(g=1000)), (1300, 1636.5, 6, "dash just before it meets the 2000 gridline"),
              (1315, 1627.5, 6, XING.format(g=2000)), (1320, 1625.5, 6, XING.format(g=2000))],
    "n1761": [(828, 2069.0, 5.5, "first ink of the drawn line, right of the first circle"),
              (1130, 1923.0, 7.5, XING.format(g=1000))],
    "n147": [
        (831, 2207.0, 5, "first dash rests on the bottom frame: only its upper edge (v 2204) is visible; center estimated as edge plus half a line width"),
        (845, 2205.5, 5, "dash rests on the bottom frame: upper edge v 2201 visible, lower edge hidden in the frame"),
        (855, 2205.5, 5, "dash rests on the bottom frame: upper edge v 2201 visible, lower edge hidden in the frame"),
        (893, 2201.0, 3.5, "dash just above the bottom frame (separated from it by one pixel row)"),
        (910, 2200.0, 4.5, ""),
        (916, 2199.5, 5, ""),
        (956, 2196.5, 5, ""),
        (965, 2196.5, 5, ""),
        (1005, 2194.5, 6, "just right of the fourth triangle"),
        (1015, 2193.5, 5, ""),
    ],
}
ends = {  # last ink sample, read with scan
    "n4695": (2199, 864.0, 6.5, "last ink of the drawn line before the plus on the 250 gridline"),
    "n3814": (2202, 1102.5, 6, "last ink of the drawn line before the triangle on the 250 gridline"),
    "n2934": (2208, 1423.5, 6, "last ink of the drawn line before the square on the 250 gridline"),
    "n1761": (2208, 1731.5, 5, "last ink of the drawn line before the circle on the 250 gridline"),
    "n147": (2192, 2160.5, 5, "last clean ink; to the right the dash runs into the left side of the triangle on the 250 gridline"),
}
features = {
    "n4695": [(826, 1732.5, 0, 9, "feature: first point of the drawn line"),
              (2068, 844.5, 18, 5, "feature: peak of the drawn line, flat between u 2050 and 2085 (the plus at u 2026 interrupts the ink just before)"),
              (2199, 864.0, 0, 6.5, "feature: last point of the drawn line; the line falls from the peak to here")],
    "n3814": [(830, 1819.5, 0, 9, "feature: first point of the drawn line"),
              (2196, 1102.5, 8, 6, "feature: peak of the drawn line; the line still rises slightly to its end, so the maximum is at the last ink (flat within 2 px from u 2165)"),
              (2202, 1102.5, 0, 6, "feature: last point of the drawn line")],
    "n2934": [(838, 1977.5, 0, 8, "feature: first point of the drawn line"),
              (2190, 1423.5, 20, 6, "feature: peak of the drawn line; flat at v 1423.5 from u 2125 to the end"),
              (2208, 1423.5, 0, 6, "feature: last point of the drawn line")],
    "n1761": [(828, 2069.0, 0, 5.5, "feature: first point of the drawn line"),
              (2205, 1730.5, 5, 6, "feature: peak of the drawn line; the line rises to its end, maximum at the last ink"),
              (2208, 1731.5, 0, 5, "feature: last point of the drawn line")],
    "n147": [(831, 2207.0, 0, 5, "feature: first point of the drawn line (dash on the bottom frame, center estimated)"),
             (2065, 2159.5, 110, 6, "feature: peak of the drawn line; flat at v 2159.5 to 2160.5 from u 1955 to 2190, so its x is not defined"),
             (2192, 2160.5, 0, 5, "feature: last point of the drawn line (last clean ink)")],
}
for sid in ["n4695", "n3814", "n2934", "n1761", "n147"]:
    pts = []
    for p in manual[sid]:
        pts.append((p[0], p[1], 0, p[2], p[3]))
    for path, tmin, tmax, umin, umax in traces[sid]:
        for d in dashes(path, tmin, tmax, umin, umax):
            for u, v, t in pick(d):
                pts.append((u, v, 0, round(t / 2 * 2) / 2, steep_note(t)))
    e = ends[sid]
    pts.append((e[0], e[1], 0, e[2], e[3]))
    pts.sort(key=lambda p: p[0])
    dedup = []
    for p in pts:
        if dedup and abs(p[0] - dedup[-1][0]) < 3:
            if p[4] and not dedup[-1][4]:
                dedup[-1] = p
            continue
        dedup.append(p)
    for k, (u, v, bu, bv, note) in enumerate(dedup, 1):
        rows.append({"figure_id": FIG, "panel": "1", "series_id": sid, "point_kind": "trace", "sequence": str(k),
                     "pixel_u": str(u), "pixel_v": str(v), "u_bound_px": str(bu), "v_bound_px": str(bv),
                     "symbol": "", "note": note})
    for k, (u, v, bu, bv, note) in enumerate(features[sid], 1):
        rows.append({"figure_id": FIG, "panel": "1", "series_id": sid, "point_kind": "feature", "sequence": str(k),
                     "pixel_u": str(u), "pixel_v": str(v), "u_bound_px": str(bu), "v_bound_px": str(bv),
                     "symbol": "", "note": note})
cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with open("points-p1.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(Counter((r["series_id"], r["point_kind"]) for r in rows))
