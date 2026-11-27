"""List the enclosed white holes (4-connected white components not touching the box border)
inside a box of the page image: centroid, area, bbox. A mechanical aid for crowded clusters of
hollow markers; what it lists is checked on the zoomed crop before anything is recorded.

    python holes.py <image> u0 v0 u1 v1 [--min-area 6]
"""
import argparse

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("box", nargs=4, type=int)
ap.add_argument("--min-area", type=int, default=6)
a = ap.parse_args()
u0, v0, u1, v1 = a.box
g = np.asarray(Image.open(a.image).convert("L"))[v0:v1, u0:u1]
white = g >= 128
h, w = white.shape
lab = np.zeros((h, w), dtype=int)
n = 0
for i in range(h):
    for j in range(w):
        if white[i, j] and lab[i, j] == 0:
            n += 1
            stack = [(i, j)]
            lab[i, j] = n
            while stack:
                y, x = stack.pop()
                for c, d in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= c < h and 0 <= d < w and white[c, d] and lab[c, d] == 0:
                        lab[c, d] = n
                        stack.append((c, d))
print(f"box u {u0}..{u1} v {v0}..{v1}: enclosed holes (centroid u, v; area; bbox u0-u1, v0-v1)")
for k in range(1, n + 1):
    ys, xs = np.where(lab == k)
    if ys.min() == 0 or xs.min() == 0 or ys.max() == h - 1 or xs.max() == w - 1:
        continue
    if len(ys) < a.min_area:
        continue
    print(f"  ({xs.mean() + u0:7.1f}, {ys.mean() + v0:7.1f})  area {len(ys):4d}  "
          f"u {xs.min() + u0}-{xs.max() + u0}  v {ys.min() + v0}-{ys.max() + v0}")
