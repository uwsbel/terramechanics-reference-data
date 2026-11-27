"""Reader helper (visualization only): enlarged crop in which the printed grid (rows and columns that are dark
over most of a wide, deskewed window) is drawn light gray and the remaining ink black, so the three curves
can be followed through the dense log grid. A pixel scale every 10 px (labels every `lab` px) in page
coordinates; optional points CSV drawn on top. usage: viz2.py image u0 v0 u1 v1 zoom out.png [lab] [points.csv] [thr]"""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw
img = sys.argv[1]; u0, v0, u1, v1, z = map(int, sys.argv[2:7]); out = sys.argv[7]
lab = int(sys.argv[8]) if len(sys.argv) > 8 else 20
pts = sys.argv[9] if len(sys.argv) > 9 and sys.argv[9] != "-" else None
thr = float(sys.argv[10]) if len(sys.argv) > 10 else 0.3
SH, SV = -0.0045, 0.0064      # tilt of horizontal lines (dv/du) and vertical lines (du/dv) on this page
g = np.asarray(Image.open(img).convert("L")) < 128
M = 200
A0, B0, A1, B1 = u0 - M, v0 - M, u1 + M, v1 + M
uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
# row projection: for each row offset r (rows of the window, deskewed), fraction of dark pixels over u in [A0, A1)
us = np.arange(A0, A1)
rows = {}
for v in range(v0 - 3, v1 + 3):
    vv = np.round(v + SH * (us - uc)).astype(int)
    rows[v] = g[vv, us].mean()
vs = np.arange(B0, B1)
cols = {}
for u in range(u0 - 3, u1 + 3):
    uu = np.round(u + SV * (vs - vc)).astype(int)
    cols[u] = g[vs, uu].mean()
H, W = v1 - v0, u1 - u0
grid = np.zeros((H, W), bool)
for j in range(H):
    for i in range(W):
        u, v = u0 + i, v0 + j
        # the row through (u, v) at the window centre, and the column through it
        vr = int(round(v - SH * (u - uc))); ur = int(round(u - SV * (v - vc)))
        if any(rows.get(vr + d, 0) > thr for d in (-1, 0, 1)) or any(cols.get(ur + d, 0) > thr for d in (-1, 0, 1)):
            grid[j, i] = True
ink = g[v0:v1, u0:u1]
rgb = np.full((H, W, 3), 255, np.uint8)
rgb[ink & grid] = (190, 190, 190)
rgb[ink & ~grid] = (0, 0, 0)
im = Image.fromarray(rgb).resize((W * z, H * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range((u0 // 10 + 1) * 10, u1, 10):
    x = (u - u0) * z; big = u % lab == 0
    d.line([(x, 0), (x, 20 if big else 10)], fill=(255, 0, 0) if big else (255, 170, 170))
    d.line([(x, im.height - (20 if big else 10)), (x, im.height)], fill=(255, 0, 0) if big else (255, 170, 170))
    if big: d.text((x + 2, 12), str(u), fill=(255, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    y = (v - v0) * z; big = v % lab == 0
    d.line([(0, y), (20 if big else 10, y)], fill=(0, 0, 255) if big else (170, 170, 255))
    d.line([(im.width - (20 if big else 10), y), (im.width, y)], fill=(0, 0, 255) if big else (170, 170, 255))
    if big: d.text((22, y - 6), str(v), fill=(0, 0, 255))
if pts:
    colors = {"average": (0, 170, 0), "upper": (230, 0, 0), "lower": (0, 90, 255)}
    with open(pts, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            x, y = (float(r["pixel_u"]) - u0) * z, (float(r["pixel_v"]) - v0) * z
            if not (0 <= x < im.width and 0 <= y < im.height): continue
            c = colors.get(r["series_id"], (255, 128, 0))
            bu, bv = max(float(r.get("u_bound_px") or 2), 1) * z, max(float(r.get("v_bound_px") or 2), 1) * z
            if r["point_kind"] == "feature":
                d.rectangle([x - bu - 4, y - bv - 4, x + bu + 4, y + bv + 4], outline=c, width=2)
            else:
                d.ellipse([x - bu, y - bv, x + bu, y + bv], outline=c, width=2)
im.save(out)
print("wrote", out, im.size)
