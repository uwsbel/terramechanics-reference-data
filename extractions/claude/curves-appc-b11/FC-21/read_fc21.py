# Builds points-p1.csv for FC-21 (Claude's blind reading, batch curves-appc-b11).
# Markers: centers fitted with ring templates (fit_rings.py), entered here as read.
# Traces: the two edges of the hatched band, which on this page are drawn on the 45 and 40 grid
# lines; each sample is placed at a target Dr along the line (piecewise map of cal-p1) and its v is
# the centre of the line's ink measured on the page around that u (robust straight-line fit of the
# ink-run centres of columns u-20..u+20, crossing hatch vertices and grid-line blobs set aside).
import csv, importlib.util, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parent.parent
spec = importlib.util.spec_from_file_location("cal", WS / "tools" / "calibrate_axes.py")
cal = importlib.util.module_from_spec(spec); spec.loader.exec_module(cal)
IMG = WS / "packet" / "p0157.png"
g = np.asarray(Image.open(IMG).convert("L")) < 128
calj, X, Y = cal.piecewise_maps(HERE / "cal-p1", str(IMG))

FIG, PANEL = "FC-21", 1
rows = []
def add(series, kind, seq, u, v, bu, bv, sym, note):
    rows.append(dict(figure_id=FIG, panel=PANEL, series_id=series, point_kind=kind, sequence=seq,
                     pixel_u=round(u, 2), pixel_v=round(v, 2), u_bound_px=bu, v_bound_px=bv, symbol=sym, note=note))

# ---- markers (left to right) ----
markers = [
    (667.5, 2036.25, 2, 2, "pair 1 left; long joining line runs right to circle at u 1357.5 (pair 1 right); hatch lines touch its ring"),
    (1031.25, 1984.5, 2, 2, "pair 2 left; hatch lines touch its ring"),
    (1176.5, 1985.75, 2, 2, "pair 2 right; joining line hides the left side of its ring"),
    (1357.5, 2024.5, 3, 4, "pair 1 right; upper of two overlapping circles at Dr about 0.39 (the other is 11 px lower), also crossed by the Dr 0.4 grid line and hatch lines; center from a two-ring fit; bound widened"),
    (1359.0, 2035.5, 3, 4, "single; lower of two overlapping circles at Dr about 0.39, overlapping the pair 1 right circle, the Dr 0.4 grid line and hatch lines; no joining line of its own; center from a two-ring fit; bound widened"),
    (2338.5, 2204.25, 2, 2, "pair 3 left; hatch line merges with the top of its ring"),
    (2339.5, 2244.75, 2, 2, "single; directly below pair 3 left; hatch lines touch its ring"),
    (2423.5, 2198.75, 2, 2, "pair 3 right; joining line hides the left side of its ring; ring ends about 8 px inside the right frame, not cut"),
]
for i, (u, v, bu, bv, note) in enumerate(markers, 1):
    add("data", "marker", i, u, v, bu, bv, "circle", note)

# ---- band edges ----
def ink_center(u, c, s, half=20):
    """centre v of the near-horizontal line v ~ c + s*u at column u, from columns u-half..u+half"""
    pts = []
    for uu in range(int(round(u)) - half, int(round(u)) + half + 1):
        v0 = int(round(c + s * uu))
        col = g[v0 - 10:v0 + 11, uu]
        idx = np.where(col)[0]
        if len(idx) == 0:
            continue
        k = idx[np.argmin(abs(idx - 10))]
        a = b = k
        while a > 0 and col[a - 1]: a -= 1
        while b < len(col) - 1 and col[b + 1]: b += 1
        if a == 0 or b == len(col) - 1 or (b - a + 1) > 7 or (b - a + 1) < 3:
            continue          # crossing grid line, hatch vertex, frame: not the line alone
        pts.append((uu, v0 - 10 + (a + b) / 2, b - a + 1))
    P = np.array(pts)
    c1, c0 = np.polyfit(P[:, 0], P[:, 1], 1)
    res = P[:, 1] - (c0 + c1 * P[:, 0])
    keep = np.abs(res) <= 1.5
    c1, c0 = np.polyfit(P[keep, 0], P[keep, 1], 1)
    return float(c0 + c1 * u), int(keep.sum()), float(np.median(P[keep, 2]))

def u_at(target, c, s, lo=560, hi=2470):
    f = lambda u: X.value(u, c + s * u)[0] - target
    a, b = lo, hi
    for _ in range(60):
        m = (a + b) / 2
        if f(a) * f(m) <= 0: b = m
        else: a = m
    return (a + b) / 2

edges = [
    ("band-top", 1963.6, -0.0186, 595.0, 2443.0, "top edge of the hatched band, drawn on the 45 grid line (one line of grid thickness)"),
    ("band-bottom", 2346.2, -0.0176, 602.0, 2452.0, "bottom edge of the hatched band, drawn on the 40 grid line (one line of grid thickness)"),
]
targets = [round(-0.05 + 0.05 * k, 2) for k in range(23)]   # -0.05 .. 1.05
report = []
for sid, c, s, u_first, u_last, what in edges:
    seq = 0
    v, n, th = ink_center(u_first + 20, c, s)        # the ends: line centre extrapolated from just inside
    v = v + (u_first - (u_first + 20)) * s
    seq += 1
    add(sid, "trace", seq, u_first, v, 5, 3, "", f"left end: {what}; its ink meets the left frame here (frame inner edge), u bound covers the frame centre")
    first = (u_first, v)
    for t in targets:
        u = u_at(t, c, s)
        v, n, th = ink_center(u, c, s)
        seq += 1
        add(sid, "trace", seq, u, v, 3, 3, "", f"Dr {t:.2f} sample; ink centre from {n} columns, line {th:.0f} px thick")
        report.append((sid, t, round(u, 1), round(v, 2), n, th))
    v, n, th = ink_center(u_last - 20, c, s)
    v = v + 20 * s
    seq += 1
    add(sid, "trace", seq, u_last, v, 5, 3, "", f"right end: {what}; its ink meets the right frame here (frame inner edge), u bound covers the frame centre")
    last = (u_last, v)
    add(sid, "feature", 1, first[0], first[1], 5, 3, "", "first point (left end at the left frame); straight line, no knee; flat on the drawing, so no peak is read")
    add(sid, "feature", 2, last[0], last[1], 5, 3, "", "last point (right end at the right frame)")

cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with (HERE / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows")
for r in report:
    print(r)
print("knots x:", [(k['value'], round(k['err'], 2)) for k in X.knots], "rejected", [(k['value'], k['reason']) for k in X.rejected])
print("knots y:", [(k['value'], round(k['err'], 2)) for k in Y.knots], "rejected", [(k['value'], k['reason']) for k in Y.rejected])
