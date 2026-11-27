"""A zoomed crop with the fitted segment centre lines, the vertices, the ends and the marker circles
drawn over the page, for checking by eye. Usage: python crop_lines.py <image> <lines.json> u0 v0 u1 v1 zoom out.png"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
img = Image.open(sys.argv[1]).convert("RGB")
L = json.load(open(sys.argv[2]))
u0, v0, u1, v1, z = map(int, sys.argv[3:8])
c = img.crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(c)
P = lambda u, v: ((u - u0 + 0.5) * z, (v - v0 + 0.5) * z)
for k in range(u0 - u0 % 10, u1, 10):
    d.line([P(k - 0.5, v0 - 0.5), P(k - 0.5, v1)], fill=(255, 200, 200) if k % 50 else (255, 120, 120))
for k in range(v0 - v0 % 10, v1, 10):
    d.line([P(u0 - 0.5, k - 0.5), P(u1, k - 0.5)], fill=(200, 200, 255) if k % 50 else (120, 120, 255))
for name, s in L["segments"].items():
    a, b = np.array(s["a"]), np.array(s["b"])
    dd = (b - a) / np.hypot(*(b - a))
    d.line([P(*(a - 60 * dd)), P(*(b + 60 * dd))], fill=(0, 170, 0), width=1)
for m in L["markers"].values():
    for r in (11.2, 19.2):
        d.ellipse([P(m[0] - r, m[1] - r), P(m[0] + r, m[1] + r)], outline=(0, 120, 255))
    d.ellipse([P(m[0] - 0.7, m[1] - 0.7), P(m[0] + 0.7, m[1] + 0.7)], fill=(0, 120, 255))
for key in ("vertex_dense", "vertex_loose"):
    u, v = L[key]
    d.ellipse([P(u - 1.5, v - 1.5), P(u + 1.5, v + 1.5)], outline=(255, 0, 0), width=2)
for name, e in L["ends"].items():
    for p, col in ((e["ink_end"], (255, 0, 255)), (e["ring"][0] if e["ring"] else None, (255, 140, 0))):
        if p:
            d.ellipse([P(p[0] - 1.5, p[1] - 1.5), P(p[0] + 1.5, p[1] + 1.5)], outline=col, width=2)
for k in range(u0 - u0 % 10, u1, 10):
    if k % 50 == 0:
        d.text(P(k, v0), str(k), fill=(200, 0, 0))
for k in range(v0 - v0 % 10, v1, 10):
    if k % 50 == 0:
        d.text(P(u0, k), str(k), fill=(0, 0, 200))
c.save(sys.argv[8])
print("wrote", sys.argv[8])
