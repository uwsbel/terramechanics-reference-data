"""Draw points-p1.csv over a zoomed page crop: a cross at each point and its bound box (reading check).
usage: show_points.py <image> <points.csv> u0 v0 u1 v1 zoom out.png"""
import csv, sys
from PIL import Image, ImageDraw
COL = {"rc2": (230, 0, 0), "ps": (0, 160, 0), "rs": (0, 0, 230), "rsm-b": (210, 120, 0), "rsm-a": (170, 0, 170), "ss": (0, 160, 160)}
img, pts, u0, v0, u1, v1, z, out = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:8]), sys.argv[8]
im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1)).point(lambda x: 120 + x * 135 // 255)
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range((u0 // 10 + 1) * 10, u1, 10):
    d.line([((u - u0) * z, 0), ((u - u0) * z, 4 if u % 50 else 12)], fill=(0, 0, 0))
    if u % 50 == 0: d.text(((u - u0) * z + 2, 12), str(u), fill=(200, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    d.line([(0, (v - v0) * z), (4 if v % 50 else 12, (v - v0) * z)], fill=(0, 0, 0))
    if v % 50 == 0: d.text((14, (v - v0) * z - 5), str(v), fill=(0, 0, 200))
for r in csv.DictReader(open(pts, encoding="utf-8")):
    u, v = float(r["pixel_u"]), float(r["pixel_v"])
    if not (u0 <= u < u1 and v0 <= v < v1): continue
    c = COL[r["series_id"]]
    x, y = (u - u0 + 0.5) * z, (v - v0 + 0.5) * z
    bu, bv = float(r["u_bound_px"]) * z, float(r["v_bound_px"]) * z
    d.rectangle([x - bu, y - bv, x + bu, y + bv], outline=c)
    d.line([x - 5, y, x + 5, y], fill=c, width=2); d.line([x, y - 5, x, y + 5], fill=c, width=2)
    tag = r["sequence"] + ("F" if r["point_kind"] == "feature" else "")
    d.text((x + bu + 2, y - 6), tag, fill=c)
im.save(out); print("wrote", out, im.size)
