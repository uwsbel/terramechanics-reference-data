"""Draw tracked curves over a zoomed crop of the page (reading aid only).
usage: show_tracks.py <image> <u0> <v0> <u1> <v1> <zoom> <out.png> name[,name...]"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
COL = {"rc2": (230, 0, 0), "ps": (0, 150, 0), "rs": (0, 0, 230), "rsmb": (200, 0, 200), "rsma": (230, 130, 0), "ss": (0, 170, 170)}
img, u0, v0, u1, v1, z, out = sys.argv[1], *map(int, sys.argv[2:7]), sys.argv[7]
names = sys.argv[8].split(",")
im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1))
im = im.point(lambda x: 140 + x * 115 // 255)  # lighten so overlays read
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for step in range(0, max(u1 - u0, v1 - v0), 10):
    pass
for u in range((u0 // 25 + 1) * 25, u1, 25):
    d.line([((u - u0) * z, 0), ((u - u0) * z, 6)], fill=(0, 0, 0))
    if u % 100 == 0:
        d.text(((u - u0) * z + 2, 2), str(u), fill=(200, 0, 0))
for v in range((v0 // 25 + 1) * 25, v1, 25):
    d.line([(0, (v - v0) * z), (6, (v - v0) * z)], fill=(0, 0, 0))
    if v % 100 == 0:
        d.text((2, (v - v0) * z + 2), str(v), fill=(0, 0, 200))
for n in names:
    recs = json.loads((HERE.parent / "tracks" / f"{n}.json").read_text())
    c = COL.get(n.split("_")[0], (0, 0, 0))
    for r in recs:
        u = r["u"]
        if not (u0 <= u < u1):
            continue
        x = (u - u0 + 0.5) * z
        if r["status"] == "ink":
            y = (r["v"] - v0 + 0.5) * z
            d.point((x, y), fill=c)
            if u % 3 == 0:
                d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=c)
        elif r["status"] in ("hgrid", "merged", "grid"):
            y = (r["vp"] - v0 + 0.5) * z
            d.point((x, y), fill=(120, 120, 120))
        else:
            y = (r["vp"] - v0 + 0.5) * z
            if u % 2 == 0:
                d.point((x, y), fill=c)
im.save(out)
print("wrote", out, im.size)
