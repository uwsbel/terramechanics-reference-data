"""Per-symbol outer extents inside a reader-chosen tight box (reader's aid).

For each row of symbols.csv (id, series_id, symbol, bu0, bv0, bu1, bv1) prints the extents of the
dark pixels inside the box, both with the fitted grid lines masked (+-halfw px) and unmasked, and
flags an extent where the two differ (a grid line runs along that side of the box or through the
symbol's extreme), so the reader can settle it by eye.
"""
import sys, json, csv
import numpy as np
from PIL import Image

img, calp, symp = sys.argv[1:4]
halfw = 4
g = np.array(Image.open(img).convert('L'))
dark_all = g < 160
cal = json.load(open(calp))
H, W = g.shape


def gridmask(u0, v0, u1, v1):
    vv, uu = np.mgrid[v0:v1 + 1, u0:u1 + 1]
    m = np.zeros(vv.shape, bool)
    for L in cal['vertical_lines']:
        hw = halfw + (2 if L['y_value'] in (0.0, 35.0) else 0)
        m |= np.abs(uu - (L['u_at_v0'] + L['slope_du_dv'] * vv)) <= hw
    for L in cal['horizontal_lines']:
        hw = halfw + (2 if L['x_value'] in (0.0, 0.32) else 0)
        m |= np.abs(vv - (L['v_at_u0'] + L['slope_dv_du'] * uu)) <= hw
    return m


print('id,series,symbol,m_u0,m_v0,m_u1,m_v1,r_u0,r_v0,r_u1,r_v1,flags')
for row in csv.DictReader(open(symp)):
    u0, v0, u1, v1 = (int(row[k]) for k in ('bu0', 'bv0', 'bu1', 'bv1'))
    d = dark_all[v0:v1 + 1, u0:u1 + 1]
    m = gridmask(u0, v0, u1, v1)
    res = []
    for dd in (d & ~m, d):
        vs, us = np.nonzero(dd)
        res.append((us.min() + u0, vs.min() + v0, us.max() + u0, vs.max() + v0) if len(us) else (0, 0, 0, 0))
    flags = ''.join(n for n, a, b in zip(('L', 'T', 'R', 'B'), res[0], res[1]) if a != b)
    print('%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%s' % ((row['id'], row['series_id'], row['symbol']) + res[0] + res[1] + (flags,)))
