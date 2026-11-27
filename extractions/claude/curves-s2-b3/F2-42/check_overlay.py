"""Zoomed check view: the page crop enlarged, each sample drawn as a small colored cross with its bound box.
usage: check_overlay.py u0 v0 u1 v1 zoom out.png"""
import csv, sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
u0, v0, u1, v1, z = map(int, sys.argv[1:6]); out = sys.argv[6]
im = Image.open(HERE.parents[1] / "packet" / "p0102.png").convert("RGB").crop((u0, v0, u1, v1))
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
# lighten black ink so the marks stand out
px = im.load()
for i in range(im.size[0]):
    for j in range(im.size[1]):
        if px[i, j][0] < 128: px[i, j] = (150, 150, 150)
d = ImageDraw.Draw(im)
col = {"lpt22": (230, 0, 0), "lpt23": (0, 160, 0), "lpt24": (0, 0, 255), "lpt25": (230, 130, 0)}
for r in csv.DictReader(open(HERE / "points-p1.csv", encoding="utf-8")):
    u, v = (float(r["pixel_u"]) - u0 + 0.5) * z, (float(r["pixel_v"]) - v0 + 0.5) * z
    bu, bv = float(r["u_bound_px"]) * z, float(r["v_bound_px"]) * z
    c = col[r["series_id"]]
    d.rectangle([u - bu, v - bv, u + bu, v + bv], outline=c, width=1)
    d.line([(u - 4, v), (u + 4, v)], fill=c, width=2); d.line([(u, v - 4), (u, v + 4)], fill=c, width=2)
    if r["point_kind"] == "feature":
        d.ellipse([u - 7, v - 7, u + 7, v + 7], outline=c, width=2)
im.save(out); print("wrote", out)
