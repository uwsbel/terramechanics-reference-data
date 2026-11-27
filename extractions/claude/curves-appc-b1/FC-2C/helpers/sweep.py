"""Ink sweep: list connected clusters of dark pixels in a box after removing grid lines, so that
no marker outside the region read by eye is missed. Pure NumPy (no SciPy in this env)."""
import sys
import numpy as np
from PIL import Image
from collections import deque
im = np.array(Image.open("packet/p0122.png").convert("L"))
u0, v0, u1, v1 = map(int, sys.argv[1:5])
band = sys.argv[5] if len(sys.argv) > 5 else None   # "vlo,vhi,umax" region already read
sub = (im[v0:v1, u0:u1] < 128).copy()
rows = sub.mean(axis=1) > 0.3; cols = sub.mean(axis=0) > 0.3
for r in np.where(rows)[0]: sub[max(0, r-5):r+6, :] = False
for c in np.where(cols)[0]: sub[:, max(0, c-5):c+6] = False
H, W = sub.shape
seen = np.zeros_like(sub, bool)
out = []
for y in range(H):
    for x in range(W):
        if sub[y, x] and not seen[y, x]:
            q = deque([(y, x)]); seen[y, x] = True; pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((ny, nx))
            if len(pts) >= 6:
                ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                out.append((u0 + (min(xs)+max(xs))/2, v0 + (min(ys)+max(ys))/2, max(xs)-min(xs)+1, max(ys)-min(ys)+1, len(pts)))
vlo, vhi, umax = (map(float, band.split(","))) if band else (None, None, None)
for cu, cv, w, h, n in sorted(out):
    flag = ""
    if band and (cv < vlo or cv > vhi or cu > umax): flag = "*"
    print(f"  u={cu:7.1f} v={cv:7.1f} w={w:3d} h={h:3d} px={n:4d} {flag}")
