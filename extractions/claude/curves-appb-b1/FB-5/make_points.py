"""Write out/FB-5/points-p1.csv (pixels) for FB-5 from the measurements of markers.py, outer.py,
template.py and lines.py (lines.json). Trace samples lie on the fitted centre line of each drawn
segment (rms of the ink about it 0.5 to 0.7 px); each is checked against the ink on a profile across
the line, and a sample where the line runs through a marker ring is noted. The x positions of the
1 psi samples come from the piecewise map of cal-p1 (tools/calibrate_axes.py), inverted along the
segment by bisection.
Usage: python make_points.py <image> <lines.json> <cal_dir> <out.csv>"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from calibrate_axes import piecewise_maps  # noqa: E402

img, lines_json, cal_dir, out_csv = sys.argv[1:5]
g = np.asarray(Image.open(img).convert("L"))
dark = g < 128
L = json.load(open(lines_json))
cal, X, Y = piecewise_maps(cal_dir, img)
R_OUT = 19.2
M = L["markers"]

rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append({"figure_id": "FB-5", "panel": 1, "series_id": series, "point_kind": kind, "sequence": seq,
                 "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv,
                 "symbol": symbol, "note": note})


# ---- markers (sequence by increasing confining pressure within the series)
CLEAN = "open circle, centre from circles fitted to its hole and to its ring's outer edge (agree within {d:.1f} px)"
markers = {
    "dr84": [
        ("dense_left_lowL", 4, 4, "left of two overlapping circles at the lower left of the dense line (distinct: two holes and the lens between them visible); centre from a joint ring-template match of both circles; bound widened for the overlap"),
        ("dense_left_lowR", 4, 4, "right of two overlapping circles at the lower left of the dense line; the dense line's left end meets the top of this ring; centre from a joint ring-template match; bound widened for the overlap"),
        ("dense_left_top", 2, 2, CLEAN.format(d=1.3) + "; the dense line runs along the right side of its ring"),
        ("dense_mid_up", 2, 2, CLEAN.format(d=0.1) + "; the upper dense segment runs along the lower right of its ring"),
        ("dense_mid_low", 2, 2, CLEAN.format(d=1.4) + "; the lower dense segment runs through the left side of its ring; the vertex is at the top of this ring"),
        ("dense_top_low", 2, 2, CLEAN.format(d=0.8) + "; the dense line runs through the left side of its ring"),
        ("dense_top_up", 2, 2, CLEAN.format(d=0.8) + "; the dense line's right end touches its ring"),
    ],
    "dr26": [
        ("loose_bot_up", 2, 2, CLEAN.format(d=0.6) + "; the loose line meets its ring at the lower right, where it touches the ring below"),
        ("loose_bot_low", 2, 2, CLEAN.format(d=0.8) + "; touches the ring above"),
        ("loose_mid_up", 2, 2, CLEAN.format(d=1.1) + "; touches the ring below; the vertex of the loose line is hidden where the two rings touch"),
        ("loose_mid_low", 2, 2, CLEAN.format(d=0.6) + "; touches the ring above"),
        ("loose_top_low", 5, 5, "partly printed open circle: only the lower left arc of its ring is inked (it reads as a '(' at page scale), with two specks where the top of the ring would be; centre from a ring-template match of the measured radii to the arc; same u as the circle above it and the loose line ends half way between them; bound widened"),
        ("loose_top_up", 2, 2, CLEAN.format(d=0.7) + "; the loose line ends below it, without touching"),
    ],
}


def xval(u, v):
    return X.value(u, v)[0]


for series, lst in markers.items():
    lst = sorted(lst, key=lambda m: xval(*M[m[0]]))
    for i, (name, bu, bv, note) in enumerate(lst, 1):
        u, v = M[name]
        add(series, "marker", i, u, v, bu, bv, "circle", note)


# ---- traces
def seg_dir(s):
    a, b = np.array(s["a"]), np.array(s["b"])
    return a, (b - a) / np.hypot(*(b - a))


def on_line(s, x_target):
    """Point of segment s's fitted line where the piecewise x equals x_target (bisection)."""
    a, d = seg_dir(s)
    lo, hi = -100.0, np.hypot(*(np.array(s["b"]) - a)) + 100.0
    flo = xval(*(a + lo * d)) - x_target
    for _ in range(60):
        mid = (lo + hi) / 2
        fm = xval(*(a + mid * d)) - x_target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return a + (lo + hi) / 2 * d


def ink_check(s, p):
    """Offset of the ink centre from the fitted line at p (profile across, nearest run) and its width."""
    _, d = seg_dir(s)
    n = np.array([-d[1], d[0]])
    offs = np.arange(-12, 12.01, 0.5)
    vals = [bool(dark[int(round(p[1] + o * n[1])), int(round(p[0] + o * n[0]))]) for o in offs]
    best, i = None, 0
    while i < len(offs):
        if vals[i]:
            j = i
            while j + 1 < len(offs) and vals[j + 1]:
                j += 1
            c, w = (offs[i] + offs[j]) / 2, offs[j] - offs[i] + 0.5
            if best is None or abs(c) < abs(best[0]):
                best = (c, w)
            i = j + 1
        else:
            i += 1
    return best


def ring_near(p):
    out = []
    for name, m in M.items():
        r = np.hypot(p[0] - m[0], p[1] - m[1])
        if r <= R_OUT + 1:
            out.append(name)
    return out


HALF = {"dense_1": 4.25, "dense_2": 4.5, "loose_1": 4.75, "loose_2": 4.75}   # half the median line width (lines.py)
groups = {
    "dr84": ("dense_1", "dense_2", L["vertex_dense"], L["ends"]["dense_left"], L["ends"]["dense_right"]),
    "dr26": ("loose_1", "loose_2", L["vertex_loose"], L["ends"]["loose_left"], L["ends"]["loose_right"]),
}
END_NOTES = {
    "dense_left": ("left end: the line's ink meets the outer edge of the right circle of the overlapping pair at the "
                   "lower left; it may run on hidden under that ring for up to 14 px (to the white interior)"),
    "dense_right": "right end: the line's ink ends here, touching the lower right of the upper top marker's ring",
    "loose_left": ("left end: the line's ink meets the outer edge of the upper of the two lower-left rings, where the two "
                   "rings touch; it may run on hidden through the joined rings for up to 35 px (to the outer edge of the "
                   "lower ring, beyond which the page is white)"),
    "loose_right": "right end: the line's ink ends here, free (half way between the two top markers, touching neither)",
}
feat_rows = []
for series, (s1n, s2n, vtx, eL, eR) in groups.items():
    s1, s2 = L["segments"][s1n], L["segments"][s2n]
    pL = np.array(eL["ring"][0] if eL["ring"] else eL["ink_end"])
    pR = np.array(eR["ink_end"])
    pV = np.array(vtx)
    xL, xV, xR = xval(*pL), xval(*pV), xval(*pR)
    samples = [(pL, s1n, "end", "left")]
    samples += [(on_line(s1, k), s1n, "grid", k) for k in range(int(np.floor(xL)) + 1, int(np.ceil(xV)))]
    samples += [(pV, s1n, "vertex", None)]
    samples += [(on_line(s2, k), s2n, "grid", k) for k in range(int(np.floor(xV)) + 1, int(np.ceil(xR)))]
    samples += [(pR, s2n, "end", "right")]
    gname = "dense" if series == "dr84" else "loose"
    for i, (p, sn, role, k) in enumerate(samples, 1):
        h = HALF[sn]
        chk = ink_check(L["segments"][sn], p)
        rings = ring_near(p)
        bits = []
        if role == "end":
            bits.append(END_NOTES[f"{gname}_{k}"])
        elif role == "vertex":
            bits.append("vertex: intersection of the two fitted segments")
        else:
            bits.append(f"sample at {k} psi on the fitted segment")
        if chk is not None and role == "grid":
            bits.append(f"ink centre {chk[0]:+.1f} px from the fitted line, ink width {chk[1]:.1f} px")
        if rings and role == "grid":
            bits.append("the line runs through the ring of marker " + ", ".join(rings) + " here (position from the straight fit)")
        add(series, "trace", i, float(p[0]), float(p[1]), h, h, "", "; ".join(bits))
    # features: first point, vertex, last point, label
    s1a, d1 = seg_dir(s1)
    if gname == "dense":
        fL = (pL, 6, 13)     # 14 px hidden along the line (direction (0.43, -0.90)): du 6, dv 13
        vnote = ("vertex: intersection of the two fitted segments (they meet at 17 deg); on the ink: the upper segment's ink "
                 "runs down between the two mid markers to the top of the lower ring, where the lower segment arrives")
        fV = (pV, 5, 5)
    else:
        fL = (pL, 26, 25)    # up to 35 px hidden along the line (direction (-0.72, 0.70))
        vnote = ("vertex: intersection of the two fitted segments (they meet at 11 deg); hidden where the rings of the two mid "
                 "markers touch, so located by the fits only; bound widened")
        fV = (pV, 6, 6)
    h1, h2 = HALF[s1n], HALF[s2n]
    feat_rows.append((series, [
        (fL[0], fL[1], fL[2], "first point; " + END_NOTES[f"{gname}_left"] + "; bound widened along the line to cover the hidden part"),
        (fV[0], fV[1], fV[2], vnote),
        (pR, h2, h2, "last point; " + END_NOTES[f"{gname}_right"]),
    ]))

LABELS = {
    "dr84": ((2429, 1068, 2744, 1201), "label: Dense / D_r = 0.84",
             "printed in two lines, 'Dense' over 'Dr = o.84' (the zero is typed small, like an 'o'); centre of the bounding box of both lines (u 2429-2744, v 1068-1201); right of the top end of the upper line"),
    "dr26": ((2450, 2495, 2766, 2613), "label: Loose / D_r = 0.26",
             "printed in two lines, 'Loose' over 'Dr = 0.26' with the '0.' poorly printed (only the top arc of the 0 is inked, no decimal point visible, the '=' broken); it fits the series' printed Dr; centre of the bounding box of both lines (u 2450-2766, v 2495-2613); right of the top end of the lower line"),
}
for series, feats in feat_rows:
    seq = 1
    for p, bu, bv, note in feats:
        add(series, "feature", seq, float(p[0]), float(p[1]), bu, bv, "", note)
        seq += 1
    (u0, v0, u1, v1), lab, lnote = LABELS[series]
    add(series, "feature", seq, (u0 + u1) / 2, (v0 + v1) / 2, 10, 10, "", lab + "; " + lnote)

with open(out_csv, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"wrote {out_csv}: {len(rows)} rows")
for r in rows:
    if r["point_kind"] == "trace":
        print(r["series_id"], r["sequence"], r["pixel_u"], r["pixel_v"], "|", r["note"][:150])
