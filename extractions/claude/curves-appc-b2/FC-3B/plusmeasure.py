"""Locate plus signs: around (u,v) find columns whose vertical dark run (through v) is longer than
`minlen`; u = center of those columns, v = center of the run at the middle column."""
import sys
import numpy as np
from PIL import Image
g = np.array(Image.open("packet/p0124.png").convert("L")) < 128
def run_through(col, v, maxgap=1):
    if not col[v]: 
        return None
    a = v
    while a-1 >= 0 and col[a-1]: a -= 1
    b = v
    while b+1 < len(col) and col[b+1]: b += 1
    return a, b
for arg in sys.argv[1:]:
    u, v = map(int, arg.split(","))
    cols = []
    for uu in range(u-14, u+15):
        best = None
        for vv in range(v-6, v+7):
            r = run_through(g[:, uu], vv)
            if r and (best is None or r[1]-r[0] > best[1]-best[0]): best = r
        if best and 18 <= best[1]-best[0] <= 40:
            cols.append((uu, best))
    if not cols:
        print(f"({u},{v}): no bar found"); continue
    us = [c[0] for c in cols]
    # keep the contiguous group of columns nearest u
    groups = [[cols[0]]]
    for c in cols[1:]:
        if c[0] - groups[-1][-1][0] <= 1: groups[-1].append(c)
        else: groups.append([c])
    grp = min(groups, key=lambda gr: abs((gr[0][0]+gr[-1][0])/2 - u))
    uc = (grp[0][0] + grp[-1][0]) / 2
    mid = grp[len(grp)//2][1]
    vc = (mid[0] + mid[1]) / 2
    print(f"({u},{v}) -> bar columns {grp[0][0]}..{grp[-1][0]} (n={len(grp)}), run {mid[0]}..{mid[1]} => center ({uc},{vc})")
