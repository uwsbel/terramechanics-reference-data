"""Print the dark runs (center, width) along columns or rows of an image, inside a window.

usage: runs.py <image> col <u0> <u1> <step> <v0> <v1>    runs along v in columns u
       runs.py <image> row <v0> <v1> <step> <u0> <u1>    runs along u in rows v
"""
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
mode = sys.argv[2]
a0, a1, st, b0, b1 = map(int, sys.argv[3:8])
for a in range(a0, a1 + 1, st):
    line = g[b0:b1 + 1, a] if mode == "col" else g[a, b0:b1 + 1]
    idx = np.where(line)[0]
    runs = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                runs.append((s, p))
                s = i
            p = i
        runs.append((s, p))
    print(f"{mode} {a}: " + "  ".join(f"{b0 + (s + p) / 2:.1f}({p - s + 1})" for s, p in runs))
