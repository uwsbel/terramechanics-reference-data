"""Dark runs per column (or per row) inside a window, on a given image (page or de-gridded aid).
Columns: u from U0 to U1 step S, v window from a path (piecewise linear center) +- H.
Prints u: run(top-bottom) ...  Rows mode: v from V0 to V1, u window."""
import sys
import numpy as np
from PIL import Image
img = sys.argv[1]; mode = sys.argv[2]
a0, a1, step = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
b0, b1 = int(sys.argv[6]), int(sys.argv[7])
g = np.asarray(Image.open(img).convert("L")) < 128
def runs(col, off):
    idx = np.where(col)[0]
    out = []
    if len(idx) == 0: return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s + off, p + off)); s = i
        p = i
    out.append((s + off, p + off))
    return out
for a in range(a0, a1 + 1, step):
    if mode == "col":
        r = runs(g[b0:b1, a], b0)
    else:
        r = runs(g[a, b0:b1], b0)
    print(a, " ".join(f"{s}-{e}" for s, e in r if e - s >= 1))
