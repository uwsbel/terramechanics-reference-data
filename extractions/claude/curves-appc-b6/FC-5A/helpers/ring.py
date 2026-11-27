"""Center of a ring-shaped symbol (circle) from its connected ink component.
Seeds at a given dark pixel, flood-fills within a window, reports the bounding box, the center of
the bounding box and the centroid of the inner white hole.
usage: ring.py image u_seed v_seed half_window"""
import sys
import numpy as np
from PIL import Image
from collections import deque
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
us, vs, h = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
u0, v0 = us - h, vs - h
w = g[v0:vs + h + 1, u0:us + h + 1].copy()
# hole: white component containing the window center region nearest the seed... seed given as hole pixel
seen = np.zeros_like(w, bool)
q = deque([(h, h)]); seen[h, h] = True
assert not w[h, h], "seed must be a white pixel inside the ring"
pts = []
while q:
    y, x = q.popleft(); pts.append((y, x))
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < w.shape[0] and 0 <= xx < w.shape[1] and not seen[yy, xx] and not w[yy, xx]:
            seen[yy, xx] = True; q.append((yy, xx))
P = np.array(pts)
if len(P) > 0.5 * w.size:
    print("hole leaks out of the window"); sys.exit()
cy, cx = P.mean(0)
print(f"hole: {len(P)} px, bbox u {P[:,1].min()+u0}-{P[:,1].max()+u0} v {P[:,0].min()+v0}-{P[:,0].max()+v0}, centroid ({cx+u0:.1f}, {cy+v0:.1f})")
# outer extent along the row and column through the hole centroid
r = int(round(cy)); c = int(round(cx))
row = w[r]; col = w[:, c]
def extent(line, i):
    a = i
    while a > 0 and not line[a]: a -= 1
    while a > 0 and line[a - 1]: a -= 1
    b = i
    while b < len(line) - 1 and not line[b]: b += 1
    while b < len(line) - 1 and line[b + 1]: b += 1
    return a, b
a, b = extent(row, c); print(f"outer along row v={r+v0}: u {a+u0}-{b+u0}, mid {(a+b)/2+u0:.1f}")
a, b = extent(col, r); print(f"outer along col u={c+u0}: v {a+v0}-{b+v0}, mid {(a+b)/2+v0:.1f}")
