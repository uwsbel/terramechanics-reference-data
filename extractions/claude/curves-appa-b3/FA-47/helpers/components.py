"""List the connected dark components (8-connectivity) inside a box: bbox, size, centre.
Usage: components.py <image> u0 v0 u1 v1 [min_pixels]"""
import sys
import numpy as np
from PIL import Image

img = sys.argv[1]
u0, v0, u1, v1 = map(int, sys.argv[2:6])
mn = int(sys.argv[6]) if len(sys.argv) > 6 else 20
g = np.asarray(Image.open(img).convert("L"))[v0:v1, u0:u1] < 128
lab = np.zeros(g.shape, int)
n = 0
H, W = g.shape
for y in range(H):
    for x in range(W):
        if g[y, x] and not lab[y, x]:
            n += 1
            st = [(y, x)]; lab[y, x] = n; pts = []
            while st:
                cy, cx = st.pop(); pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and g[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; st.append((ny, nx))
            if len(pts) >= mn:
                P = np.array(pts)
                print(f"comp n={len(pts):5d} u {P[:,1].min()+u0:5d}-{P[:,1].max()+u0:5d} v {P[:,0].min()+v0:5d}-{P[:,0].max()+v0:5d}")
