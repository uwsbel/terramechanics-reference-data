"""Shared pieces for the F2-47 reading helpers (second Claude reader, 2026-11-02).

Binary page (dark < 128), the calibrated grid lines of cal-p1 (each with its own tilt), and a
piecewise pixel-to-value map between adjacent drawn lines used only to choose sampling columns and
to print rough values while reading. The values written to points-p1-native.csv come from
tools/calibrate_axes.py piecewise, not from here.
Pixel coordinates are those of the unrotated page (u right, v down).
"""
import json
import numpy as np
from PIL import Image

ROOT = '<local path>/'
IMG = np.array(Image.open(ROOT + 'packet/p0108.png').convert('L')) < 128
CAL = json.load(open(ROOT + 'out/F2-47/cal-p1/calibration.json'))
VL = sorted(CAL['vertical_lines'], key=lambda L: L['x_value'])
HL = sorted(CAL['horizontal_lines'], key=lambda L: L['y_value'])


def vline_u(L, v):
    return L['u_at_v0'] + L['slope_du_dv'] * v


def hline_v(L, u):
    return L['v_at_u0'] + L['slope_dv_du'] * u


def x_of(u, v):
    us = [vline_u(L, v) for L in VL]
    for i in range(len(VL) - 1):
        if us[i] <= u <= us[i + 1] or (i == 0 and u < us[0]) or i == len(VL) - 2:
            return VL[i]['x_value'] + (u - us[i]) / (us[i + 1] - us[i]) * (VL[i + 1]['x_value'] - VL[i]['x_value'])


def y_of(u, v):
    vs = [hline_v(L, u) for L in HL]   # decreasing with value
    for i in range(len(HL) - 1):
        if vs[i + 1] <= v <= vs[i] or (i == 0 and v > vs[0]) or i == len(HL) - 2:
            return HL[i]['y_value'] + (v - vs[i]) / (vs[i + 1] - vs[i]) * (HL[i + 1]['y_value'] - HL[i]['y_value'])


def u_of(x, v):
    for i in range(len(VL) - 1):
        a, b = VL[i], VL[i + 1]
        if a['x_value'] <= x <= b['x_value']:
            ua, ub = vline_u(a, v), vline_u(b, v)
            return ua + (x - a['x_value']) / (b['x_value'] - a['x_value']) * (ub - ua)
    raise ValueError(x)


def runs_col(u, v0, v1):
    col = IMG[v0:v1, u]
    out, i = [], 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]:
                j += 1
            out.append((v0 + i, v0 + j - 1))
            i = j
        else:
            i += 1
    return out


def runs_row(v, u0, u1):
    row = IMG[v, u0:u1]
    out, i = [], 0
    while i < len(row):
        if row[i]:
            j = i
            while j < len(row) and row[j]:
                j += 1
            out.append((u0 + i, u0 + j - 1))
            i = j
        else:
            i += 1
    return out


def near_vgrid(u, v, tol=6):
    return any(abs(u - vline_u(L, v)) <= tol for L in VL)


def near_hgrid(u, v, tol=6):
    for L in HL:
        if abs(v - hline_v(L, u)) <= tol:
            return L['y_value']
    return None
