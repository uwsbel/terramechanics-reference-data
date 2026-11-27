"""Zoomed crop of the page with a centre line (centerline csv: v,u_center,...) and optional points csv
(pixel_u, pixel_v) drawn over it, for checking by eye.
usage: show_line.py page u0 v0 u1 v1 zoom out.png centerline.csv [points.csv]"""
import csv
import sys

from PIL import Image, ImageDraw

page, u0, v0, u1, v1, z, out, cl = sys.argv[1:9]
u0, v0, u1, v1, z = int(u0), int(v0), int(u1), int(v1), int(z)
im = Image.open(page).convert("RGB").crop((u0, v0, u1, v1))
im = im.resize((im.width * z, im.height * z), Image.NEAREST)
d = ImageDraw.Draw(im)
f = lambda u, v: ((u - u0 + 0.5) * z, (v - v0 + 0.5) * z)
for r in csv.DictReader(open(cl, encoding="utf-8")):
    if r["u_center"] == "":
        continue
    u, v = float(r["u_center"]), float(r["v"])
    if u0 <= u <= u1 and v0 <= v <= v1:
        x, y = f(u, v)
        col = {"": (255, 0, 0), "merged": (255, 140, 0), "trimmed": (0, 170, 0)}.get(r["flag"], (255, 0, 255))
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=col)
if len(sys.argv) > 9:
    for r in csv.DictReader(open(sys.argv[9], encoding="utf-8")):
        u, v = float(r["pixel_u"]), float(r["pixel_v"])
        bu, bv = float(r.get("u_bound_px") or 0), float(r.get("v_bound_px") or 0)
        if u0 <= u <= u1 and v0 <= v <= v1:
            x, y = f(u, v)
            col = (0, 0, 255) if r["point_kind"] == "trace" else (200, 0, 200)
            d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=col, width=2)
            d.line([x - bu * z, y, x + bu * z, y], fill=col)
            d.line([x, y - bv * z, x, y + bv * z], fill=col)
im.save(out)
print("wrote", out, im.size)
