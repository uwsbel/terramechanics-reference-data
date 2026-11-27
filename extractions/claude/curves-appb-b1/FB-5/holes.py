"""Enclosed white regions (holes) inside the FB-5 frame: every white region not connected to the
frame's interior background. A plotted open circle leaves a hole of about 380 px; letters leave
smaller ones. Usage: python holes.py <image>"""
import sys
from collections import deque
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
u0, v0, u1, v1 = 700, 900, 2820, 3970
sub = ~g[v0:v1, u0:u1]
H, W = sub.shape
lab = np.zeros(sub.shape, np.int32)
n = 0
regions = []
for sv in range(H):
    for su in range(W):
        if sub[sv, su] and lab[sv, su] == 0:
            n += 1
            q = deque([(sv, su)]); lab[sv, su] = n
            pts = []
            touches = False
            while q:
                v, u = q.popleft(); pts.append((v, u))
                if v == 0 or u == 0 or v == H - 1 or u == W - 1:
                    touches = True
                for dv, du in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    a, b = v + dv, u + du
                    if 0 <= a < H and 0 <= b < W and sub[a, b] and lab[a, b] == 0:
                        lab[a, b] = n; q.append((a, b))
            if not touches and len(pts) < 5000:
                P = np.array(pts)
                regions.append((len(pts), P[:, 1].mean() + u0, P[:, 0].mean() + v0))
for a, u, v in sorted(regions, key=lambda r: (r[2], r[1])):
    if a >= 30:
        print(f"hole area {a:5d} px at ({u:.1f}, {v:.1f})")
