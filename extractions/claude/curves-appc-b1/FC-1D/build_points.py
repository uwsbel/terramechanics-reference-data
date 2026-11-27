"""Assemble points-p1.csv and points-p2.csv for FC-1D (Claude, blind reading).

Markers were read by eye on zoom-4 tiles and zoom-6 detail crops (coordinates typed below and in
trace_helper.MARKERS). Trace samples come from trace_helper.py (ridge following of each drawn
line), subsampled every 5 thousandths of displacement at columns away from vertical gridlines and
marker symbols; the n2345 tail (u > 1600), which the ridge follower lost, is taken from column
scans. Features: first point, peak (minimum v of the drawn line) and last point of each trace.

Run from the FC-1D workspace:
    python out/FC-1D/build_points.py packet/p0119.png out/FC-1D/cal-p1/calibration.json out/FC-1D/trace-raw.csv
"""
import csv
import json
import math
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from trace_helper import MARKERS  # noqa: E402

FIG = "FC-1D"
SYMBOL = {"n3520": "x", "n2935": "asterisk", "n2345": "square", "n1468": "triangle-down",
          "n587": "triangle-up", "n294": "circle", "n0": "circle"}
# default half-width of the reading uncertainty for a clean marker center, by symbol
BOUND = {"x": 2, "asterisk": 2, "square": 3, "triangle-down": 3, "triangle-up": 3, "circle": 3}
N0_NOTE = "filled circle (dot); legend gives no symbol for the 0 and 294 psf tests"

# upper-panel marker notes keyed by (series, u as typed in MARKERS): (u_bound, v_bound, note)
P1_NOTES = {
    ("n3520", 857.5): (4, 3, "on x=50 gridline; found on a detail crop, hidden in the overview"),
    ("n3520", 1204.5): (3, 3, "drawn line runs through the marker along the plateau"),
    ("n3520", 1441): (4, 3, "on x=150 gridline"),
    ("n3520", 1737.5): (4, 3, "on x=200 gridline"),
    ("n3520", 2027.5): (4, 3, "on x=250 gridline; doubles as the legend symbol for 3520 psf"),
    ("n2935", 1440): (4, 3, "on x=150 gridline"),
    ("n2935", 1736): (4, 3, "on x=200 gridline"),
    ("n2935", 2032): (4, 4, "on x=250 gridline and touching y=4000 gridline; doubles as the legend symbol for 2935 psf"),
    ("n2345", 794): (3, 3, "square sits about 40 px above the drawn line (line passes below it)"),
    ("n2345", 1147): (4, 3, "on x=100 gridline"),
    ("n2345", 1625): (3, 3, "square about 30 px above the drawn line"),
    ("n2345", 1737): (4, 3, "on x=200 gridline; square about 75 px above the drawn line"),
    ("n2345", 2047): (4, 3, "on x=250 gridline; doubles as the legend symbol for 2345 psf; line ends here"),
    ("n1468", 750): (3, 3, "touches y=2000 gridline"),
    ("n1468", 866): (4, 3, "on x=50 gridline"),
    ("n1468", 1506): (4, 4, "merged with the drawn line, outline hard to separate"),
    ("n1468", 1632): (3, 3, "marker about 25 px above the drawn line"),
    ("n1468", 1748): (4, 3, "on x=200 gridline"),
    ("n587", 875): (4, 3, "on x=50 gridline"),
    ("n587", 1755): (4, 3, "on x=200 gridline, just above y=1000 gridline"),
    ("n587", 1877): (3, 3, "just below y=1000 gridline"),
    ("n587", 2049): (4, 3, "on x=250 gridline; doubles as the legend symbol for 587 psf"),
    ("n294", 934): (3, 4, "on y=1000 gridline"),
    ("n294", 1054): (3, 4, "on y=1000 gridline"),
    ("n294", 1172): (4, 4, "on x=100 gridline, touching y=1000 gridline"),
}

# lower panel markers: series -> list of (u, v, u_bound, v_bound, note)
P2 = {
    "n3520": [
        (598, 3402.5, 4, 3, "on x=0 gridline (frame); symbol could be x or asterisk, the vertical stroke may be the gridline"),
        (650, 3384, 2, 2, ""),
        (762, 3358, 2, 2, ""),
        (890, 3350, 4, 3, "on x=50 gridline, just below the zero line"),
        (1001, 3335, 3, 4, "on the zero line"),
        (1123, 3310.5, 2, 2, ""),
        (1240, 3291, 2, 2, ""),
        (1358, 3276, 2, 2, ""),
        (1474, 3253, 4, 3, "on x=150 gridline"),
        (1592.5, 3233, 2, 2, ""),
        (1767.5, 3206, 3, 2, "just right of x=200 gridline"),
        (1885, 3190, 2, 2, ""),
        (2057.5, 3174, 4, 3, "on x=250 gridline"),
    ],
    "n2935": [
        (614.6, 3361, 3, 3, "in the dense cluster at x near 0"),
        (676.7, 3360, 2, 2, ""),
        (788, 3355.5, 2, 2, ""),
        (999, 3311.7, 2, 2, ""),
        (1123, 3283, 2, 2, ""),
        (1236, 3265, 2, 2, ""),
        (1361, 3245, 2, 2, ""),
        (1469.6, 3217.5, 4, 3, "on x=150 gridline"),
        (1647.5, 3191, 2, 2, ""),
        (1764, 3176, 3, 2, "just right of x=200 gridline"),
        (1881, 3160, 2, 2, ""),
        (2054, 3130, 4, 3, "on x=250 gridline"),
    ],
    "n2345": [
        (565.8, 3364, 3, 3, "left of the x=0 frame line (negative displacement as drawn)"),
        (638.3, 3330.4, 3, 4, "on the zero line"),
        (712.5, 3361, 3, 3, ""),
        (762, 3331, 3, 4, "on the zero line"),
        (827.5, 3326.7, 3, 4, "bottom side on the zero line"),
        (941.7, 3316, 3, 3, ""),
        (1067.5, 3289, 3, 3, ""),
        (1183.3, 3266, 4, 3, "on x=100 gridline"),
        (1298, 3241, 3, 3, "square printed incompletely (left side open)"),
        (1416, 3217.5, 3, 3, ""),
        (1528, 3189, 3, 3, ""),
        (1647, 3164, 3, 3, ""),
        (1765, 3156, 4, 3, "on x=200 gridline"),
        (1879, 3134, 4, 4, "square printed incompletely (only top and right sides and part of the base)"),
        (2055, 3097.5, 4, 3, "on x=250 gridline"),
    ],
    "n1468": [
        (585.4, 3344, 4, 4, "left of the x=0 frame line, base on the zero line, apex merges with the triangle-up below"),
        (907, 3318, 4, 4, "overlaps the triangle-up at x near 48"),
        (999.5, 3287, 4, 5, "overlaps the triangle-up above it (the two form a diamond); center from the shared bar and the lower apex"),
        (1119, 3254, 4, 5, "overlaps the triangle-up above it (diamond)"),
        (1236, 3215, 3, 3, ""),
        (1295, 3200, 4, 5, "overlaps the triangle-up above it (diamond)"),
        (1414, 3184, 3, 3, ""),
        (1525.5, 3151, 3, 3, ""),
        (1646, 3130.5, 3, 3, ""),
        (1759, 3100, 4, 3, "on x=200 gridline"),
        (1880, 3082.5, 3, 3, ""),
        (2052, 3060.5, 4, 3, "on x=250 gridline"),
    ],
    "n587": [
        (592.5, 3376, 4, 4, "on the x=0 frame line, apex merges with the triangle-down above"),
        (648, 3359, 3, 3, ""),
        (884, 3305.5, 4, 4, "on x=50 gridline, overlaps the triangle-down at x near 52"),
        (999.5, 3260, 4, 5, "overlaps the triangle-down below it (diamond); center from the upper apex and the shared bar"),
        (1119, 3229, 4, 5, "overlaps the triangle-down below it (diamond)"),
        (1295, 3169, 4, 5, "overlaps the triangle-down below it (diamond)"),
        (1412, 3135.5, 3, 3, ""),
        (1527, 3100.5, 3, 3, ""),
        (1648, 3074, 3, 3, ""),
        (1759, 3054, 4, 3, "on x=200 gridline"),
        (1879, 3028, 3, 4, "on the +100 frame line (upper edge of the panel); above +100, calibration extrapolated"),
        (2055, 2999, 4, 3, "on x=250 gridline; above the +100 frame line, calibration extrapolated"),
    ],
    "n294": [
        (712.5, 3331, 3, 4, "bottom of the ring on the zero line"),
        (828.3, 3285, 3, 3, ""),
        (945, 3239, 3, 3, ""),
        (1059, 3182.5, 3, 3, ""),
        (1181, 3139, 4, 3, "on x=100 gridline"),
        (1292, 3106, 3, 3, ""),
        (1410.5, 3065, 3, 3, ""),
        (1525, 3025.5, 3, 3, "above the +100 frame line, calibration extrapolated"),
    ],
    "n0": [
        (710.8, 3292.5, 2, 2, N0_NOTE),
        (830, 3230, 2, 2, N0_NOTE),
        (948, 3162.5, 2, 2, N0_NOTE),
        (997, 3125.5, 2, 2, N0_NOTE),
        (1117.5, 3066, 2, 2, N0_NOTE),
        (1234, 3005.5, 2, 2, N0_NOTE + "; above the +100 frame line, calibration extrapolated"),
        (1353, 2957.5, 2, 2, N0_NOTE + "; above the +100 frame line, calibration extrapolated"),
    ],
}

COLS = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
        "u_bound_px", "v_bound_px", "symbol", "note"]


def scan_n2345_tail(g, u_start, v_start):
    """Column scan of the n2345 drawn line for u > u_start (the ridge follower lost it there)."""
    out = []
    v = v_start
    last_u = u_start
    for u in range(int(u_start), 2047, 3):
        col = g[1840:2070, u - 1:u + 2].min(axis=1) < 200
        runs = []
        s = None
        for i, d in enumerate(col):
            if d and s is None:
                s = i
            elif not d and s is not None:
                runs.append(((s + i - 1) / 2 + 1840, i - s))
                s = None
        tol = 12 + 0.5 * (u - last_u)   # the line descends while the scan has no accepted run
        cand = [r for r in runs if 8 <= r[1] <= 22 and abs(r[0] - v) <= tol]
        if not cand:
            continue
        r = min(cand, key=lambda r: abs(r[0] - v))
        v = r[0]
        last_u = u
        out.append((u, v, r[1]))
    return out


def main():
    img, calp, rawp = sys.argv[1:4]
    g = np.asarray(Image.open(img).convert("L"))
    cal = json.load(open(calp))
    ax = cal["ax"]
    vlines = [(x["u_at_v0"], x["slope_du_dv"]) for x in cal["vertical_lines"]]

    def xval(u, v):
        return ax[0] * u + ax[1] * v + ax[2]

    def near_vgrid(u, v):
        return any(abs(u0 + s * v - u) < 8 for u0, s in vlines)

    raw = {}
    for r in csv.DictReader(open(rawp)):
        if not r["seq"]:
            continue
        raw.setdefault(r["series_id"], []).append(
            (float(r["u"]), float(r["v"]), int(r["thickness"]), r["flags"]))
    # n2345 tail from column scans
    t = [p for p in raw["n2345"] if p[0] <= 1600]
    last = [p for p in t if p[2] >= 8][-1]
    t = [p for p in t if p[0] <= last[0]]
    for u, v, th in scan_n2345_tail(g, last[0] + 3, last[1]):
        t.append((u, v, th, "colscan"))
    raw["n2345"] = t

    rows1 = []
    for sid, mk in MARKERS.items():
        sym = SYMBOL[sid]
        for i, (u, v) in enumerate(sorted(mk), 1):
            ub, vb, note = P1_NOTES.get((sid, u), (BOUND[sym], BOUND[sym], ""))
            if sid == "n0":
                note = (N0_NOTE + ("; " + note if note else ""))
            rows1.append([FIG, 1, sid, "marker", i, u, v, ub, vb, sym, note])
    # traces: subsample every 5 thousandths
    for sid, pts in raw.items():
        mk = np.array(sorted(MARKERS[sid]))
        xs = np.array([xval(u, v) for u, v, _, _ in pts])
        seq = 0
        used = set()
        x_targets = np.arange(0, 260, 5)
        for xt in x_targets:
            if xt < xs.min() - 1 or xt > xs.max() + 1:
                continue
            order = np.argsort(np.abs(xs - xt))
            pick = None
            for j in order[:12]:
                u, v, th, fl = pts[j]
                if abs(xs[j] - xt) > 2.5:
                    break
                if th == 0 or th > 22:
                    continue
                if near_vgrid(u, v):
                    continue
                if np.any(np.hypot(mk[:, 0] - u, mk[:, 1] - v) < 17):
                    continue
                pick = j
                break
            if pick is None or pick in used:
                continue
            used.add(pick)
            u, v, th, fl = pts[pick]
            seq += 1
            b = max(4, math.ceil(th / 2))
            note = ""
            if "merged" in fl or th > 16:
                note = "line merged with a gridline or symbol here; bound widened"
                b = max(b, 8)
            if "hgrid" in fl and "merged" not in fl:
                note = "line runs on or next to a horizontal gridline"
            rows1.append([FIG, 1, sid, "trace", seq, round(u, 1), round(v, 1), b, b, "", note])
        # features
        first = pts[0]
        last = pts[-1]
        good = [p for p in pts if 0 < p[2] <= 22 and not near_vgrid(p[0], p[1])]
        peak = min(good, key=lambda p: p[1])
        plateau = [p for p in good if p[1] <= peak[1] + 4]
        pk_note = ""
        if plateau and (max(p[0] for p in plateau) - min(p[0] for p in plateau)) > 60:
            pk_note = ("flat plateau: drawn line within 4 px of its maximum from u=%d to %d; peak taken at the minimum v"
                       % (min(p[0] for p in plateau), max(p[0] for p in plateau)))
        rows1.append([FIG, 1, sid, "feature", 1, round(first[0], 1), round(first[1], 1), 4, 4, "",
                      "first point: drawn line starts at the first marker"])
        rows1.append([FIG, 1, sid, "feature", 2, round(peak[0], 1), round(peak[1], 1),
                      max(5, math.ceil(peak[2] / 2)), max(5, math.ceil(peak[2] / 2)), "",
                      "peak of the drawn line" + ("; " + pk_note if pk_note else "")])
        end_note = {"n3520": "last point: line ends at the x=250 gridline",
                    "n2935": "last point: line ends at the x=250 gridline",
                    "n2345": "last point: line ends at the last square on the x=250 gridline",
                    "n1468": "last point: line ends at the x=250 gridline",
                    "n587": "last point: line ends at the x=250 gridline",
                    "n294": "last point: line ends just before the last circle (x near 158)",
                    "n0": "last point: line ends about 15 thousandths past the last dot"}[sid]
        rows1.append([FIG, 1, sid, "feature", 3, round(last[0], 1), round(last[1], 1), 5, 5, "", end_note])

    with open("out/FC-1D/points-p1.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        w.writerows(rows1)

    rows2 = []
    for sid, lst in P2.items():
        for i, (u, v, ub, vb, note) in enumerate(sorted(lst), 1):
            rows2.append([FIG, 2, sid, "marker", i, u, v, ub, vb, SYMBOL[sid], note])
    with open("out/FC-1D/points-p2.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        w.writerows(rows2)
    import collections
    c1 = collections.Counter((r[2], r[3]) for r in rows1)
    c2 = collections.Counter((r[2], r[3]) for r in rows2)
    print("p1:", dict(c1))
    print("p2:", dict(c2))


if __name__ == "__main__":
    main()
