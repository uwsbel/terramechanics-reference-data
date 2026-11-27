# For a near-horizontal line v = c + s*u, report at each u the ink run that contains/nearest the line:
# its top, bottom, thickness and center, using columns u-1..u+1 (any ink).
import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
c, s = float(sys.argv[2]), float(sys.argv[3])
us = range(int(sys.argv[4]), int(sys.argv[5]) + 1, int(sys.argv[6]))
out = []
for u in us:
    v0 = int(round(c + s * u))
    col = g[v0 - 12:v0 + 13, u - 1:u + 2].any(axis=1)
    # run containing the index nearest the center
    idx = np.where(col)[0]
    if len(idx) == 0:
        print(u, "no ink"); continue
    k = idx[np.argmin(abs(idx - 12))]
    a = k
    while a > 0 and col[a - 1]: a -= 1
    b = k
    while b < len(col) - 1 and col[b + 1]: b += 1
    top, bot = v0 - 12 + a, v0 - 12 + b
    out.append((u, top, bot, bot - top + 1, (top + bot) / 2 - (c + s * u)))
    print(u, top, bot, bot - top + 1, f"{(top + bot) / 2 - (c + s * u):+.1f}")
th = np.array([o[3] for o in out]); print("median thickness", np.median(th))
