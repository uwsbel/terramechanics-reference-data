"""Centers of hollow symbols (squares, circles) from their enclosed white hole.

For each approximate center (u, v) given on the command line as name:u:v, flood-fill the white
region containing it inside a 70 x 70 window; if the fill does not reach the window border it is
the symbol's hole. Reports the hole's centroid, its bounding box, and the outer ink extents of the
ring measured along the hole's central row and column (so a line touching the ring on a diagonal
does not move them).

usage: python markers.py <page.png> name:u:v [name:u:v ...]
"""
import sys
from collections import deque

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
H = 35
for spec in sys.argv[2:]:
    name, u, v = spec.split(":")
    u, v = int(u), int(v)
    win = g[v - H:v + H + 1, u - H:u + H + 1]
    seen = np.zeros_like(win, dtype=bool)
    q = deque([(H, H)])
    if win[H, H]:
        print(name, "start pixel is ink")
        continue
    seen[H, H] = True
    pts, touches = [], False
    while q:
        r, c = q.popleft()
        pts.append((r, c))
        if r in (0, 2 * H) or c in (0, 2 * H):
            touches = True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr <= 2 * H and 0 <= cc <= 2 * H and not seen[rr, cc] and not win[rr, cc]:
                seen[rr, cc] = True
                q.append((rr, cc))
    pts = np.array(pts)
    if touches:
        print(name, "hole not closed (fill reached the window border)")
        continue
    vc = pts[:, 0].mean() + v - H
    uc = pts[:, 1].mean() + u - H
    r0, r1 = pts[:, 0].min() + v - H, pts[:, 0].max() + v - H
    c0, c1 = pts[:, 1].min() + u - H, pts[:, 1].max() + u - H
    # outer ring extents along the central row/column of the hole
    rv, cu = int(round(vc)), int(round(uc))
    row = g[rv, :]
    col = g[:, cu]
    ul = c0 - 1
    while row[ul - 1]:
        ul -= 1
    ur = c1 + 1
    while row[ur + 1]:
        ur += 1
    vt = r0 - 1
    while col[vt - 1]:
        vt -= 1
    vb = r1 + 1
    while col[vb + 1]:
        vb += 1
    print(f"{name}: hole centroid u={uc:.1f} v={vc:.1f}; hole box u {c0}..{c1} v {r0}..{r1} "
          f"({c1 - c0 + 1}x{r1 - r0 + 1}, {len(pts)} px); outer along center row u {ul}..{ur} "
          f"(mid {(ul + ur) / 2:.1f}, w {ur - ul + 1}), along center col v {vt}..{vb} (mid {(vt + vb) / 2:.1f}, h {vb - vt + 1})")
