"""Build out/FC-6A/points-p1.csv for FC-6A (p0131.png), panel 1.

Markers: centers read by the reader from row/column dumps of the page (helpers ascii.py, rowruns.py)
and zoomed crops; listed below with their evidence. Triangle centers are centroids of the
reconstructed triangle (rule 8): vertices from the measured side centerlines and base.

Traces: the three drawn lines are sampled at every 250 psf of normal stress. The column u of a
sample is where the line fitted to that line's ink (fit_lines.py, rms < 1 px) has the target sigma
under the adopted calibration (cal-p1); v is the measured center of the line's ink run in that
column when the run is a single clean stroke, otherwise the fitted v on merged ink (noted). A
sample that falls in a gap of the ink (a dash gap) is moved along the line to the nearest clean
ink and noted; a sample that falls on a plotted symbol is left out (rule 7) and listed in notes.md.
"""
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
dark = g < 160
cal = json.loads((OUT / "cal-p1" / "calibration.json").read_text())
ax, ay = cal["ax"], cal["ay"]
fits = json.loads((HERE / "fit_lines.json").read_text())
FIG = "FC-6A"
SER = {"A": "dr5-40", "M": "dr19-28", "B": "dr103-107"}


def val(u, v):
    return ax[0] * u + ax[1] * v + ax[2], ay[0] * u + ay[1] * v + ay[2]


def u_at_sigma(name, s):
    a, b = fits[name]
    return (s - ax[2] - ax[1] * a) / (ax[0] + ax[1] * b)


def runs_at(u, lo, hi):
    col = dark[lo:hi, u]
    idx = np.where(col)[0]
    out = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                out.append((lo + s, lo + p))
                s = i
            p = i
        out.append((lo + s, lo + p))
    return out


rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append({"figure_id": FIG, "panel": 1, "series_id": series, "point_kind": kind, "sequence": seq,
                 "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv,
                 "symbol": symbol, "note": note})


# ---------------- markers ----------------
def centroid(apex, bl, br):
    return (apex[0] + bl[0] + br[0]) / 3, (apex[1] + bl[1] + br[1]) / 3


TRI = [
    (centroid((973.5, 2953.1), (956.3, 2987.5), (997.2, 2987.5)),
     "at the origin corner; line A and the lowest dash of line B cross its base; sides from rows 2959-2983, base centerline v 2987.5"),
    (centroid((1446.3, 2521.3), (1425.4, 2557.5), (1467.2, 2557.5)),
     "under circle C1 (apex hidden in the circle) and crossed by lines M and B; base-left corner hidden by line B, "
     "reconstructed from the left side at v 2540 and the right side (rows 2548-2553) with an equilateral shape; "
     "rule 9: it sits on line B (squares' line, 3 px) and next to line M, 45 px below line A; series by shape"),
    (centroid((1765.5, 2185.0), (1747.5, 2219.0), (1789.0, 2219.0)),
     "crossed by line M; line A has a gap at this triangle (A passes through its apex); base centerline v 2219; "
     "rule 9: its centroid sits on line M (circles' line, 3 px), 27 px below line A; series by shape"),
    (centroid((2030.0, 1894.5), (2010.0, 1928.0), (2050.0, 1928.0)),
     "the dashed reference lines labelled 3680 and 3820 meet at this triangle; circle C3 touches its apex; "
     "line A has a gap here, line M crosses the base-right corner; base centerline v 1928"),
    (centroid((2264.5, 1633.5), (2245.5, 1663.5), (2283.5, 1663.5)),
     "right side faint below v 1645, base-right corner merges with line A (corner reconstructed symmetric); "
     "triangle sits about 31 px above line A"),
]
for i, ((u, v), note) in enumerate(TRI, 1):
    add(SER["A"], "marker", i, u, v, 3, 6, "triangle-up",
        f"T{i-1}: centroid of reconstructed triangle (rule 8), v bound >= height/6; " + note)

CIR = [
    (1147.0, 2881.0, 2, "C0: clean"),
    (1440.0, 2526.0, 3, "C1: the apex of triangle T1 lies inside the ring and its left side crosses the hole; ring outer extent u 1429-1451, v 2515-2538"),
    (1782.5, 2152.8, 2.5, "C2: top touches square S2's bottom edge, bottom crossed by line A where A resumes; "
                          "rule 9: it sits on line A (triangles' line, 13 px) and 43 px above line M; series by shape"),
    (2042.0, 1885.5, 2.5, "C3: bottom touches triangle T3's apex, right side touches line A; rule 9: nearest line is A "
                          "(triangles' line, 21 px), 48 px above line M; series by shape"),
    (2288.0, 1738.0, 2, "C4: clean; between the right ends of lines M and B"),
]
for i, (u, v, b, note) in enumerate(CIR, 1):
    add(SER["M"], "marker", i, u, v, b, b, "circle", note)
add(SER["M"], "marker", 6, 892.5, 3054.5, 2, 2, "circle",
    "Cx: circle printed OUTSIDE the plot frame, below-left of the origin, at negative sigma and tau (about -145, -162 psf); "
    "same size as the circle symbols; it sits at the same height (within about 2 px) as the point where the dashed extension of "
    "line M meets the sigma = 0 axis, 41 px to its left; not a physical test (negative normal stress); series by shape "
    "only; probably an intercept or identity mark, not a data point")

SQ = [
    (1149.2, 2772.8, 2, "S0: right side touches line A; rule 9: nearest line is A (triangles' line, 24 px), 48 px above "
                        "line B; series by shape"),
    (1440.0, 2591.0, 2, "S1: clean"),
    (1784.0, 2128.5, 2.5, "S2: top edge merges with the tau = 3000 grid line (center from sides and bottom, size 25 px)"),
    (2038.5, 2098.5, 2.5, "S3: left side coincides with the dashed reference line drawn at sigma ~3750 (labelled 3820); "
                          "bottom edge touches the tau = 3000 grid line"),
    (2288.8, 1796.8, 2, "S4: clean; line B ends 12 px left of its left side"),
]
for i, (u, v, b, note) in enumerate(SQ, 1):
    add(SER["B"], "marker", i, u, v, b, b, "square", note)

# symbol exclusion boxes for trace samples (u0, v0, u1, v1)
SYMBOX = [(951, 2948, 1002, 2992), (1422, 2512, 1470, 2561), (1744, 2181, 1793, 2223),
          (2006, 1889, 2054, 1932), (2241, 1626, 2288, 1667),
          (1135, 2869, 1159, 2893), (1428, 2513, 1452, 2537), (1771, 2141, 1794, 2165),
          (2030, 1873, 2054, 1898), (2276, 1726, 2300, 1750),
          (1133, 2757, 1166, 2788), (1424, 2576, 1456, 2607), (1768, 2112, 1801, 2144),
          (2022, 2083, 2054, 2113), (2273, 1781, 2305, 1812)]


def on_symbol(u, v, pad=2):
    return any(x0 - pad <= u <= x1 + pad and y0 - pad <= v <= y1 + pad for x0, y0, x1, y1 in SYMBOX)


def other_lines_near(name, u, v, tol=16):
    return [o for o in fits if o != name and abs(fits[o][0] + fits[o][1] * u - v) < tol]


def grid_near(u, v, tol=9):
    for l in cal["horizontal_lines"]:
        if abs(v - (l["v_at_u0"] + l["slope_dv_du"] * u)) < tol:
            return True
    for l in cal["vertical_lines"]:
        if abs(u - (l["u_at_v0"] + l["slope_du_dv"] * v)) < tol:
            return True
    return False


def clean_center(name, u, win=7):
    """measured center of a single stroke near the fit at column u, or None"""
    a, b = fits[name]
    vp = a + b * u
    for s, p in runs_at(u, int(vp) - 14, int(vp) + 15):
        c = (s + p) / 2
        if abs(c - vp) <= win and 8 <= p - s + 1 <= 17:
            return c, p - s + 1
    return None


def run_touches_symbol(u, s_, p_):
    return any(x0 <= u <= x1 and not (p_ < y0 or s_ > y1) for x0, y0, x1, y1 in SYMBOX)


def ink_at(u, v, r=2):
    return dark[int(round(v)) - r:int(round(v)) + r + 1, u].any()


skipped = []


def trace(name, left, right, dashed_until):
    """left/right: (u, v, bu, bv, note) end samples; samples every 250 psf between."""
    a, b = fits[name]
    series = SER[name]
    seq = 1
    add(series, "trace", seq, left[0], left[1], left[2], left[3], "", left[4])
    s_left = val(left[0], left[1])[0]
    s_right = val(right[0], right[1])[0]
    s = 250 * int(np.ceil((s_left + 5) / 250))
    while s < s_right - 1e-6:
        u0 = u_at_sigma(name, s)
        uc = int(round(u0))
        dnote = "dashed; " if uc < dashed_until else ""
        if on_symbol(uc, a + b * uc):
            skipped.append(f"{name} ({series}) sigma {s}: the line passes over a plotted symbol there, left out (rule 7)")
            s += 250
            continue
        chosen = None
        vp0 = a + b * uc
        tol_c = 3.5 if dnote else 2.0      # dashes of M lie about 2 px below the solid part's fit
        near_other = other_lines_near(name, uc, vp0)
        near_grid = grid_near(uc, vp0, tol=14)
        runs = [(s_, p_) for s_, p_ in runs_at(uc, int(vp0) - 14, int(vp0) + 15)
                if s_ - 1 <= vp0 <= p_ + 1]     # the run that contains the fitted point
        if runs and run_touches_symbol(uc, *runs[0]):
            pass                                  # run joined to a symbol outline: moved below
        elif runs and not near_other and not near_grid:
            s_, p_ = runs[0]
            c, w_ = (s_ + p_) / 2, p_ - s_ + 1
            if 11 <= w_ <= 17 and abs(c - vp0) <= tol_c:
                chosen = (uc, c, "")                                  # clean single stroke: measured center
            elif w_ > 17:
                chosen = (uc, vp0, "fitted position on merged ink (run joined by adjacent symbol or stray ink)")
            # else a thin run (end of a dash or of a segment): moved below
        elif runs:
            what = []
            if near_other:
                what.append("merged with line " + "/".join(near_other))
            if near_grid:
                what.append("at or next to a grid line")
            chosen = (uc, vp0, "fitted position on merged ink (" + ", ".join(what) + ")")
        if chosen is None:
            for du in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9, 10, -10, 11, -11, 12, -12]:
                u = uc + du
                vp = a + b * u
                if on_symbol(u, vp) or other_lines_near(name, u, vp) or grid_near(u, vp, tol=14):
                    continue
                rr = [(s_, p_) for s_, p_ in runs_at(u, int(vp) - 14, int(vp) + 15) if s_ - 1 <= vp <= p_ + 1]
                if rr and 11 <= rr[0][1] - rr[0][0] + 1 <= 17 and abs((rr[0][0] + rr[0][1]) / 2 - vp) <= tol_c                         and not run_touches_symbol(u, *rr[0]):
                    r0 = [(s_, p_) for s_, p_ in runs_at(uc, int(vp0) - 14, int(vp0) + 15) if s_ - 1 <= vp0 <= p_ + 1]
                    if r0 and run_touches_symbol(uc, *r0[0]):
                        why = "the run there touches a symbol outline"
                    else:
                        why = "dash gap or dash end" if dnote else "gap or end of a drawn segment"
                    chosen = (u, (rr[0][0] + rr[0][1]) / 2,
                              f"moved {du:+d} px along the line from the {s} psf column ({why})")
                    break
        if chosen is None:
            skipped.append(f"{name} ({series}) sigma {s}: no ink within 12 px, left out")
            s += 250
            continue
        u, v, note = chosen
        seq += 1
        add(series, "trace", seq, u, v, 0, 7, "", (dnote + f"sigma {s}" + ("; " + note if note else "")).strip())
        s += 250
    seq += 1
    add(series, "trace", seq, right[0], right[1], right[2], right[3], "", right[4])
    return seq


def fitted_point_at_sigma(name, s):
    u = u_at_sigma(name, s)
    return u, fits[name][0] + fits[name][1] * u


# A: left end at the sigma = 0 axis, the frame corner (A runs into the corner, solid)
uA0, vA0 = fitted_point_at_sigma("A", 0.0)
# M: left end where its last dash meets the sigma = 0 axis; line through the measured centers of its last two dashes
dash_pts = []
for u in list(range(936, 946)) + list(range(962, 984)):
    a, b = fits["M"]
    vp = a + b * u
    for s_, p_ in runs_at(u, int(vp) - 10, int(vp) + 11):
        c = (s_ + p_) / 2
        if abs(c - vp) <= 6 and 10 <= p_ - s_ + 1 <= 17:
            dash_pts.append((u, c))
dash_pts = np.array(dash_pts)
db, da = np.polyfit(dash_pts[:, 0], dash_pts[:, 1], 1)
uM0 = (-ax[2] - ax[1] * da) / (ax[0] + ax[1] * db)
vM0 = da + db * uM0
# B: the dashed extension ends where it meets the tau = 0 frame line; sigma = 0 crossing extrapolated
hl0 = [l for l in cal["horizontal_lines"] if l["y_value"] == 0.0][0]
aB, bB = fits["B"]
uBt = (aB - hl0["v_at_u0"]) / (hl0["slope_dv_du"] - bB)
vBt = aB + bB * uBt
uB0, vB0 = fitted_point_at_sigma("B", 0.0)

A_right = (2343.0, clean_center("A", 2343)[0], 5, 5, "right end of the ink (solid line ends at sigma ~4860)")
M_right = (2252.0, 1725.0, 5, 5, "right end of the ink (ink ends at u 2254, last full-width column 2252)")
B_right = (2261.0, 1801.0, 5, 5, "right end of the ink (ends 12 px left of square S4)")

trace("A", (round(uA0, 1), round(vA0, 1), 5, 5,
            "left end: solid line runs into the frame corner at the origin; point where the fitted line meets sigma = 0 "
            "(ink merges with the frame)"),
      A_right, dashed_until=0)
trace("M", (round(uM0, 1), round(vM0, 1), 4, 4,
            "dashed; left end: the lowest dash reaches the sigma = 0 axis below the frame (tau < 0) and its ink runs on "
            "to u 926; point on the dash centerline at sigma = 0"),
      M_right, dashed_until=1181)
trace("B", (round(uBt, 1), round(vBt, 1), 4, 5,
            "dashed; left end: the lowest dash runs into the tau = 0 frame line about 12 px right of the sigma = 0 axis "
            "(merged with line A and the frame); it does not reach the sigma = 0 axis"),
      B_right, dashed_until=1175)

# features: intercepts
add(SER["A"], "feature", 1, round(uA0, 1), round(vA0, 1), 3, 4, "",
    "intercept: line A meets sigma = 0 at the frame corner, 3 px below the tau = 0 line center (tau about -14 psf, "
    "zero within the bound)")
vMfit = fits["M"][0] + fits["M"][1] * uM0
add(SER["M"], "feature", 1, round(uM0, 1), round(vM0, 1), 3, 4, "",
    "intercept: the dashed extension of line M meets sigma = 0 below the frame (tau < 0), on the measured dash "
    f"centerline; the solid part's fit extrapolated gives v {vMfit:.1f} there ({vM0 - vMfit:+.1f} px)")
add(SER["B"], "feature", 1, round(uB0, 1), round(vB0, 1), 3, 5, "",
    "intercept: extrapolated on the line fitted to B (its dashes lie within 2 px of the fit); the drawn dashed "
    "extension stops at the tau = 0 frame line, about 12 px short of the sigma = 0 axis")

cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px",
        "symbol", "note"]
with (OUT / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
(HERE / "skipped.txt").write_text("\n".join(skipped) + "\n", encoding="utf-8")
print(f"{len(rows)} rows; skipped:")
print("\n".join(skipped))
print("M dash line:", da, db, "M left end", uM0, vM0, val(uM0, vM0))
print("B tau=0 end", uBt, vBt, val(uBt, vBt), "B sigma=0", uB0, vB0, val(uB0, vB0))
print("A sigma=0", uA0, vA0, val(uA0, vA0))
