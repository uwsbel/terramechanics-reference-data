"""Fit the center of an open-circle symbol on the page image (helper for the FC-18 blind reading).

    python fit_circle.py <image> u v [u v ...]

For each rough center (u, v) it searches centers within +-10 px and radii 10 to 24 px for the ring
that is darkest relative to the ground just inside and just outside it (ring contrast), sampling 120
angles. Prints the best center, the radius, and the contrast; it also prints the best center when
the angles where other ink (lines through the circle) is found just outside the ring are dropped,
so a center pulled by a crossing line shows up as a difference between the two.
"""
import sys

import numpy as np
from PIL import Image


def bilinear(g, u, v):
    u0 = np.floor(u).astype(int); v0 = np.floor(v).astype(int)
    fu = u - u0; fv = v - v0
    return (g[v0, u0] * (1 - fu) * (1 - fv) + g[v0, u0 + 1] * fu * (1 - fv)
            + g[v0 + 1, u0] * (1 - fu) * fv + g[v0 + 1, u0 + 1] * fu * fv)


def fit(g, u, v, mask_outside=False):
    ang = np.linspace(0, 2 * np.pi, 120, endpoint=False)
    c, s = np.cos(ang), np.sin(ang)
    best = None
    for cu in np.arange(u - 10, u + 10.01, 0.5):
        for cv in np.arange(v - 10, v + 10.01, 0.5):
            for r in np.arange(10, 24.01, 0.5):
                ring = bilinear(g, cu + r * c, cv + r * s)
                ins = bilinear(g, cu + (r - 6) * c, cv + (r - 6) * s)
                out = bilinear(g, cu + (r + 6) * c, cv + (r + 6) * s)
                keep = np.ones_like(ring, dtype=bool)
                if mask_outside:
                    keep = (out < 0.5) & (ins < 0.5)   # drop angles crossed by other ink (darkness above one half)
                    if keep.sum() < 40:
                        continue
                score = ring[keep].mean() - 0.5 * (ins[keep].mean() + out[keep].mean())
                if best is None or score > best[0]:
                    best = (score, cu, cv, r, int(keep.sum()))
    return best


def main():
    img = sys.argv[1]
    g = 1.0 - np.asarray(Image.open(img).convert("L"), dtype=float) / 255.0   # darkness 0..1
    vals = [float(x) for x in sys.argv[2:]]
    for u, v in zip(vals[::2], vals[1::2]):
        a = fit(g, u, v)
        b = fit(g, u, v, mask_outside=True)
        print(f"guess ({u:.0f},{v:.0f}): all angles center ({a[1]:.1f},{a[2]:.1f}) r {a[3]:.1f} contrast {a[0]:.2f}; "
              f"clean angles center ({b[1]:.1f},{b[2]:.1f}) r {b[3]:.1f} contrast {b[0]:.2f} on {b[4]}/120 angles")


if __name__ == "__main__":
    main()
