"""Draw observation points (u, curve, v) over a zoomed crop of the page: lower red, average green, upper blue."""
import csv, sys
from pathlib import Path
from PIL import Image, ImageDraw
base = Path(__file__).resolve().parents[1]
page = Image.open(base.parents[1] / "packet" / "p0054.png").convert("RGB")
src, name, u0, v0, u1, v1, zoom = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:8])
col = {"lower": (230, 0, 0), "average": (0, 170, 0), "upper": (0, 80, 255)}
im = page.crop((u0, v0, u1, v1)).resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.45)
d = ImageDraw.Draw(im)
for u in range((u0 // 10 + 1) * 10, u1, 10):
    x = (u - u0) * zoom; d.line([(x, 0), (x, im.size[1])], fill=(255, 200, 200) if u % 50 else (255, 120, 120))
    if u % 50 == 0: d.text((x + 2, 2), str(u), fill=(200, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    y = (v - v0) * zoom; d.line([(0, y), (im.size[0], y)], fill=(200, 200, 255) if v % 50 else (120, 120, 255))
    if v % 50 == 0: d.text((2, y + 2), str(v), fill=(0, 0, 200))
for r in csv.DictReader(open(src, encoding="utf-8")):
    u = float(r.get("u") or r.get("pixel_u")); v = float(r.get("v") or r.get("pixel_v"))
    c = col.get(r.get("curve") or r.get("series_id"), (0, 0, 0))
    if u0 <= u <= u1 and v0 <= v <= v1:
        x, y = (u - u0) * zoom, (v - v0) * zoom
        rr = 2 if zoom < 4 else 3
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c)
im.save(base / "crops" / f"{name}.png")
print("wrote", name)
