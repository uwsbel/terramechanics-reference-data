"""Connected components of ink inside a box: centroid, bounding box, area (to read dot centers).
usage: blobs.py u0 v0 u1 v1 [max_area]"""
import sys
import numpy as np
from inklib import G
u0, v0, u1, v1 = map(int, sys.argv[1:5]); mx = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
sub = G[v0:v1 + 1, u0:u1 + 1].copy()
lab = np.zeros(sub.shape, int); n = 0
for (i, j) in zip(*np.nonzero(sub)):
    if lab[i, j]: continue
    n += 1; st = [(i, j)]; lab[i, j] = n
    while st:
        a, b = st.pop()
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                x, y = a + da, b + db
                if 0 <= x < sub.shape[0] and 0 <= y < sub.shape[1] and sub[x, y] and not lab[x, y]:
                    lab[x, y] = n; st.append((x, y))
for k in range(1, n + 1):
    ii, jj = np.nonzero(lab == k)
    if len(ii) > mx or len(ii) < 4: continue
    print(f"blob u={jj.mean() + u0:.1f} v={ii.mean() + v0:.1f}  bbox u {jj.min() + u0}-{jj.max() + u0} v {ii.min() + v0}-{ii.max() + v0}  area {len(ii)}")
