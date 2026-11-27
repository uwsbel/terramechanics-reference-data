# horizontal ink runs in rows v (u0..u1)
import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
u0, u1 = int(sys.argv[2]), int(sys.argv[3])
for v in map(int, sys.argv[4].split(",")):
    row = g[v, u0:u1]; runs, s = [], None
    for i, d in enumerate(row):
        if d and s is None: s = i
        if not d and s is not None: runs.append((u0 + s, u0 + i - 1)); s = None
    if s is not None: runs.append((u0 + s, u1 - 1))
    print(v, " ".join(f"{a}-{b}" for a, b in runs))
