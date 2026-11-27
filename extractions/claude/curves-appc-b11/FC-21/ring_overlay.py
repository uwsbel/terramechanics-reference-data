# zoomed crop with fitted ring outlines (inner r 12, outer r 18.5) drawn at given centers
import sys
from PIL import Image, ImageDraw
img, out = sys.argv[1], sys.argv[2]
u0, v0, u1, v1, z = map(int, sys.argv[3:8])
cs = [tuple(map(float, c.split(":"))) for c in sys.argv[8:]]
im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
cols = [(220, 0, 0), (0, 120, 255), (0, 160, 0)]
for i, (cu, cv) in enumerate(cs):
    x, y = (cu - u0 + 0.5) * z, (cv - v0 + 0.5) * z
    for r in (12, 18.5):
        d.ellipse([x - r * z, y - r * z, x + r * z, y + r * z], outline=cols[i % 3], width=2)
    d.line([x - 6, y, x + 6, y], fill=cols[i % 3], width=2); d.line([x, y - 6, x, y + 6], fill=cols[i % 3], width=2)
im.save(out)
