"""Zoomed overlay of a points file on the page (reading check)."""
import csv, sys
from PIL import Image, ImageDraw
COL = {"upper": (0, 0, 230), "average": (0, 170, 0), "lower": (230, 0, 0)}
img, pts, out = sys.argv[1], sys.argv[2], sys.argv[3]
u0, v0, u1, v1 = (int(x) for x in sys.argv[4:8]); z = int(sys.argv[8]) if len(sys.argv) > 8 else 3
im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
import numpy as np
a = np.asarray(im).copy(); a[a[:, :, 0] < 128] = (120, 120, 120); im = Image.fromarray(a)
d = ImageDraw.Draw(im)
for uu in range((u0 // 25 + 1) * 25, u1, 25):
    d.line([((uu - u0) * z, 0), ((uu - u0) * z, im.height)], fill=(255, 210, 210))
    if uu % 100 == 0: d.text(((uu - u0) * z + 2, 2), str(uu), fill=(200, 0, 0))
for vv in range((v0 // 25 + 1) * 25, v1, 25):
    d.line([(0, (vv - v0) * z), (im.width, (vv - v0) * z)], fill=(210, 210, 255))
    if vv % 100 == 0: d.text((2, (vv - v0) * z + 2), str(vv), fill=(0, 0, 200))
for r in csv.DictReader(open(pts, encoding="utf-8")):
    u, v = float(r["pixel_u"]), float(r["pixel_v"]); bu, bv = float(r["u_bound_px"]), float(r["v_bound_px"])
    x, y = (u - u0) * z, (v - v0) * z; c = COL[r["series_id"]]
    if r["point_kind"] == "trace":
        d.rectangle([x - bu * z, y - bv * z, x + bu * z, y + bv * z], outline=c)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=c)
    else:
        d.line([x - 8, y - 8, x + 8, y + 8], fill=(255, 0, 255), width=2); d.line([x - 8, y + 8, x + 8, y - 8], fill=(255, 0, 255), width=2)
im.save(out); print("wrote", out)
