"""Shared helpers for the second (resumed) reading of Figure 2-45 (page p0106.png, printed sideways).

Pixel coordinates are those of the unrotated page as scanned (u right, v down). Penetration x increases
up the page (v decreasing); load y increases to the left (u decreasing). Run from the workspace root.
"""
import json
import numpy as np
from PIL import Image

IMG = 'packet/p0106.png'
CAL = 'out/F2-45/cal-p1/calibration.json'

INK = np.array(Image.open(IMG).convert('L')) < 128
cal = json.load(open(CAL))
VL = sorted(cal['vertical_lines'], key=lambda L: L['y_value'])      # constant load: u = u0 + k v
HL = sorted(cal['horizontal_lines'], key=lambda L: L['x_value'])    # constant penetration: v = v0 + k u


def vline_u(L, v):
    return L['u_at_v0'] + L['slope_du_dv'] * v


def hline_v(L, u):
    return L['v_at_u0'] + L['slope_dv_du'] * u


def x_of(u, v):
    """Penetration, linear between the two constant-penetration lines around (u, v). Used only to
    choose sampling locations; the values of the data come from tools/calibrate_axes.py."""
    vs = [hline_v(L, u) for L in HL]
    xs = [L['x_value'] for L in HL]
    n = len(HL)
    for i in range(n - 1):
        lo, hi = vs[i], vs[i + 1]            # lo is the larger v (smaller x)
        if hi <= v <= lo or (i == 0 and v > lo) or (i == n - 2 and v < hi):
            return xs[i] + (xs[i + 1] - xs[i]) * (lo - v) / (lo - hi)
    return float('nan')


def y_of(u, v):
    us = [vline_u(L, v) for L in VL]
    ys = [L['y_value'] for L in VL]
    n = len(VL)
    for i in range(n - 1):
        lo, hi = us[i], us[i + 1]
        if hi <= u <= lo or (i == 0 and u > lo) or (i == n - 2 and u < hi):
            return ys[i] + (ys[i + 1] - ys[i]) * (lo - u) / (lo - hi)
    return float('nan')


def v_at_x(x, u):
    """Row v of the constant-penetration line x at column u (piecewise between the drawn lines)."""
    xs = [L['x_value'] for L in HL]
    i = int(np.clip(np.searchsorted(xs, x) - 1, 0, len(HL) - 2))
    a, b = HL[i], HL[i + 1]
    f = (x - a['x_value']) / (b['x_value'] - a['x_value'])
    return hline_v(a, u) + f * (hline_v(b, u) - hline_v(a, u))


def near_vgrid(u, v, half):
    """Interior constant-load lines (25 to 275) within half px of (u, v)."""
    return any(abs(u - vline_u(L, v)) <= half for L in VL[1:-1])


def near_hgrid(u, v, half):
    return any(abs(v - hline_v(L, u)) <= half for L in HL[1:-1])


def runs(row_bool, off):
    d = np.diff(np.concatenate([[0], row_bool.astype(int), [0]]))
    s = np.where(d == 1)[0]
    e = np.where(d == -1)[0] - 1
    return [(int(a) + off, int(b) + off) for a, b in zip(s, e)]


def label(mask):
    """8-connected components of a boolean mask; list of (N, 2) arrays of (row, col)."""
    lab = np.zeros(mask.shape, np.int32)
    comps = []
    for a0, b0 in zip(*np.nonzero(mask)):
        if lab[a0, b0]:
            continue
        n = len(comps) + 1
        st = [(a0, b0)]
        lab[a0, b0] = n
        pix = []
        while st:
            a, b = st.pop()
            pix.append((a, b))
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    x, y = a + da, b + db
                    if 0 <= x < mask.shape[0] and 0 <= y < mask.shape[1] and mask[x, y] and not lab[x, y]:
                        lab[x, y] = n
                        st.append((x, y))
        comps.append(np.array(pix))
    return comps


def erode_disk(mask, r):
    out = mask.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                out &= np.roll(np.roll(mask, dy, axis=0), dx, axis=1)
    return out
