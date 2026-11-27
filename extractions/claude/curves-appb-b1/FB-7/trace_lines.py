"""Measure the centre of the drawn polylines of FB-7 on the ink, segment by segment.

For each segment (rough end points given by the reader from the crops) the ink is profiled across the
segment every 2 px along it; the dark run nearest the predicted centre gives the line's centre and its
thickness across. Profiles within EXCL px of a plotted symbol's centre are not used (a sample there would
be on the symbol's outline), and neither are runs thicker than MAXW (another line or a symbol). Each
segment is fitted with a straight line on its own ink (outliers above 1.5 px set aside); vertices are the
intersections of consecutive fitted segments.

usage: python trace_lines.py <image>  (prints a JSON summary used by build_points.py)
"""
import json
import sys

import numpy as np
from PIL import Image

EXCL = {"circle": 25.0, "square": 29.0}
MAXW = 11.5

SYMBOLS = [  # centres from find_symbols.py, checked by eye (build_points.py holds the final reading)
    ("square", 2101.5, 1646.0), ("circle", 1829.5, 1519.5), ("circle", 1940.5, 1676.5), ("circle", 1757.5, 1688.5),
    ("circle", 1907.5, 1770.5), ("square", 1801.5, 1827.0), ("circle", 1237.5, 1827.5), ("circle", 1928.5, 1827.5),
    ("circle", 1243.5, 1871.5), ("square", 1190.5, 1899.0), ("square", 1101.5, 1995.0), ("square", 810.5, 2136.0),
    ("square", 1187.5, 2169.0), ("circle", 773.5, 2211.5), ("circle", 784.5, 2278.5), ("circle", 1170.5, 2317.5),
    ("square", 786.5, 2409.0), ("circle", 762.5, 2671.5), ("circle", 497.5, 3020.5), ("circle", 497.5, 3071.0),
    ("square", 499.5, 3087.5), ("square", 502.5, 3361.0), ("circle", 501.5, 3482.5), ("circle", 501.5, 3502.5),
    ("circle", 503.5, 3848.5),
]

POLYLINES = {   # rough vertices (pixels), left to right, read from the crops
    "upper": [(518.0, 3000.0), (770.5, 2217.2), (1247.8, 1870.3), (2030.0, 1585.0)],
    "lower": [(507.0, 3695.0), (784.8, 2429.0), (1201.5, 2101.5), (1982.0, 1773.0)],
}


def profile_center(g, p, n, half=14.0, step=0.25):
    """Dark runs along the normal n through p; returns (centre offset, width) of the run nearest 0."""
    s = np.arange(-half, half + 1e-9, step)
    U = np.rint(p[0] + s * n[0]).astype(int)
    V = np.rint(p[1] + s * n[1]).astype(int)
    d = g[V, U]
    runs, i = [], 0
    while i < len(s):
        if d[i]:
            j = i
            while j + 1 < len(s) and d[j + 1]:
                j += 1
            runs.append((s[i], s[j], i == 0 or j == len(s) - 1))
            i = j + 1
        else:
            i += 1
    if not runs:
        return None
    a, b, clipped = min(runs, key=lambda r: 0 if r[0] <= 0 <= r[1] else min(abs(r[0]), abs(r[1])))
    if clipped or min(abs(a), abs(b)) > 6 and not (a <= 0 <= b):
        return None
    return (a + b) / 2, b - a + step


def near_symbol(p):
    for kind, u, v in SYMBOLS:
        if np.hypot(p[0] - u, p[1] - v) < EXCL[kind]:
            return True
    return False


def measure_segment(g, a, b):
    a, b = np.array(a), np.array(b)
    d = b - a
    L = np.hypot(*d)
    t_hat = d / L
    n = np.array([-t_hat[1], t_hat[0]])
    out = []
    for t in np.arange(0, L + 1e-9, 2.0):
        p = a + t * t_hat
        if near_symbol(p):
            continue
        r = profile_center(g, p, n)
        if r is None:
            continue
        off, w = r
        if w > MAXW:
            continue
        q = p + off * n
        if near_symbol(q):
            continue
        out.append((float(q[0]), float(q[1]), float(w), float(t)))
    return out, t_hat, n


def fit_line(pts, t_hat, n, trim=12.0, L=None):
    """Fit s = c0 + c1 t (s across, t along) to points, leaving out trim px at both ends."""
    P = np.array([[x, y] for x, y, _, _ in pts])
    T = np.array([tt for *_, tt in pts])
    keep = (T >= trim) & (T <= (L - trim if L else T.max()))
    S = P @ n
    TT = P @ t_hat
    c = np.polyfit(TT[keep], S[keep], 1)
    res = S[keep] - np.polyval(c, TT[keep])
    k2 = np.abs(res) <= 1.5
    c = np.polyfit(TT[keep][k2], S[keep][k2], 1)
    res2 = S[keep][k2] - np.polyval(c, TT[keep][k2])
    return c, float(np.sqrt(np.mean(res2 ** 2))), int(k2.sum()), int(keep.sum())


def line_points(c, t_hat, n, t):
    return np.outer(t, t_hat) + np.outer(np.polyval(c, t), n)


def main():
    g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
    summary = {}
    for name, verts in POLYLINES.items():
        segs = []
        for a, b in zip(verts, verts[1:]):
            pts, t_hat, n = measure_segment(g, a, b)
            L = float(np.hypot(b[0] - a[0], b[1] - a[1]))
            c, rms, nk, nn = fit_line(pts, t_hat, n, L=L)
            w = float(np.median([p[2] for p in pts]))
            # thickness across the line: the run is measured along n, which is perpendicular to the rough segment
            segs.append({"a": a, "b": b, "t_hat": t_hat.tolist(), "n": n.tolist(), "c": [float(x) for x in c],
                         "rms": rms, "n_fit": nk, "n_meas": len(pts), "width_px": w, "ink": pts})
            print(f"{name} seg {a}->{b}: {len(pts)} ink samples, fit rms {rms:.2f} px on {nk}/{nn}, median width {w:.1f} px",
                  file=sys.stderr)
        # vertices: intersections of consecutive fitted lines
        vx = []
        for s1, s2 in zip(segs, segs[1:]):
            # line i: points with p.n = c0 + c1 (p.t)  ->  (n - c1 t).p = c0
            A, rhs = [], []
            for s in (s1, s2):
                t_hat, n, c = np.array(s["t_hat"]), np.array(s["n"]), s["c"]
                A.append(n - c[0] * t_hat)
                rhs.append(c[1])
            p = np.linalg.solve(np.array(A), np.array(rhs))
            vx.append(p.tolist())
            print(f"{name} vertex at u {p[0]:.1f} v {p[1]:.1f}", file=sys.stderr)
        summary[name] = {"segments": segs, "vertices": vx}
    json.dump(summary, sys.stdout, indent=0)


if __name__ == "__main__":
    main()
