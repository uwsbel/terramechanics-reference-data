"""Dots of the dotted trace (lpt85, Four-Inch Footpad) of F2-48.

The grid bands are masked, the remaining ink is labelled (8-connected), and the dots are chained
from a seed dot in a clean stretch in both directions: the next dot is the nearest component of dot
size within 8 to 40 px ahead, within 35 degrees of the current direction (up to 75 px and 25
degrees when a dot is lost under a grid line). A dot is flagged `grid` when grid-line ink lies
within 2 px of it (it may be cut by the mask, so its centroid is not used for a sample), `solid`
when it touches the solid trace. Writes out/F2-48/dots.csv in drawing order (penetration 0 first).
"""
import csv
import math
from collections import deque
import numpy as np
from trace_lib import B, NV, NU, grid_mask, x_of, y_of

U0, V0, U1, V1 = 1050, 1330, 2275, 3762
gm = grid_mask()
rem = B & ~gm
sub = rem[V0:V1, U0:U1]
lab = np.zeros(sub.shape, np.int32)
comps = {}
nid = 0
H, W = sub.shape
for y, x in zip(*np.nonzero(sub)):
    if lab[y, x]:
        continue
    nid += 1
    q = deque([(y, x)])
    lab[y, x] = nid
    pts = []
    while q:
        cy, cx = q.popleft()
        pts.append((cy, cx))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = nid
                    q.append((ny, nx))
    p = np.array(pts)
    comps[nid] = dict(id=nid, area=len(p), u=p[:, 1].mean() + U0, v=p[:, 0].mean() + V0,
                      umin=p[:, 1].min() + U0, umax=p[:, 1].max() + U0,
                      vmin=p[:, 0].min() + V0, vmax=p[:, 0].max() + V0)
print(nid, "components")


def is_dot(c):
    return 8 <= c["area"] <= 400 and c["umax"] - c["umin"] <= 24 and c["vmax"] - c["vmin"] <= 24


cands = [c for c in comps.values() if is_dot(c)]


def chain(seed, d):
    out = []
    cur = seed
    used = {seed["id"]}
    while True:
        best = None
        for maxd, maxang in ((40, 35), (75, 25)):
            for c in cands:
                if c["id"] in used:
                    continue
                du, dv = c["u"] - cur["u"], c["v"] - cur["v"]
                r = math.hypot(du, dv)
                if r < 6 or r > maxd:
                    continue
                cosang = (du * d[0] + dv * d[1]) / r
                if cosang < math.cos(math.radians(maxang)):
                    continue
                if best is None or r < best[0]:
                    best = (r, c)
            if best:
                break
        if not best:
            return out
        r, c = best
        nd = ((c["u"] - cur["u"]) / r, (c["v"] - cur["v"]) / r)
        d = ((0.6 * d[0] + 0.4 * nd[0]), (0.6 * d[1] + 0.4 * nd[1]))
        n = math.hypot(*d)
        d = (d[0] / n, d[1] / n)
        used.add(c["id"])
        out.append(c)
        cur = c


def nearest(u, v):
    return min(cands, key=lambda c: math.hypot(c["u"] - u, c["v"] - v))


seed = nearest(2062, 3306)
s2 = nearest(2048, 3277)
d = (s2["u"] - seed["u"], s2["v"] - seed["v"])
n = math.hypot(*d)
d = (d[0] / n, d[1] / n)
up = chain(seed, d)                   # toward the end (penetration increasing, up the page)
down = chain(seed, (-d[0], -d[1]))    # toward the start
seq = list(reversed(down)) + [seed] + up


def flag(c):
    u0, u1 = int(c["umin"]) - 2, int(c["umax"]) + 3
    v0, v1 = int(c["vmin"]) - 2, int(c["vmax"]) + 3
    f = []
    if (gm[v0:v1, u0:u1] & B[v0:v1, u0:u1]).any():
        f.append("grid")
    return ";".join(f)


with open("out/F2-48/dots.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["order", "comp", "u", "v", "area", "du", "dv", "x", "y", "flag", "gap_prev"])
    prev = None
    for i, c in enumerate(seq, 1):
        gap = math.hypot(c["u"] - prev["u"], c["v"] - prev["v"]) if prev else 0
        w.writerow([i, c["id"], f"{c['u']:.1f}", f"{c['v']:.1f}", c["area"],
                    c["umax"] - c["umin"] + 1, c["vmax"] - c["vmin"] + 1,
                    f"{x_of(c['u'], c['v']):.3f}", f"{y_of(c['u'], c['v']):.1f}", flag(c), f"{gap:.1f}"])
        prev = c
print(len(seq), "dots chained; first", seq[0]["u"], seq[0]["v"], "last", seq[-1]["u"], seq[-1]["v"])
np.save("out/F2-48/dot-labels.npy", lab)
