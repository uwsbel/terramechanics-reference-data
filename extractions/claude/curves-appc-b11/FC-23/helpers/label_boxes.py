"""Bounding boxes of printed tick labels: dark pixels in a strip, grouped into clusters separated by
at least `gap` white pixels along the strip (reading aid for the by-eye label check)."""
import sys
import numpy as np
from PIL import Image
img, u0, v0, u1, v1, axis, gap = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6], int(sys.argv[7])
g = np.asarray(Image.open(img).convert("L"))[v0:v1, u0:u1] < 150
prof = g.any(axis=0) if axis == "x" else g.any(axis=1)
idx = np.nonzero(prof)[0]
groups = []
s = p = idx[0]
for i in idx[1:]:
    if i - p > gap:
        groups.append((s, p)); s = i
    p = i
groups.append((s, p))
for a, b in groups:
    if axis == "x":
        sub = g[:, a:b + 1]; rows = np.nonzero(sub.any(axis=1))[0]
        print(f"u {u0+a}-{u0+b} centre {u0+(a+b)/2:.1f}; v {v0+rows[0]}-{v0+rows[-1]} centre {v0+(rows[0]+rows[-1])/2:.1f}")
    else:
        sub = g[a:b + 1, :]; cols = np.nonzero(sub.any(axis=0))[0]
        print(f"v {v0+a}-{v0+b} centre {v0+(a+b)/2:.1f}; u {u0+cols[0]}-{u0+cols[-1]} centre {u0+(cols[0]+cols[-1])/2:.1f}")
