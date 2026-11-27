"""Measure the connected ink component nearest a guessed point: bbox, size, centroid.
Used to size the symbol templates from clean, isolated markers (lower panel)."""
import sys, numpy as np
from PIL import Image
im = np.array(Image.open(sys.argv[1]).convert("L")) < 128
def cc_at(u, v, r=20):
    # flood fill from the nearest ink pixel within r
    H, W = im.shape
    v0, v1, u0, u1 = max(v-r,0), min(v+r,H), max(u-r,0), min(u+r,W)
    sub = im[v0:v1, u0:u1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: return None
    d = (ys+v0-v)**2 + (xs+u0-u)**2
    k = np.argmin(d); sv, su = ys[k]+v0, xs[k]+u0
    seen = np.zeros_like(im); stack = [(sv, su)]; seen[sv, su] = True; pts = []
    while stack:
        y, x = stack.pop(); pts.append((y, x))
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy, xx = y+dy, x+dx
            if 0 <= yy < H and 0 <= xx < W and im[yy, xx] and not seen[yy, xx]:
                seen[yy, xx] = True; stack.append((yy, xx))
        if len(pts) > 5000: break
    pts = np.array(pts)
    return pts
for arg in sys.argv[2:]:
    name, u, v = arg.split(":"); u, v = int(u), int(v)
    p = cc_at(u, v)
    if p is None: print(name, "no ink"); continue
    vmin, umin = p.min(0); vmax, umax = p.max(0)
    print(f"{name}: n={len(p)} u {umin}..{umax} (w {umax-umin+1}) v {vmin}..{vmax} (h {vmax-vmin+1}) bbox center ({(umin+umax)/2:.1f},{(vmin+vmax)/2:.1f}) centroid ({p[:,1].mean():.1f},{p[:,0].mean():.1f})")
