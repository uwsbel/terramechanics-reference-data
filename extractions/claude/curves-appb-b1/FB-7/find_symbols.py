"""Locate plotted symbols on FB-7 (p0113.png) by template matching, as an aid to the by-eye reading.

Templates are cut from clean symbols on the page itself (bounding box centre = symbol centre):
open circle (1829.5, 1519.5), filled circle (1907.5, 1770.5), square with x (2101.5, 1646.0).
Score: fraction of template pixels that agree with the page (dark where the template is dark, white
where it is white), over the symbol's box plus a 2 px margin. A line crossing a symbol lowers the score
a little; local maxima above a threshold are listed with the page pixel of the symbol's box centre.
usage: python find_symbols.py <image>
"""
import sys

import numpy as np
from PIL import Image

BOX = (470, 840, 2760, 3945)   # plot interior and frame
TEMPLATES = {
    "open circle": (1810, 1849, 1499, 1540),
    "filled circle": (1888, 1927, 1750, 1791),
    "square with x": (2084, 2119, 1627, 1665),
}


def corr(img, tpl):
    """Sum over the template window of img*tpl for every placement (valid region), by FFT."""
    H, W = img.shape
    h, w = tpl.shape
    F = np.fft.rfft2(img, s=(H + h, W + w))
    T = np.fft.rfft2(tpl[::-1, ::-1], s=(H + h, W + w))
    c = np.fft.irfft2(F * T, s=(H + h, W + w))
    return c[h - 1:H, w - 1:W]


def main():
    g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
    u0, v0, u1, v1 = BOX
    img = np.where(g[v0:v1, u0:u1], 1.0, -1.0)
    found = []
    for name, (a, b, c, d) in TEMPLATES.items():
        m = 2
        t = np.where(g[c - m:d + m + 1, a - m:b + m + 1], 1.0, -1.0)
        n = t.size
        s = (corr(img, t) / n + 1) / 2          # agreement fraction
        h, w = t.shape
        # local maxima
        thr = 0.80
        ys, xs = np.where(s >= thr)
        order = np.argsort(-s[ys, xs])
        taken = []
        for i in order:
            y, x = ys[i], xs[i]
            if any(abs(y - yy) < 20 and abs(x - xx) < 20 for yy, xx in taken):
                continue
            taken.append((y, x))
            uc = u0 + x + m + (b - a) / 2
            vc = v0 + y + m + (d - c) / 2
            found.append((name, float(s[y, x]), uc, vc))
    for name, sc, uc, vc in sorted(found, key=lambda r: (r[3], r[2])):
        print(f"{name:14s} score {sc:.3f}  centre u {uc:7.1f} v {vc:7.1f}")


if __name__ == "__main__":
    main()
