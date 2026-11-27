"""List dark runs along rows of the plot, with grid lines masked, to see the curve structure.
Usage: python runs.py v0 v1 step [u0 u1]"""
import sys, numpy as np
from PIL import Image
im = np.array(Image.open('packet/p0088.png').convert('L'))
dark = im < 128
# grid lines (from plot_grid lines)
hrows = [1416.0,1618.5,1827.5,2034.5,2239.5,2446.0,2653.5,2861.0,3066.5,3274.5,3476.5,3689.0]
vcols = [541.0,749.5,958.0,1167.0,1369.0,1575.0,1782.0,1988.5]
mask = np.ones_like(dark)
for r in hrows:
    mask[int(r)-6:int(r)+7, :] = 0
for c in vcols:
    mask[:, int(c)-5:int(c)+6] = 0
ink = dark & mask.astype(bool)
v0, v1, step = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
u0 = int(sys.argv[4]) if len(sys.argv) > 4 else 530
u1 = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
for v in range(v0, v1 + 1, step):
    row = ink[v, u0:u1]
    runs = []
    inrun = False
    for i, d in enumerate(row):
        if d and not inrun:
            s = i; inrun = True
        elif not d and inrun:
            runs.append((s + u0, i - 1 + u0)); inrun = False
    if inrun: runs.append((s + u0, u1 - 1))
    print(v, ' '.join(f'{a}-{b}' for a, b in runs))
