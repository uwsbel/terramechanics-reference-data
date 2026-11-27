"""Connected components of dark ink inside the plot frame of FC-3A (8-connectivity), helper."""
import sys, numpy as np
from collections import deque
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 160
u0, v0, u1, v1 = 924, 1468, 2370, 3198   # inside the frame lines
sub = g[v0:v1, u0:u1].copy()
H, W = sub.shape
lab = np.zeros(sub.shape, int); n = 0; comps = []
ys, xs = np.nonzero(sub)
for y, x in zip(ys, xs):
    if lab[y, x]: continue
    n += 1; q = deque([(y, x)]); lab[y, x] = n; pts = []
    while q:
        cy, cx = q.popleft(); pts.append((cy, cx))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n; q.append((ny, nx))
    p = np.array(pts)
    comps.append((n, len(p), u0 + p[:, 1].min(), v0 + p[:, 0].min(), u0 + p[:, 1].max(), v0 + p[:, 0].max()))
comps.sort(key=lambda c: (c[2], c[3]))
for c in comps:
    if c[1] >= 15:
        print("comp %4d  npx %6d  u %4d..%4d  v %4d..%4d" % (c[0], c[1], c[2], c[4], c[3], c[5]))
np.save(sys.argv[2], lab)
