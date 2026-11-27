"""Colour visual of a page region: ink black, grid-row ink (known horizontal grid rows) grey; enlarged with a
pixel grid. Usage: vis.py u0 v0 u1 v1 zoom out.png [marks.csv]  (marks: u,v,color)"""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
u0, v0, u1, v1, z = map(int, sys.argv[1:6]); out = sys.argv[6]
sub = g[v0:v1, u0:u1]
rgb = np.full(sub.shape + (3,), 255, np.uint8)
rgb[sub] = (0, 0, 0)
im = Image.fromarray(rgb).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range(u0 - u0 % 10, u1, 10):
    if u >= u0:
        d.line([((u - u0) * z, 0), ((u - u0) * z, im.size[1])], fill=(255, 160, 160) if u % 50 else (255, 0, 0), width=1)
        if u % 50 == 0: d.text(((u - u0) * z + 2, 2), str(u), fill=(255, 0, 0))
for v in range(v0 - v0 % 10, v1, 10):
    if v >= v0:
        d.line([(0, (v - v0) * z), (im.size[0], (v - v0) * z)], fill=(160, 160, 255) if v % 50 else (0, 0, 255), width=1)
        if v % 50 == 0: d.text((2, (v - v0) * z + 2), str(v), fill=(0, 0, 255))
if len(sys.argv) > 7:
    cols = {"A": (0, 170, 0), "B": (230, 0, 0), "C": (0, 120, 255), "X": (255, 140, 0)}
    with open(sys.argv[7]) as f:
        for r in csv.DictReader(f):
            u, v = float(r["u"]), float(r["v"]); c = cols.get(r["s"], (255, 0, 255))
            x, y = (u - u0 + 0.5) * z, (v - v0 + 0.5) * z
            if 0 <= x < im.size[0] and 0 <= y < im.size[1]:
                d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=c, width=2)
im.save(out)
print("wrote", out, im.size)
