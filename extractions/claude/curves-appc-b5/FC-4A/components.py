import numpy as np, json
from PIL import Image
from collections import deque
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
u0, v0, u1, v1 = 928, 1000, 2420, 3482   # inside left/bottom frame, include area above top frame
D = g[v0:v1, u0:u1] < 160
# blank the frame lines (top ~1160-1175, right ~2373-2384)
for u in range(u0, u1):
    vt = 1156.6 + 0.0048 * u
    D[int(vt - 6 - v0):int(vt + 7 - v0), u - u0] = False
D[:, 2372 - u0:2386 - u0] = False
seen = np.zeros_like(D)
comps = []
H, Wd = D.shape
ys, xs = np.nonzero(D)
for y, x in zip(ys, xs):
    if seen[y, x]: continue
    q = deque([(y, x)]); seen[y, x] = True; pix = []
    while q:
        cy, cx = q.popleft(); pix.append((cy, cx))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < Wd and D[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
    p = np.array(pix)
    comps.append((len(p), p[:, 1].min() + u0, p[:, 1].max() + u0, p[:, 0].min() + v0, p[:, 0].max() + v0))
comps.sort(key=lambda c: (c[3], c[1]))
for c in comps:
    if c[0] >= 3:
        print("n=%5d  u %4d..%4d  v %4d..%4d  size %dx%d" % (c[0], c[1], c[2], c[3], c[4], c[2]-c[1]+1, c[4]-c[3]+1))
