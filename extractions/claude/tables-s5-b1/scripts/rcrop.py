"""Crop the clockwise-rotated page p0325 and label it with ORIGINAL scan pixel coordinates.
Rotated (x, y) maps to the original (u, v) by u = y, v = H - 1 - x, H = original height."""
import sys
from PIL import Image, ImageDraw
src = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); zoom = float(sys.argv[6]); out = sys.argv[7]
step = int(sys.argv[8]) if len(sys.argv) > 8 else 50
im = Image.open(src).convert('L')
H = im.size[1]
r = im.transpose(Image.ROTATE_270)
c = r.crop((x0, y0, x1, y1))
c = c.resize((int((x1 - x0) * zoom), int((y1 - y0) * zoom)), Image.LANCZOS).convert('RGB')
m = 40
canvas = Image.new('RGB', (c.size[0] + 2 * m, c.size[1] + 2 * m), 'white')
canvas.paste(c, (m, m))
d = ImageDraw.Draw(canvas)
for x in range((x0 // step + 1) * step, x1, step):
    px = m + (x - x0) * zoom
    d.line([(px, m - 8), (px, m)], fill='red'); d.line([(px, m + c.size[1]), (px, m + c.size[1] + 8)], fill='red')
    d.text((px - 12, 2), f"v{H - 1 - x}", fill='red'); d.text((px - 12, m + c.size[1] + 10), f"v{H - 1 - x}", fill='red')
for y in range((y0 // step + 1) * step, y1, step):
    py = m + (y - y0) * zoom
    d.line([(m - 8, py), (m, py)], fill='blue'); d.line([(m + c.size[0], py), (m + c.size[0] + 8, py)], fill='blue')
    d.text((0, py - 5), f"u{y}", fill='blue'); d.text((m + c.size[0] + 2, py - 5), f"u{y}", fill='blue')
canvas.save(out)
print(out, canvas.size)
