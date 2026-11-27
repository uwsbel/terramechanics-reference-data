"""Reader helper: sample a drawn straight line (a failure envelope) on the page.
For a column u the line's centre is the midpoint of the dark run that crosses the predicted line (bilevel
page: centre = (first + last dark row) / 2); a run much thicker than the line's median (a grid line, a
symbol touching it) or missing (a gap) is reported and not used. A sample at u is the local straight-line
fit of the centres of columns u-h..u+h evaluated at u. Targets in normal stress are converted to u with
the tool's own piecewise map (bisection along the line).
usage: trace.py <tools_dir> <cal_dir> <image> --p0 u v --p1 u v [--xs 500,1000,...] [--us u1,u2] [--h 6]
       [--profile step]"""
import argparse
import sys

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("tools")
ap.add_argument("cal")
ap.add_argument("image")
ap.add_argument("--p0", nargs=2, type=float, required=True)
ap.add_argument("--p1", nargs=2, type=float, required=True)
ap.add_argument("--xs", default="")
ap.add_argument("--us", default="")
ap.add_argument("--h", type=int, default=6)
ap.add_argument("--win", type=float, default=12)
ap.add_argument("--profile", type=int, default=0)
a = ap.parse_args()
sys.path.insert(0, a.tools)
import calibrate_axes as ca  # noqa: E402

cal, X, Y = ca.piecewise_maps(a.cal, a.image)
g = np.asarray(Image.open(a.image).convert("L")) < 128
(u0, v0), (u1, v1) = a.p0, a.p1
k = (v1 - v0) / (u1 - u0)


def run_at(u, vp):
    col = g[:, int(u)]
    vi = int(round(vp))
    best = None
    for c in range(vi - int(a.win), vi + int(a.win) + 1):
        if 0 <= c < len(col) and col[c]:
            lo = c
            while lo > 0 and col[lo - 1]:
                lo -= 1
            hi = c
            while hi < len(col) - 1 and col[hi + 1]:
                hi += 1
            d = abs((lo + hi) / 2 - vp)
            if best is None or d < best[0]:
                best = (d, lo, hi)
    return None if best is None else (best[1], best[2])


# global fit to refine the predicted line
us = np.arange(min(u0, u1), max(u0, u1) + 1, 3)
pts = []
for u in us:
    r = run_at(u, v0 + k * (u - u0))
    if r:
        pts.append((u, (r[0] + r[1]) / 2, r[1] - r[0] + 1))
P = np.array(pts)
med = np.median(P[:, 2])
ok = (P[:, 2] >= med - 3) & (P[:, 2] <= med + 3)
c1, c0 = np.polyfit(P[ok, 0], P[ok, 1], 1)
res = P[ok, 1] - (c0 + c1 * P[ok, 0])
print(f"global fit: v = {c0:.2f} + {c1:.5f} u over {ok.sum()} cols (of {len(P)}); median vertical run {med:.1f} px; "
      f"centre residual rms {np.sqrt(np.mean(res**2)):.2f} px; perpendicular thickness {med / np.sqrt(1 + c1**2):.1f} px")
if a.profile:
    for u in np.arange(min(u0, u1), max(u0, u1) + 1, a.profile):
        r = run_at(u, c0 + c1 * u)
        print(f"  profile u {u:.0f}: " + ("no run" if not r else f"v {r[0]}..{r[1]} centre {(r[0]+r[1])/2:.1f} thick {r[1]-r[0]+1} dev {(r[0]+r[1])/2 - (c0 + c1*u):+.1f}"))


def local(u):
    cs = []
    for uu in range(int(round(u)) - a.h, int(round(u)) + a.h + 1):
        r = run_at(uu, c0 + c1 * uu)
        if r and abs((r[1] - r[0] + 1) - med) <= 3:
            cs.append((uu, (r[0] + r[1]) / 2, r[1] - r[0] + 1))
    if len(cs) < 4:
        return None
    C = np.array(cs)
    q1, q0 = np.polyfit(C[:, 0], C[:, 1], 1)
    return q0 + q1 * u, len(cs), float(np.median(C[:, 2])), float(np.sqrt(np.mean((C[:, 1] - (q0 + q1 * C[:, 0]))**2)))


def x_at(u):
    return X.value(u, c0 + c1 * u)[0]


def u_for_x(xt):
    lo, hi = min(u0, u1) - 200, max(u0, u1) + 200
    for _ in range(60):
        m = (lo + hi) / 2
        if x_at(m) < xt:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


targets = [("x", float(s)) for s in a.xs.split(",") if s] + [("u", float(s)) for s in a.us.split(",") if s]
print("target,u,v_local,v_global,n_cols,vert_run,fit_rms,x_piecewise,y_piecewise")
for kind, t in targets:
    u = u_for_x(t) if kind == "x" else t
    L = local(u)
    vg = c0 + c1 * u
    if L is None:
        print(f"{kind}={t:g},{u:.1f},NA,{vg:.1f},,,,")
        continue
    v, n, th, rms = L
    xv = X.value(u, v)[0]
    yv = Y.value(u, v)[0]
    print(f"{kind}={t:g},{u:.1f},{v:.1f},{vg:.1f},{n},{th:.0f},{rms:.2f},{xv:.1f},{yv:.1f}")
