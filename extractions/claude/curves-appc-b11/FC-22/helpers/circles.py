"""Circle centres: rays cast from a seed inside the hole; the inner and outer edges of the ring along
each ray give points on the two boundaries; a least-squares circle is fitted to each. Rays that hit a
grid line or the curve (ring thicker than expected) are dropped."""
import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"), dtype=float)
def fit(P):
    P = np.array(P); A = np.c_[2 * P[:, 0], 2 * P[:, 1], np.ones(len(P))]
    b = (P ** 2).sum(1); c, *_ = np.linalg.lstsq(A, b, rcond=None)
    r = np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2); res = np.hypot(P[:, 0] - c[0], P[:, 1] - c[1]) - r
    return c[0], c[1], r, np.sqrt(np.mean(res ** 2))
def sample(u, v):
    u0, v0 = int(u), int(v); fu, fv = u - u0, v - v0
    return (g[v0, u0] * (1 - fu) * (1 - fv) + g[v0, u0 + 1] * fu * (1 - fv) + g[v0 + 1, u0] * (1 - fu) * fv + g[v0 + 1, u0 + 1] * fu * fv)
for seed in [(1689.5, 2010.0), (2342.0, 1584.0)]:
    inner, outer, used = [], [], []
    for ang in np.arange(0, 360, 5):
        d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))])
        prof = [sample(*(np.array(seed) + t * d)) for t in np.arange(0, 35, 0.25)]
        prof = np.array(prof); ts = np.arange(0, 35, 0.25)
        dk = prof < 128
        if not dk.any(): continue
        i0 = np.argmax(dk); rest = ~dk[i0:]
        if not rest.any(): continue
        i1 = i0 + np.argmax(rest)
        inner.append(seed + ts[i0] * d); outer.append(seed + ts[i1] * d); used.append((ang, ts[i0], ts[i1]))
    for nm, P in (("inner", inner), ("outer", outer)):
        print(seed, nm, "n", len(P), "fit u %.2f v %.2f r %.2f rms %.2f" % fit(P))
    print("   ray (angle, inner t, outer t):", " ".join(f"{a}:{x:.1f}/{y:.1f}" for a, x, y in used))
