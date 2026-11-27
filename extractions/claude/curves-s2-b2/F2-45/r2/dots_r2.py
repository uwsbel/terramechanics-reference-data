"""Dotted trace (lpt79, Four-Inch Footpad, LPT No. 79) of Figure 2-45: the dots and their drawing order.

The ink inside the frame, less the interior grid bands (+-3 px around each fitted line) and less the
solid trace (its tracked run in each row, widened by 3 px), is split into 8-connected components. A
component is dot-like when its box is at most 18 px each way, it has at least 15 px of ink and fills at
least 45 percent of its box. Dot-like components are chained from the one nearest the origin end
(u 2230, v 3559), each next one 8 to 45 px away and within 35 degrees of the running direction,
preferring a spacing near 17.5 px. A dot's center is the centroid of its ink. Writes
out/F2-45/r2/dots.csv: k, u, v, n, umin, umax, vmin, vmax, spacing, near_grid (fitted line within 9 px).
"""
import csv
import numpy as np
from common import INK, VL, HL, vline_u, hline_v, label, near_vgrid, near_hgrid, erode_disk

v0, v1, u0, u1 = 1472, 3586, 392, 2270
sub = INK[v0:v1, u0:u1].copy()
vv = np.arange(v0, v1)[:, None]
uu = np.arange(u0, u1)[None, :]
grid = np.zeros_like(sub)
for L in VL[1:-1]:
    grid |= np.abs(uu - (L['u_at_v0'] + L['slope_du_dv'] * vv)) <= 3
for L in HL[1:-1]:
    grid |= np.abs(vv - (L['v_at_u0'] + L['slope_dv_du'] * uu)) <= 3
m = sub & ~grid
for r in csv.DictReader(open('out/F2-45/r2/solid-rows.csv')):
    if r['s'] == '':
        continue
    v = int(r['v']) - v0
    if 0 <= v < m.shape[0]:
        m[v, max(int(r['s']) - 3 - u0, 0):max(int(r['e']) + 4 - u0, 0)] = False

comps = label(m)
# Touching dots: a component that is dot-wide across its principal axis but longer than one dot along it
# is a run of k touching dots, k = 1 + round((length - 12) / 17.5) (one dot is about 12 px long, the dot
# pitch about 17.5 px); it is split by 1-D k-means along the axis, and each part's centroid is a dot.
# A run of two or more must lie along the trace direction (within 30 degrees).
TDIR = np.array([-0.5, -0.866])
blobs = []
for c in comps:
    n = len(c)
    if n < 15:
        continue
    pu, pv = c[:, 1].astype(float), c[:, 0].astype(float)
    mu, mv = pu.mean(), pv.mean()
    X = np.stack([pu - mu, pv - mv], 1)
    w, V = np.linalg.eigh(X.T @ X)
    ax1 = V[:, 1]
    p1 = X @ ax1
    p2 = X @ V[:, 0]
    L1, L2 = np.ptp(p1) + 1, np.ptp(p2) + 1
    if L2 > 16 or L1 > 75 or n < 0.4 * L1 * L2:
        continue
    k = max(1, 1 + int(round((L1 - 12) / 17.5)))
    if k == 1 and L1 > 18:
        continue
    if k >= 2 and abs(ax1 @ TDIR) < np.cos(np.radians(30)):
        continue
    cent = np.linspace(p1.min(), p1.max(), 2 * k + 1)[1::2]
    for _ in range(20):
        lab = np.argmin(np.abs(p1[:, None] - cent[None, :]), axis=1)
        cent = np.array([p1[lab == j].mean() if np.any(lab == j) else cent[j] for j in range(k)])
    for j in range(k):
        sel = lab == j
        if sel.sum() < 10:
            continue
        us, vs = pu[sel], pv[sel]
        blobs.append(dict(u=us.mean() + u0, v=vs.mean() + v0, n=int(sel.sum()), umin=int(us.min()) + u0,
                          umax=int(us.max()) + u0, vmin=int(vs.min()) + v0, vmax=int(vs.max()) + v0,
                          split=k))
P = np.array([[b['u'], b['v']] for b in blobs])
start = int(np.argmin(np.hypot(P[:, 0] - 2230, P[:, 1] - 3559)))
chain, used = [start], {start}
d = np.array([-0.5, -0.866])
while True:
    p = P[chain[-1]]
    best = None
    for i in range(len(P)):
        if i in used:
            continue
        q = P[i] - p
        dist = float(np.hypot(*q))
        if not (8 <= dist <= 45):
            continue
        cosang = float(q @ d / dist)
        if cosang < np.cos(np.radians(35)):
            continue
        score = abs(dist - 17.5) + 25 * (1 - cosang)
        if best is None or score < best[0]:
            best = (score, i)
    if best is None:
        break
    i = best[1]
    q = P[i] - p
    d = 0.6 * d + 0.4 * q / np.hypot(*q)
    d /= np.hypot(*d)
    chain.append(i)
    used.add(i)

with open('out/F2-45/r2/dots.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['k', 'u', 'v', 'n', 'umin', 'umax', 'vmin', 'vmax', 'spacing', 'near_grid', 'split'])
    prev = None
    for k, i in enumerate(chain, 1):
        b = blobs[i]
        sp = '' if prev is None else round(float(np.hypot(b['u'] - prev[0], b['v'] - prev[1])), 2)
        ng = int(near_vgrid(b['u'], b['v'], 9) or near_hgrid(b['u'], b['v'], 9))
        wr.writerow([k, round(b['u'], 2), round(b['v'], 2), b['n'], b['umin'], b['umax'], b['vmin'],
                     b['vmax'], sp, ng, b['split']])
        prev = (b['u'], b['v'])
print('components', len(comps), 'dot-like', len(blobs), 'chained', len(chain),
      'first', P[chain[0]].round(1), 'last', P[chain[-1]].round(1))
unused = [blobs[i] for i in range(len(blobs)) if i not in used]
print('dot-like not chained:', len(unused))
for b in unused:
    print('  ', round(b['u'], 1), round(b['v'], 1), b['n'], b['umax'] - b['umin'] + 1, b['vmax'] - b['vmin'] + 1, b['split'])
