"""Reader helper: dark runs along page rows near the curves. Rows lying on a horizontal grid line (dark over
most of a wide window) are flagged. usage: runs.py image v0 v1 step [halfwin]"""
import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
v0, v1, st = map(int, sys.argv[2:5]); hw = int(sys.argv[5]) if len(sys.argv) > 5 else 70
for v in range(v0, v1 + 1, st):
    c = int(690 + 0.4 * (v - 1300))
    a, b = max(c - hw, 680), c + hw
    row = g[v, a:b]
    wide = g[v, 1950:2140].mean() if v < 3740 else 1.0   # right of the table and curves: grid line test
    runs, s = [], None
    for i, d in enumerate(row):
        if d and s is None: s = i
        if not d and s is not None: runs.append((a + s, a + i - 1)); s = None
    if s is not None: runs.append((a + s, b - 1))
    flag = "GRIDROW" if wide > 0.5 else ""
    print(f"v {v} {flag:7s} " + " ".join(f"{p}-{q}({q-p+1})" for p, q in runs))
