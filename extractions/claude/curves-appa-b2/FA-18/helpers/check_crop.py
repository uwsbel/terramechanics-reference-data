"""Claude reader helper (FA-18): zoomed crop of the page with the reading's points drawn as small
crosses (upper red, average green, lower blue) and their bound boxes, for checking by eye."""
import csv, sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve()
WS = HERE.parents[3]
u0, v0, u1, v1, z = map(int, sys.argv[1:6]); out = sys.argv[6]
im = Image.open(WS / "packet/p0039.png").convert("RGB").crop((u0, v0, u1, v1))
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
# lighten the page so the marks stand out
im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.45)
d = ImageDraw.Draw(im)
col = {"upper": (230, 0, 0), "average": (0, 160, 0), "lower": (0, 0, 230)}
for r in csv.DictReader(open(WS / "out/FA-18/points-p1.csv", encoding="utf-8")):
    u, v = float(r["pixel_u"]), float(r["pixel_v"])
    if not (u0 <= u <= u1 and v0 <= v <= v1):
        continue
    x, y = (u - u0) * z, (v - v0) * z
    bu, bv = float(r["u_bound_px"]) * z, float(r["v_bound_px"]) * z
    c = col[r["series_id"]]
    d.rectangle([x - bu, y - bv, x + bu, y + bv], outline=c)
    s = 4 if r["point_kind"] == "trace" else 7
    d.line([x - s, y, x + s, y], fill=c, width=2); d.line([x, y - s, x, y + s], fill=c, width=2)
for i in range(0, u1 - u0 + 1, 10):
    d.text((i * z + 1, 1), str(u0 + i) if (u0 + i) % 50 == 0 else "", fill=(120, 0, 120))
for j in range(0, v1 - v0 + 1, 10):
    d.text((1, j * z + 1), str(v0 + j) if (v0 + j) % 50 == 0 else "", fill=(120, 0, 120))
im.save(WS / "out/FA-18" / out)
print("wrote", out)
