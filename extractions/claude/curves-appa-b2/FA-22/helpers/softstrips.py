"""Stack soft-rendered crops (Gaussian blur, bicubic zoom) with a 10 px grid (labelled every 50 px).
Viewing aid only. Usage: python softstrips.py out zoom blur label:u0:v0:u1:v1 ..."""
import sys
from PIL import Image, ImageDraw, ImageFilter
import fa22lib as L
out, z, r = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
page = Image.open(L.PAGE).convert("L")
tiles = []
for s in sys.argv[4:]:
    lab, u0, v0, u1, v1 = s.split(":"); u0, v0, u1, v1 = int(u0), int(v0), int(u1), int(v1)
    t = page.crop((u0 - 5, v0 - 5, u1 + 5, v1 + 5)).filter(ImageFilter.GaussianBlur(r)).crop((5, 5, 5 + u1 - u0, 5 + v1 - v0))
    t = t.resize((int((u1 - u0) * z), int((v1 - v0) * z)), Image.BICUBIC).convert("RGB")
    d = ImageDraw.Draw(t)
    for u in range(u0 - u0 % 10 + 10, u1, 10):
        x = (u - u0) * z
        d.line([(x, 0), (x, 6 if u % 50 else 14)], fill=(255, 0, 0), width=1)
        d.line([(x, t.size[1] - (6 if u % 50 else 14)), (x, t.size[1])], fill=(255, 0, 0), width=1)
        if u % 50 == 0: d.text((x + 2, 12), str(u), fill=(220, 0, 0))
    for v in range(v0 - v0 % 10 + 10, v1, 10):
        y = (v - v0) * z
        d.line([(0, y), (6 if v % 50 else 14, y)], fill=(0, 0, 255), width=1)
        d.line([(t.size[0] - (6 if v % 50 else 14), y), (t.size[0], y)], fill=(0, 0, 255), width=1)
        if v % 50 == 0: d.text((16, y - 6), str(v), fill=(0, 0, 220))
    d.rectangle([0, 0, 7 * len(lab) + 6, 11], fill=(255, 255, 160)); d.text((3, 0), lab, fill=(0, 0, 0))
    tiles.append(t)
W = max(t.size[0] for t in tiles); H = sum(t.size[1] + 6 for t in tiles)
M = Image.new("RGB", (W, H), (90, 90, 90)); y = 0
for t in tiles:
    M.paste(t, (0, y)); y += t.size[1] + 6
M.save(out); print("wrote", out, M.size)
