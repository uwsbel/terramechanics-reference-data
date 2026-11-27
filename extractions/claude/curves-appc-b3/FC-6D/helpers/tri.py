"""Aid for reading triangle symbols by eye: for an approximate center (u, v) and orientation
(up | down), print the apex row (the first/last dark pixel in the 5 columns around u), and for each
row from the apex toward the flat edge the leftmost and rightmost dark run that touches the
symbol's outline, so the reader can see where the flat edge is even when a line or the frame
merges with it. Threshold 128.

usage: tri.py <image> up|down u v [halfwidth=20] [rows=36]
"""
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
orient, u, v = sys.argv[2], int(float(sys.argv[3])), int(float(sys.argv[4]))
hw = int(sys.argv[5]) if len(sys.argv) > 5 else 20
nrows = int(sys.argv[6]) if len(sys.argv) > 6 else 36
step = 1 if orient == "up" else -1
# apex: search from v - step*nrows/2 toward the flat edge for the first dark pixel in center cols
start = v - step * (nrows // 2)
apex = None
for k in range(nrows):
    r = start + step * k
    if g[r, u - 2:u + 3].any():
        apex = r
        break
print(f"apex row {apex} (searched from {start})")
for k in range(nrows):
    r = apex + step * k
    row = g[r, u - hw:u + hw + 1]
    s = "".join("#" if c else "." for c in row)
    print(f"{r:5d} {s}")
