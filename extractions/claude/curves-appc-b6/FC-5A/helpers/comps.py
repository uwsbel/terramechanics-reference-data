"""List connected ink components (8-connected) inside a box: bbox and pixel count.
usage: comps.py image u0 v0 u1 v1 [min_px]"""
import sys
import numpy as np
from PIL import Image
from collections import deque
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
u0, v0, u1, v1 = map(int, sys.argv[2:6]); mn = int(sys.argv[6]) if len(sys.argv) > 6 else 5
w = g[v0:v1, u0:u1]; seen = np.zeros_like(w, bool)
for y in range(w.shape[0]):
    for x in range(w.shape[1]):
        if w[y, x] and not seen[y, x]:
            q = deque([(y, x)]); seen[y, x] = True; pts = []
            while q:
                a, b = q.popleft(); pts.append((a, b))
                for da in (-1, 0, 1):
                    for db in (-1, 0, 1):
                        aa, bb = a + da, b + db
                        if 0 <= aa < w.shape[0] and 0 <= bb < w.shape[1] and w[aa, bb] and not seen[aa, bb]:
                            seen[aa, bb] = True; q.append((aa, bb))
            P = np.array(pts)
            if len(P) >= mn:
                print(f"n {len(P):5d}  u {P[:,1].min()+u0}-{P[:,1].max()+u0}  v {P[:,0].min()+v0}-{P[:,0].max()+v0}")
