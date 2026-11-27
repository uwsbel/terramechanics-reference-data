"""Search the whole plot for ring-shaped marks of radius 14 to 19 px (a check that no circle was missed)."""
import sys, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"))
d = (g < 128).astype(np.uint8)
u0, v0, u1, v1 = 560, 1150, 2700, 3560
th = np.linspace(0, 2*np.pi, 72, endpoint=False)
best = []
for R in (14.5, 16.5, 18.5):
    du = np.round(R*np.cos(th)).astype(int); dv = np.round(R*np.sin(th)).astype(int)
    acc = np.zeros((v1-v0, u1-u0), float)
    for a, b in zip(du, dv):
        acc += d[v0+b:v1+b, u0+a:u1+a]
    acc /= len(th)
    # interior must be mostly white: sample r = 0.45R
    di = np.round(0.45*R*np.cos(th[::6])).astype(int); dvi = np.round(0.45*R*np.sin(th[::6])).astype(int)
    inner = np.zeros_like(acc)
    for a, b in zip(di, dvi):
        inner += d[v0+b:v1+b, u0+a:u1+a]
    inner /= len(di)
    score = acc - inner
    ys, xs = np.where(score > 0.6)
    for y, x in zip(ys, xs):
        best.append((score[y, x], u0+x, v0+y, R))
best.sort(reverse=True)
picked = []
for s, u, v, R in best:
    if all(np.hypot(u-pu, v-pv) > 25 for _, pu, pv, _ in picked):
        picked.append((s, u, v, R))
for s, u, v, R in sorted(picked, key=lambda p: p[1]):
    print(f"ring at ({u}, {v}) R {R} score {s:.2f}")
