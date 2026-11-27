"""Reader helper: raw enlarged crop around the curves for sample rows k0..k1 with each sample row (line of
constant grain size, from cal-p1) drawn in cyan and labelled; optional points CSV overlaid.
usage: sheet.py k0 k1 zoom out.png [halfwidth] [points.csv]"""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw
from calmap import c, v_of_g, IMAGE
k0, k1, z = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); out = sys.argv[4]
hw = int(sys.argv[5]) if len(sys.argv) > 5 else 70
pts = sys.argv[6] if len(sys.argv) > 6 else None
def vt(k):
    g = 10 ** (0.05 * k); v = 2000.0
    for _ in range(5): v = v_of_g(g, c(v))
    return v
vs = [vt(k) for k in range(k0, k1 + 1)]
v0, v1 = int(min(vs)) - 20, int(max(vs)) + 20
u0 = int(min(c(v0), c(v1))) - hw; u1 = int(max(c(v0), c(v1))) + hw
g = np.asarray(Image.open(IMAGE).convert("L"))[v0:v1, u0:u1]
rgb = np.stack([g] * 3, -1).astype(np.uint8)
rgb[g < 128] = (60, 60, 60)
im = Image.fromarray(rgb).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for k in range(k0, k1 + 1):
    gs = 10 ** (0.05 * k)
    ya = (v_of_g(gs, u0) - v0) * z; yb = (v_of_g(gs, u1) - v0) * z
    d.line([(0, ya), (im.width, yb)], fill=(0, 200, 230), width=1)
    d.text((im.width - 60, ya - 12), f"k{k}", fill=(0, 150, 200))
for u in range((u0 // 10 + 1) * 10, u1, 10):
    x = (u - u0) * z; big = u % 50 == 0
    d.line([(x, 0), (x, 16 if big else 8)], fill=(255, 0, 0)); d.line([(x, im.height - (16 if big else 8)), (x, im.height)], fill=(255, 0, 0))
    if u % 20 == 0: d.text((x + 2, 10), str(u), fill=(255, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    y = (v - v0) * z; big = v % 50 == 0
    d.line([(0, y), (16 if big else 8, y)], fill=(0, 0, 255)); d.line([(im.width - (16 if big else 8), y), (im.width, y)], fill=(0, 0, 255))
    if v % 20 == 0: d.text((18, y - 6), str(v), fill=(0, 0, 255))
if pts:
    colors = {"average": (0, 170, 0), "upper": (230, 0, 0), "lower": (0, 90, 255)}
    with open(pts, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            x, y = (float(r["pixel_u"]) - u0) * z, (float(r["pixel_v"]) - v0) * z
            if not (0 <= x < im.width and 0 <= y < im.height): continue
            cl = colors.get(r["series_id"], (255, 128, 0))
            bu, bv = float(r["u_bound_px"]) * z, float(r["v_bound_px"]) * z
            if r["point_kind"] == "feature":
                d.rectangle([x - bu - 3, y - bv - 3, x + bu + 3, y + bv + 3], outline=cl, width=2)
            else:
                d.ellipse([x - bu, y - bv, x + bu, y + bv], outline=cl, width=2)
                d.line([(x - 3, y), (x + 3, y)], fill=cl, width=2)
im.save(out); print("wrote", out, im.size, "box", u0, v0, u1, v1)
