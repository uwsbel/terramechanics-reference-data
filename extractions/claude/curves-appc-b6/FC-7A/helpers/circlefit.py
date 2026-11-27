"""Fit a circle symbol's ring by its inner edge: rays from a seed center, first dark pixel after
the white interior (skipping the center dot), Kasa least-squares fit with outlier rejection.
Also reports the center dot's centroid (dark pixels within r_dot of the fitted center).
Usage: circlefit.py image u0 v0 [dark] [r_start] [r_max]"""
import sys, math
import numpy as np
from PIL import Image

img = sys.argv[1]
u0, v0 = float(sys.argv[2]), float(sys.argv[3])
dark = int(sys.argv[4]) if len(sys.argv) > 4 else 160
r_start = float(sys.argv[5]) if len(sys.argv) > 5 else 8.0
r_max = float(sys.argv[6]) if len(sys.argv) > 6 else 30.0
g = np.asarray(Image.open(img).convert("L"))
D = g < dark

def ring_points(uc, vc):
    pin, pout = [], []
    for k in range(144):
        t = 2 * math.pi * k / 144
        cu, cv = math.cos(t), math.sin(t)
        r = r_start
        # skip dark (dot) until white
        while r < r_max and D[int(round(vc + r * cv)), int(round(uc + r * cu))]:
            r += 0.25
        while r < r_max and not D[int(round(vc + r * cv)), int(round(uc + r * cu))]:
            r += 0.25
        if r >= r_max:
            continue
        ri = r
        while r < r_max + 15 and D[int(round(vc + r * cv)), int(round(uc + r * cu))]:
            r += 0.25
        pin.append((uc + ri * cu, vc + ri * cv, ri, t))
        pout.append((uc + r * cu, vc + r * cv, r, t))
    return pin, pout

def kasa(pts):
    A = np.array([[p[0], p[1], 1.0] for p in pts])
    b = np.array([-(p[0] ** 2 + p[1] ** 2) for p in pts])
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    uc, vc = -c[0] / 2, -c[1] / 2
    R = math.sqrt(uc ** 2 + vc ** 2 - c[2])
    return uc, vc, R

uc, vc = u0, v0
for it in range(4):
    pin, pout = ring_points(uc, vc)
    pts = pin
    fu, fv, R = kasa(pts)
    for _ in range(5):
        res = [abs(math.hypot(p[0] - fu, p[1] - fv) - R) for p in pts]
        keep = [p for p, e in zip(pts, res) if e < 1.5]
        if len(keep) < 20:
            break
        fu, fv, R = kasa(keep)
        pts = keep
    uc, vc = fu, fv
res = [math.hypot(p[0] - uc, p[1] - vc) - R for p in pts]
print(f"inner-edge fit: center u {uc:.1f} v {vc:.1f}  R_in {R:.1f}  n {len(pts)}/{len(pin)}  rms {np.sqrt(np.mean(np.square(res))):.2f}")
# outer edge: use rays whose ring thickness is plausible (<= 9 px)
po = [q for p, q in zip(pin, pout) if q[2] - p[2] <= 9 and math.hypot(p[0]-uc, p[1]-vc) - R < 1.5]
if len(po) > 20:
    ou, ov, oR = kasa(po)
    for _ in range(5):
        res = [abs(math.hypot(p[0] - ou, p[1] - ov) - oR) for p in po]
        keep = [p for p, e in zip(po, res) if e < 1.5]
        if len(keep) < 15:
            break
        ou, ov, oR = kasa(keep)
        po = keep
    print(f"outer-edge fit: center u {ou:.1f} v {ov:.1f}  R_out {oR:.1f}  n {len(po)}")
# dot centroid
ys, xs = np.mgrid[int(vc) - 9:int(vc) + 10, int(uc) - 9:int(uc) + 10]
m = D[ys, xs] & (np.hypot(xs - uc, ys - vc) < min(9, R - 2))
if m.sum():
    print(f"dot centroid: u {xs[m].mean():.1f} v {ys[m].mean():.1f}  npx {m.sum()}")
