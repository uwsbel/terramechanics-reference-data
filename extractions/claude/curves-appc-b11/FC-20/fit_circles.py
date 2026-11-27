"""Fit open-circle centers on the page (reader's helper, FC-20).

For each seed (u, v) given by eye: rays are cast from the current center at 72 angles; along each
ray the first dark pixel (inner edge of the ring) and the next white pixel (outer edge) are found;
the ring's centerline point is their midpoint. Rays whose inner edge is not 10 to 20 px out (a grid
line or curve crossing the interior) or whose ring is thicker than 9 px (merged with a line) are
set aside. A circle is fitted to the midpoints by least squares (Kasa), and the procedure repeats
from the new center three times. Prints the center, radius, number of rays used, and the RMS of
the midpoints about the fitted circle. Pixel coordinates refer to the unrotated 300 dpi page.
"""
import sys
import numpy as np
from PIL import Image

img = np.asarray(Image.open(sys.argv[1]).convert("L"), dtype=float)
DARK = 128
ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)


def cast(u, v):
    pts, used = [], []
    for a in ang:
        c, s = np.cos(a), np.sin(a)
        inner = outer = None
        for r in np.arange(8, 30, 0.5):   # from 8 px: a grid line through the center is skipped
            uu, vv = int(round(u + r * c)), int(round(v + r * s))
            d = img[vv, uu] < DARK
            if inner is None and d:
                inner = r
            elif inner is not None and not d:
                outer = r
                break
        if inner is None or outer is None or not (10 <= inner <= 20) or outer - inner > 9:
            continue
        m = (inner + outer) / 2
        pts.append((u + m * c, v + m * s))
        used.append(round(np.degrees(a)))
    return np.array(pts), used


def kasa(P):
    x, y = P[:, 0], P[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    b = x ** 2 + y ** 2
    (cx, cy, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    r = np.sqrt(c + cx ** 2 + cy ** 2)
    return cx, cy, r


for s in sys.argv[2:]:
    u, v = (float(x) for x in s.split(","))
    for _ in range(4):
        P, used = cast(u, v)
        u, v, r = kasa(P)
    res = np.hypot(P[:, 0] - u, P[:, 1] - v) - r
    print(f"seed {s} -> center ({u:.1f},{v:.1f}) radius {r:.1f}; rays used {len(P)}/72; rms {np.sqrt(np.mean(res ** 2)):.2f} px")
