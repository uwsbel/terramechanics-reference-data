"""Stack zoomed rectangular crops of the page vertically, each with a pixel grid every 10 px
(labelled every 50 px in page pixels). Viewing aid only.
Usage: python strips.py <out.png> <zoom> label:u0:v0:u1:v1 ..."""
import sys
from PIL import Image, ImageDraw
import fa22lib as L
out, zoom = sys.argv[1], int(sys.argv[2])
page = Image.open(L.PAGE).convert("RGB")
tiles = []
for s in sys.argv[3:]:
    lab, u0, v0, u1, v1 = s.split(":"); u0, v0, u1, v1 = int(u0), int(v0), int(u1), int(v1)
    t = page.crop((u0, v0, u1, v1)).resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
    d = ImageDraw.Draw(t)
    for u in range(u0 - u0 % 10 + 10, u1, 10):
        x = (u - u0) * zoom
        d.line([(x, 0), (x, t.size[1])], fill=(255, 0, 0) if u % 50 == 0 else (255, 170, 170), width=1)
        if u % 50 == 0:
            d.text((x + 2, 2), str(u), fill=(220, 0, 0))
    for v in range(v0 - v0 % 10 + 10, v1, 10):
        y = (v - v0) * zoom
        d.line([(0, y), (t.size[0], y)], fill=(0, 0, 255) if v % 50 == 0 else (170, 170, 255), width=1)
        if v % 50 == 0:
            d.text((2, y + 2), str(v), fill=(0, 0, 220))
    d.rectangle([0, 0, 8 * len(lab) + 6, 12], fill=(255, 255, 200)); d.text((3, 0), lab, fill=(0, 0, 0))
    tiles.append(t)
W = max(t.size[0] for t in tiles); H = sum(t.size[1] + 6 for t in tiles)
M = Image.new("RGB", (W, H), (90, 90, 90)); y = 0
for t in tiles:
    M.paste(t, (0, y)); y += t.size[1] + 6
M.save(out); print("wrote", out, M.size)
