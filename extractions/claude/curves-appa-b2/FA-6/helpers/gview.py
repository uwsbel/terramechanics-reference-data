"""Visual aid: smoothed crop of the page at zoom Z with a light pixel grid every 10 px (labels every 50 px)
drawn in colour so the ink stays readable."""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
src, out = sys.argv[1], sys.argv[2]
u0, v0, u1, v1 = map(int, sys.argv[3:7]); Z = float(sys.argv[7]); sig = float(sys.argv[8])
im = Image.open(src).convert("L").filter(ImageFilter.GaussianBlur(sig))
c = im.crop((u0, v0, u1, v1)).resize((int((u1 - u0) * Z), int((v1 - v0) * Z)), Image.LANCZOS).convert("RGB")
ov = Image.new("RGB", c.size, (255, 255, 255)); d = ImageDraw.Draw(ov)
try:
    f = ImageFont.truetype("arial.ttf", 12)
except OSError:
    f = ImageFont.load_default()
for u in range((u0 // 10 + 1) * 10, u1, 10):
    x = (u - u0) * Z
    d.line([(x, 0), (x, c.height)], fill=(255, 120, 120) if u % 50 == 0 else (255, 215, 215), width=1)
for v in range((v0 // 10 + 1) * 10, v1, 10):
    y = (v - v0) * Z
    d.line([(0, y), (c.width, y)], fill=(120, 120, 255) if v % 50 == 0 else (215, 215, 255), width=1)
from PIL import ImageChops
c = ImageChops.multiply(c, ov)
d = ImageDraw.Draw(c)
for u in range((u0 // 50 + 1) * 50, u1, 50):
    d.text(((u - u0) * Z + 2, 1), str(u), fill=(200, 0, 0), font=f)
for v in range((v0 // 50 + 1) * 50, v1, 50):
    d.text((2, (v - v0) * Z + 1), str(v), fill=(0, 0, 200), font=f)
c.save(out)
