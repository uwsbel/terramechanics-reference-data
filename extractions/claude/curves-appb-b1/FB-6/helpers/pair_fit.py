"""The overlapping pair of loose circles near (1959, 2674): the outer boundary of the pair's ink,
split into the upper arc (only the upper circle there) and the lower arc (only the lower circle),
each fitted with a circle; also the edges of the visible white crescents."""
import math, sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")); dark = g < 128
cu, cv = 1959.5, 2674.0
def fit(P):
    x, y = P[:, 0], P[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]; b = x ** 2 + y ** 2
    (a0, b0, c), *_ = np.linalg.lstsq(A, b, rcond=None); r = math.sqrt(c + a0 ** 2 + b0 ** 2)
    return a0, b0, r, float(np.sqrt(np.mean((np.hypot(x - a0, y - b0) - r) ** 2)))
def fit_fixed_r(P, r):
    best = None
    for a0 in np.arange(cu - 6, cu + 6, 0.1):
        for b0 in np.arange(P[:, 1].mean() - 30, P[:, 1].mean() + 30, 0.1):
            pass
    # Gauss-Newton on centre with fixed radius
    a0, b0 = P[:, 0].mean(), P[:, 1].mean()
    for _ in range(50):
        d = np.hypot(P[:, 0] - a0, P[:, 1] - b0); res = d - r
        J = np.c_[-(P[:, 0] - a0) / d, -(P[:, 1] - b0) / d]
        step, *_ = np.linalg.lstsq(J, -res, rcond=None); a0 += step[0]; b0 += step[1]
    return a0, b0, float(np.sqrt(np.mean(res ** 2)))
# outer boundary by rays from the pair's centre, from outside inward (first ink from radius 45)
pts = []
for a in np.arange(0, 360, 2):
    du, dv = math.cos(math.radians(a)), math.sin(math.radians(a))
    for r in np.arange(45, 0, -0.5):
        if dark[int(round(cv + r * dv)), int(round(cu + r * du))]:
            pts.append((a, cu + r * du, cv + r * dv)); break
P = np.array([(u, v) for a, u, v in pts])
up = P[P[:, 1] < 2659]; lo = P[P[:, 1] > 2690]
# the line enters at the lower left: drop lower-arc points left of the line's entry
lo = lo[~((lo[:, 0] < 1950) & (lo[:, 1] > 2692))]
print("upper arc", len(up), "free fit", [round(x, 2) for x in fit(up)], "fixed r 20.6", [round(x, 2) for x in fit_fixed_r(up, 20.6)])
print("lower arc", len(lo), "free fit", [round(x, 2) for x in fit(lo)], "fixed r 20.6", [round(x, 2) for x in fit_fixed_r(lo, 20.6)])
# crescents: white rows inside the pair
for v in range(2650, 2700):
    row = dark[v, 1938:1982]
    w = np.where(~row)[0]
    inner = [x + 1938 for x in w if 1944 < x + 1938 < 1976]
    if inner:
        print(v, min(inner), max(inner), len(inner))
