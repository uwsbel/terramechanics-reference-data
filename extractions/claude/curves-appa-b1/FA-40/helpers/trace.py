"""Follow one drawn curve column by column and report its centre line, for reading trace samples.

usage: trace.py <tools_dir> <cal_dir> <image> --u0 U --v0 V --u1 U [--dark 160] [--win 30]
               [--targets 0.05,0.10,...] [--exclude u0:u1,u0:u1] [--dump file.csv]

For every column u from u0 to u1 the dark run nearest the predicted position (linear extrapolation of
the last good columns) is taken; its top and bottom edges give the centre (midpoint) and the vertical
thickness. A column whose run is much thicker than the median (a grid line crossing, a vertical grid
line, a label) is flagged and not used. At a target x value the centre is a local straight-line fit
of the good columns within +-8 px of the u where the piecewise map gives that x, iterated. Prints the
u, v of each target with the line's perpendicular thickness there.
"""
import argparse
import csv
import math
import sys

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("tools")
ap.add_argument("cal")
ap.add_argument("image")
ap.add_argument("--u0", type=int, required=True)
ap.add_argument("--v0", type=float, required=True)
ap.add_argument("--u1", type=int, required=True)
ap.add_argument("--dark", type=int, default=160)
ap.add_argument("--win", type=float, default=30)
ap.add_argument("--targets", default="")
ap.add_argument("--exclude", default="", help="u ranges a:b never used (vertical grid lines, symbols)")
ap.add_argument("--dump")
ap.add_argument("--half", type=int, default=8)
ap.add_argument("--open", type=int, default=0, help="square opening of the dark mask (odd size): removes lines thinner than this")
ap.add_argument("--tol", type=float, default=3, help="a run longer than the local median by more than this is a crossing")
ap.add_argument("--line", default="", help="a,b: a straight edge v = a + b u; every column is searched around it, no tracking")
ap.add_argument("--maxrun", type=int, default=28, help="a run longer than this is a crossing and does not steer the tracker")
a = ap.parse_args()
sys.path.insert(0, a.tools)
import calibrate_axes as ca

g = np.asarray(Image.open(a.image).convert("L"))
mask = g < a.dark
if a.open:
    from PIL import ImageFilter
    m = Image.fromarray((mask * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MinFilter(a.open)).filter(ImageFilter.MaxFilter(a.open))
    mask = np.asarray(m) > 127
cal, X, Y = ca.piecewise_maps(a.cal, a.image)
excl = []
for r in filter(None, a.exclude.split(",")):
    lo, hi = r.split(":")
    excl.append((int(lo), int(hi)))

step = 1 if a.u1 >= a.u0 else -1
cols = []   # (u, top, bottom, centre, thick, good)
hist = []
v_pred = a.v0
fixed = [float(x) for x in a.line.split(",")] if a.line else None
for u in range(a.u0, a.u1 + step, step):
    if fixed:
        v_pred = fixed[0] + fixed[1] * u
    col = mask[:, u]
    lo, hi = int(v_pred - a.win), int(v_pred + a.win)
    idx = np.where(col[lo:hi])[0] + lo
    if len(idx) == 0:
        cols.append((u, None, None, None, None, False))
        continue
    # runs
    runs, s, p = [], int(idx[0]), int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            runs.append((s, p)); s = i
        p = i
    runs.append((s, p))
    # extend a run touching the window edge
    ext = []
    for s, p in runs:
        while s > 0 and col[s - 1]:
            s -= 1
        while p < len(col) - 1 and col[p + 1]:
            p += 1
        ext.append((s, p))
    best = min(ext, key=lambda r: abs((r[0] + r[1]) / 2 - v_pred))
    c, t = (best[0] + best[1]) / 2, best[1] - best[0] + 1
    cols.append((u, best[0], best[1], c, t, True))
    if t > a.maxrun:
        v_pred = v_pred + (hist[-1][1] - hist[-2][1]) * step / max(1, abs(hist[-1][0] - hist[-2][0])) if len(hist) >= 2 else v_pred
        continue
    hist.append((u, c))
    if len(hist) >= 6:
        uu = np.array([h[0] for h in hist[-6:]]); vv = np.array([h[1] for h in hist[-6:]])
        k, b = np.polyfit(uu, vv, 1)
        v_pred = k * (u + step) + b
    else:
        v_pred = c

th = np.array([c[4] for c in cols if c[4] is not None])
med = float(np.median(th))
good = []
for (u, top, bot, c, t, ok) in cols:
    if not ok:
        continue
    bad = any(lo <= u <= hi for lo, hi in excl)
    good.append((u, top, bot, c, t, not bad))
# a run thicker than expected from its neighbours is a crossing: compare with the local median
arr = np.array([[r[0], r[3], r[4]] for r in good])
flags = []
for i, r in enumerate(good):
    j0, j1 = max(0, i - 15), min(len(good), i + 16)
    loc = np.median(arr[j0:j1, 2])
    flags.append(r[5] and r[4] <= loc + a.tol)
good = [r[:5] + (f,) for r, f in zip(good, flags)]
print(f"columns {len(cols)}, followed {len(good)}, used {sum(r[5] for r in good)}; median vertical run {med:.1f} px")
print(f"first column u={good[0][0]} centre v={good[0][3]:.1f} run {good[0][1]}..{good[0][2]}; "
      f"last column u={good[-1][0]} centre v={good[-1][3]:.1f} run {good[-1][1]}..{good[-1][2]}")

U = np.array([r[0] for r in good if r[5]], dtype=float)
C = np.array([r[3] for r in good if r[5]], dtype=float)
T = np.array([r[4] for r in good if r[5]], dtype=float)


def centre_at(u):
    m = np.abs(U - u) <= a.half
    if m.sum() < 4:
        return None, None, None, int(m.sum())
    k, b = np.polyfit(U[m], C[m], 1)
    ang = math.atan(abs(k))
    perp = float(np.median(T[m])) * math.cos(ang)
    return float(k * u + b), float(k), perp, int(m.sum())


if a.dump:
    with open(a.dump, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["u", "top", "bottom", "centre", "run", "used"])
        for r in good:
            w.writerow(r)

if a.targets:
    print("target,u,v,slope_dv_du,perp_thick,n_cols,x_check,y")
    for tgt in [float(x) for x in a.targets.split(",")]:
        # start from the affine map
        ax = cal["ax"]
        v = float(np.median(C))
        u = (tgt - ax[2] - ax[1] * v) / ax[0]
        for _ in range(30):
            vc, k, perp, n = centre_at(u)
            if vc is None:
                break
            xv = X.value(u, vc)[0]
            if abs(xv - tgt) < 1e-6:
                break
            # dx/du along the curve, numerically
            x2 = X.value(u + 1, vc + k)[0]
            u = u + (tgt - xv) / (x2 - xv)
        vc, k, perp, n = centre_at(u)
        if vc is None:
            print(f"{tgt},{u:.1f},NA,,,{n},,")
            continue
        print(f"{tgt},{u:.1f},{vc:.1f},{k:.3f},{perp:.1f},{n},{X.value(u, vc)[0]:.4f},{Y.value(u, vc)[0]:.3f}")
