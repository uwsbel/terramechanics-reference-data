"""Assemble points-p1.csv of FB-7 (Claude's reading): markers located by template matching (find_symbols.py)
and checked by eye on zoomed crops (overlapped ones read from their edges), polylines measured on the
ink (trace_lines.py), features, labels.

Trace samples: left end, every vertex that lies on visible line ink, every 1 psi of confining pressure
between them, right end. A 1 psi position or a vertex hidden under a plotted symbol gets no trace
sample (rule 7); a vertex always gets a `feature` (the intersection of the two fitted segments), with a
note and a wider bound when it is hidden. A trace sample's position is the centre of the line's ink
measured across the line at that position; bound = half the line thickness measured there.

usage: python build_points.py <image> <trace_lines.json> <cal_dir> <out_csv>
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace_lines import SYMBOLS, EXCL, profile_center  # noqa: E402

FIG = "FB-7"
SERIES = {"upper": "dr99p5", "lower": "dr77"}

# Markers: (series, symbol, u, v, bu, bv, note)
MARKERS = [
    # Dr = 1.04, square with x (the legend key at (1806, 1314) next to "Dr = 1.04" is not a data point)
    ("dr104", "square with x", 499.5, 3087.5, 2, 3, "on the left frame (sigma3 = 0); its top half is overlapped by an open circle (dr99p5) centred 16 px above it; centre from the square's sides and bottom edge"),
    ("dr104", "square with x", 502.5, 3361.0, 2, 2, "on the left frame (sigma3 = 0); the y = 2 tick touches its lower right corner"),
    ("dr104", "square with x", 786.5, 2409.0, 2, 2, "the dr77 polyline's vertex lies at its bottom edge; the polyline passes through the square"),
    ("dr104", "square with x", 810.5, 2136.0, 2, 2, ""),
    ("dr104", "square with x", 1101.5, 1995.0, 2, 2, "the dr99p5 polyline crosses its upper left part"),
    ("dr104", "square with x", 1187.5, 2169.0, 2, 2, ""),
    ("dr104", "square with x", 1190.5, 1899.0, 2, 2, "the dr99p5 polyline passes through it, just before that polyline's second vertex"),
    ("dr104", "square with x", 1801.5, 1827.0, 2, 2, "the dr77 polyline passes through it"),
    ("dr104", "square with x", 2101.5, 1646.0, 2, 2, "right of the end of the dr99p5 polyline and below its label; same size and height as the data squares, not level with the label text, so read as a data point and not as a legend key"),
    # Dr = 0.995, open circle (the group whose polyline is labelled Dr = 0.995)
    ("dr99p5", "circle", 497.5, 3020.5, 2, 2, "on the left frame (sigma3 = 0); the dr99p5 polyline starts at its outline"),
    ("dr99p5", "circle", 497.5, 3071.0, 2, 4, "on the left frame (sigma3 = 0); its lower half is overlapped by a square (dr104); centre from its top edge, left side and the top of its inner hole"),
    ("dr99p5", "circle", 773.5, 2211.5, 2, 2, "the dr99p5 polyline's first vertex is inside it"),
    ("dr99p5", "circle", 1243.5, 1871.5, 2, 2, "the dr99p5 polyline's second vertex is inside it"),
    ("dr99p5", "circle", 1757.5, 1688.5, 2, 2, "on the dr99p5 polyline"),
    ("dr99p5", "circle", 1829.5, 1519.5, 2, 2, "above both polylines"),
    ("dr99p5", "circle", 1940.5, 1676.5, 2, 2, "between the two polylines, nearer the dr99p5 polyline"),
    # Dr = 0.77, filled circle (the group whose polyline is labelled Dr = 0.77)
    ("dr77", "filled circle", 501.0, 3482.5, 2, 3, "on the left frame (sigma3 = 0); two filled circles overlap here (one blob 62 px tall, 39 px wide, waist at v 3490); this one from the blob's top edge; a third hidden between them cannot be excluded"),
    ("dr77", "filled circle", 501.0, 3502.5, 2, 3, "on the left frame (sigma3 = 0); the lower of the two overlapping filled circles, from the blob's bottom edge"),
    ("dr77", "filled circle", 503.5, 3848.5, 2, 2, "on the left frame (sigma3 = 0)"),
    ("dr77", "filled circle", 762.5, 2671.5, 2, 2, "just right of the dr77 polyline, not touching it"),
    ("dr77", "filled circle", 784.5, 2278.5, 2, 2, "between the two polylines, nearer the dr99p5 polyline"),
    ("dr77", "filled circle", 1170.5, 2317.5, 2, 2, "below both polylines"),
    ("dr77", "filled circle", 1237.5, 1827.5, 2, 2, "above the dr99p5 polyline, just above the open circle at its second vertex"),
    ("dr77", "filled circle", 1907.5, 1770.5, 2, 2, "just above the end of the dr77 polyline"),
    ("dr77", "filled circle", 1928.5, 1827.5, 2, 2, "just below the end of the dr77 polyline, touching it"),
]

LABELS = {  # centre of the printed text (ink bounding box)
    "dr104": (2029.0, 1326.0, "Dr = 1.04", "legend entry: the key symbol, a square with x, is at (1806, 1314) left of the text; no polyline carries this label"),
    "dr99p5": (2299.0, 1588.5, "Dr = 0.995", "printed just right of the end of the upper polyline; no key symbol"),
    "dr77": (2173.0, 1773.5, "Dr = 0.77", "printed just right of the end of the lower polyline; no key symbol"),
}

LEFT_FRAME = (486.40, 0.00561)   # u = a + b v, from cal_ticks.py


def near_symbol(p, pad=0.0):
    for kind, u, v in SYMBOLS:
        r = EXCL["square" if "square" in kind else "circle"]
        if np.hypot(p[0] - u, p[1] - v) < r + pad:
            return (kind, u, v)
    return None


def seg_point(seg, T):
    th, n, c = np.array(seg["t_hat"]), np.array(seg["n"]), seg["c"]
    return T * th + (c[0] * T + c[1]) * n


def seg_T(seg, p):
    return float(np.array(p) @ np.array(seg["t_hat"]))


def solve_x(X, seg, k, T0, T1):
    f = lambda T: X.value(*seg_point(seg, T))[0] - k
    a, b = T0, T1
    fa = f(a)
    if fa * f(b) > 0:
        return None
    for _ in range(60):
        m = 0.5 * (a + b)
        fm = f(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return 0.5 * (a + b)


def ink_at(g, seg, T):
    """Centre of the line's ink across the segment at T, and the line's thickness there."""
    p = seg_point(seg, T)
    r = profile_center(g, p, np.array(seg["n"]))
    if r is None:
        return None
    off, w = r
    return p + off * np.array(seg["n"]), w


def main():
    image, tl, cal_dir, out = sys.argv[1:5]
    g = np.asarray(Image.open(image).convert("L")) < 128
    cal, X, Y = ca.piecewise_maps(cal_dir, image)
    lines = json.loads(Path(tl).read_text(encoding="utf-8"))
    rows = []

    def add(series, kind, seq, u, v, bu, bv, symbol, note):
        rows.append({"figure_id": FIG, "panel": 1, "series_id": series, "point_kind": kind, "sequence": seq,
                     "pixel_u": round(float(u), 1), "pixel_v": round(float(v), 1),
                     "u_bound_px": round(float(bu), 1), "v_bound_px": round(float(bv), 1),
                     "symbol": symbol, "note": note})

    # markers, numbered per series from left to right
    for s in ("dr104", "dr99p5", "dr77"):
        ms = sorted([m for m in MARKERS if m[0] == s], key=lambda m: (round(X.value(m[2], m[3])[0], 2), -m[3]))
        for i, (_, sym, u, v, bu, bv, note) in enumerate(ms, 1):
            add(s, "marker", i, u, v, bu, bv, sym, note)

    report = []
    for name, data in lines.items():
        series = SERIES[name]
        segs, verts = data["segments"], data["vertices"]
        half_w = [0.5 * s["width_px"] for s in segs]
        trace, feats = [], []
        # left end
        s0 = segs[0]
        a, b = LEFT_FRAME
        def h(T):
            p = seg_point(s0, T)
            return p[0] - b * p[1] - a
        Ta, Tb = seg_T(s0, (480, 3800)), seg_T(s0, (600, 3300))
        if name == "upper":
            Ta, Tb = seg_T(s0, (470, 3120)), seg_T(s0, (560, 2850))
        for _ in range(60):
            Tm = 0.5 * (Ta + Tb)
            if h(Ta) * h(Tm) <= 0:
                Tb = Tm
            else:
                Ta = Tm
        at_frame = seg_point(s0, 0.5 * (Ta + Tb))
        if name == "upper":
            # The line's last 45 px run along the right side of the open circle at (497.5, 3020.5), merged with
            # its outline, and its right edge is seen receding into the left frame at v 3035 to 3046; its centre
            # line meets the frame's centre line at the top of the second open circle (497.5, 3071.0), whose
            # centre lies on the line's extension. First trace sample: the last position where the line's own
            # ink is clear of the outline (more than 28 px from the circle's centre: outer radius 20.5 px plus half the
            # line plus 3 px, and profile width at most 1.05 times the segment's median width).
            T = seg_T(s0, (497.5, 3020.5))
            while True:
                p = seg_point(s0, T)
                q = ink_at(g, s0, T)
                if np.hypot(p[0] - 497.5, p[1] - 3020.5) > 28 and q is not None and q[1] <= 1.05 * s0["width_px"]:
                    break
                T += 0.25
            trace.append((q[0], 0.5 * q[1], 0.5 * q[1], "left end of the line's clear ink: below this the line runs on the outline of the open circle at sigma3 = 0 and into the frame (see the first-point feature)"))
            feats.append((at_frame, 4.0, 6.0, "first point: where the line's centre line meets the left frame's centre line (sigma3 = 0), at the top of the lower open circle at sigma3 = 0; the last 45 px of the line are merged with the upper open circle's outline and the frame, so this point is on merged ink, not a trace sample"))
        else:
            note = "left end: the line merges into the left frame; taken where its centre line meets the frame's centre line (sigma3 = 0); its own ink is clear down to v 3652 and its right edge reaches the frame's edge at v 3702"
            trace.append((at_frame, half_w[0], 6.0, note))
            feats.append((at_frame, max(half_w[0], 2.0), 6.0, "first point; " + note))
        left = (trace[0][0],)
        # walk the segments
        xl = X.value(*left[0])[0]
        for i, seg in enumerate(segs):
            Ta = seg_T(seg, left[0]) if i == 0 else seg_T(seg, verts[i - 1])
            if i < len(segs) - 1:
                Tb = seg_T(seg, verts[i])
            else:
                # right end: walk along the centre line until the ink stops
                T = seg_T(seg, seg["b"]) - 30
                while True:
                    p = seg_point(seg, T + 0.5)
                    if not g[int(round(p[1])), int(round(p[0]))]:
                        # confirm white for 3 px
                        if all(not g[int(round(seg_point(seg, T + d)[1])), int(round(seg_point(seg, T + d)[0]))] for d in (1, 2, 3)):
                            break
                    T += 0.5
                Tb = T
            x0 = X.value(*seg_point(seg, Ta))[0]
            x1 = X.value(*seg_point(seg, Tb))[0]
            for k in range(int(np.floor(x0)) + 1, int(np.ceil(x1))):
                if not (x0 < k < x1):
                    continue
                T = solve_x(X, seg, k, Ta, Tb)
                p = seg_point(seg, T)
                hit = near_symbol(p)
                if hit:
                    report.append(f"{series}: no trace sample at sigma3 = {k} psi, hidden by the {hit[0]} at ({hit[1]}, {hit[2]})")
                    continue
                if i > 0 and np.hypot(*(p - np.array(verts[i - 1]))) < 3 and not near_symbol(np.array(verts[i - 1])):
                    report.append(f"{series}: sigma3 = {k} psi is within 3 px of the vertex sample, not repeated")
                    continue
                q = ink_at(g, seg, T)
                if q is None or q[1] > 11.5:
                    report.append(f"{series}: no clean ink at sigma3 = {k} psi (width {None if q is None else round(q[1], 1)})")
                    continue
                trace.append((q[0], 0.5 * q[1], 0.5 * q[1], f"sigma3 = {k} psi"))
            if i < len(segs) - 1:
                vx = np.array(verts[i])
                hit = near_symbol(vx)
                if hit:
                    feats.append((vx, 4.0, 4.0, f"vertex: intersection of the two fitted segments, hidden by the {hit[0]} at ({hit[1]}, {hit[2]}); no trace sample here"))
                    report.append(f"{series}: vertex {i + 1} at ({vx[0]:.1f}, {vx[1]:.1f}) hidden by the {hit[0]} at ({hit[1]}, {hit[2]})")
                else:
                    trace.append((vx, half_w[i], half_w[i], "vertex (on the ink)"))
                    feats.append((vx, max(half_w[i], 2.0), max(half_w[i], 2.0), "vertex: intersection of the two fitted segments, on the ink"))
            else:
                p = seg_point(seg, Tb)
                note = "right end: where the line's ink ends"
                trace.append((p, half_w[i], half_w[i], note))
                feats.append((p, max(half_w[i], 2.0), max(half_w[i], 2.0), "last point; " + note))
        for j, (p, bu, bv, note) in enumerate(trace, 1):
            add(series, "trace", j, p[0], p[1], bu, bv, "", note)
        for j, (p, bu, bv, note) in enumerate(feats, 1):
            add(series, "feature", j, p[0], p[1], bu, bv, "", note)
    # label features
    for s, (u, v, text, note) in LABELS.items():
        n = sum(1 for r in rows if r["series_id"] == s and r["point_kind"] == "feature")
        add(s, "feature", n + 1, u, v, 4, 4, "", f"label: {text}; {note}")

    cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in report:
        print(r)
    from collections import Counter
    print(Counter((r["series_id"], r["point_kind"]) for r in rows))


if __name__ == "__main__":
    main()
