"""Zoomed check crop: the page with this reading's samples drawn (centre dot, bound box, sequence)."""
import csv, sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
img = Image.open(HERE.parents[1] / "packet" / "p0104.png").convert("RGB")
COL = {"lpt69": (220, 0, 0), "lpt64a": (0, 150, 0), "lpt74": (0, 0, 230), "lpt73": (230, 130, 0), "lpt24": (170, 0, 170)}
u0, v0, u1, v1, z = map(int, sys.argv[1:6]); out = sys.argv[6]
only = sys.argv[7].split(",") if len(sys.argv) > 7 else None
im = img.crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for r in csv.DictReader(open(HERE / "points-p1.csv", encoding="utf-8")):
    if only and r["series_id"] not in only:
        continue
    u, v = float(r["pixel_u"]), float(r["pixel_v"]); bu, bv = float(r["u_bound_px"]), float(r["v_bound_px"])
    if not (u0 - 20 <= u <= u1 + 20 and v0 - 20 <= v <= v1 + 20):
        continue
    c = COL[r["series_id"]]
    X, Y = (u - u0) * z, (v - v0) * z
    d.rectangle([X - bu * z, Y - bv * z, X + bu * z, Y + bv * z], outline=c, width=1)
    rr = 3 if r["point_kind"] == "trace" else 5
    d.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=c if r["point_kind"] == "trace" else None, outline=c, width=2)
    d.text((X + 6, Y - 12 if r["point_kind"] == "trace" else Y + 4), f"{r['series_id'][3:]}.{r['sequence']}", fill=c)
im.save(HERE / "crops" / out)
print("wrote", out, im.size)
