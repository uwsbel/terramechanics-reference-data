import sys, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"))
mode = sys.argv[2]  # 'rows' -> horizontal lines in strip u0..u1 over v range; 'cols'
a0, a1, b0, b1 = map(int, sys.argv[3:7])
thr = float(sys.argv[7]) if len(sys.argv) > 7 else 0.5
dark = g < 160
if mode == "rows":
    sub = dark[b0:b1, a0:a1]; frac = sub.mean(axis=1); off = b0
else:
    sub = dark[a0:a1, b0:b1]; frac = sub.mean(axis=0); off = b0
idx = np.where(frac >= thr)[0]
runs = []
if len(idx):
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            runs.append((s, p)); s = i
        p = i
    runs.append((s, p))
for s, p in runs:
    seg = frac[s:p+1]
    c = (np.arange(s, p+1) * seg).sum() / seg.sum() + off
    print(f"{c:8.1f}  w={p-s+1:2d}  max={seg.max():.2f}")
