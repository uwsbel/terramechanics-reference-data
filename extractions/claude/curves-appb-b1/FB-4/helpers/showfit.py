"""Zoomed crop with fitted ring outlines (inner and outer radius) and centres drawn in colour, and
the fitted segment centre lines, to check a fit by eye. Pixels: model-only ink in red tint,
page-only ink in blue tint, both in black."""
import json
import sys
import numpy as np
from PIL import Image, ImageDraw

img, segf, out = sys.argv[1], sys.argv[2], sys.argv[3]
u0, v0, u1, v1, z = [int(x) for x in sys.argv[4:9]]
r_in, r_out = float(sys.argv[9]), float(sys.argv[10])
cs = [tuple(float(c) for c in s.split(",")) for s in sys.argv[11:]]
D = np.asarray(Image.open(img).convert("L"))[v0:v1, u0:u1] < 128
U, V = np.meshgrid(np.arange(u0, u1), np.arange(v0, v1))
M = np.zeros(D.shape, bool)
for cu, cv in cs:
    d = np.hypot(U - cu, V - cv)
    M |= (d >= r_in) & (d <= r_out)
rgb = np.full(D.shape + (3,), 255, np.uint8)
rgb[D & M] = (0, 0, 0)
rgb[D & ~M] = (90, 90, 230)
rgb[~D & M] = (255, 170, 170)
im = Image.fromarray(rgb).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
S = json.load(open(segf))
for name, s in S.items():
    if s["steep"]:
        pts = [((s["c0"] + s["k"] * v - u0) * z, (v - v0) * z) for v in (v0, v1)]
    else:
        pts = [((u - u0) * z, (s["c0"] + s["k"] * u - v0) * z) for u in (u0, u1)]
    d.line(pts, fill=(0, 160, 0), width=1)
cols = [(230, 120, 0), (200, 0, 200), (0, 150, 150)]
for i, (cu, cv) in enumerate(cs):
    x, y = (cu - u0 + 0.5) * z, (cv - v0 + 0.5) * z
    for r in (r_in, r_out):
        d.ellipse([x - r * z, y - r * z, x + r * z, y + r * z], outline=cols[i % 3], width=1)
    d.line([x - 6, y, x + 6, y], fill=cols[i % 3], width=2)
    d.line([x, y - 6, x, y + 6], fill=cols[i % 3], width=2)
for u in range((u0 // 10 + 1) * 10, u1, 10):
    d.line([((u - u0) * z, 0), ((u - u0) * z, 6)], fill=(255, 0, 0))
    if u % 20 == 0:
        d.text(((u - u0) * z + 2, 6), str(u), fill=(200, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    d.line([(0, (v - v0) * z), (6, (v - v0) * z)], fill=(0, 0, 255))
    if v % 20 == 0:
        d.text((8, (v - v0) * z - 5), str(v), fill=(0, 0, 200))
im.save(out)
print("wrote", out)
