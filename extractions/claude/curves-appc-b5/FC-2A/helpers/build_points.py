"""Build out/FC-2A/points-p1.csv (pixel readings) for FC-2A.

Markers: centers measured with markers.py (hole centroid, checked against the ring's outer extents
on the central row and column) and confirmed on the zoomed crops in ../crops/m_*.png.
Traces: per line, the measured ink center column by column (scan as in traces.py); each sample is
a local straight-line fit to the ink centers of the clean columns within +-8 px of it (never the
global fit), skipped when it would fall in a dash gap or on a symbol (rule 7).
Features: intercept (line centerline carried to the left-axis center line, x = 0) and the printed
angle label's ink bounding-box center.

usage: python build_points.py <page.png> <calibration.json> <out_points.csv>
"""
import json
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
cal = json.load(open(sys.argv[2], encoding="utf-8"))
out_csv = sys.argv[3]
ax, ay = cal["ax"], cal["ay"]
X = lambda u, v: ax[0] * u + ax[1] * v + ax[2]
Y = lambda u, v: ay[0] * u + ay[1] * v + ay[2]
la = cal["left_axis"]

FIG = "FC-2A"
rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append(dict(figure_id=FIG, panel=1, series_id=series, point_kind=kind, sequence=seq,
                     pixel_u=round(float(u), 1), pixel_v=round(float(v), 1), u_bound_px=bu, v_bound_px=bv,
                     symbol=symbol, note=note))


# ---------------------------------------------------------------- markers
markers = {
    "dr33-53": [  # squares; all six lie on or next to the upper (49.5 deg) line
        (1179.3, 2983.7, "on its line (the line runs into the lower-left and upper-right corners)"),
        (1400.3, 2769.7, "just below-right of its line, not touching"),
        (1605.7, 2492.4, "on its line (the line runs into the lower-left and upper-right corners)"),
        (1830.4, 2192.7, "above-left of its line, about 25 px clear"),
        (2039.5, 2066.4, "below-right of its line, about 45 px clear"),
        (2259.5, 1854.0, "below-right of its line, about 120 px clear; outline broken at the top (print), center from outer extents"),
    ],
    "dr115-130": [  # circles; lower (46.7 deg) line
        (1185.4, 3061.6, "on its line (the line runs into the lower-left and upper-right of the ring)"),
        (1402.4, 2816.8, "above-left of its line, ring touching the line at its lower right"),
        (1611.3, 2593.3, "above-left of its line, ring touching the line at its lower right"),
        (1819.3, 2403.8, "on its line (the line runs into the lower-left and upper-right of the ring)"),
        (2040.6, 2217.7, "below-right of its line, about 35 px clear"),
        (2255.8, 2052.9, "below-right of its line, about 100 px clear"),
    ],
}
symbols = {"dr33-53": "square", "dr115-130": "circle"}
all_markers = []
for s, ms in markers.items():
    for i, (u, v, note) in enumerate(ms, 1):
        add(s, "marker", i, u, v, 2, 2, symbols[s], "hollow; " + note)
        all_markers.append((u, v))

# ---------------------------------------------------------------- traces
lines = {"dr33-53": ((1020, 3165), (2333, 1654)), "dr115-130": ((1033, 3220), (2374, 1818))}
labels_box = {"dr33-53": (1645, 2262, 1750, 2395), "dr115-130": (1828, 2222, 1930, 2350)}
printed = {"dr33-53": "49.5°", "dr115-130": "46.7°"}


def runs(col, off):
    idx = np.where(col)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s + off, p + off))
            s = i
        p = i
    out.append((s + off, p + off))
    return out


fits = {}
report = []
for s, ((u0, v0), (u1, v1)) in lines.items():
    b0 = (v1 - v0) / (u1 - u0)
    a0 = v0 - b0 * u0
    cols = {}
    for u in range(940, 2420):
        vp = a0 + b0 * u
        rs = [r for r in runs(g[int(vp) - 22:int(vp) + 23, u], int(vp) - 22) if abs((r[0] + r[1]) / 2 - vp) < 20]
        if rs:
            r = min(rs, key=lambda r: abs((r[0] + r[1]) / 2 - vp))
            cols[u] = ((r[0] + r[1]) / 2, r[1] - r[0] + 1)
    # global fit on the clean solid part, for the thickness, the direction and the intercept
    sol = np.array([(u, c) for u, (c, L) in cols.items() if u0 + 5 < u < u1 - 5 and 13 <= L <= 18
                    and min(np.hypot(u - mu, c - mv) for mu, mv in all_markers) > 25], dtype=float)
    b, a = np.polyfit(sol[:, 0], sol[:, 1], 1)
    Lmed = float(np.median([cols[int(u)][1] for u in sol[:, 0]]))
    t = Lmed / np.sqrt(1 + b * b)
    half = round(t / 2, 1)
    fits[s] = (a, b, t)
    # dash segments: ink runs in u before the solid part starts
    us = sorted(u for u in cols if cols[u][1] >= 3)
    segs, cur = [], [us[0], us[0]]
    for u in us[1:]:
        if u == cur[1] + 1:
            cur[1] = u
        else:
            segs.append(tuple(cur))
            cur = [u, u]
    segs.append(tuple(cur))
    solid = max(segs, key=lambda sg: sg[1] - sg[0])
    dashes = [sg for sg in segs if sg[1] < solid[0] and sg[1] - sg[0] > 10]
    report.append(f"{s}: global fit v = {a:.2f} + {b:.5f} u, thickness {t:.1f} px; solid ink u {solid[0]}..{solid[1]}; dashes {dashes}")

    # intercept: the first dash's centerline (local fit on its clean columns, away from the axis ink)
    d0 = dashes[0]
    dc = np.array([(u, cols[u][0]) for u in range(d0[0], d0[1] + 1) if u >= la["u_at_v0"] + la["slope_du_dv"] * cols[u][0] + 4
                   and cols[u][1] >= 11], dtype=float)
    bd, ad = np.polyfit(dc[:, 0], dc[:, 1], 1)
    # use the global direction through the dash's mean center (a 25-px dash is too short for its own slope)
    uc, vc = dc[:, 0].mean(), dc[:, 1].mean()
    a_d = vc - b * uc
    # meet the left axis u = al + bl v
    al, bl = la["u_at_v0"], la["slope_du_dv"]
    ui = (al + bl * a_d) / (1 - bl * b)
    vi = a_d + b * ui
    ug = (al + bl * a) / (1 - bl * b)
    vg = a + b * ug
    report.append(f"   first dash own slope {bd:.3f} (global {b:.3f}); intercept from dash: u {ui:.1f} v {vi:.1f} y {Y(ui, vi):.1f}; "
                  f"from solid fit extended: u {ug:.1f} v {vg:.1f} y {Y(ug, vg):.1f}")

    seq = 1
    add(s, "trace", seq, ui, vi, half, half, "", "left end on the shear-stress axis (x = 0): first dash's centerline where its ink joins the axis ink; dashed")
    # columns where the line's ink is merged with a symbol (run clearly longer than the line's own,
    # next to a marker) or interrupted by a symbol's white interior
    dmark = lambda u, v: min(np.hypot(u - mu, v - mv) for mu, mv in all_markers)
    bad = set()
    for u, (c, L) in cols.items():
        vline = a + b * u
        if dmark(u, vline) < 30 and (L >= Lmed + 3 or abs(c - vline) > 3):
            bad.add(u)
    # samples every 250 psf
    tgt = 250
    while True:
        uu = None
        for u in range(int(ui) + 1, solid[1] + 1):
            if u in cols and u + 1 in cols and X(u, cols[u][0]) <= tgt < X(u + 1, cols[u + 1][0]):
                uu = u
                break
        if uu is None:
            break
        seg = next((sg for sg in segs if sg[0] <= uu <= sg[1]), None)
        in_gap = seg is None
        near_bad = [u for u in bad if abs(u - uu) <= 3]
        dashed = seg is not None and seg != solid
        if in_gap or near_bad:
            report.append(f"   skip x={tgt}: {'dash gap' if in_gap else 'on a symbol (merged columns %d..%d)' % (min(near_bad), max(near_bad))} at u {uu}")
            tgt += 250
            continue
        clean = [u for u in range(uu - 8, uu + 9) if u in cols and seg[0] + 2 <= u <= seg[1] - 2 and abs(cols[u][1] - Lmed) <= 4
                 and not any(abs(u - w) <= 3 for w in bad)]
        if len(clean) < 6:
            report.append(f"   skip x={tgt}: only {len(clean)} clean columns at u {uu}")
            tgt += 250
            continue
        arr = np.array([(u, cols[u][0]) for u in clean], dtype=float)
        bl_, al_ = np.polyfit(arr[:, 0], arr[:, 1], 1)
        us_ = (tgt - ax[2] - ax[1] * al_) / (ax[0] + ax[1] * bl_)   # solve x(u, al_ + bl_ u) = tgt
        vs_ = al_ + bl_ * us_
        nb = min(bad, key=lambda w: abs(w - us_))
        note = f"x = {tgt} psf sample" + ("; dashed" if dashed else "")
        if abs(nb - us_) <= 10:
            note += f"; a symbol touches the line {abs(nb - us_):.0f} px away, fit on the clean columns only"
        seq += 1
        add(s, "trace", seq, us_, vs_, half, half, "", note)
        tgt += 250
    # right end: walk along the local centerline of the last 40 clean columns until the ink ends
    endc = np.array([(u, cols[u][0]) for u in range(solid[1] - 45, solid[1] - 5) if u in cols and abs(cols[u][1] - Lmed) <= 4], dtype=float)
    be, ae = np.polyfit(endc[:, 0], endc[:, 1], 1)
    step = 0.25 / np.hypot(1, be)
    uw = solid[1] - 10.0
    while g[int(round(ae + be * (uw + step))), int(round(uw + step))]:
        uw += step
    pe = (uw, ae + be * uw)
    seq += 1
    add(s, "trace", seq, pe[0], pe[1], half, half, "", "right end of the solid line's ink (last ink on its centerline)")
    report.append(f"   right end u {pe[0]:.1f} v {pe[1]:.1f}; x {X(*pe):.1f} y {Y(*pe):.1f}")

    # features
    add(s, "feature", 1, ui, vi, half, half, "", "intercept")
    # label center: ink bounding box in the label box, excluding both lines' ink
    u0b, v0b, u1b, v1b = labels_box[s]
    vv, uu_ = np.nonzero(g[v0b:v1b, u0b:u1b])
    P = np.stack([uu_ + u0b, vv + v0b], axis=1).astype(float)
    keep = np.ones(len(P), bool)
    for (aa, bb, tt) in fits.values():
        keep &= np.abs(P[:, 1] - (aa + bb * P[:, 0])) / np.hypot(1, bb) > tt / 2 + 3
    if len(fits) < 2:   # the other line is fitted later; exclude it with its rough position
        for s2, ((p0u, p0v), (p1u, p1v)) in lines.items():
            if s2 not in fits:
                bb = (p1v - p0v) / (p1u - p0u)
                aa = p0v - bb * p0u
                keep &= np.abs(P[:, 1] - (aa + bb * P[:, 0])) / np.hypot(1, bb) > 11
    P = P[keep]
    lu, lv = (P[:, 0].min() + P[:, 0].max()) / 2, (P[:, 1].min() + P[:, 1].max()) / 2
    report.append(f"   label {printed[s]}: ink box u {P[:, 0].min():.0f}..{P[:, 0].max():.0f} v {P[:, 1].min():.0f}..{P[:, 1].max():.0f}, center {lu:.1f} {lv:.1f}")
    add(s, "feature", 2, lu, lv, round((P[:, 0].max() - P[:, 0].min()) / 2, 1), round((P[:, 1].max() - P[:, 1].min()) / 2, 1), "",
        f"label: {printed[s]}")

cols_out = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
order = {"marker": 0, "trace": 1, "feature": 2}
rows.sort(key=lambda r: (r["series_id"] != "dr33-53", order[r["point_kind"]], r["sequence"]))
import csv
with open(out_csv, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols_out, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("\n".join(report))
print(f"wrote {out_csv}: {len(rows)} rows")
