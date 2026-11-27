"""Draw the column traces (trace-<curve>.csv) and optional points over a zoomed crop (reader's helper).

usage: view_trace.py <page.png> u0 v0 u1 v1 zoom out.png [points.csv]
Trace centers: mean red, upper green, lower blue; flagged columns (hgrid, circle, thin) in orange.
Points (pixel_u, pixel_v) as magenta crosses with their bound boxes. Grid labels every 25 px.
"""
import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
page, u0, v0, u1, v1, z, out = sys.argv[1], *map(int, sys.argv[2:7]), sys.argv[7]
im = Image.open(page).convert("RGB").crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
font = ImageFont.load_default()
for u in range((u0 // 25 + 1) * 25, u1, 25):
    d.line([((u - u0) * z, 0), ((u - u0) * z, im.height)], fill=(255, 190, 190))
    if u % 100 == 0:
        d.text(((u - u0) * z + 2, 2), str(u), fill=(200, 0, 0), font=font)
for v in range((v0 // 25 + 1) * 25, v1, 25):
    d.line([(0, (v - v0) * z), (im.width, (v - v0) * z)], fill=(190, 190, 255))
    if v % 100 == 0:
        d.text((2, (v - v0) * z + 2), str(v), fill=(0, 0, 200), font=font)
col = {"mean": (230, 0, 0), "upper": (0, 160, 0), "lower": (0, 0, 230)}
for name, c in col.items():
    f = HERE / f"trace-{name}.csv"
    if not f.exists():
        continue
    for r in csv.DictReader(f.open(encoding="utf-8")):
        if not r["v"]:
            continue
        u, v = float(r["u"]), float(r["v"])
        if not (u0 <= u < u1 and v0 <= v < v1):
            continue
        x, y = (u - u0 + 0.5) * z, (v - v0 + 0.5) * z
        cc = c if r["status"] == "ink" else (255, 150, 0)
        d.point([(x, y)], fill=cc)
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=cc)
if len(sys.argv) > 8:
    for r in csv.DictReader(open(sys.argv[8], encoding="utf-8")):
        u, v = float(r["pixel_u"]), float(r["pixel_v"])
        bu, bv = float(r.get("u_bound_px") or 0), float(r.get("v_bound_px") or 0)
        if not (u0 <= u < u1 and v0 <= v < v1):
            continue
        x, y = (u - u0 + 0.5) * z, (v - v0 + 0.5) * z
        d.line([(x - 6, y), (x + 6, y)], fill=(220, 0, 220), width=2)
        d.line([(x, y - 6), (x, y + 6)], fill=(220, 0, 220), width=2)
        d.rectangle([x - bu * z, y - bv * z, x + bu * z, y + bv * z], outline=(220, 0, 220))
im.save(out)
print("wrote", out, im.size)
