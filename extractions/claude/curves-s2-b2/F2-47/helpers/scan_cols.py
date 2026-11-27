"""List dark runs down a column of the page at each requested penetration value.

Usage: python out/F2-47/helpers/scan_cols.py <calibration.json> <image> x1,x2,... [--v0 V0 --v1 V1]
The column u of a penetration value x is interpolated between the two calibrated vertical grid
lines around it (each with its own tilt), at the row v of the run, so the sample sits on the
drawn grid as printed. Horizontal grid lines are reported with a tag so they are not mistaken
for a trace; a run that is much thicker than a grid line where a grid line is expected is a
trace crossing the line (tagged 'on-grid').
"""
import json, sys
import numpy as np
from PIL import Image

cal = json.load(open(sys.argv[1]))
img = np.array(Image.open(sys.argv[2]).convert('L'))
xs = [float(s) for s in sys.argv[3].split(',')]
v0, v1 = 1685, 3240
args = sys.argv[4:]
if '--v0' in args: v0 = int(args[args.index('--v0')+1])
if '--v1' in args: v1 = int(args[args.index('--v1')+1])
halfw = 1
if '--halfwidth' in args: halfw = int(args[args.index('--halfwidth')+1])
dark = 128

vl = sorted(cal['vertical_lines'], key=lambda L: L['x_value'])
hl = sorted(cal['horizontal_lines'], key=lambda L: L['y_value'])

def u_of(x, v):
    for a, b in zip(vl[:-1], vl[1:]):
        if a['x_value'] <= x <= b['x_value']:
            ua = a['u_at_v0'] + a['slope_du_dv']*v
            ub = b['u_at_v0'] + b['slope_du_dv']*v
            return ua + (x-a['x_value'])/(b['x_value']-a['x_value'])*(ub-ua)
    raise ValueError(x)

def grid_v(u):
    return [(L['y_value'], L['v_at_u0'] + L['slope_dv_du']*u) for L in hl]

for x in xs:
    u = u_of(x, (v0+v1)/2)
    for _ in range(3):
        pass
    ui = int(round(u))
    col = img[v0:v1, ui-halfw:ui+halfw+1].min(axis=1) < dark
    runs = []
    i = 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]: j += 1
            runs.append((v0+i, v0+j-1))
            i = j
        else:
            i += 1
    gv = grid_v(u)
    print(f"x={x:5.2f}  u={u:7.1f} (col {ui}, +-{halfw})")
    for a, b in runs:
        c = (a+b)/2; t = b-a+1
        tag = ''
        for yv, gvv in gv:
            if abs(c-gvv) <= 6 and t <= 9: tag = f'grid y={yv:.0f}'
            elif a-3 <= gvv <= b+3: tag = f'on-grid y={yv:.0f}'
        # recompute u at this v for the record
        uu = u_of(x, c)
        print(f"   v {a:5d}..{b:5d}  center {c:7.1f}  thick {t:3d}  u_at_v {uu:7.1f}  {tag}")
