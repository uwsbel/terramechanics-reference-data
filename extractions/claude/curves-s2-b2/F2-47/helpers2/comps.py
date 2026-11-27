"""Connected ink components of the F2-47 plot area with the grid lines masked (helper).

Usage: python comps.py [--mask 4] [--min 60] [--box u0 v0 u1 v1] [--save comps.npz]
Pixels within `mask` px of a calibrated grid line or frame line (each line with its own tilt) are
set to white, then dark pixels (< 128) are grouped into 8-connected components (union-find on
column runs). Each component of at least `min` pixels is listed: id, u range, v range, pixel count,
centroid. With --save the label image of the box is written so other helpers can ask which
component a pixel belongs to. Pixel coordinates are those of the unrotated page.
"""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import IMG, VL, HL, vline_u, hline_v

args = sys.argv[1:]
def opt(name, default, n=1, typ=int):
    if name in args:
        i = args.index(name)
        vals = [typ(x) for x in args[i + 1:i + 1 + n]]
        return vals if n > 1 else vals[0]
    return default
mask = opt('--mask', 4, typ=float); mn = opt('--min', 60)
u0, v0, u1, v1 = opt('--box', [506, 1700, 2640, 3240], 4)
save = None
if '--save' in args: save = args[args.index('--save') + 1]
sub = IMG[v0:v1, u0:u1].copy()
V, U = np.mgrid[v0:v1, u0:u1]
for L in VL:
    sub[np.abs(U - vline_u(L, V)) <= mask] = False
for L in HL:
    sub[np.abs(V - hline_v(L, U)) <= mask] = False
H, W = sub.shape
lab = np.zeros((H, W), dtype=np.int32)
parent = [0]
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
prev = []
for c in range(W):
    col = sub[:, c].astype(np.int8)
    idx = np.flatnonzero(np.diff(np.concatenate(([0], col, [0]))))
    cur = []
    for s, e in zip(idx[0::2], idx[1::2]):
        parent.append(len(parent)); rid = len(parent) - 1
        lab[s:e, c] = rid
        for ps, pe, pid in prev:
            if ps <= e and pe >= s - 1 + 0 and not (pe < s - 1 or ps > e):   # 8-connectivity
                a, b = find(rid), find(pid)
                if a != b: parent[b] = a
        cur.append((s, e - 1, rid)); 
    # fix: prev entries need (start, end) inclusive with 8-connectivity tolerance
    prev = [(s - 1, e + 1, r) for s, e, r in cur]
    prev = [(s, e, r) for s, e, r in prev]
roots = np.array([find(i) for i in range(len(parent))])
lab = roots[lab]
lab[~sub] = 0
ids, counts = np.unique(lab[lab > 0], return_counts=True)
keep = {i: n for i, n in zip(ids, counts) if n >= mn}
out = []
for i, n in keep.items():
    vv, uu = np.nonzero(lab == i)
    out.append((uu.min() + u0, uu.max() + u0, vv.min() + v0, vv.max() + v0, n, uu.mean() + u0, vv.mean() + v0, i))
out.sort()
for o in out:
    print(f"id {o[7]:6d} u {o[0]}-{o[1]} v {o[2]}-{o[3]} n {o[4]} centroid ({o[5]:.1f},{o[6]:.1f})")
if save:
    np.savez_compressed(save, lab=lab, box=np.array([u0, v0, u1, v1]))
