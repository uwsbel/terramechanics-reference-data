"""Print dark runs along rows or columns of the page image (for locating ticks, axes, lines)."""
import sys
import numpy as np
from PIL import Image

img, mode = sys.argv[1], sys.argv[2]
g = np.asarray(Image.open(img).convert("L")) < 128

def runs(arr, off):
    idx = np.where(arr)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s + off, p + off))
            s = i
        p = i
    out.append((s + off, p + off))
    return out

if mode == "col":   # col u v0 v1 : dark runs in column u between v0 and v1
    u, v0, v1 = map(int, sys.argv[3:6])
    for uu in [u]:
        print(uu, runs(g[v0:v1, uu], v0))
elif mode == "row":  # row v u0 u1
    v, u0, u1 = map(int, sys.argv[3:6])
    print(v, runs(g[v, u0:u1], u0))
elif mode == "cols":  # cols u0 u1 step v0 v1
    u0, u1, st, v0, v1 = map(int, sys.argv[3:8])
    for uu in range(u0, u1, st):
        print(uu, runs(g[v0:v1, uu], v0))
elif mode == "rows":  # rows v0 v1 step u0 u1
    v0, v1, st, u0, u1 = map(int, sys.argv[3:8])
    for vv in range(v0, v1, st):
        print(vv, runs(g[vv, u0:u1], u0))
