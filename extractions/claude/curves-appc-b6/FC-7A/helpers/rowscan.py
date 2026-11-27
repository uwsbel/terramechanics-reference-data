"""Row scan along a roughly known straight line: for each image row v, find the dark run in u
nearest the predicted position u_pred(v) = u0 + (v - v0) / slope, and print its center and width.
Usage: rowscan.py image u0 v0 slope_dv_du v_from v_to [dark] [step]"""
import sys
import numpy as np
from PIL import Image

img, u0, v0, s, va, vb = sys.argv[1], *map(float, sys.argv[2:7])
dark = int(sys.argv[7]) if len(sys.argv) > 7 else 160
step = int(sys.argv[8]) if len(sys.argv) > 8 else 1
g = np.asarray(Image.open(img).convert("L"))
lo, hi = int(min(va, vb)), int(max(va, vb))
for v in range(hi, lo - 1, -step):
    up = u0 + (v - v0) / s
    a, b = int(up - 40), int(up + 40)
    row = g[v, a:b] < dark
    runs, i = [], 0
    while i < len(row):
        if row[i]:
            j = i
            while j + 1 < len(row) and row[j + 1]:
                j += 1
            runs.append((a + i, a + j))
            i = j + 1
        else:
            i += 1
    if not runs:
        print(f"{v} pred {up:.1f}  -- no ink")
        continue
    best = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - up))
    c = (best[0] + best[1]) / 2
    print(f"{v} pred {up:.1f}  run {best[0]}-{best[1]} c {c:.1f} w {best[1]-best[0]+1}  d {c-up:+.1f}  nruns {len(runs)}")
