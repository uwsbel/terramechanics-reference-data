import sys, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 160
# x ticks: below the bottom axis, rows 3218..3228
def runs(mask, off):
    idx = np.where(mask)[0]; out=[]
    if len(idx)==0: return out
    s=p=idx[0]
    for i in idx[1:]:
        if i!=p+1: out.append((off+(s+p)/2, p-s+1)); s=i
        p=i
    out.append((off+(s+p)/2, p-s+1)); return out
for v in (3215, 3220, 3225):
    print("x-tick row", v, runs(g[v, 880:2420], 880))
# y ticks: left of left axis, columns 895..908
for u in (898, 902, 905):
    print("y-tick col", u, runs(g[1400:3240, u], 1400))
