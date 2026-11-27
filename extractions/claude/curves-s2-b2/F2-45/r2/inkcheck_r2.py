"""Own ink check of the samples: distance from each sample to the nearest ink pixel, with and without the
grid bands (+-3 px around each fitted interior line) and the frame removed."""
import csv
import numpy as np
from common import INK, VL, HL, vline_u, hline_v
H, W = INK.shape
vv = np.arange(H)[:, None]; uu = np.arange(W)[None, :]
def nearest(mask, u, v, r=12):
    a0, a1, b0, b1 = int(v) - r, int(v) + r + 1, int(u) - r, int(u) + r + 1
    vs, us = np.nonzero(mask[a0:a1, b0:b1])
    if len(vs) == 0: return 99
    return float(np.min(np.hypot(us + b0 - u, vs + a0 - v)))
sub = INK.copy()
box = (slice(1400, 3700), slice(300, 2400))
V = vv[box[0]]; U = uu[:, box[1]]
g = np.zeros((V.shape[0], U.shape[1]), bool)
for L in VL:
    g |= np.abs(U - (L['u_at_v0'] + L['slope_du_dv'] * V)) <= (3 if 0 < L['y_value'] < 300 else 7)
for L in HL:
    g |= np.abs(V - (L['v_at_u0'] + L['slope_dv_du'] * U)) <= (3 if 0 < L['x_value'] < 7 else 7)
sub[box] &= ~g
for r in csv.DictReader(open('out/F2-45/points-p1.csv')):
    u, v = float(r['pixel_u']), float(r['pixel_v'])
    d0 = nearest(INK, u, v); d1 = nearest(sub, u, v)
    flag = '  <-- check' if d1 > 2 else ''
    print(r['series_id'], r['point_kind'], r['sequence'], u, v, 'ink %.1f  no-grid %.1f' % (d0, d1), flag)
