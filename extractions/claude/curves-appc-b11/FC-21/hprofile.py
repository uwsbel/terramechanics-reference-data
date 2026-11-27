# vertical runs of ink in columns u (step) within v0..v1: prints the dark runs per column
import sys
import numpy as np
from PIL import Image
img = sys.argv[1]; u0, u1, step, v0, v1 = map(int, sys.argv[2:7])
g = np.asarray(Image.open(img).convert("L")) < 128
for u in range(u0, u1 + 1, step):
    col = g[v0:v1, u]
    runs, s = [], None
    for i, d in enumerate(col):
        if d and s is None: s = i
        if not d and s is not None: runs.append((v0 + s, v0 + i - 1)); s = None
    if s is not None: runs.append((v0 + s, v1 - 1))
    print(u, " ".join(f"{a}-{b}({b-a+1})" for a, b in runs))
