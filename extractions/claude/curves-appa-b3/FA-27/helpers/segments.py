"""Find the ink of the plotted lines of a density chart: remove the grid (pixels in long horizontal or
vertical runs), label the remaining ink, and list each component with a straight-line fit v = a + b u.
Usage: segments.py <image> u0 v0 u1 v1 [min_pixels] [hrun] [vrun]
Prints one row per component: id, n, u_min, u_max, v at u_min and u_max from the fit, slope, rms."""
import sys
import numpy as np
from PIL import Image

img = sys.argv[1]
u0, v0, u1, v1 = map(int, sys.argv[2:6])
min_pix = int(sys.argv[6]) if len(sys.argv) > 6 else 40
HRUN = int(sys.argv[7]) if len(sys.argv) > 7 else 45
VRUN = int(sys.argv[8]) if len(sys.argv) > 8 else 30
g = np.asarray(Image.open(img).convert("L"))[v0:v1, u0:u1] < 128


def long_runs(mask, axis, L):
    """Boolean array of pixels that belong to a run of length >= L along `axis`."""
    m = mask if axis == 1 else mask.T
    out = np.zeros_like(m)
    for i in range(m.shape[0]):
        row = m[i]
        d = np.diff(np.concatenate([[0], row.astype(int), [0]]))
        st, en = np.where(d == 1)[0], np.where(d == -1)[0]
        for s, e in zip(st, en):
            if e - s >= L:
                out[i, s:e] = True
    return out if axis == 1 else out.T


grid = long_runs(g, 1, HRUN) | long_runs(g, 0, VRUN)
# grow the grid mask by one pixel across so the halo of a grid line does not survive as a sliver
gm = grid.copy()
gm[1:, :] |= grid[:-1, :]
gm[:-1, :] |= grid[1:, :]
gm[:, 1:] |= grid[:, :-1]
gm[:, :-1] |= grid[:, 1:]
ink = g & ~gm
np.save(sys.argv[1].replace("\\", "/").split("/")[-1] + ".ink.npy", ink) if False else None

# connected components (4-connectivity), iterative flood fill
lab = np.zeros(ink.shape, dtype=np.int32)
n = 0
H, W = ink.shape
comps = []
for y in range(H):
    for x in range(W):
        if ink[y, x] and lab[y, x] == 0:
            n += 1
            stack = [(y, x)]
            lab[y, x] = n
            pts = []
            while stack:
                cy, cx = stack.pop()
                pts.append((cy, cx))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and ink[ny, nx] and lab[ny, nx] == 0:
                        lab[ny, nx] = n
                        stack.append((ny, nx))
            comps.append(pts)
print("id,n,u_min,u_max,v_at_umin,v_at_umax,slope,rms,height")
k = 0
for pts in comps:
    if len(pts) < min_pix:
        continue
    P = np.array(pts, dtype=float)
    vv, uu = P[:, 0] + v0, P[:, 1] + u0
    if np.ptp(uu) < 8:
        continue
    b, a = np.polyfit(uu, vv, 1)
    rms = float(np.sqrt(np.mean((vv - (a + b * uu)) ** 2)))
    k += 1
    print(f"{k},{len(pts)},{uu.min():.0f},{uu.max():.0f},{a + b * uu.min():.1f},{a + b * uu.max():.1f},{b:.4f},{rms:.2f},{np.ptp(vv)+1:.0f}")
