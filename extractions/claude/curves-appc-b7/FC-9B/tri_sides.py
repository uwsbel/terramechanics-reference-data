"""Reader helper: centroid of an upright triangle symbol reconstructed from its sides (rule 8).
In each row between the apex region and the base, the leftmost and rightmost dark runs inside the box
(after blanking mask boxes: grid lines, the fitted line, stray ink) are the left and right side strokes;
their centres are fitted with straight lines u = a + b v. The base centreline is the mean row of the
base run (rows where the ink spans most of the symbol's width). Vertices: the two side lines' crossing
(apex) and their crossings with the base centreline; centroid = mean of the vertices.
usage: tri_sides.py <image> u0 v0 u1 v1 --rows r0 r1 --base b0 b1 [--lrows r0 r1] [--rrows r0 r1] [--mask u0 v0 u1 v1]...
  --rows: the rows used for the side fits; --base: the rows of the base stroke"""
import sys

import numpy as np
from PIL import Image

a = sys.argv[1:]
img = a[0]
u0, v0, u1, v1 = map(int, a[1:5])
rows = base = lrows = rrows = None
masks = []
i = 5
while i < len(a):
    if a[i] == "--rows":
        rows = (int(a[i + 1]), int(a[i + 2])); i += 3
    elif a[i] == "--lrows":
        lrows = (int(a[i + 1]), int(a[i + 2])); i += 3
    elif a[i] == "--rrows":
        rrows = (int(a[i + 1]), int(a[i + 2])); i += 3
    elif a[i] == "--base":
        base = (int(a[i + 1]), int(a[i + 2])); i += 3
    elif a[i] == "--mask":
        masks.append(tuple(map(int, a[i + 1:i + 5]))); i += 5
    else:
        raise SystemExit("bad args")
g = np.asarray(Image.open(img).convert("L")) < 128
b = g.copy()
for (m0, n0, m1, n1) in masks:
    b[n0:n1, m0:m1] = False


def runs(v):  # noqa: E302
    r = b[v, u0:u1]
    idx = np.nonzero(r)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for k in idx[1:]:
        if k != p + 1:
            out.append((s + u0, p + u0)); s = k
        p = k
    out.append((s + u0, p + u0))
    return out


if base is None or rows is None:
    # automatic: base rows = the bottom rows whose longest run spans 70 percent of the ink's width
    sub = b[v0:v1, u0:u1]
    ys, xs = np.nonzero(sub)
    width = xs.max() - xs.min() + 1
    longest = []
    for v in range(v0, v1):
        rr = runs(v)
        longest.append(max([q - p + 1 for p, q in rr], default=0))
    wide = [v0 + k for k, w in enumerate(longest) if w >= 0.7 * width]
    blo = bhi = wide[-1]
    while blo - 1 in wide:
        blo -= 1
    base = base or (blo, bhi)
    top = v0 + ys.min()
    rows = rows or (top + 6, base[0] - 2)
    print(f"auto: ink top {top}, base rows {base[0]}..{base[1]}, side rows {rows[0]}..{rows[1]}")
L, R = [], []
lrows = lrows or rows
rrows = rrows or rows
for v in range(min(lrows[0], rrows[0]), max(lrows[1], rrows[1]) + 1):
    rr = runs(v)
    if len(rr) >= 2:
        if lrows[0] <= v <= lrows[1]:
            L.append((v, (rr[0][0] + rr[0][1]) / 2, rr[0][1] - rr[0][0] + 1))
        if rrows[0] <= v <= rrows[1]:
            R.append((v, (rr[-1][0] + rr[-1][1]) / 2, rr[-1][1] - rr[-1][0] + 1))
L, R = np.array(L), np.array(R)
bl, al = np.polyfit(L[:, 0], L[:, 1], 1)
br, ar = np.polyfit(R[:, 0], R[:, 1], 1)
resl = L[:, 1] - (al + bl * L[:, 0]); resr = R[:, 1] - (ar + br * R[:, 0])
vb = (base[0] + base[1]) / 2
va = (ar - al) / (bl - br)
ua = al + bl * va
ul, ur = al + bl * vb, ar + br * vb
cu, cv = (ua + ul + ur) / 3, (va + 2 * vb) / 3
print(f"left side: {len(L)} rows, run width median {np.median(L[:, 2]):.0f}, fit rms {np.sqrt(np.mean(resl**2)):.2f}; "
      f"right side: {len(R)} rows, width {np.median(R[:, 2]):.0f}, rms {np.sqrt(np.mean(resr**2)):.2f}")
print(f"apex ({ua:.1f},{va:.1f}); base centreline v {vb:.1f}, corners u {ul:.1f}..{ur:.1f}; height {vb - va:.1f} width {ur - ul:.1f}")
print(f"centroid u {cu:.1f} v {cv:.1f}; h/6 = {(vb - va) / 6:.1f}")
