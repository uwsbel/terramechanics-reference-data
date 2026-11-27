"""Visual aid: crop of an image, Gaussian-smoothed (sigma px) and resampled by a zoom factor with a labelled
pixel grid (original page pixels). Not used for any value."""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
src, out = sys.argv[1], sys.argv[2]
u0, v0, u1, v1 = map(int, sys.argv[3:7])
zoom, sigma, step = float(sys.argv[7]), float(sys.argv[8]), int(sys.argv[9])
im = Image.open(src).convert("L")
if sigma > 0:
    im = im.filter(ImageFilter.GaussianBlur(sigma))
crop = im.crop((u0, v0, u1, v1)).resize((int((u1 - u0) * zoom), int((v1 - v0) * zoom)), Image.LANCZOS).convert("RGB")
d = ImageDraw.Draw(crop)
try:
    font = ImageFont.truetype("arial.ttf", 12)
except OSError:
    font = ImageFont.load_default()
for u in range((u0 // step + 1) * step, u1, step):
    x = (u - u0) * zoom
    d.line([(x, 0), (x, 6)], fill=(255, 0, 0)); d.line([(x, crop.height - 6), (x, crop.height)], fill=(255, 0, 0))
    if u % (step * 2) == 0:
        d.text((x + 2, 2), str(u), fill=(200, 0, 0), font=font)
for v in range((v0 // step + 1) * step, v1, step):
    y = (v - v0) * zoom
    d.line([(0, y), (6, y)], fill=(0, 0, 255)); d.line([(crop.width - 6, y), (crop.width, y)], fill=(0, 0, 255))
    if v % (step * 2) == 0:
        d.text((8, y - 6), str(v), fill=(0, 0, 200), font=font)
crop.save(out)
print("wrote", out, crop.size)
