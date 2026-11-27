"""List enclosed white regions (symbol holes) inside a box of the page image.

    python holes.py <image> u0 v0 u1 v1 [--dark 160] [--min 8]

A hole is a 4-connected white component that does not touch the box border. For each hole prints
its pixel bbox (u0..u1, v0..v1), area, area centroid and, for a triangle hole, the centroid of
the triangle spanned by the bbox (top/bottom flat side decided by which half holds more white).
Used only as a cross-check of marker centers read by eye on zoomed crops.
"""
import sys
from collections import deque
import numpy as np
from PIL import Image

def main():
    a = sys.argv[1:]
    img = a[0]; u0, v0, u1, v1 = map(int, a[1:5])
    dark = 160; mn = 8
    if "--dark" in a: dark = int(a[a.index("--dark") + 1])
    if "--min" in a: mn = int(a[a.index("--min") + 1])
    g = np.asarray(Image.open(img).convert("L"))[v0:v1, u0:u1]
    white = g >= dark
    H, W = white.shape
    lab = np.zeros((H, W), int); n = 0
    for y in range(H):
        for x in range(W):
            if white[y, x] and lab[y, x] == 0:
                n += 1; q = deque([(y, x)]); lab[y, x] = n; pts = []; border = False
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    if cy in (0, H - 1) or cx in (0, W - 1): border = True
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and white[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = n; q.append((ny, nx))
                if border or len(pts) < mn: continue
                p = np.array(pts)
                ys, xs = p[:, 0] + v0, p[:, 1] + u0
                top, bot, lef, rig = ys.min(), ys.max(), xs.min(), xs.max()
                mid = (top + bot) / 2
                upper = (ys < mid).sum(); lower = (ys > mid).sum()
                kind = "wider-at-bottom(tri-up?)" if lower > 1.3 * upper else ("wider-at-top(tri-down?)" if upper > 1.3 * lower else "symmetric")
                if lower > 1.3 * upper: tc = bot - (bot - top) / 3
                elif upper > 1.3 * lower: tc = top + (bot - top) / 3
                else: tc = mid
                print(f"hole u {lef}..{rig} v {top}..{bot} area {len(pts)} centroid ({xs.mean():.1f}, {ys.mean():.1f}) "
                      f"bbox-center ({(lef+rig)/2:.1f}, {mid:.1f}) {kind} tri-centroid-v {tc:.1f}")

if __name__ == "__main__":
    main()
