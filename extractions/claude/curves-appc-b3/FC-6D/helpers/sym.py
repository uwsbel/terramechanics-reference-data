"""Print the dark-pixel extent inside small windows (one per argument "u0,v0,u1,v1"), as an aid to
reading a symbol's center by eye: bbox of dark pixels (threshold 128), bbox center, and the
centroid of the bbox for a triangle (1/3 of the height from the flat edge) for both orientations,
and for a plus the strongest column and row bands (the bars), 60 percent of the maximum count.
The reader chooses the window on a zoomed crop so it holds the symbol only, then checks the
result on the crop. Also prints an ASCII map of the window ('#' dark).

usage: sym.py <image> u0,v0,u1,v1 [u0,v0,u1,v1 ...] [--map]
"""
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
show = "--map" in sys.argv
for w in [a for a in sys.argv[2:] if a != "--map"]:
    u0, v0, u1, v1 = [int(x) for x in w.split(",")]
    sub = g[v0:v1 + 1, u0:u1 + 1] < 128
    vv, uu = np.where(sub)
    if len(uu) == 0:
        print(w, "no dark pixels")
        continue
    umin, umax, vmin, vmax = uu.min() + u0, uu.max() + u0, vv.min() + v0, vv.max() + v0
    h = vmax - vmin
    print(f"{w}: u {umin}..{umax} (c {(umin+umax)/2:.1f})  v {vmin}..{vmax} (c {(vmin+vmax)/2:.1f})  "
          f"tri-up centroid v {vmax - h/3:.1f}  tri-down centroid v {vmin + h/3:.1f}  n={len(uu)}")
    colc, rowc = sub.sum(axis=0), sub.sum(axis=1)
    cs = np.where(colc >= 0.6 * colc.max())[0]
    rs = np.where(rowc >= 0.6 * rowc.max())[0]
    print(f"    plus: vertical bar u {cs.min()+u0}..{cs.max()+u0} (c {(cs.min()+cs.max())/2+u0:.1f}), "
          f"horizontal bar v {rs.min()+v0}..{rs.max()+v0} (c {(rs.min()+rs.max())/2+v0:.1f})")
    if show:
        for r in range(sub.shape[0]):
            print(f"{v0 + r:5d} " + "".join("#" if c else "." for c in sub[r]))
