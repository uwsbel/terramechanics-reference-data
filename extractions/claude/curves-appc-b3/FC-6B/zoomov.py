"""Zoom into an overlay image: python zoomov.py overlay.png box_u0 box_v0 u0 v0 u1 v1 zoom out.png
(box_u0, box_v0 = the page offset the overlay was cropped at; u0.. in page pixels)."""
import sys
from PIL import Image, ImageDraw
src, bu, bv, u0, v0, u1, v1, z, out = sys.argv[1:]
bu, bv, u0, v0, u1, v1, z = map(int, (bu, bv, u0, v0, u1, v1, z))
im = Image.open(src).crop((u0 - bu, v0 - bv, u1 - bu, v1 - bv))
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range((u0 // 25 + 1) * 25, u1, 25):
    d.line([((u - u0) * z, 0), ((u - u0) * z, 8)], fill=(0, 0, 0)); d.text(((u - u0) * z + 2, 0), str(u), fill=(0, 0, 0))
for v in range((v0 // 25 + 1) * 25, v1, 25):
    d.line([(0, (v - v0) * z), (8, (v - v0) * z)], fill=(0, 0, 0)); d.text((2, (v - v0) * z + 2), str(v), fill=(0, 0, 0))
im.save(out)
print("wrote", out, im.size)
