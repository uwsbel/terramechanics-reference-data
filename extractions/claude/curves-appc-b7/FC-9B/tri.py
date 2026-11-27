"""Reader helper: centroid of an upright triangle symbol drawn by a round pen (ink = centreline dilated by
the pen). Takes the largest 8-connected ink component in a box (optionally with mask boxes blanked, to
cut off a line touching the symbol), and reports its outer extremes, the stroke width w (vertical run of
the base), the centreline vertices (outer extremes moved in by w/2) and the centroid, one third of the
centreline height above the centreline base (protocol rule 8).
usage: tri.py <image> u0 v0 u1 v1 [--mask u0 v0 u1 v1]..."""
import sys
from collections import deque

import numpy as np
from PIL import Image

args = sys.argv[1:]
img = args[0]
u0, v0, u1, v1 = map(int, args[1:5])
masks = []
i = 5
while i < len(args):
    if args[i] == "--mask":
        masks.append(tuple(map(int, args[i + 1:i + 5])))
        i += 5
    else:
        raise SystemExit("bad args")
g = np.asarray(Image.open(img).convert("L"))
b = (g[v0:v1, u0:u1] < 128).copy()
for (a0, c0, a1, c1) in masks:
    b[max(0, c0 - v0):max(0, c1 - v0), max(0, a0 - u0):max(0, a1 - u0)] = False
lab = np.zeros(b.shape, int)
comps = []
n = 0
for (y, x) in zip(*np.nonzero(b)):
    if lab[y, x]:
        continue
    n += 1
    q = deque([(y, x)])
    lab[y, x] = n
    pix = []
    while q:
        cy, cx = q.popleft()
        pix.append((cy, cx))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < b.shape[0] and 0 <= nx < b.shape[1] and b[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n
                    q.append((ny, nx))
    comps.append(pix)
comps.sort(key=len, reverse=True)
P = np.array(comps[0])
V, U = P[:, 0] + v0, P[:, 1] + u0
top, bot = V.min(), V.max()
apex_u = U[V <= top + 1].mean()
base = V >= bot - 2
left, right = U[base].min(), U[base].max()
# stroke width: vertical run of the base at columns in its middle third
ws = []
for x in range(int(left + (right - left) / 3), int(right - (right - left) / 3) + 1):
    col = sorted(V[U == x])
    run = [v for v in col if v > bot - 15]
    # the bottom-most contiguous run
    r = 1
    for k in range(len(run) - 1, 0, -1):
        if run[k] - run[k - 1] == 1:
            r += 1
        else:
            break
    ws.append(r)
w = float(np.median(ws)) if ws else 5.0
# outer extremes are pixel centres; the ink edge is half a pixel further out
top_e, bot_e, left_e, right_e = top - 0.5, bot + 0.5, left - 0.5, right + 0.5
va, vb = top_e + w / 2, bot_e - w / 2
ul, ur = left_e + w / 2, right_e - w / 2
cu = (ul + ur + apex_u) / 3
cv = vb - (vb - va) / 3
print(f"component {len(P)} px (next {len(comps[1]) if len(comps) > 1 else 0}); bbox u {U.min()}..{U.max()} v {top}..{bot}")
print(f"apex u {apex_u:.1f}; base outer u {left}..{right}; stroke w {w:.1f}")
print(f"centreline: apex ({apex_u:.1f},{va:.1f}) base v {vb:.1f} u {ul:.1f}..{ur:.1f}; height {vb - va:.1f} width {ur - ul:.1f}")
print(f"centroid u {cu:.1f} v {cv:.1f}; bbox midpoint v {(top_e + bot_e) / 2:.1f}; h/6 = {(vb - va) / 6:.1f}")
