"""Column scan along a roughly known straight line: for each image column u, find the dark run in v
nearest the predicted position v_pred(u) = v0 + s*(u - u0), and print its center and length.
Usage: colscan.py image u0 v0 slope_dv_du u_from u_to [dark] [step] [win]"""
import sys
import numpy as np
from PIL import Image

img = sys.argv[1]
u0, v0, s, ua, ub = map(float, sys.argv[2:7])
dark = int(sys.argv[7]) if len(sys.argv) > 7 else 160
step = int(sys.argv[8]) if len(sys.argv) > 8 else 1
win = int(sys.argv[9]) if len(sys.argv) > 9 else 30
g = np.asarray(Image.open(img).convert("L"))
for u in range(int(ua), int(ub) + 1, step):
    vp = v0 + s * (u - u0)
    a, b = int(vp - win), int(vp + win)
    col = g[a:b, u] < dark
    runs, i = [], 0
    while i < len(col):
        if col[i]:
            j = i
            while j + 1 < len(col) and col[j + 1]:
                j += 1
            runs.append((a + i, a + j))
            i = j + 1
        else:
            i += 1
    if not runs:
        print(f"{u} pred {vp:.1f}  -- no ink")
        continue
    best = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - vp))
    c = (best[0] + best[1]) / 2
    print(f"{u} pred {vp:.1f}  run {best[0]}-{best[1]} c {c:.1f} len {best[1]-best[0]+1}  d {c-vp:+.1f}  nruns {len(runs)}")
