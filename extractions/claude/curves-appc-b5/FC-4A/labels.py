import sys, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")).astype(int)
d = g < 160
def blobs_rows(u0,u1,v0,v1,gap=6):
    cnt = d[v0:v1,u0:u1].sum(axis=1)
    rows = np.where(cnt>0)[0]+v0
    runs=[]
    for r in rows:
        if runs and r-runs[-1][-1]<=gap: runs[-1].append(r)
        else: runs.append([r])
    return [(r[0],r[-1]) for r in runs]
print("y labels (u 760..880):")
for a,b in blobs_rows(760,880,1100,3520):
    cols = np.where(d[a:b+1,760:880].any(axis=0))[0]+760
    print("  v %d..%d center %.1f  u %d..%d" % (a,b,(a+b)/2, cols.min(), cols.max()))
def blobs_cols(u0,u1,v0,v1,gap=12):
    cnt = d[v0:v1,u0:u1].sum(axis=0)
    cols = np.where(cnt>0)[0]+u0
    runs=[]
    for c in cols:
        if runs and c-runs[-1][-1]<=gap: runs[-1].append(c)
        else: runs.append([c])
    return [(r[0],r[-1]) for r in runs]
print("x labels (v 3515..3570):")
for a,b in blobs_cols(820,2460,3515,3575):
    rows = np.where(d[3515:3575,a:b+1].any(axis=1))[0]+3515
    print("  u %d..%d center %.1f  v %d..%d" % (a,b,(a+b)/2, rows.min(), rows.max()))
