"""Geometry of the isolated open circles of FB-4: centre from the hole (flood fill of the white
interior from a seed), and the inner and outer radius of the ring along 72 rays from that centre
(rays that run into an attached line are recognised by an outer radius far above the median)."""
import sys
from collections import deque
import numpy as np
from PIL import Image

D = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
seeds = [(771, 3210), (956, 2578), (1284, 1832), (1285, 1899), (1295, 2474), (1300, 2154), (1947, 1840), (1948, 2061)]


def hole(seed, lim=20):
    su, sv = seed
    seen = set()
    q = deque([(su, sv)])
    while q:
        u, v = q.popleft()
        if (u, v) in seen or D[v, u] or abs(u - su) > lim or abs(v - sv) > lim:
            continue
        seen.add((u, v))
        q.extend([(u + 1, v), (u - 1, v), (u, v + 1), (u, v - 1)])
    P = np.array(list(seen), float)
    return P


for s in seeds:
    P = hole(s)
    cu, cv = P[:, 0].mean(), P[:, 1].mean()
    w = P[:, 0].max() - P[:, 0].min() + 1
    h = P[:, 1].max() - P[:, 1].min() + 1
    rin, rout = [], []
    for a in np.linspace(0, 2 * np.pi, 72, endpoint=False):
        ca, sa = np.cos(a), np.sin(a)
        r = 0.0
        while not D[int(round(cv + r * sa)), int(round(cu + r * ca))]:
            r += 0.25
        r_in = r
        while D[int(round(cv + r * sa)), int(round(cu + r * ca))] and r < 40:
            r += 0.25
        rin.append(r_in); rout.append(r)
    rin, rout = np.array(rin), np.array(rout)
    ok = rout < np.median(rout) + 3
    # outer-edge centre: fit a circle to the outer edge points on clean rays
    ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)[ok]
    ex, ey = cu + rout[ok] * np.cos(ang), cv + rout[ok] * np.sin(ang)
    A = np.c_[2 * ex, 2 * ey, np.ones(len(ex))]
    b = ex ** 2 + ey ** 2
    (xc, yc, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    R = np.sqrt(c + xc ** 2 + yc ** 2)
    print(f"seed {s}: hole centroid ({cu:.2f}, {cv:.2f}) hole {w:.0f}x{h:.0f} px, n={len(P)}; "
          f"r_in median {np.median(rin):.2f}, r_out median {np.median(rout[ok]):.2f} ({ok.sum()}/72 clean rays); "
          f"outer-edge circle ({xc:.2f}, {yc:.2f}) R {R:.2f}")
