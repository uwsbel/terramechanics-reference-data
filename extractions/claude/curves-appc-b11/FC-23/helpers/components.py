"""List the ink pieces (connected components, grid lines blanked) inside a page box: centroid, extent,
direction (principal axis slope dv/du), length along it, and mean thickness. Reading aid only.
usage: components.py <image> u0 v0 u1 v1 [min_px]"""
import json
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
CAL = json.loads((HERE.parent / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))


def blank_grid(dark, u0, v0, u1, v1, half=3):
    d = dark.copy()
    H, W = d.shape
    for l in CAL["vertical_lines"]:
        a, b = l["u_at_v0"], l["slope_du_dv"]
        for v in range(v0, v1):
            u = a + b * v
            lo, hi = int(round(u - half)), int(round(u + half))
            if hi >= u0 and lo < u1:
                d[v - v0, max(0, lo - u0):max(0, min(u1 - u0, hi - u0 + 1))] = False
    for l in CAL["horizontal_lines"]:
        c, s = l["v_at_u0"], l["slope_dv_du"]
        for u in range(u0, u1):
            v = c + s * u
            lo, hi = int(round(v - half)), int(round(v + half))
            if hi >= v0 and lo < v1:
                d[max(0, lo - v0):max(0, min(v1 - v0, hi - v0 + 1)), u - u0] = False
    return d


def label(d):
    H, W = d.shape
    lab = np.zeros((H, W), dtype=np.int32)
    n = 0
    comps = []
    ys, xs = np.nonzero(d)
    for y, x in zip(ys, xs):
        if lab[y, x]:
            continue
        n += 1
        q = deque([(y, x)])
        lab[y, x] = n
        pix = []
        while q:
            cy, cx = q.popleft()
            pix.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and d[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = n
                        q.append((ny, nx))
        comps.append(np.array(pix))
    return comps


if __name__ == "__main__":
    img = sys.argv[1]
    u0, v0, u1, v1 = map(int, sys.argv[2:6])
    mn = int(sys.argv[6]) if len(sys.argv) > 6 else 40
    g = np.asarray(Image.open(img).convert("L"))
    dark = g[v0:v1, u0:u1] < 150
    d = blank_grid(dark, u0, v0, u1, v1)
    comps = label(d)
    rows = []
    for p in comps:
        if len(p) < mn:
            continue
        v = p[:, 0] + v0
        u = p[:, 1] + u0
        cu, cv = u.mean(), v.mean()
        cov = np.cov(np.vstack([u - cu, v - cv]))
        w, vec = np.linalg.eigh(cov)
        e = vec[:, 1]
        slope = e[1] / e[0] if abs(e[0]) > 1e-9 else float("inf")
        along = (u - cu) * e[0] + (v - cv) * e[1]
        length = along.max() - along.min() + 1
        thick = len(p) / length
        rows.append((cu, cv, u.min(), u.max(), v.min(), v.max(), slope, length, thick, len(p)))
    rows.sort()
    print("cu,cv,umin,umax,vmin,vmax,slope,length,thick,npx")
    for r in rows:
        print(f"{r[0]:.0f},{r[1]:.0f},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]:.2f},{r[7]:.0f},{r[8]:.1f},{r[9]}")
