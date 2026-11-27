"""Draw sample points (from a JSON of the tracer, or a points CSV) over a soft rendering of a page
region, zoomed, for checking by eye. Usage: python checkov.py <points.json|csv> <out.png> u0 v0 u1 v1 zoom"""
import sys, json, csv
from PIL import Image, ImageDraw, ImageFilter
import fa22lib as L
src, out = sys.argv[1], sys.argv[2]
u0, v0, u1, v1 = map(int, sys.argv[3:7]); z = float(sys.argv[7])
COL = {"upper": (0, 160, 255), "average": (230, 0, 0), "lower": (0, 170, 0)}
pts = []
if src.endswith(".json"):
    d = json.loads(open(src, encoding="utf-8").read())
    for s, lst in d.items():
        for i, m in enumerate(lst):
            pts.append((s, m["u"], m["v"], f"{m['e']:+.2f}", "trace"))
else:
    for r in csv.DictReader(open(src, encoding="utf-8")):
        pts.append((r["series_id"], float(r["pixel_u"]), float(r["pixel_v"]), r["sequence"], r["point_kind"]))
im = Image.open(L.PAGE).convert("L").crop((u0, v0, u1, v1)).filter(ImageFilter.GaussianBlur(0.8))
im = im.resize((int((u1 - u0) * z), int((v1 - v0) * z)), Image.BICUBIC).convert("RGB")
# lighten the page so marks stand out
im = Image.eval(im, lambda p: 110 + int(p * 145 / 255))
d = ImageDraw.Draw(im)
for u in range(u0 - u0 % 10 + 10, u1, 10):
    x = (u - u0) * z
    d.line([(x, 0), (x, 5 if u % 50 else 12)], fill=(255, 0, 0)); 
    if u % 50 == 0: d.text((x + 2, 10), str(u), fill=(200, 0, 0))
for v in range(v0 - v0 % 10 + 10, v1, 10):
    y = (v - v0) * z
    d.line([(0, y), (5 if v % 50 else 12, y)], fill=(0, 0, 255))
    if v % 50 == 0: d.text((14, y - 6), str(v), fill=(0, 0, 200))
for s, u, v, lab, kind in pts:
    if not (u0 <= u <= u1 and v0 <= v <= v1):
        continue
    x, y = (u - u0) * z, (v - v0) * z
    c = COL.get(s, (200, 0, 200))
    if kind == "marker":
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=c, width=2)
    elif kind == "feature":
        d.rectangle([x - 6, y - 6, x + 6, y + 6], outline=c, width=2)
    else:
        d.line([(x - 5, y), (x + 5, y)], fill=c, width=2); d.line([(x, y - 5), (x, y + 5)], fill=c, width=2)
    d.text((x + 6, y - 12), lab, fill=c)
im.save(out); print("wrote", out, im.size)
