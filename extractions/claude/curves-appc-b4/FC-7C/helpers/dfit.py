"""Quarter-circle (D) symbols: corner and radius from the two straight edges (reader's aid).

On the page as scanned the D has a straight top edge and a straight right edge meeting at the
top-right corner, and an arc from the top-left to the bottom-right. The straight edges are taken
as the median outer boundary (top edge: topmost ink per column over the middle third of the box
width; right edge: rightmost ink per row over the middle third of the box height, grid-line
rows/columns skipped), so a stroke overshoot at an arc end does not move them. R is the mean of
(right - leftmost ink) and (bottommost ink - top). The center reported is the area centroid of the
quarter disk: (right - 0.4244 R, top + 0.4244 R).
Usage: python dfit.py <image> <calibration.json> id,u0,v0,u1,v1 ...
"""
import sys, json
import numpy as np
from PIL import Image

g = np.array(Image.open(sys.argv[1]).convert('L')) < 160
cal = json.load(open(sys.argv[2]))


def masked(u, v):
    for L in cal['vertical_lines']:
        if abs(u - (L['u_at_v0'] + L['slope_du_dv'] * v)) <= 4:
            return True
    for L in cal['horizontal_lines']:
        if abs(v - (L['v_at_u0'] + L['slope_dv_du'] * u)) <= 4:
            return True
    return False


print('id,left,top,right,bottom,R,uc,vc')
for spec in sys.argv[3:]:
    i, u0, v0, u1, v1 = spec.split(',')
    u0, v0, u1, v1 = int(u0), int(v0), int(u1), int(v1)
    d = g[v0:v1 + 1, u0:u1 + 1].copy()
    for vv in range(v0, v1 + 1):
        for uu in range(u0, u1 + 1):
            if masked(uu, vv):
                d[vv - v0, uu - u0] = False
    vs, us = np.nonzero(d)
    left, bottom = us.min() + u0, vs.max() + v0
    lo, hi = left, us.max() + u0
    tops = []
    for uu in range(int(lo + 0.33 * (hi - lo)), int(lo + 0.67 * (hi - lo)) + 1):
        col = np.nonzero(d[:, uu - u0])[0]
        if len(col):
            tops.append(col.min() + v0)
    top = float(np.median(tops))
    rights = []
    for vv in range(int(top + 0.33 * (bottom - top)), int(top + 0.67 * (bottom - top)) + 1):
        row = np.nonzero(d[vv - v0])[0]
        if len(row):
            rights.append(row.max() + u0)
    right = float(np.median(rights))
    R = ((right - left) + (bottom - top)) / 2
    print('%s,%d,%.1f,%.1f,%d,%.1f,%.1f,%.1f' % (i, left, top, right, bottom, R, right - 0.4244 * R, top + 0.4244 * R))
