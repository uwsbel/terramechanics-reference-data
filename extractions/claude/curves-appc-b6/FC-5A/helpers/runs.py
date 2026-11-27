"""For columns u in a range, list dark runs (v_top-v_bottom) between v0 and v1, one line per column.
usage: runs.py image u0 u1 step v0 v1"""
import sys
import numpy as np
from PIL import Image
img = sys.argv[1]
u0, u1, st, v0, v1 = map(int, sys.argv[2:7])
g = np.asarray(Image.open(img).convert("L")) < 128
for u in range(u0, u1 + 1, st):
    col = g[v0:v1, u]
    idx = np.where(col)[0]
    out = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                out.append((s + v0, p + v0)); s = i
            p = i
        out.append((s + v0, p + v0))
    print(f"{u}: " + "  ".join(f"{a}-{b}" for a, b in out))
