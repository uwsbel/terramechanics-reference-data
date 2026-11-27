"""Connected ink components inside the plot frame, with the grid lines masked (F2-47 helper).

Usage: python out/F2-47/helpers/components.py <calibration.json> <image> [--box u0 v0 u1 v1]
       [--mask 5] [--min 40]

Pixels within `mask` px of a calibrated grid line (each line with its own tilt) are set to white,
so dashes and letters that touch a grid line are not joined through it. The remaining dark pixels
(threshold 128) are grouped into 8-connected components; each component of at least `min` pixels
is listed with its bounding box, pixel count, centroid and the end points of its principal axis
(for a dash: its two ends along the line). Used to locate the dashes of the dashed trace; every
dash used for a sample is checked by eye on a zoomed crop.
"""
import argparse, json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('cal'); ap.add_argument('image')
ap.add_argument('--box', type=int, nargs=4, default=[505, 1700, 2640, 3236])
ap.add_argument('--mask', type=float, default=5)
ap.add_argument('--min', type=int, default=40)
a = ap.parse_args()

cal = json.load(open(a.cal))
img = np.array(Image.open(a.image).convert('L')) < 128
u0, v0, u1, v1 = a.box
sub = img[v0:v1, u0:u1].copy()
V, U = np.mgrid[v0:v1, u0:u1]
for L in cal['vertical_lines']:
    uc = L['u_at_v0'] + L['slope_du_dv'] * V
    sub[np.abs(U - uc) <= a.mask] = False
for L in cal['horizontal_lines']:
    vc = L['v_at_u0'] + L['slope_dv_du'] * U
    sub[np.abs(V - vc) <= a.mask] = False

H, W = sub.shape
parent = {}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(x, y):
    rx, ry = find(x), find(y)
    if rx != ry: parent[ry] = rx
runs_prev = []
allruns = []
rid = 0
for r in range(H):
    row = sub[r]
    runs = []
    c = 0
    idx = np.flatnonzero(np.diff(np.concatenate(([0], row.view(np.int8), [0]))))
    for s, e in zip(idx[0::2], idx[1::2]):
        runs.append((s, e - 1, rid)); parent[rid] = rid; allruns.append((r, s, e - 1, rid)); rid += 1
    for s, e, i in runs:
        for ps, pe, pi in runs_prev:
            if ps <= e + 1 and pe >= s - 1:
                union(i, pi)
    runs_prev = runs
comps = {}
for r, s, e, i in allruns:
    comps.setdefault(find(i), []).append((r, s, e))
out = []
for k, rr in comps.items():
    n = sum(e - s + 1 for r, s, e in rr)
    if n < a.min: continue
    vs = np.concatenate([np.full(e - s + 1, r) for r, s, e in rr]) + v0
    us = np.concatenate([np.arange(s, e + 1) for r, s, e in rr]) + u0
    cu, cv = us.mean(), vs.mean()
    X = np.stack([us - cu, vs - cv])
    w, vec = np.linalg.eigh(X @ X.T / n)
    d = vec[:, 1]
    proj = d[0] * (us - cu) + d[1] * (vs - cv)
    p0, p1 = proj.min(), proj.max()
    e0 = (cu + d[0] * p0, cv + d[1] * p0); e1 = (cu + d[0] * p1, cv + d[1] * p1)
    if e0[0] > e1[0]: e0, e1 = e1, e0
    width = n / max(p1 - p0, 1)
    out.append((us.min(), us.max(), vs.min(), vs.max(), n, cu, cv, e0, e1, p1 - p0, width))
out.sort()
print('umin umax vmin vmax  npx  centroid(u,v)  end0(u,v) end1(u,v)  length  mean_width')
for o in out:
    print(f"{o[0]:5d} {o[1]:5d} {o[2]:5d} {o[3]:5d} {o[4]:6d}  ({o[5]:7.1f},{o[6]:7.1f})  "
          f"({o[7][0]:7.1f},{o[7][1]:7.1f}) ({o[8][0]:7.1f},{o[8][1]:7.1f})  {o[9]:6.1f} {o[10]:5.1f}")
