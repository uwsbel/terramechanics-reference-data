"""Reader helper: an enlarged crop where ink belonging to long horizontal or vertical runs (the printed grid)
is shown light gray and the remaining ink (curves, text) black, with a pixel scale every 10 px (labels every
`lab` px) in page coordinates. Visualization only; every value read is a pixel of the page itself.
usage: viz.py image u0 v0 u1 v1 zoom out.png [runlen] [lab] [points.csv]"""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw
img = sys.argv[1]; u0, v0, u1, v1, z = map(int, sys.argv[2:7]); out = sys.argv[7]
L = int(sys.argv[8]) if len(sys.argv) > 8 else 25
lab = int(sys.argv[9]) if len(sys.argv) > 9 else 20
pts = sys.argv[10] if len(sys.argv) > 10 else None
g = np.asarray(Image.open(img).convert("L"))
pad = max(L, 2)
G = g[v0 - pad:v1 + pad, u0 - pad:u1 + pad] < 128
def run_open(m, axis, L):
    # pixels lying on a run of >= L dark pixels along axis
    h = L // 2
    er = np.ones_like(m)
    for k in range(-h, h + 1):
        er &= np.roll(m, k, axis=axis)
    di = np.zeros_like(m)
    for k in range(-h, h + 1):
        di |= np.roll(er, k, axis=axis)
    return di & m
hz = run_open(G, 1, L) if L > 0 else np.zeros_like(G); vt = run_open(G, 0, L) if L > 0 else np.zeros_like(G)
grid = hz | vt
curve = G & ~grid
sl = (slice(pad, pad + v1 - v0), slice(pad, pad + u1 - u0))
G, grid, curve = G[sl], grid[sl], curve[sl]
rgb = np.full(G.shape + (3,), 255, np.uint8)
rgb[grid] = (175, 175, 175)
rgb[curve] = (0, 0, 0)
im = Image.fromarray(rgb).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range((u0 // 10 + 1) * 10, u1, 10):
    x = (u - u0) * z
    col = (255, 0, 0) if u % lab == 0 else (255, 190, 190)
    d.line([(x, 0), (x, 12 if u % lab else 20)], fill=col, width=1)
    d.line([(x, im.height - (12 if u % lab else 20)), (x, im.height)], fill=col, width=1)
    if u % lab == 0:
        d.text((x + 2, 20), str(u), fill=(255, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    y = (v - v0) * z
    col = (0, 0, 255) if v % lab == 0 else (190, 190, 255)
    d.line([(0, y), (12 if v % lab else 20, y)], fill=col, width=1)
    d.line([(im.width - (12 if v % lab else 20), y), (im.width, y)], fill=col, width=1)
    if v % lab == 0:
        d.text((22, y - 6), str(v), fill=(0, 0, 255))
if pts:
    colors = {"average": (0, 160, 0), "upper": (230, 0, 0), "lower": (0, 0, 230)}
    with open(pts, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            x, y = (float(r["pixel_u"]) - u0) * z, (float(r["pixel_v"]) - v0) * z
            c = colors.get(r["series_id"], (255, 128, 0))
            bu, bv = float(r.get("u_bound_px") or 2) * z, float(r.get("v_bound_px") or 2) * z
            if r["point_kind"] == "feature":
                d.rectangle([x - bu - 3, y - bv - 3, x + bu + 3, y + bv + 3], outline=c, width=2)
            else:
                d.ellipse([x - bu, y - bv, x + bu, y + bv], outline=c, width=2)
                d.line([(x - 2, y), (x + 2, y)], fill=c)
im.save(out)
print("wrote", out, im.size)
