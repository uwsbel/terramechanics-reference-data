"""Helpers for the F2-48 reading (Figure 2-48, page image packet/p0109.png, printed sideways).

Pixel coordinates are those of the page as scanned (u right, v down, origin top-left).
Penetration (x, in) increases up the page; load (y, lb) increases to the left.
The grid lines come from out/F2-48/cal-p1/calibration.json (tools/calibrate_axes.py detect);
values between them are interpolated linearly between the two bracketing lines, each with its own
tilt, which is what the piecewise map of the protocol does. These helpers only choose where to
sample; the values written to the native file come from tools/calibrate_axes.py.
"""
import json
import numpy as np
from PIL import Image

IMG = "packet/p0109.png"
CAL = "out/F2-48/cal-p1/calibration.json"

g = np.array(Image.open(IMG).convert("L"))
B = g < 128                     # the scan is bilevel (0 or 255)
NV, NU = B.shape
cal = json.load(open(CAL))
HL = sorted(cal["horizontal_lines"], key=lambda L: L["x_value"])   # penetration lines, x = 0..8
VL = sorted(cal["vertical_lines"], key=lambda L: L["y_value"])     # load lines, y = 0..1200


def v_line(L, u):
    return L["v_at_u0"] + L["slope_dv_du"] * u


def u_line(L, v):
    return L["u_at_v0"] + L["slope_du_dv"] * v


# half widths of the grid bands to mask (measured: interior lines 5 to 6 px thick, frames 7 to 11)
def h_half(L):
    return 6.5 if L["x_value"] == 0 else 4.0


def v_half(L):
    return 4.5 if L["y_value"] in (0.0, 1200.0) else 3.5


def x_of(u, v):
    """penetration (in) at pixel (u, v), linear between the bracketing penetration lines"""
    vs = [v_line(L, u) for L in HL]
    xs = [L["x_value"] for L in HL]
    for k in range(len(HL) - 1):
        if vs[k] >= v >= vs[k + 1] or k == len(HL) - 2 or (k == 0 and v > vs[0]):
            return xs[k] + (vs[k] - v) / (vs[k] - vs[k + 1]) * (xs[k + 1] - xs[k])


def y_of(u, v):
    """load (lb) at pixel (u, v), linear between the bracketing load lines"""
    us = [u_line(L, v) for L in VL]
    ys = [L["y_value"] for L in VL]
    for k in range(len(VL) - 1):
        if us[k] >= u >= us[k + 1] or k == len(VL) - 2 or (k == 0 and u > us[0]):
            return ys[k] + (us[k] - u) / (us[k] - us[k + 1]) * (ys[k + 1] - ys[k])


def v_at_x(x, u):
    """row v of the constant-penetration line x at column u"""
    xs = [L["x_value"] for L in HL]
    k = min(max(int(np.searchsorted(xs, x, side="right")) - 1, 0), len(HL) - 2)
    a, b = HL[k], HL[k + 1]
    return v_line(a, u) + (x - xs[k]) / (xs[k + 1] - xs[k]) * (v_line(b, u) - v_line(a, u))


def grid_mask():
    vv, uu = np.mgrid[0:NV, 0:NU]
    m = np.zeros_like(B)
    for L in VL:
        m |= np.abs(uu - u_line(L, vv)) <= v_half(L)
    for L in HL:
        m |= np.abs(vv - v_line(L, uu)) <= h_half(L)
    return m


def near_h_grid(u, v, margin):
    """the penetration grid line within margin px of (u, v), or None"""
    for L in HL:
        if abs(v - v_line(L, u)) <= h_half(L) + margin:
            return L
    return None


def near_v_grid(u, v, margin):
    for L in VL:
        if abs(u - u_line(L, v)) <= v_half(L) + margin:
            return L
    return None


def runs_1d(arr):
    """(start, end) inclusive index pairs of True runs"""
    a = np.concatenate([[False], arr, [False]]).astype(np.int8)
    d = np.diff(a)
    s = np.nonzero(d == 1)[0]
    e = np.nonzero(d == -1)[0] - 1
    return list(zip(s, e))
