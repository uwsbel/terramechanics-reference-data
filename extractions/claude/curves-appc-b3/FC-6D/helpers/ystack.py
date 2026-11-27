"""Aid for the lower panel's stacked symbols (a triangle-down with a plus right below it). For a
window u0,v0,u1,v1 that holds one stack and nothing else, print per row the dark count and the
leftmost/rightmost dark column, then a summary: the triangle's top edge (first row with a run
of >= 15 dark pixels), its width there (outer extent over the first 5 rows), the plus's
horizontal bar (the row band below top+22 with the largest count, rows >= 70 percent of that
maximum) and its lower arm (dark columns in the rows below the bar). The reader checks every
summary against the printed rows and the zoomed crop. Threshold 128.

usage: ystack.py <image> u0,v0,u1,v1 [--rows]
"""
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
u0, v0, u1, v1 = [int(x) for x in sys.argv[2].split(",")]
sub = g[v0:v1 + 1, u0:u1 + 1]
cnt = sub.sum(axis=1)
if "--rows" in sys.argv:
    for i, r in enumerate(sub):
        idx = np.where(r)[0]
        if len(idx):
            print(f"{v0+i:5d} n={cnt[i]:3d} u {idx.min()+u0}..{idx.max()+u0}  " + "".join("#" if c else "." for c in r))
top = next(i for i in range(len(cnt)) if cnt[i] >= 15)
rows5 = sub[top:top + 5]
cols = np.where(rows5.any(axis=0))[0]
wl, wr = cols.min() + u0, cols.max() + u0
below = range(top + 22, len(cnt))
m = max(cnt[i] for i in below)
bar = [i for i in below if cnt[i] >= 0.7 * m]
bar_lo, bar_hi = min(bar), max(bar)
arm = sub[bar_hi + 1:]
armcols = np.where(arm.sum(axis=0) >= 3)[0]
print(f"{sys.argv[2]}: tri top v {top+v0}, width u {wl}..{wr} (c {(wl+wr)/2:.1f}, w {wr-wl+1}); "
      f"plus bar v {bar_lo+v0}..{bar_hi+v0} (c {(bar_lo+bar_hi)/2+v0:.1f}); "
      f"lower arm u {armcols.min()+u0 if len(armcols) else None}..{armcols.max()+u0 if len(armcols) else None}")
