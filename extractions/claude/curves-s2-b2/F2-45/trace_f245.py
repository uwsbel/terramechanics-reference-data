"""Blind reading of Figure 2-45 (page p0106.png, printed sideways): trace extraction helper.

Run from the workspace root:  python out/F2-45/trace_f245.py
Pixel coordinates are those of the unrotated page (u right, v down). Penetration (x) increases up the
page (v decreasing), load (y) increases to the left (u decreasing).

1. Solid trace (lpt95): tracked row by row (constant v) from the origin corner upward, following ink
   runs that connect to the previous row's run. Rows inside a horizontal grid line band, and runs that
   touch a vertical grid line band, are not used for the center; the center there is interpolated from
   the clean rows on either side. Writes out/F2-45/work/solid-rows.csv.
2. Dotted trace (lpt79): dots found as cores that survive an erosion with a disk of radius 3 px (grid
   lines are 4 to 6 px thick and the text strokes about 5 px, so they vanish; the dots are 10 to 13 px
   across), the frame and the solid trace masked; the dot center is the centroid of the original ink of
   the dot (the ink within 7 px of the core, grid band pixels left out). Dots are chained in drawing
   order from the origin end. Writes out/F2-45/work/dots.csv.
"""
import csv
import json
import os
import numpy as np
from PIL import Image

IMG = 'packet/p0106.png'
CAL = 'out/F2-45/cal-p1/calibration.json'
WORK = 'out/F2-45/work'
os.makedirs(WORK, exist_ok=True)

img = np.array(Image.open(IMG).convert('L'))
INK = img < 128
H, W = INK.shape
cal = json.load(open(CAL))
VL = sorted(cal['vertical_lines'], key=lambda L: L['y_value'])     # load lines u = u0 + k v
HL = sorted(cal['horizontal_lines'], key=lambda L: L['x_value'])   # penetration lines v = v0 + k u

GRID_HALF = 4       # grid lines are 4 to 6 px thick around the fitted center


def vline_u(L, v):
    return L['u_at_v0'] + L['slope_du_dv'] * v


def hline_v(L, u):
    return L['v_at_u0'] + L['slope_dv_du'] * u


def x_of(u, v):
    """Penetration, piecewise linear between the two horizontal lines around (u, v) (used to choose
    the sampling rows only; the values of the data come from calibrate_axes.py piecewise)."""
    vs = [hline_v(L, u) for L in HL]          # decreasing with x
    xs = [L['x_value'] for L in HL]
    for i in range(len(HL) - 1):
        if vs[i + 1] <= v <= vs[i] or (i == 0 and v > vs[0]) or (i == len(HL) - 2 and v < vs[-1]):
            return xs[i] + (xs[i + 1] - xs[i]) * (vs[i] - v) / (vs[i] - vs[i + 1])
    return float('nan')


def y_of(u, v):
    us = [vline_u(L, v) for L in VL]          # decreasing with y
    ys = [L['y_value'] for L in VL]
    for i in range(len(VL) - 1):
        if us[i + 1] <= u <= us[i] or (i == 0 and u > us[0]) or (i == len(VL) - 2 and u < us[-1]):
            return ys[i] + (ys[i + 1] - ys[i]) * (us[i] - u) / (us[i] - us[i + 1])
    return float('nan')


def in_hgrid(v, u, half=GRID_HALF):
    for L in HL[1:-1]:                         # interior lines; the frame is handled separately
        if abs(v - hline_v(L, u)) <= half:
            return True
    return False


def touches_vgrid(u0, u1, v, half=GRID_HALF):
    for L in VL[1:-1]:
        gu = vline_u(L, v)
        if u0 - half <= gu <= u1 + half:
            return True
    return False


def frame_u(v):
    """Inner edges of the left (300) and right (0) frame lines at row v (frame lines about 10 px)."""
    return vline_u(VL[-1], v) + 7, vline_u(VL[0], v) - 7


def frame_v(u):
    return hline_v(HL[-1], u) + 8, hline_v(HL[0], u) - 8     # top inner edge, bottom inner edge


def runs(row_bool, off):
    d = np.diff(np.concatenate([[0], row_bool.astype(int), [0]]))
    s = np.where(d == 1)[0]
    e = np.where(d == -1)[0] - 1
    return [(int(a) + off, int(b) + off) for a, b in zip(s, e)]


# ---------------------------------------------------------------- solid trace
def grid_only(r, v):
    """A run that is only a vertical grid line (narrow and centered on a fitted load line)."""
    c, w = (r[0] + r[1]) / 2, r[1] - r[0] + 1
    return w <= 9 and any(abs(c - vline_u(L, v)) <= GRID_HALF + 1 for L in VL[1:-1])


def track(v_start, u_start, step, v_stop):
    """Follow the solid line row by row from (u_start, v_start), step -1 (up, penetration increasing)
    or +1 (down). A run is a candidate when it touches the previous chosen run (8-connected, tolerance
    widened across skipped grid rows); a run that is only a vertical grid line is dropped when another
    candidate exists; among several the one nearest the prediction (straight fit to the last 20 clean
    centers) is kept. Stops at v_stop or when no candidate is left."""
    rows, prev, prev_v, centers = [], None, None, []
    v = v_start
    while (v >= v_stop) if step < 0 else (v <= v_stop):
        fu0, fu1 = frame_u(v)
        uref = (prev[0] + prev[1]) / 2 if prev else u_start
        if in_hgrid(v, uref):
            rows.append(dict(v=v, s='', e='', c='', clean=0, note='hgrid'))
            v += step
            continue
        rr = runs(INK[v, int(fu0):int(fu1) + 1], int(fu0))
        if len(centers) >= 6:
            vs = np.array([c[0] for c in centers[-20:]], float)
            us = np.array([c[1] for c in centers[-20:]], float)
            m, k = np.polyfit(vs, us, 1)
            pred = m * v + k
        else:
            pred = uref
        if prev is None:
            cand = [r for r in rr if r[0] - 2 <= u_start <= r[1] + 2]
        else:
            tol = 1 + 2 * (abs(v - prev_v) - 1)
            cand = [r for r in rr if r[1] >= prev[0] - tol and r[0] <= prev[1] + tol]
        if len(cand) > 1:
            ng = [r for r in cand if not grid_only(r, v)]
            cand = ng or cand
        if len(cand) > 1:
            cand = [min(cand, key=lambda r: abs((r[0] + r[1]) / 2 - pred))]
        if not cand:
            rows.append(dict(v=v, s='', e='', c='', clean=0, note='lost'))
            break
        s, e = cand[0]
        tv = touches_vgrid(s, e, v)
        clean = (not tv) and (e - s + 1) <= 60
        note = '' if clean else ('vgrid' if tv else 'wide')
        rows.append(dict(v=v, s=s, e=e, c=(s + e) / 2, clean=int(clean), note=note))
        if clean:
            centers.append((v, (s + e) / 2))
        prev, prev_v = (s, e), v
        v += step
    return rows


# ---------------------------------------------------------------- dotted trace
def erode_disk(mask, r):
    out = mask.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                out &= np.roll(np.roll(mask, dy, axis=0), dx, axis=1)
    return out


def label(mask):
    """8-connected components; returns list of arrays of (v, u)."""
    lab = np.zeros(mask.shape, int)
    comps = []
    vs, us = np.nonzero(mask)
    for v0, u0 in zip(vs, us):
        if lab[v0, u0]:
            continue
        n = len(comps) + 1
        stack = [(v0, u0)]
        lab[v0, u0] = n
        pix = []
        while stack:
            v, u = stack.pop()
            pix.append((v, u))
            for dv in (-1, 0, 1):
                for du in (-1, 0, 1):
                    a, b = v + dv, u + du
                    if 0 <= a < mask.shape[0] and 0 <= b < mask.shape[1] and mask[a, b] and not lab[a, b]:
                        lab[a, b] = n
                        stack.append((a, b))
        comps.append(np.array(pix))
    return comps


if __name__ == '__main__':
    # solid trace: start on the clean stretch above the origin (seen on the origin crop at zoom 4:
    # at v = 3500 the solid line is the run at u about 2110, the dots are at u about 2195); track
    # upward to the top frame and downward to the bottom frame, then join in drawing order.
    up = track(3500, 2112, -1, 1462)
    down = track(3501, 2112, +1, 3588)
    solid = list(reversed(down)) + up
    with open(f'{WORK}/solid-rows.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['v', 's', 'e', 'c', 'clean', 'note'])
        w.writeheader()
        w.writerows(solid)
    print('solid rows', len(solid), 'first', solid[0], 'last', solid[-1])
    print('notes:', {k: sum(1 for r in solid if r['note'] == k) for k in set(r['note'] for r in solid)})

    # dotted trace
    v0, v1, u0, u1 = 1470, 3592, 392, 2272
    sub = INK[v0:v1, u0:u1].copy()
    core = erode_disk(sub, 3)
    # mask the frame and the solid trace (its run in each row, widened by 3 px)
    for r in solid:
        if r['s'] != '':
            a, b = int(r['s']) - 3 - u0, int(r['e']) + 3 - u0
            vv = int(r['v']) - v0
            if 0 <= vv < core.shape[0]:
                core[vv, max(a, 0):max(b + 1, 0)] = False
    comps = label(core)
    rows = []
    for cpx in comps:
        n = len(cpx)
        cv, cu = cpx[:, 0].mean() + v0, cpx[:, 1].mean() + u0
        rows.append(dict(n_core=n, cu=round(cu, 2), cv=round(cv, 2),
                         umin=int(cpx[:, 1].min() + u0), umax=int(cpx[:, 1].max() + u0),
                         vmin=int(cpx[:, 0].min() + v0), vmax=int(cpx[:, 0].max() + v0)))
    with open(f'{WORK}/cores.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print('cores', len(rows))
