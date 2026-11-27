"""Draw a center line (centerline-p<n>.json) or points CSV over a zoomed crop of the page, for checking by eye."""
import csv
import json
import sys
from PIL import Image, ImageDraw
from trace_tools import IMG

src, box, zoom, out = sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]), sys.argv[4]
u0, v0, u1, v1 = box
im = Image.open(IMG).convert("RGB").crop((u0, v0, u1, v1)).resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
d = ImageDraw.Draw(im)
step = 10 if zoom >= 3 else 50
for u in range((u0 // step + 1) * step, u1, step):
    d.line([((u - u0) * zoom, 0), ((u - u0) * zoom, im.height)], fill=(255, 200, 200) if u % (4 * step) else (255, 120, 120))
    if u % (4 * step) == 0:
        d.text(((u - u0) * zoom + 2, 2), str(u), fill=(200, 0, 0))
for v in range((v0 // step + 1) * step, v1, step):
    d.line([(0, (v - v0) * zoom), (im.width, (v - v0) * zoom)], fill=(200, 200, 255) if v % (4 * step) else (120, 120, 255))
    if v % (4 * step) == 0:
        d.text((2, (v - v0) * zoom + 2), str(v), fill=(0, 0, 200))
COL = {"row": (0, 170, 0), "row-amb": (255, 140, 0), "col": (0, 120, 255), "col-amb": (200, 0, 200),
       "trace": (230, 0, 0), "feature": (0, 160, 255)}
if src.endswith(".json"):
    pts = json.load(open(src))["points"]
    for p in pts:
        x, y = (p["u"] - u0 + 0.5) * zoom, (p["v"] - v0 + 0.5) * zoom
        r = max(1, zoom // 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=COL[p["kind"]])
else:
    for r_ in csv.DictReader(open(src, encoding="utf-8")):
        u, v = float(r_["pixel_u"]), float(r_["pixel_v"])
        bu, bv = float(r_["u_bound_px"]), float(r_["v_bound_px"])
        x, y = (u - u0 + 0.5) * zoom, (v - v0 + 0.5) * zoom
        c = COL[r_["point_kind"]]
        if r_["point_kind"] == "feature":
            d.rectangle([x - bu * zoom, y - bv * zoom, x + bu * zoom, y + bv * zoom], outline=c, width=2)
        else:
            d.ellipse([x - bu * zoom, y - bv * zoom, x + bu * zoom, y + bv * zoom], outline=c, width=2)
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=c)
im.save(out)
print("wrote", out, im.size)
