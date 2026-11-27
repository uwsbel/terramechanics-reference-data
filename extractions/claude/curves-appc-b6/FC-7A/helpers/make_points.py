"""Write out/FC-7A/points-p1.csv for Figure C-7A from the readings below.

Markers: circle centers from helpers/circlefit.py (ring inner and outer edge fits, center dot as a
check); triangle centroids read on ASCII ink maps (helpers/ascii.py), as the mean of the centroid
of the outer outline and the centroid of the inner hole (rule 8).
Traces: each line measured column by column on its ink (dark run nearest a seed line), leaving out
columns inside a symbol's zone, columns where the run is merged with a grid line or symbol
(longer than 14 px) and dash gaps. A sample at x = 2k psi sits at the clean column whose center,
from a straight fit over clean columns within +-12 px, maps closest to x = 2k. Left ends: straight
fit over the first two dashes, intersected with the x = 0 axis line. Right ends: see notes.
Usage: make_points.py   (run from the workspace root)
"""
import csv
import json

import numpy as np
from PIL import Image

CAL = "out/FC-7A/cal-p1/calibration.json"
IMG = "packet/p0135.png"
cal = json.load(open(CAL))
ax, ay = cal["ax"], cal["ay"]


def X(u, v):
    return ax[0] * u + ax[1] * v + ax[2]


def Y(u, v):
    return ay[0] * u + ay[1] * v + ay[2]


g = np.asarray(Image.open(IMG).convert("L")) < 160

# --- markers -------------------------------------------------------------------------------
circles = [  # u, v, bound, note
    (877.5, 2858.2, 2, "ring fit (877.3, 2857.9 inner; 877.6, 2858.6 outer), center dot 877.5, 2858.2; the 45 deg line runs into the ring on both sides; y = 5 grid line through the ring top"),
    (983.8, 2761.4, 2, "ring fit; the x = 5 grid line passes through the left part of the circle; the 45 deg line runs into the ring on both sides"),
    (1073.9, 2664.1, 2, "ring fit and center dot agree within 0.5 px; the 45 deg line runs into the ring on both sides"),
    (1295.6, 2416.6, 3, "ring fit; the x = 10 grid line passes through the left part of the circle and the 45 deg line through its lower right, so the ring is partly hidden; bound widened"),
    (1521.9, 2196.8, 2, "ring fit; the 45 deg line runs into the ring on both sides (through the center); y = 15 grid line along the ring bottom"),
    (2299.1, 1410.7, 2, "ring fit; the 45 deg line passes over the upper-left part of the ring and ends just beyond it"),
]
triangles = [  # u, v, u_bound, v_bound, note
    (876.3, 2706.0, 3, 7, "centroid: outer outline (apex 875.2, 2682.5; base 857 to 896.5 at 2720.5) gives v 2707.8, inner hole gives 2704.2; center dot 878, 2706; bbox midpoint v 2701.5; sits above the 50.5 deg line (off the line)"),
    (987.3, 2611.2, 3, 7, "centroid: outer outline (apex 987, 2585.5; base bottom 2625.5, right corner 1007.5; left corner hidden under the line) gives v 2611.8, inner hole 2610.5; center dot 985.5, 2612; the x = 5 grid line and the 50.5 deg line pass through it"),
    (1082.5, 2515.0, 3, 8, "centroid: apex hidden under the 50.5 deg line (outer apex estimated at 2489 from the hole apex 2499.5), base bottom 2531.5 merged with the y = 10 grid line; outer gives v 2517.3, inner hole 2512.8; center dot 1082, 2514; bound widened"),
    (1296.7, 2216.2, 3, 7, "centroid: outer outline (apex 1296.5, 2194.5; base 1277 to 1316.5, bottom 2228.5) gives v 2217.2, inner hole 2215.2; the x = 10 and y = 15 grid lines and the 50.5 deg line all pass through it"),
    (1523.5, 1887.5, 3, 7, "centroid: outer outline (apex 1525, 1865.5; base 1504 to 1541.5, bottom merged with the y = 20 grid line, about 1900) gives v 1888.5, inner hole 1886.5; sits above and left of the 50.5 deg line (off the line)"),
    (2339.0, 1053.5, 3, 7, "centroid: outer outline (apex 2338.5, 1030.5; base 2318 to 2360.5, bottom 1066) gives v 1054.2, inner hole 1052.8; center dot 2339.5, 1052; isolated, well below the 50.5 deg line"),
]
# symbol zones for the traces: circles by center and radius, triangles by bbox (+3 px)
zones = [("circle", u, v, 23.0) for u, v, *_ in circles]
tri_boxes = [(857, 2682, 897, 2721), (966, 2585, 1008, 2626), (1060, 2489, 1101, 2532),
             (1277, 2194, 1317, 2229), (1504, 1865, 1542, 1903), (2318, 1030, 2361, 1067)]
zones += [("tri", *b) for b in tri_boxes]


def in_zone(u, v, pad=0.0):
    for z in zones:
        if z[0] == "circle":
            if np.hypot(u - z[1], v - z[2]) < z[3] + pad:
                return True
        elif z[1] - 3 - pad <= u <= z[3] + 3 + pad and z[2] - 3 - pad <= v <= z[4] + 3 + pad:
            return True
    return False


def measure(u0, v0, s, ua, ub, maxlen=14):
    out = {}
    for u in range(ua, ub + 1):
        vp = v0 + s * (u - u0)
        a, b = int(vp - 25), int(vp + 25)
        col = g[a:b, u]
        runs, i = [], 0
        while i < len(col):
            if col[i]:
                j = i
                while j + 1 < len(col) and col[j + 1]:
                    j += 1
                runs.append((a + i, a + j))
                i = j + 1
            else:
                i += 1
        near = [r for r in runs if abs((r[0] + r[1]) / 2 - vp) < 14]
        if not near:
            continue
        r = min(near, key=lambda r: abs((r[0] + r[1]) / 2 - vp))
        c = (r[0] + r[1] + 1) / 2
        if r[1] - r[0] + 1 > maxlen or in_zone(u, c):
            continue
        out[u] = c
    return out


def local(cd, u, half=12, nmin=8):
    loc = [(uu, cd[uu]) for uu in range(u - half, u + half + 1) if uu in cd]
    if len(loc) < nmin:
        return None
    q = np.polyfit([p[0] for p in loc], [p[1] for p in loc], 1)
    return float(np.polyval(q, u)), len(loc)


def sample_at(cd, t):
    best = None
    for u in cd:
        r = local(cd, u)
        if r is None:
            continue
        vv, n = r
        if in_zone(u, vv, pad=5.0):  # keep samples at least 8 px clear of a symbol's outline
            continue
        e = abs(X(u, vv) - t)
        if best is None or e < best[0]:
            best = (e, u, vv, n)
    return best


lines = {
    "dr100": dict(seed=(666, 3012, -1.249), rng=(676, 2300), first_dashes=(676, 771), solid_from=853,
                  label=(1724.0, 1758.5, "50.5°")),
    "dr53": dict(seed=(666, 3088, -1.042), rng=(676, 2306), first_dashes=(676, 768), solid_from=838,
                 label=(1717.5, 2045.0, "45°")),
}
rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append(dict(figure_id="FC-7A", panel=1, series_id=series, point_kind=kind, sequence=seq,
                     pixel_u=round(u, 1), pixel_v=round(v, 1), u_bound_px=bu, v_bound_px=bv,
                     symbol=symbol, note=note))


for k, (u, v, b, note) in enumerate(circles, 1):
    add("dr53", "marker", k, u, v, b, b, "dotted circle", "circle with a center dot, as in the legend; " + note)
for k, (u, v, bu, bv, note) in enumerate(triangles, 1):
    add("dr100", "marker", k, u, v, bu, bv, "dotted triangle", "upright triangle with a center dot, as in the legend; " + note)

report = []
for sid in ("dr100", "dr53"):
    L = lines[sid]
    cd = measure(*L["seed"], *L["rng"])
    # left end: fit over the first two dashes, intersect with x = 0
    a, b = L["first_dashes"]
    us = [u for u in cd if a <= u <= b]
    q = np.polyfit(us, [cd[u] for u in us], 1)
    uu = np.linspace(640, 700, 6001)
    xx = np.array([X(u, np.polyval(q, u)) for u in uu])
    i = int(np.argmin(np.abs(xx)))
    ul, vl = float(uu[i]), float(np.polyval(q, uu[i]))
    report.append(f"{sid}: first-dash fit v = {q[1]:.2f} + {q[0]:.4f} u over {len(us)} columns; "
                  f"x=0 at u {ul:.1f} v {vl:.1f} y {Y(ul, vl):.3f}")
    seq = 1
    add(sid, "trace", seq, ul, vl, 5, 5, "", "left end: the dashed part reaches the shear axis; placed where the first dash's centerline meets the x = 0 axis line (the dash ink merges with the axis ink); dashed")
    for t in range(2, 27, 2):
        e, u, vv, n = sample_at(cd, float(t))
        dashed = u < L["solid_from"]
        note = f"x = {t} psi sample on the line ink (local fit over {n} clean columns)"
        if e > 0.02:
            # why the exact x = t column was not used: is the point of the line at x = t (the straight
            # local line through this sample, slope of the seed) inside a symbol zone?
            uu_ = np.arange(u - 40, u + 40, 0.25)
            vv_ = vv + L["seed"][2] * (uu_ - u)
            k_ = int(np.argmin(np.abs(np.array([X(a_, b_) for a_, b_ in zip(uu_, vv_)]) - t)))
            near_sym = in_zone(uu_[k_], vv_[k_], pad=5.0)
            why = "falls on or next to a symbol" if near_sym else "falls where the line ink merges with a grid line"
            note += f"; x = {t} {why}, sample at the nearest clean line ink, x = {X(u, vv):.3f}"
        for vline in cal["vertical_lines"]:
            ug = vline["u_at_v0"] + vline["slope_du_dv"] * vv
            if abs(ug - u) < 8:
                note += f"; crosses the x = {vline['x_value']:g} grid line here"
        for hline in cal["horizontal_lines"]:
            vg = hline["v_at_u0"] + hline["slope_dv_du"] * u
            if abs(vg - vv) < 10:
                note += f"; crosses the y = {hline['y_value']:g} grid line here"
        if sid == "dr100" and t == 2:
            # 5 px from the lower end of the third dash, where the column runs are cut by the dash
            # cap and merged with the y = 5 grid line: the column fit sat 2.5 px above the ink's
            # center; read instead from row centers (row 2858: ink u 787 to 795, center 791)
            u, vv = 791, 2858.0
            note = ("x = 2 psi sample on the line ink, read from the row centers of the dash (row 2858, "
                    "ink u 787 to 795) because the column runs here are cut by the dash end and merged "
                    "with the y = 5 grid line; 3 px from the dash's lower end")
        if dashed:
            note += "; dashed"
        seq += 1
        add(sid, "trace", seq, u, vv, 4, 4, "", note)
        report.append(f"{sid} x={t}: u {u} v {vv:.1f} x {X(u, vv):.3f} y {Y(u, vv):.3f} n {n}")
    # right end
    if sid == "dr100":
        us = [u for u in cd if 2200 <= u <= 2300]
        q = np.polyfit(us, [cd[u] for u in us], 1)
        uu = np.linspace(2290, 2330, 4001)
        yy = np.array([Y(u, np.polyval(q, u)) for u in uu])
        i = int(np.argmin(np.abs(yy - 35.0)))
        ur, vr = float(uu[i]), float(np.polyval(q, uu[i]))
        add(sid, "trace", seq + 1, ur, vr, 6, 7, "", "right end: the line runs into the top frame line (y = 35) and stops there; placed where its centerline meets the frame centerline; its own ink is last seen apart from the frame at the frame's lower edge (about u 2308, v 961), inside the bound")
        report.append(f"{sid} right end: local fit v = {q[1]:.2f} + {q[0]:.4f} u; y=35 at u {ur:.1f} v {vr:.1f} x {X(ur, vr):.3f}")
    else:
        us = [u for u in cd if 2230 <= u <= 2280]
        q = np.polyfit(us, [cd[u] for u in us], 1)
        ur = 2307.0
        vr = float(np.polyval(q, ur))
        add(sid, "trace", seq + 1, ur, vr, 4, 4, "", "right end: where the line's ink ends (tip at u 2307 to 2309, v 1373 to 1384), just beyond the last circle, whose upper-left ring the line passes over")
        report.append(f"{sid} right end: local fit v = {q[1]:.2f} + {q[0]:.4f} u; at u {ur} v {vr:.1f} x {X(ur, vr):.3f} y {Y(ur, vr):.3f}")
    # features
    add(sid, "feature", 1, ul, vl, 5, 5, "", "intercept: where the line's dashed extension meets the normal-load-zero axis, from the fit over the first two dashes")
    lu, lv, txt = L["label"]
    add(sid, "feature", 2, lu, lv, 6, 6, "", f"label: {txt} (center of the glyph bounding box; printed rotated along the line, on its lower-right side)")

with open("out/FC-7A/points-p1.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("\n".join(report))
print(f"wrote {len(rows)} rows")
