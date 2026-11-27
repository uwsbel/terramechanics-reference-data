"""Triangle apex by extrapolating the two slanted outer edges (reader's aid for triangles whose
apex lies on a horizontal grid line). For each box: leftmost ink per row, skipping rows within
`band` px of the given grid row v_line (or none), fit a line to the upper edge rows and to the
lower edge rows (rows farther than `skip` px from the apex row and from the base corners),
intersect them. Prints the extrapolated sharp tip and, for comparison, the observed tip.
Usage: python apex.py <image> id,u0,v0,u1,v1,v_line ...
"""
import sys
import numpy as np
from PIL import Image

g = np.array(Image.open(sys.argv[1]).convert('L')) < 160
for spec in sys.argv[2:]:
    i, u0, v0, u1, v1, vl = spec.split(',')
    u0, v0, u1, v1 = int(u0), int(v0), int(u1), int(v1)
    vl = float(vl) if vl else None
    rows = []
    for v in range(v0, v1 + 1):
        if vl is not None and abs(v - vl) <= 4:
            continue
        us = np.nonzero(g[v, u0:u1 + 1])[0]
        if len(us):
            rows.append((v, us.min() + u0))
    rows = np.array(rows, float)
    vmid = (v0 + v1) / 2
    up = rows[(rows[:, 0] < vmid - 3) & (rows[:, 0] > v0 + 4)]
    lo = rows[(rows[:, 0] > vmid + 3) & (rows[:, 0] < v1 - 4)]
    a1, b1 = np.polyfit(up[:, 0], up[:, 1], 1)
    a2, b2 = np.polyfit(lo[:, 0], lo[:, 1], 1)
    v = (b2 - b1) / (a1 - a2)
    u = a1 * v + b1
    print('%s tip_extrap u=%.1f v=%.1f slopes %.2f %.2f observed_min_u=%d' % (i, u, v, a1, a2, rows[:, 1].min()))
