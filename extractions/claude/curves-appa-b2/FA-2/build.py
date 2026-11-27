"""Samples of the FA-2 traces from the tracked stroke centres (track.py) where the three curves are
apart, by crossing each stroke's centre polyline with the sampling lines (grain size 10^(0.05 k), and
percent finer every 5 percent where a curve rises by more than 10 percent between two k samples).

A crossing between two centre points more than GAP px apart lies in a gap of the stroke: on a dashed
curve the sample moves to the nearer dash end (rule 7); on the solid average curve such gaps are where
the stroke crosses a grid line or touches another curve, and the crossing is interpolated and then
checked to lie on ink. Every sample is reviewed on overlays before it is written.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fa2_tools as T  # noqa: E402

GAP = 4.5
GOOD = ("clean", "edge-low", "edge-high")
DASH_END = ("clean", "edge-low", "edge-high", "partial")


SMOOTH = 7   # half window (px along the scan) of the local straight-line fit that removes pixel steps


def smooth(rows):
    """local linear fit of the centre over +-SMOOTH scan lines of the same stroke piece (no gap inside)."""
    good = [(t, c, f) for t, c, f, r in rows if c is not None and f in DASH_END]
    out = []
    for t, c, f in good:
        nb = [(tt, cc) for tt, cc, ff in good if abs(tt - t) <= SMOOTH]
        # stay within one continuous piece: drop neighbours beyond a missing scan line
        ts = sorted(tt for tt, _ in nb)
        lo = hi = t
        while lo - 1 in ts:
            lo -= 1
        while hi + 1 in ts:
            hi += 1
        nb = [(tt, cc) for tt, cc in nb if lo <= tt <= hi]
        if len(nb) >= 5:
            A = np.array(nb)
            k1, k0 = np.polyfit(A[:, 0], A[:, 1], 1)
            out.append((t, float(k0 + k1 * t), f))
        else:
            out.append((t, c, f))
    return out


def load(paths):
    pts = {"lower": [], "average": [], "upper": []}
    for p in paths:
        trk = json.loads(Path(p).read_text(encoding="utf-8"))
        for name, rows in trk.items():
            base = name.split(":")[0]
            row = name.endswith(":row")
            for t, c, flag in smooth(rows):
                u, v = (c, t) if row else (t, c)
                pts[base].append((u, v, flag))
    for k in pts:
        # one point per position; order along the curve (u and v both grow from the coarse end)
        pts[k] = sorted(set(pts[k]), key=lambda p: p[0] + p[1])
    return pts


def chain(points):
    """keep partial points only where they continue a run of good points (a dash end), not stray."""
    out = []
    for i, p in enumerate(points):
        if p[2] in GOOD:
            out.append(p)
            continue
        nb = [q for q in points[max(0, i - 3):i + 4] if q is not p and q[2] in GOOD and math.dist(p[:2], q[:2]) <= 3]
        if nb:
            out.append(p)
    return out


def g_of(u, v):
    return math.log10(T.X.value(u, v)[0])


def p_of(u, v):
    return T.Y.value(u, v)[0]


def crossings(points, fn, target):
    """crossings of the polyline with the level set fn(u, v) = target: (u, v, kind, i)"""
    out = []
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        fa, fb = fn(a[0], a[1]) - target, fn(b[0], b[1]) - target
        if fa == 0:
            out.append((a[0], a[1], "on-point", i))
            continue
        if fa * fb < 0:
            d = math.dist(a[:2], b[:2])
            w = fa / (fa - fb)
            u, v = a[0] + w * (b[0] - a[0]), a[1] + w * (b[1] - a[1])
            if d <= GAP:
                kind = "interp"
            else:   # ink all along the straight piece between the two centres: a grid crossing, not a dash gap
                n = int(d) + 1
                dark = [T.GRAY[int(round(a[1] + (b[1] - a[1]) * j / n)), int(round(a[0] + (b[0] - a[0]) * j / n))] < 128
                        for j in range(n + 1)]
                kind = f"bridge{d:.0f}" if np.mean(dark) >= 0.9 else f"gap{d:.0f}"
            out.append((u, v, kind, i))
    return out


if __name__ == "__main__":
    pts = load(sys.argv[1:])
    for name in ("lower", "average", "upper"):
        P = chain(pts[name])
        print(f"== {name}: {len(P)} centre points")
        for k in range(14, -25, -1):
            for u, v, kind, i in crossings(P, g_of, 0.05 * k):
                print(f"  k={k:>3} g={10 ** (0.05 * k):.4f}  u {u:7.1f} v {v:7.1f}  {kind}  pct {p_of(u, v):6.2f}")
