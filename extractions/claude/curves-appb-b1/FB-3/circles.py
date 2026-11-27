"""Circle centres of FB-3 markers: (1) the enclosed white hole of each clean circle, flood-filled from a
seed, its centroid and a circle fitted to its boundary; (2) the outer edge fitted on the arcs not
touched by a line. Prints the radii so the ring model of the overlapping symbols can use them."""
import sys
import numpy as np
from PIL import Image
from collections import deque
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128

def flood(seed, lim=40):
    u0, v0 = seed
    seen = set(); q = deque([(u0, v0)])
    while q:
        u, v = q.popleft()
        if (u, v) in seen or g[v, u] or abs(u - u0) > lim or abs(v - v0) > lim:
            continue
        seen.add((u, v))
        q.extend([(u + 1, v), (u - 1, v), (u, v + 1), (u, v - 1)])
    return np.array(sorted(seen))

def fit_circle(pts):
    x, y = pts[:, 0].astype(float), pts[:, 1].astype(float)
    A = np.c_[2 * x, 2 * y, np.ones_like(x)]
    b = x ** 2 + y ** 2
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    r = np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)
    res = np.hypot(x - c[0], y - c[1]) - r
    return c[0], c[1], r, np.sqrt(np.mean(res ** 2))

def hole(seed):
    H = flood(seed)
    S = set(map(tuple, H))
    # boundary: hole pixels with an ink 4-neighbour; the edge is half a pixel outside
    bd = []
    for u, v in H:
        for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if g[v + dv, u + du]:
                bd.append((u + du * 0.5, v + dv * 0.5))
    bd = np.array(bd)
    cu, cv = H[:, 0].mean(), H[:, 1].mean()
    fu, fv, r, rms = fit_circle(bd)
    return len(H), (cu, cv), (fu, fv, r, rms), (H[:, 0].min(), H[:, 0].max(), H[:, 1].min(), H[:, 1].max())

seeds = {"dense 2.3 upper": (875, 2972), "dense 2.3 lower": (863, 3126), "dense 4.9 blob": (1236, 1991),
         "dense 9.9 upper": (1938, 886), "dense 9.9 lower": (1937, 933), "loose 4 C (lowest)": (1105, 3852),
         "loose 6": (1385, 3232), "loose 13.6 upper": (2443, 2204), "loose 13.6 lower": (2445, 2285),
         "loose 4 A (upper)": (1103, 3763), "loose 4 B (left)": (1092, 3793)}
for k, s in seeds.items():
    n, c, f, ext = hole(s)
    print(f"{k:20s} hole px {n:4d} centroid ({c[0]:.2f}, {c[1]:.2f})  fit ({f[0]:.2f}, {f[1]:.2f}) r {f[2]:.2f} rms {f[3]:.2f}  u {ext[0]}-{ext[1]} v {ext[2]}-{ext[3]}")
