"""Probe the page at target penetrations (F2-47 reading helper).

Usage: python out/F2-47/helpers/probe.py <calibration.json> <image> <x> <v_guess> [--win 30]

Finds the column u of penetration x at row v (interpolated between the two calibrated vertical
grid lines around x, each with its own tilt), lists the dark runs (threshold 128) of that column
within +-win px of v_guess, and for each run the load it would read (interpolated between the two
calibrated horizontal lines around it). The run the reader takes is decided by eye; this only
lists the candidates. Pixel coordinates are those of the unrotated page.
"""
import json, sys
import numpy as np
from PIL import Image

cal = json.load(open(sys.argv[1]))
img = np.array(Image.open(sys.argv[2]).convert('L')) < 128
x = float(sys.argv[3]); vg = float(sys.argv[4])
win = 30
if '--win' in sys.argv: win = int(sys.argv[sys.argv.index('--win') + 1])
vl = sorted(cal['vertical_lines'], key=lambda L: L['x_value'])
hl = sorted(cal['horizontal_lines'], key=lambda L: L['y_value'])

def u_of(x, v):
    for a, b in zip(vl[:-1], vl[1:]):
        if a['x_value'] <= x <= b['x_value']:
            ua = a['u_at_v0'] + a['slope_du_dv'] * v; ub = b['u_at_v0'] + b['slope_du_dv'] * v
            return ua + (x - a['x_value']) / (b['x_value'] - a['x_value']) * (ub - ua)
    raise ValueError(x)

def y_of(u, v):
    for a, b in zip(hl[:-1], hl[1:]):
        va = a['v_at_u0'] + a['slope_dv_du'] * u; vb = b['v_at_u0'] + b['slope_dv_du'] * u
        if vb <= v <= va or b is hl[-1] or a is hl[0] and v > va:
            return a['y_value'] + (v - va) / (vb - va) * (b['y_value'] - a['y_value'])
    return None

def x_of(u, v):
    for a, b in zip(vl[:-1], vl[1:]):
        ua = a['u_at_v0'] + a['slope_du_dv'] * v; ub = b['u_at_v0'] + b['slope_du_dv'] * v
        if ua <= u <= ub or (a is vl[0] and u < ua) or b is vl[-1]:
            return a['x_value'] + (u - ua) / (ub - ua) * (b['x_value'] - a['x_value'])

u = u_of(x, vg)
ui = int(round(u))
col = img[int(vg - win):int(vg + win) + 1, ui]
print(f"x={x}  u={u:.1f} -> column {ui}  (x at column: {x_of(ui, vg):.4f})")
i = 0
while i < len(col):
    if col[i]:
        j = i
        while j < len(col) and col[j]: j += 1
        t = int(vg - win) + i; b = int(vg - win) + j - 1
        c = (t + b) / 2
        print(f"   v {t}..{b}  center {c:.1f}  len {b - t + 1}  load {y_of(ui, c):.1f}  x {x_of(ui, c):.4f}")
        i = j
    else:
        i += 1
