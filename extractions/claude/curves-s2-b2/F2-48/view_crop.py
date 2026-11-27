"""Zoomed crop of packet/p0109.png with points drawn on it, for checking a reading by eye.

python out/F2-48/view_crop.py u0 v0 u1 v1 zoom out.png [csv ...]
Each csv has pixel_u, pixel_v (and optionally series_id, u_bound_px, v_bound_px) or u, v columns.
lpt87 (solid) in red, lpt85 (dotted) in blue, centerline files in green; bounds drawn as boxes.
"""
import csv
import sys
from PIL import Image, ImageDraw

u0, v0, u1, v1, z = map(int, sys.argv[1:6])
out = sys.argv[6]
im = Image.open("packet/p0109.png").convert("RGB").crop((u0, v0, u1, v1))
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
# pixel grid every 10 px, labels every 50
for u in range((u0 // 10 + 1) * 10, u1, 10):
    x = (u - u0) * z
    d.line([(x, 0), (x, im.height)], fill=(255, 200, 200) if u % 50 else (255, 120, 120))
    if u % 50 == 0:
        d.text((x + 2, 2), str(u), fill=(200, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    y = (v - v0) * z
    d.line([(0, y), (im.width, y)], fill=(200, 200, 255) if v % 50 else (120, 120, 255))
    if v % 50 == 0:
        d.text((2, y + 2), str(v), fill=(0, 0, 200))
for path in sys.argv[7:]:
    for r in csv.DictReader(open(path)):
        u = r.get("pixel_u") or r.get("u")
        v = r.get("pixel_v") or r.get("v")
        if not u or not v:
            continue
        u, v = float(u), float(v)
        if not (u0 <= u < u1 and v0 <= v < v1):
            continue
        x, y = (u - u0 + 0.5) * z, (v - v0 + 0.5) * z
        sid = r.get("series_id", "")
        col = (230, 0, 0) if sid == "lpt87" else (0, 90, 255) if sid == "lpt85" else (0, 170, 0)
        if "pixel_u" in r:
            bu = float(r.get("u_bound_px") or 0) * z
            bv = float(r.get("v_bound_px") or 0) * z
            d.rectangle([x - bu, y - bv, x + bu, y + bv], outline=col)
            d.line([(x - 4, y), (x + 4, y)], fill=col)
            d.line([(x, y - 4), (x, y + 4)], fill=col)
            d.text((x + bu + 2, y - 6), r.get("sequence", ""), fill=col)
        else:
            d.point((x, y), fill=col)
im.save(out)
print("wrote", out, im.size)
