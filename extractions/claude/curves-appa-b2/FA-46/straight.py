"""Straightened band image: column u, rows v - vc(u) in [-H, H]; ink black, grid-row ink grey.
Usage: straight.py u0 u1 zoom out.png [H] [marks.csv with u,v,s]"""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw
from common import vc, grid_at, g
u0, u1, z, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
H = int(sys.argv[5]) if len(sys.argv) > 5 else 40
W = u1 - u0 + 1
img = np.full((2 * H + 1, W, 3), 255, np.uint8)
for i, u in enumerate(range(u0, u1 + 1)):
    c = int(round(vc(u)))
    for j in range(2 * H + 1):
        v = c - H + j
        if g[v, u]:
            img[j, i] = (160, 160, 160) if grid_at(v, u) else (0, 0, 0)
im = Image.fromarray(img).resize((W * z, (2 * H + 1) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range(u0 - u0 % 10, u1 + 1, 10):
    if u >= u0:
        x = (u - u0) * z
        d.line([(x, 0), (x, 6 if u % 50 else 14)], fill=(255, 0, 0))
        if u % 50 == 0: d.text((x + 2, 2), str(u), fill=(255, 0, 0))
for j in range(0, 2 * H + 1, 5):
    y = j * z
    d.line([(0, y), (6 if (j - H) % 10 else 14, y)], fill=(0, 0, 255))
    if (j - H) % 10 == 0: d.text((16, y - 5), str(j - H), fill=(0, 0, 255))
if len(sys.argv) > 6:
    cols = {"A": (0, 170, 0), "B": (230, 0, 0), "C": (0, 120, 255)}
    for r in csv.DictReader(open(sys.argv[6])):
        u, v = float(r["u"]), float(r["v"])
        if u0 <= u <= u1:
            j = v - (round(vc(int(round(u)))) - H)
            x, y = (u - u0 + 0.5) * z, (j + 0.5) * z
            c = cols.get(r["s"], (255, 0, 255))
            d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=c, width=2)
im.save(out); print("wrote", out, im.size)
