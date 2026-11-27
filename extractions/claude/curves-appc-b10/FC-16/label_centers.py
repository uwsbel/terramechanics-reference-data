import sys, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"))
def clusters(prof, gap):
    idx = np.where(prof > 0)[0]
    out = []
    if len(idx)==0: return out
    s = p = idx[0]
    for i in idx[1:]:
        if i - p > gap:
            out.append((s, p)); s = i
        p = i
    out.append((s, p)); return out
# x labels: rows 3535..3600
sub = g[3535:3600, 600:2560] < 128
for s, p in clusters(sub.sum(axis=0), 18):
    blk = sub[:, s:p+1]; rows = np.where(blk.any(axis=1))[0]
    print(f"x-label cluster u {600+s}..{600+p} center {600+(s+p)/2:.1f}  v {3535+rows.min()}..{3535+rows.max()}")
# y labels: cols 540..635
sub = g[1150:3560, 540:635] < 128
for s, p in clusters(sub.sum(axis=1), 12):
    blk = sub[s:p+1, :]; cols = np.where(blk.any(axis=0))[0]
    print(f"y-label cluster v {1150+s}..{1150+p} center {1150+(s+p)/2:.1f}  u {540+cols.min()}..{540+cols.max()}")
