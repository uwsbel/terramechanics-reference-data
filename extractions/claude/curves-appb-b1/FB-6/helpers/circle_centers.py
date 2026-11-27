"""Centres of the open-circle symbols of FB-6: from a rough centre, rays every 5 degrees find the inner
edge (first ink) and the outer edge (first white after the ring's ink); a circle is fitted to each set
by least squares, with rays whose radius is off the median by more than 3 px set aside (a line or a
tick crossing the ring or the hole). Prints both fits; the reader decides by eye."""
import math
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128


def fit_circle(P):
    x, y = P[:, 0], P[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    b = x ** 2 + y ** 2
    (cx, cy, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    r = math.sqrt(c + cx ** 2 + cy ** 2)
    res = np.hypot(x - cx, y - cy) - r
    return cx, cy, r, float(np.sqrt(np.mean(res ** 2)))


def edges(u0, v0, rmax=40):
    inner, outer = [], []
    for a in np.arange(0, 360, 5):
        du, dv = math.cos(math.radians(a)), math.sin(math.radians(a))
        rs = np.arange(0, rmax, 0.5)
        vals = [dark[int(round(v0 + r * dv)), int(round(u0 + r * du))] for r in rs]
        try:
            i = next(k for k, d in enumerate(vals) if d)
        except StopIteration:
            continue
        j = next((k for k in range(i, len(vals)) if not vals[k]), None)
        inner.append((a, rs[i]))
        if j is not None:
            outer.append((a, rs[j]))
    return inner, outer


def robust(u0, v0, pts):
    if not pts:
        return None
    r = np.array([p[1] for p in pts])
    med = np.median(r)
    keep = [p for p in pts if abs(p[1] - med) <= 3]
    P = np.array([(u0 + rr * math.cos(math.radians(a)), v0 + rr * math.sin(math.radians(a))) for a, rr in keep])
    if len(P) < 6:
        return None
    return fit_circle(P) + (len(keep), len(pts))


for arg in sys.argv[2:]:
    name, uv = arg.split("=")
    u0, v0 = (float(t) for t in uv.split(","))
    for it in range(3):   # re-centre on the inner fit
        inner, outer = edges(u0, v0)
        fi = robust(u0, v0, inner)
        if fi is None:
            break
        u0, v0 = fi[0], fi[1]
    inner, outer = edges(u0, v0)
    fi, fo = robust(u0, v0, inner), robust(u0, v0, outer)
    s = f"{name}: "
    if fi:
        s += f"inner centre ({fi[0]:.1f}, {fi[1]:.1f}) r {fi[2]:.1f} rms {fi[3]:.2f} rays {fi[4]}/{fi[5]}; "
    if fo:
        s += f"outer centre ({fo[0]:.1f}, {fo[1]:.1f}) r {fo[2]:.1f} rms {fo[3]:.2f} rays {fo[4]}/{fo[5]}"
    print(s)
