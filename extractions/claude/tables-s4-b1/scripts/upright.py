"""Crop a box from the unrotated scan, turn it upright (90 deg clockwise), zoom, and draw a light
grid labeled in ORIGINAL scan pixels: vertical lines at constant v (label v=...), horizontal lines at
constant u (label u=...)."""
import sys
from PIL import Image, ImageDraw, ImageFont
img, u0, v0, u1, v1, zoom, out = sys.argv[1], *map(int, sys.argv[2:6]), float(sys.argv[6]), sys.argv[7]
step = int(sys.argv[8]) if len(sys.argv) > 8 else 50
im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1)).transpose(Image.ROTATE_270)
W, H = int(im.width * zoom), int(im.height * zoom)
im = im.resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("arial.ttf", 14)
except OSError:
    font = ImageFont.load_default()
for v in range((v0 // step + 1) * step, v1, step):
    x = (v1 - v) * zoom
    d.line([(x, 0), (x, H)], fill=(255, 190, 190), width=1)
    d.text((x + 2, 2), f"v{v}", fill=(200, 0, 0), font=font)
for u in range((u0 // step + 1) * step, u1, step):
    y = (u - u0) * zoom
    d.line([(0, y), (W, y)], fill=(190, 190, 255), width=1)
    d.text((2, y + 2), f"u{u}", fill=(0, 0, 200), font=font)
im.save(out)
print(out, W, H)
