"""Fit each drawn envelope line from its ink, then list the ink segments along the fitted line.
For every column u, the dark run nearest the predicted v (within `win` px) is taken if its vertical
thickness is line-like; the run centers are fitted by least squares with outlier rejection.
usage: linefit.py image"""
import sys, json
import numpy as np
from PIL import Image

img = sys.argv[1]
g = np.asarray(Image.open(img).convert("L")) < 128
# initial guesses: (name, u_ref, v_ref, slope dv/du)
LINES = [("L1_41.5", 1130, 2756, -0.881), ("L2_36.9", 1130, 2794.5, -0.74),
         ("L3_32.8", 1130, 2827.5, -0.647), ("L4_29", 1130, 2858.5, -0.556)]

def runs_at(u, v0, v1):
    col = g[v0:v1, u]
    idx = np.where(col)[0]
    out = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                out.append((s + v0, p + v0)); s = i
            p = i
        out.append((s + v0, p + v0))
    return out

res = {}
for name, ur, vr, sl in LINES:
    a, b = sl, vr - sl * ur          # v = a u + b
    for it in range(4):
        pts = []
        for u in range(1000, 2300):
            vp = a * u + b
            best = None
            for (t, bt) in runs_at(u, int(vp) - 20, int(vp) + 20):
                c, w = (t + bt) / 2, bt - t + 1
                if 9 <= w <= 18 and abs(c - vp) <= (8 if it == 0 else 3):
                    if best is None or abs(c - vp) < abs(best[0] - vp):
                        best = (c, w)
            if best:
                pts.append((u, best[0], best[1]))
        P = np.array(pts)
        a, b = np.polyfit(P[:, 0], P[:, 1], 1)
    r = P[:, 1] - (a * P[:, 0] + b)
    print(f"{name}: v = {a:.5f} u + {b:.2f}; n={len(P)} cols, rms {r.std():.2f} px, median run {np.median(P[:,2]):.0f} px, u {P[:,0].min():.0f}..{P[:,0].max():.0f}")
    res[name] = {"a": a, "b": b, "median_run": float(np.median(P[:, 2]))}
    # ink along the fitted line, every column from u 815 to 2300: dark at the predicted center +-2?
    segs, cur = [], None
    for u in range(815, 2300):
        vp = a * u + b
        lo, hi = int(round(vp - 2)), int(round(vp + 2))
        ink = g[lo:hi + 1, u].mean() >= 0.6
        if ink and cur is None:
            cur = [u, u]
        elif ink:
            cur[1] = u
        elif cur is not None:
            segs.append(tuple(cur)); cur = None
    if cur: segs.append(tuple(cur))
    print("   ink segments (u): " + ", ".join(f"{s}-{e}" for s, e in segs))
json.dump(res, open(sys.argv[2], "w"), indent=1) if len(sys.argv) > 2 else None
