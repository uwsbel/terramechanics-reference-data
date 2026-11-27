"""Marker bounding boxes for FC-3A: ink in a window, minus the drawn-line band (helper)."""
import sys, json, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 160
lf = json.load(open(sys.argv[2]))
line = {k: (v["slope"], v["icpt"]) for k, v in lf.items()}
# approx centers from the crops, and which line touches (if any)
M = [("dr100-130", "square", 1133, 2815, "L47"), ("dr100-130", "square", 1424, 2479, "L47"),
     ("dr100-130", "square", 1777, 2184, None), ("dr100-130", "square", 2023, 1815, "L47"),
     ("dr100-130", "square", 2278, 1583, "L47"),
     ("dr0-15", "circle", 1135, 2959, "L38"), ("dr0-15", "circle", 1425, 2657, None),
     ("dr0-15", "circle", 1778, 2408, None), ("dr0-15", "circle", 2024, 2331, None),
     ("dr0-15", "circle", 2278, 2090, None)]
half = {"L47": 8.5, "L38": 8.0}
for s, sym, uc, vc, ln in M:
    w = 24
    sub = g[vc - w:vc + w + 1, uc - w:uc + w + 1].copy()
    if ln:
        b, a = line[ln]
        for j in range(sub.shape[1]):
            u = uc - w + j; vl = a + b * u
            for i in range(sub.shape[0]):
                v = vc - w + i
                if abs(v - vl) <= half[ln]: sub[i, j] = False
    ys, xs = np.nonzero(sub)
    umin, umax = uc - w + xs.min(), uc - w + xs.max(); vmin, vmax = vc - w + ys.min(), vc - w + ys.max()
    print("%-9s %-6s approx (%d,%d) line %s: bbox u %d..%d v %d..%d -> center (%.1f, %.1f) size %dx%d" % (
        s, sym, uc, vc, ln, umin, umax, vmin, vmax, (umin + umax) / 2, (vmin + vmax) / 2, umax - umin + 1, vmax - vmin + 1))
