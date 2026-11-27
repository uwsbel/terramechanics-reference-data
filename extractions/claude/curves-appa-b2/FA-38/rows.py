import sys, numpy as np
from PIL import Image
img, u0, u1, v0, v1, thr = sys.argv[1], *map(int, sys.argv[2:6]), float(sys.argv[6])
g = np.asarray(Image.open(img).convert("L"))
sub = g[v0:v1, u0:u1] < 128
f = sub.mean(axis=1)
idx = np.where(f >= thr)[0]
runs=[]
if len(idx):
    s=p=idx[0]
    for i in idx[1:]:
        if i!=p+1:
            runs.append((s,p)); s=i
        p=i
    runs.append((s,p))
for s,p in runs:
    w = f[s:p+1]
    c = (np.arange(s,p+1)*w).sum()/w.sum()+v0
    print(f"v {c:8.1f}  width {p-s+1:2d}  maxfrac {w.max():.2f}")
