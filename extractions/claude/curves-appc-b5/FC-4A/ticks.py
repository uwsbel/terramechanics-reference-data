import sys, numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")).astype(int)
d = g < 160
# left ticks: columns 900..915 (outside frame at ~918)
print("left-axis tick rows (u 900..914 dark count>=8):")
cnt = d[1100:3520, 900:915].sum(axis=1)
rows = np.where(cnt >= 8)[0] + 1100
runs=[]; 
for r in rows:
    if runs and r - runs[-1][-1] <= 1: runs[-1].append(r)
    else: runs.append([r])
for r in runs: print("  v=%.1f  (%d rows) u-span" % (np.mean(r), len(r)), np.where(d[int(np.mean(r)), 880:921])[0].min()+880)
# right side of left frame ticks inside? columns 925..940
print("inside ticks left (u 926..940):")
cnt = d[1100:3520, 926:940].sum(axis=1)
rows = np.where(cnt >= 8)[0] + 1100
runs=[]
for r in rows:
    if runs and r - runs[-1][-1] <= 1: runs[-1].append(r)
    else: runs.append([r])
for r in runs: print("  v=%.1f (%d rows)" % (np.mean(r), len(r)))
# bottom ticks: rows below frame bottom (~3490): 3495..3510 ; and above 3470..3484
for lo, hi in [(3496, 3512), (3468, 3482)]:
    print("bottom ticks rows %d..%d:" % (lo, hi))
    cnt = d[lo:hi, 880:2420].sum(axis=0)
    cols = np.where(cnt >= 8)[0] + 880
    runs=[]
    for c in cols:
        if runs and c - runs[-1][-1] <= 1: runs[-1].append(c)
        else: runs.append([c])
    for r in runs: print("  u=%.1f (%d cols)" % (np.mean(r), len(r)))
