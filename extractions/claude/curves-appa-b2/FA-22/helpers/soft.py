"""Viewing aid: a crop of the page blurred slightly and resized smoothly (the scan is bilevel; a soft
rendering shows symbol shapes better). Grid every 50 px in page pixels. Usage: python soft.py out u0 v0 u1 v1 zoom [blur]"""
import sys
from PIL import Image, ImageDraw, ImageFilter
import fa22lib as L
out = sys.argv[1]; u0, v0, u1, v1 = map(int, sys.argv[2:6]); z = float(sys.argv[6]); r = float(sys.argv[7]) if len(sys.argv) > 7 else 1.2
im = Image.open(L.PAGE).convert("L").crop((u0, v0, u1, v1)).filter(ImageFilter.GaussianBlur(r))
im = im.resize((int((u1 - u0) * z), int((v1 - v0) * z)), Image.BICUBIC).convert("RGB")
d = ImageDraw.Draw(im)
for u in range(u0 - u0 % 50 + 50, u1, 50):
    x = (u - u0) * z; d.line([(x, 0), (x, 8)], fill=(255, 0, 0), width=2); d.line([(x, im.size[1] - 8), (x, im.size[1])], fill=(255, 0, 0), width=2); d.text((x + 2, 8), str(u), fill=(220, 0, 0))
for v in range(v0 - v0 % 50 + 50, v1, 50):
    y = (v - v0) * z; d.line([(0, y), (8, y)], fill=(0, 0, 255), width=2); d.line([(im.size[0] - 8, y), (im.size[0], y)], fill=(0, 0, 255), width=2); d.text((10, y - 6), str(v), fill=(0, 0, 220))
im.save(out); print("wrote", out, im.size)
