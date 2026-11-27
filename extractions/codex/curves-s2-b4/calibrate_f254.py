"""Read knots for Figure 2-54 from the packet scan."""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import calibrate_axes as axes  # noqa: E402
from calibrate_axes import AxisKnots, fit_affine  # noqa: E402

IMAGE = Path("packet/p0117.png")
OUT = Path("out/F2-54")
SCAN = np.asarray(Image.open(IMAGE).convert("L"))
# Horizontal coordinate of the clockwise reading view is 4507 - v.
G = np.rot90(SCAN, -1)
V = SCAN.shape[0] - 1

TIMES = list(range(-20, 91, 10))
GRID_X = [1470, 1628, 1780, 1932, 2082, 2238, 2388, 2547, 2704, 2867, 3031, 3186]
GRID_U_WINDOWS = {
    1: [(309, 836), (316, 830), (319, 827), (323, 831)],
    2: [(860, 1313), (875, 1310), (882, 1309), (873, 1311)],
    3: [(1345, 2419), (1350, 2415), (1360, 2403), (1357, 2414)],
}
ZERO = {
    1: (852.0, [(1985, 2690)]),
    2: (1319.0, [(1985, 2670)]),
    3: (2335.0, [(1465, 1768), (2170, 2630)]),
}
# Each triplet gives the printed or counted value, first estimate of tick u,
# and an interior location on the ruler stub (temporary upright coordinate).
TICKS = {
    1: [(0, 861, 1845), (2, 838, 1871), (4, 818, 1871), (6, 797, 1871),
        (8, 777, 1871), (10, 756, 1845), (12, 736, 1871), (14, 715, 1871),
        (16, 694, 1872), (18, 675, 1871), (20, 654, 1845)],
    2: [(0, 1330, 1849), (2, 1314, 1875), (3, 1302, 1880),
        (4, 1292, 1875), (5, 1280, 1881), (6, 1269, 1875),
        (7, 1257, 1879), (8, 1246, 1874), (9, 1237, 1880),
        (10, 1225, 1854), (11, 1216, 1879), (12, 1204, 1875),
        (13, 1194, 1880), (14, 1183, 1875), (15, 1170, 1880),
        (16, 1160, 1876), (17, 1148, 1880), (18, 1137, 1876),
        (19, 1125, 1880), (20, 1113, 1851), (21, 1104, 1880),
        (22, 1093, 1873), (23, 1081, 1880), (24, 1071, 1874),
        (25, 1061, 1880), (26, 1049, 1874), (27, 1036, 1876),
        (28, 1025, 1873), (29, 1017, 1876), (30, 1007, 1850)],
    3: [(0, 2346, 1856), (2, 2323, 1882), (4, 2302, 1882),
        (6, 2281, 1880), (8, 2257, 1880), (10, 2233, 1859),
        (15, 2179, 1880), (20, 2120, 1858), (25, 2063, 1880),
        (30, 2005, 1858), (35, 1948, 1880), (40, 1891, 1867),
        (45, 1836, 1879), (50, 1780, 1859), (55, 1723, 1879),
        (60, 1666, 1856), (65, 1608, 1877), (70, 1551, 1855),
        (72, 1530, 1876), (74, 1508, 1874), (76, 1485, 1874),
        (78, 1463, 1875), (80, 1438, 1858)],
}


def csv_write(path, rows, fields=None):
    with path.open("w", newline="", encoding="utf-8") as stream:
        w = csv.DictWriter(stream, fields or list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def core(profile, begin, guess, minimum):
    """Find the contiguous half-contrast core around the strongest pixel."""
    contrast = 255 - profile
    best = np.max(contrast)
    if best < minimum:
        return None
    tied = np.flatnonzero(contrast == best)
    ind = min(tied, key=lambda i: abs(begin + i - guess))
    left, right = ind, ind
    while left > 0 and contrast[left - 1] >= .5 * best:
        left -= 1
    while right < len(profile) - 1 and contrast[right + 1] >= .5 * best:
        right += 1
    if left == 0 or right == len(profile) - 1:
        return None
    pixels = np.arange(left, right + 1)
    return begin + np.average(pixels, weights=contrast[pixels]), right - left + 1


def fit_line(pairs):
    p = np.array(pairs)
    slope, intercept = np.polyfit(*p.T, 1)
    offset = p[:, 1] - (intercept + slope * p[:, 0])
    med = np.median(offset)
    limit = max(1.6, 3 * 1.4826 * np.median(np.abs(offset - med)))
    keep = np.abs(offset - med) <= limit
    slope, intercept = np.polyfit(*p[keep].T, 1)
    return slope, intercept, p[keep]


def timing_line(panel, index):
    x0 = GRID_X[index]
    if index < 3:
        u0, u1 = GRID_U_WINDOWS[panel][index]
    else:
        u0, u1 = GRID_U_WINDOWS[panel][3]
    # Stay away from the label boxes in the -20 ms column.
    excluded = {1: [(395, 609)], 2: [(932, 1165)], 3: [(1625, 1864)]}
    pairs = []
    for u in range(u0, u1 + 1, 11):
        if index == 0 and any(lo <= u <= hi for lo, hi in excluded[panel]):
            continue
        guess = x0 + .0079 * (u - 300)
        a, b = round(guess)-10, round(guess)+11
        found = core(G[u-3:u+4, a:b].mean(axis=0), a, guess, 94)
        if found and found[1] <= 12:
            pairs.append((u, found[0]))
    slope, intercept, good = fit_line(pairs)
    return -slope, V-intercept, good


def dashed(panel):
    u0, intervals = ZERO[panel]
    pairs = []
    for x0, x1 in intervals:
        for x in range(x0, x1+1, 9):
            guess = u0 - .0083 * (x - 1900)
            a, b = round(guess)-5, round(guess)+6
            found = core(G[a:b, x-3:x+4].mean(axis=1), a, guess, 145)
            if found and found[1] <= 7 and abs(found[0]-guess) < 4:
                pairs.append((x, found[0]))
    slope, intercept, good = fit_line(pairs)
    return -slope, intercept+slope*V, good


def ticks_for(panel):
    for g, guess, x in TICKS[panel]:
        # Read the zero tick separately from the nearby dashed datum.
        rad = 5 if not g else 6
        a, b = guess-rad, guess+rad+1
        found = core(G[a:b, x-4:x+5].mean(axis=1), a, guess, 105)
        if found is None and g == 0:
            # The solid width of -0- merges into the solid pre-event trace.
            a, b = guess-7, guess+8
            found = core(G[a:b, x-4:x+5].mean(axis=1), a, guess, 120)
        if found is None:
            raise ValueError((panel, g, "tick not found", G[a:b, x-4:x+5].mean(axis=1)))
        yield g, float(found[0]), V-x


def anchor(x, y, u, v, x_source="", y_source=""):
    return {"x_value": x, "y_value": y, "u": round(float(u), 4), "v": round(float(v), 4),
            "x_source": x_source, "y_source": y_source}


def check_y_knots(anchors, ay):
    # A 6 px cross-stub search on panel 2 can pick up the dashed line 5.6 px
    # below its 2 g tick. The stubs were located directly, so check within 4 px.
    wide = axes.INK_HALF_WIDTH_PX
    try:
        axes.INK_HALF_WIDTH_PX = 4
        return AxisKnots(anchors, "y_value", "y_source", ay[:2], SCAN)
    finally:
        axes.INK_HALF_WIDTH_PX = wide


def read_panel(panel):
    directory = OUT / f"cal-p{panel}"
    directory.mkdir(parents=True, exist_ok=True)
    h_lines, v_lines, anchors, eye = [], [], [], []
    for index, time in enumerate(TIMES):
        slope, intercept, good = timing_line(panel, index)
        rows = [anchor(time, "", u, V-x, "detected") for u, x in good[::3]]
        anchors.extend(rows)
        h_lines.append({"x_value": time, "slope_dv_du": slope, "v_at_u0": intercept,
                        "source": "detected", "samples": len(good)})
        u_mid = 0.5 * (good[0,0] + good[-1,0])
        evidence = "Timing line counted from ruler labels"
        if time == 0:
            evidence = "Timing line interrupted by ruler labels, with the printed 0 just to its right"
        elif time == -20:
            evidence = "First timing line right of the break, partly behind caption box"
        elif time == 90:
            evidence = "Final timing line at right frame"
        if panel == 3 and time in (30, 40):
            u_mid = 1776 if time == 30 else 1774
            evidence = "Timing line contacted by .01 sec. arrowhead"
        eye.append((panel, "time_line", time, u_mid, intercept+slope*u_mid, "verified", evidence))

    slope, intercept, good = dashed(panel)
    anchors.extend(anchor("", 0, u, V-x, y_source="detected dashed zero") for x, u in good[::4])
    v_lines.append({"y_value": 0, "slope_du_dv": slope, "u_at_v0": intercept,
                    "source": "detected dashed zero", "samples": len(good)})
    x_, u_ = good[len(good)//2]
    eye.append((panel, "zero_datum", 0, u_, V-x_, "verified", "Dashed line assigned 0 g"))
    ruler_zero = None
    diagnostic = []
    for value, u, v in ticks_for(panel):
        if value == 0:
            ruler_zero = (u, v)
            difference = u-(intercept+slope*v)
            eye.append((panel, "ruler_tick", value, u, v, "verified; datum offset",
                        f"Printed 0; solid stub {difference:.2f} px below dashed datum at this v"))
            continue
        stub = "measured labeled tick" if value % 10 == 0 else "measured counted tick"
        short = {2: (1868, 1883), 11: (1875, 1886), 29: (1872, 1883)}
        if panel == 2 and value in short:
            for x in short[value]:
                start = int(u)-4
                end = start+10
                center, _ = core(G[start:end, x-1:x+2].mean(axis=1), start, u, 80)
                anchors.append(anchor("", value, center, V-x, y_source=stub))
        else:
            anchors.append(anchor("", value, u, v, y_source=stub))
        v_lines.append({"y_value": value, "slope_du_dv": slope, "u_at_v0": u-slope*v,
                        "source": stub, "samples": 1})
        eye.append((panel, "ruler_tick", value, u, v, "verified",
                    "Label aligned with this stub" if value % 10 == 0 else "Counted between labeled stubs"))
    if panel == 2:
        eye.append((panel, "ruler_tick", 1, None, None, "obscured", "No separable stub at 1 g where dashed zero passes"))
    # Use the dashed-line direction for the tick projection and preserve the
    # local tick positions in the piecewise map.
    for horizontal in h_lines:
        for vertical in v_lines:
            sh, ih = horizontal["slope_dv_du"], horizontal["v_at_u0"]
            sv, iv = vertical["slope_du_dv"], vertical["u_at_v0"]
            u = (iv + sv*ih)/(1-sv*sh)
            diagnostic.append(anchor(horizontal["x_value"], vertical["y_value"], u, ih+sh*u))
    ax, ay, rmsx, rmsy, maxx, maxy = fit_affine(diagnostic)
    u0, u1 = {1: (302, 878), 2: (870, 1350), 3: (1345, 2446)}[panel]
    cal = dict(image=IMAGE.as_posix(), box=[u0, 1288, u1, 3060],
               model="Affine diagnostic on timing-line and projected ruler-tick intersections",
               x_direction="up", y_direction="left", x_unit="ms", y_unit="g",
               ax=ax, ay=ay, x_per_px=float(np.hypot(*ax[:2])), y_per_px=float(np.hypot(*ay[:2])),
               rms_residual_x=rmsx, rms_residual_y=rmsy, max_residual_x=maxx, max_residual_y=maxy,
               n_anchors=len(anchors), n_diagnostic_intersections=len(diagnostic),
               horizontal_lines=h_lines, vertical_lines=v_lines,
               ruler_zero_tick={"u": ruler_zero[0], "v": ruler_zero[1],
                                "offset_from_dashed_px": difference})
    csv_write(directory / "anchors.csv", anchors)
    X = AxisKnots(anchors, "x_value", "x_source", ax[:2], SCAN)
    Y = check_y_knots(anchors, ay)
    for name, axis in [("time", X), ("deceleration", Y)]:
        print(panel, name, "verified", [k["value"] for k in axis.knots],
              "rejected", [(k["value"], k["reason"]) for k in axis.rejected])
        if axis.rejected:
            raise ValueError([(k["value"],k["check"]) for k in axis.rejected])
    cal["verification"] = {label: axis.knots for label, axis in [("x", X), ("y", Y)]}
    (directory / "calibration.json").write_text(json.dumps(cal, indent=2) + "\n", encoding="utf-8")
    print(f"Panel {panel}: affine RMS {rmsx:.4f} ms, {rmsy:.4f} g; max {maxx:.4f} ms, {maxy:.4f} g; "
          f"zero offset {difference:.2f} px")
    return eye


if __name__ == "__main__":
    eye = [dict(zip(("panel", "check", "value", "pixel_u", "pixel_v", "status", "note"), row))
           for panel in (1, 2, 3) for row in read_panel(panel)]
    for row in eye:
        for key in ("pixel_u", "pixel_v"):
            if row[key] is not None:
                row[key] = round(row[key], 2)
    csv_write(OUT / "calibration-eye-checks.csv", eye)








