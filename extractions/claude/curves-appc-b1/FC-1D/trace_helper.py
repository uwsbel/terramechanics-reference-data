"""Helper for the FC-1D reading (Claude, blind). Follows each upper-panel drawn curve as a ridge:
from the first marker, step 3 px along the current direction, search a short line normal to the
curve for the dark segment nearest the prediction, and record its center and thickness (measured
across the line). Thin ink lying on a horizontal gridline is rejected as the gridline. The output
is checked on the overlay and on crops; flagged points are read by eye.

Run from the FC-1D workspace:
    python out/FC-1D/trace_helper.py packet/p0119.png out/FC-1D/cal-p1/calibration.json out/FC-1D/trace-raw.csv
"""
import csv
import json
import sys

import numpy as np
from PIL import Image

DARK = 200
STEP = 3.0          # arc step in px
HALF = 16           # half-length of the normal search line
TOL = 9             # max offset along the normal to accept a segment
MAX_GAP = 46        # px of no ink before the trace is declared ended (past the last marker)
MARKER_R = 16       # ink within this radius of a marker center is the symbol, not the line
GUIDE_TOL = {"n2345": 70}  # a point farther than this from the marker polyline is another curve
GUIDE_TOL_DEFAULT = 40     # (n2345: several squares sit 40 to 60 px above the drawn line)
# where each drawn line ends (u): the five long curves end at their last marker on the x=250
# gridline; n294 and n0 end before their frame, limits read from the tiles
END_U = {"n3520": 2036, "n2935": 2040, "n2345": 2055, "n1468": 2040, "n587": 2057,
         "n294": 1514, "n0": 1470}

# Upper-panel markers read by eye from the zoom-4 tiles and zoom-6 detail crops (u, v).
MARKERS = {
    "n3520": [(626, 2134), (746.5, 1829), (857.5, 1667), (974, 1549), (1089.5, 1481), (1204.5, 1441),
              (1319, 1437.5), (1441, 1462.5), (1565.5, 1524), (1737.5, 1576), (1854, 1676),
              (2027.5, 1699)],
    "n2935": [(636, 2186), (742, 1920), (974, 1665.5), (1092, 1604), (1209, 1594),
              (1327.5, 1614), (1440, 1641), (1615, 1684), (1736, 1716), (2032, 1761)],
    "n2345": [(681, 2157.5), (794, 1930), (920, 1861), (1031, 1814), (1147, 1792.5),
              (1260, 1795), (1384, 1814.5), (1502, 1838), (1625, 1844), (1737, 1840),
              (1861, 1969), (2047, 2043)],
    "n1468": [(642, 2526), (750, 2315), (866, 2207), (980.5, 2151), (1104, 2140.5),
              (1219.5, 2141), (1276, 2144), (1388, 2142.5), (1506, 2145), (1632, 2140.5),
              (1748, 2260.5), (1866, 2260)],
    "n587": [(638, 2694), (760.5, 2558), (875, 2506), (988, 2487), (1109, 2482),
             (1280, 2521), (1398, 2539), (1522.5, 2558), (1634, 2577.5), (1755, 2592.5),
             (1877, 2623), (2049, 2627.5)],
    "n294": [(621, 2799), (710, 2698), (934, 2615), (1054, 2610), (1172, 2625),
             (1402, 2670), (1531, 2699)],
    "n0": [(699, 2818), (822.5, 2781), (929, 2771), (1001, 2768), (1120, 2774),
           (1231, 2783), (1350, 2794)],
}


def segments(dark):
    """Dark segments (center index, length) in a boolean 1-D array."""
    out = []
    s = None
    for i, d in enumerate(dark):
        if d and s is None:
            s = i
        elif not d and s is not None:
            out.append(((s + i - 1) / 2, i - s))
            s = None
    if s is not None:
        out.append(((s + len(dark) - 1) / 2, len(dark) - s))
    return out


def main():
    img, calp, outp = sys.argv[1:4]
    g = np.asarray(Image.open(img).convert("L"))
    H, W = g.shape
    cal = json.load(open(calp))
    hlines = [(h["y_value"], h["v_at_u0"], h["slope_dv_du"]) for h in cal["horizontal_lines"]]
    vlines = [(x["x_value"], x["u_at_v0"], x["slope_du_dv"]) for x in cal["vertical_lines"]]

    def is_dark(u, v):
        ui, vi = int(round(u)), int(round(v))
        return 0 <= ui < W and 0 <= vi < H and g[vi, ui] < DARK

    def row_thickness(u, v):
        """Horizontal ink thickness at row v through column u."""
        ui, vi = int(round(u)), int(round(v))
        if not is_dark(ui, vi):
            return 0
        a = ui
        while a > 0 and g[vi, a - 1] < DARK:
            a -= 1
        b = ui
        while b < W - 1 and g[vi, b + 1] < DARK:
            b += 1
        return b - a + 1

    def col_thickness(u, v):
        """Vertical ink thickness at column u through row v."""
        ui, vi = int(round(u)), int(round(v))
        if not is_dark(ui, vi):
            return 0
        a = vi
        while a > 0 and g[a - 1, ui] < DARK:
            a -= 1
        b = vi
        while b < H - 1 and g[b + 1, ui] < DARK:
            b += 1
        return b - a + 1

    def near_hgrid(u, v):
        return any(abs(v0 + s * u - v) < 5 for _, v0, s in hlines)

    def near_vgrid(u, v):
        return any(abs(u0 + s * v - u) < 6 for _, u0, s in vlines)

    rows = []
    for sid, mk in MARKERS.items():
        mk = sorted(mk)
        mu = np.array([m[0] for m in mk])
        mv = np.array([m[1] for m in mk])

        def guide_dir(u):
            # direction of the marker polyline at u
            i = int(np.searchsorted(mu, u, side="right"))
            i = min(max(i, 1), len(mu) - 1)
            d = np.array([mu[i] - mu[i - 1], mv[i] - mv[i - 1]], float)
            return d / np.linalg.norm(d)

        p = np.array(mk[0], float)
        d = guide_dir(p[0] + 1)
        hist = [p.copy()]
        gap = 0.0
        seq = 0
        rows.append((sid, seq, round(p[0], 1), round(p[1], 1), 0, "start;marker", 0))
        while p[0] < END_U[sid]:
            pp = p + STEP * d
            guide_v = float(np.interp(pp[0], mu, mv))
            n = np.array([-d[1], d[0]])
            ts = np.arange(-HALF, HALF + 1)
            dark = np.array([is_dark(*(pp + t * n)) for t in ts])
            segs = [(ts[0] + c, L) for c, L in segments(dark)]
            # offset along the normal at which the marker polyline sits
            n_v = n[1] if abs(n[1]) > 1e-6 else 1e-6
            t_guide = (guide_v - pp[1]) / n_v
            cand = [s for s in segs if abs(s[0]) <= TOL or abs(s[0] - t_guide) <= 20]
            flags = []
            near_marker = bool(np.any(np.hypot(mu - pp[0], mv - pp[1]) < MARKER_R))
            if near_marker:
                flags.append("marker")
            chosen = None
            if cand:
                c = min(cand, key=lambda s: abs(s[0]) + 0.5 * abs(s[0] - t_guide))
                q = pp + c[0] * n
                thick = c[1]
                if thick > 30:
                    flags.append("thick")          # a vertical gridline or a symbol stroke
                elif near_hgrid(*q) and col_thickness(*q) <= 8:
                    flags.append("hgrid-rejected")  # thin ink on a gridline: the gridline
                elif near_vgrid(*q) and row_thickness(*q) <= 9:
                    flags.append("vgrid-rejected")
                elif abs(q[1] - float(np.interp(q[0], mu, mv))) > GUIDE_TOL.get(sid, GUIDE_TOL_DEFAULT):
                    flags.append("far-from-markers-rejected")
                else:
                    chosen = (q, thick)
                    if near_hgrid(*q):
                        flags.append("hgrid")
                    if near_vgrid(*q):
                        flags.append("vgrid")
                    if thick > 18:
                        flags.append("merged")
                    if len(cand) > 1:
                        flags.append("multi")
            if chosen is None:
                gap += STEP
                p = pp
                # in a gap, steer toward the marker polyline
                gd = guide_dir(p[0])
                d = 0.6 * d + 0.4 * gd
                d /= np.linalg.norm(d)
                if gap > 120:
                    break
                rows.append((sid, None, round(p[0], 1), round(p[1], 1), 0, ";".join(flags + ["gap"]), round(gap)))
                continue
            q, thick = chosen
            gap = 0.0
            hist.append(q.copy())
            if near_marker:
                # symbol edges deflect the direction: steer by the marker polyline instead
                gd = guide_dir(q[0])
                d = 0.7 * d + 0.3 * gd
                d /= np.linalg.norm(d)
            elif len(hist) > 5:
                dd = hist[-1] - hist[-5]
                nd = np.linalg.norm(dd)
                if nd > 0:
                    d = 0.5 * d + 0.5 * dd / nd
                    d /= np.linalg.norm(d)
            p = q
            seq += 1
            rows.append((sid, seq, round(q[0], 1), round(q[1], 1), thick, ";".join(flags), 0))
    with open(outp, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series_id", "seq", "u", "v", "thickness", "flags", "gap"])
        w.writerows(rows)
    print("wrote", outp, len(rows), "rows")


if __name__ == "__main__":
    main()
