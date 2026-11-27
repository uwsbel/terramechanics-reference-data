"""Connected components (8-neighbour) of the ink of an image inside a box; prints one row per
component: id, area, centroid u v, bbox u0 v0 u1 v1, and the principal axis length and width.

usage: components.py <image> <u0> <v0> <u1> <v1> <out.csv>
"""
import csv
import sys
from collections import deque

import numpy as np
from PIL import Image


def components(ink):
    h, w = ink.shape
    lab = np.zeros((h, w), dtype=np.int32)
    comps = []
    n = 0
    ys, xs = np.nonzero(ink)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1
        q = deque([(y0, x0)])
        lab[y0, x0] = n
        pts = []
        while q:
            y, x = q.popleft()
            pts.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and ink[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n
                        q.append((yy, xx))
        comps.append(np.array(pts))
    return lab, comps


def main():
    img, u0, v0, u1, v1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
    g = np.asarray(Image.open(img).convert("L"))[v0:v1, u0:u1] < 128
    lab, comps = components(g)
    with open(out, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["id", "area", "cu", "cv", "bu0", "bv0", "bu1", "bv1", "length", "width"])
        for i, P in enumerate(comps, 1):
            vv, uu = P[:, 0] + v0, P[:, 1] + u0
            cu, cv = uu.mean(), vv.mean()
            if len(P) >= 3:
                C = np.cov(np.vstack([uu - cu, vv - cv]))
                ev = np.sort(np.linalg.eigvalsh(C))[::-1]
                length, width = 4 * np.sqrt(max(ev[0], 0)), 4 * np.sqrt(max(ev[1], 0))
            else:
                length = width = 0.0
            wr.writerow([i, len(P), round(cu, 2), round(cv, 2), uu.min(), vv.min(), uu.max(), vv.max(),
                         round(length, 1), round(width, 1)])
    print(f"{len(comps)} components written to {out}")


if __name__ == "__main__":
    main()
