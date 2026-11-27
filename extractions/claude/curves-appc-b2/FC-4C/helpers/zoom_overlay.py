"""Zoomed crops of an overlay image (made with plot_grid.py overlay --box), with a labelled pixel
grid in page coordinates, so the overlay can be checked region by region.

    python zoom_overlay.py <overlay.png> <box_u0> <box_v0> <crop u0 v0 u1 v1> <out.png> [--zoom 3] [--step 25]

box_u0, box_v0: the top-left corner of the box the overlay was made with.
"""
import argparse

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("overlay")
ap.add_argument("bu0", type=int)
ap.add_argument("bv0", type=int)
ap.add_argument("crop", nargs=4, type=int)
ap.add_argument("out")
ap.add_argument("--zoom", type=int, default=3)
ap.add_argument("--step", type=int, default=25)
a = ap.parse_args()
im = Image.open(a.overlay).convert("RGB")
u0, v0, u1, v1 = a.crop
c = im.crop((u0 - a.bu0, v0 - a.bv0, u1 - a.bu0, v1 - a.bv0)).resize(((u1 - u0) * a.zoom, (v1 - v0) * a.zoom), Image.NEAREST)
d = ImageDraw.Draw(c)
for u in range((u0 // a.step + 1) * a.step, u1, a.step):
    x = (u - u0) * a.zoom
    d.line([(x, 0), (x, c.height)], fill=(255, 160, 160) if u % 100 else (255, 0, 0), width=1)
    if u % 100 == 0:
        d.text((x + 2, 2), str(u), fill=(200, 0, 0))
for v in range((v0 // a.step + 1) * a.step, v1, a.step):
    y = (v - v0) * a.zoom
    d.line([(0, y), (c.width, y)], fill=(160, 160, 255) if v % 100 else (0, 0, 255), width=1)
    if v % 100 == 0:
        d.text((2, y + 2), str(v), fill=(0, 0, 200))
c.save(a.out)
print("wrote", a.out, c.size)
