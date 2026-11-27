"""Ink bounding box and centre of a printed label inside a box: python label_centre.py image u0 v0 u1 v1 [...]"""
import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
a = [int(x) for x in sys.argv[2:]]
for i in range(0, len(a), 4):
    u0, v0, u1, v1 = a[i:i + 4]
    s = g[v0:v1, u0:u1]
    rows = np.where(s.sum(axis=1) >= 2)[0]
    cols = np.where(s.sum(axis=0) >= 2)[0]
    if len(rows) == 0:
        print(f"box {u0},{v0},{u1},{v1}: no ink")
        continue
    print(f"box {u0},{v0},{u1},{v1}: ink u {u0 + cols[0]}..{u0 + cols[-1]} (centre {u0 + (cols[0] + cols[-1]) / 2:.1f}), "
          f"v {v0 + rows[0]}..{v0 + rows[-1]} (centre {v0 + (rows[0] + rows[-1]) / 2:.1f})")
