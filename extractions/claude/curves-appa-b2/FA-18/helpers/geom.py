"""Claude reader helper (FA-18): iso-lines of grain size and percent from the measured grid lines of
cal-p1 (interpolated between the two bracketing lines, in log10 for grain size), used only to choose
sampling locations on the page. The values written to the points files come from the tool
(calibrate_axes.py piecewise), never from this module."""
import json, math
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve()
WS = HERE.parents[3]
cal = json.loads((WS / "out/FA-18/cal-p1/calibration.json").read_text(encoding="utf-8"))
H = sorted((math.log10(l["x_value"]), l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"])  # v = c + k u
V = sorted((l["y_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"])                 # u = c + k v
gray = np.asarray(Image.open(WS / "packet/p0039.png").convert("L"), dtype=float)


def _interp(lines, q):
    for (qa, ca, ka), (qb, cb, kb) in zip(lines, lines[1:]):
        if qa <= q <= qb:
            f = (q - qa) / (qb - qa)
            return ca + f * (cb - ca), ka + f * (kb - ka)
    (qa, ca, ka), (qb, cb, kb) = (lines[0], lines[1]) if q < lines[0][0] else (lines[-2], lines[-1])
    f = (q - qa) / (qb - qa)
    return ca + f * (cb - ca), ka + f * (kb - ka)


def iso_g(g):
    """(c, k): the line of grain size g (mm): v = c + k u."""
    return _interp(H, math.log10(g))


def iso_p(p):
    """(c, k): the line of percent p: u = c + k v."""
    return _interp(V, p)


def value(u, v):
    """approximate (grain size mm, percent) at a pixel, by bisection on the iso-lines"""
    lo, hi = -2.0, 1.2
    for _ in range(60):
        m = 0.5 * (lo + hi)
        c, k = iso_g(10 ** m)
        if c + k * u > v:   # the line of m lies below the point: the point is coarser
            lo = m
        else:
            hi = m
    g = 10 ** (0.5 * (lo + hi))
    lo, hi = -5.0, 105.0
    for _ in range(60):
        m = 0.5 * (lo + hi)
        c, k = iso_p(m)
        if c + k * v > u:   # the line of m lies right of the point: the point has a higher percent
            lo = m
        else:
            hi = m
    return g, 0.5 * (lo + hi)


def on_iso_g(g, u):
    c, k = iso_g(g)
    return c + k * u


def on_iso_p(p, v):
    c, k = iso_p(p)
    return c + k * v
