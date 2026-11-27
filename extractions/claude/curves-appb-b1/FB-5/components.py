"""Connected ink components inside the FB-5 frame (8-neighbour, by a two-pass union-find on runs).
Usage: python components.py <image>"""
import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
V, U = np.mgrid[0:g.shape[0], 0:g.shape[1]]
inside = (V > 889.39 - 0.01394 * U + 12) & (V < 4007.82 - 0.01448 * U - 12) & (U > 637.02 + 0.01642 * V + 12) & (U < 2763.59 + 0.0175 * V - 12)
m = g & inside
parent = {}
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra
runs_prev = []
allruns = []
for v in range(m.shape[0]):
    row = m[v]
    if not row.any():
        runs_prev = []
        continue
    idx = np.where(row)[0]
    br = np.where(np.diff(idx) > 1)[0]
    starts = np.r_[idx[0], idx[br + 1]]
    ends = np.r_[idx[br], idx[-1]]
    cur = []
    for s, e in zip(starts, ends):
        key = (v, int(s))
        parent[key] = key
        for (ps, pe, pk) in runs_prev:
            if ps <= e + 1 and pe >= s - 1:
                union(pk, key)
        cur.append((int(s), int(e), key))
        allruns.append((v, int(s), int(e), key))
    runs_prev = cur
comp = {}
for v, s, e, k in allruns:
    r = find(k)
    c = comp.setdefault(r, [10**9, -1, 10**9, -1, 0])
    c[0] = min(c[0], s); c[1] = max(c[1], e); c[2] = min(c[2], v); c[3] = max(c[3], v); c[4] += e - s + 1
for c in sorted(comp.values(), key=lambda c: (c[2], c[0])):
    print(f"px {c[4]:6d}  u {c[0]}-{c[1]}  v {c[2]}-{c[3]}")
