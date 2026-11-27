"""Visual aid: for a column u (a fixed percent), a crop of the page around the band (u +- DU, v0..v1) at zoom Z,
left: page as scanned, right: de-gridded aid lightly smoothed; the column marked by two short red ticks at
the top and bottom, a labelled tick scale every 5 px in v and 10 px in u."""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
WS = sys.argv[1]; u = int(sys.argv[2]); v0, v1 = int(sys.argv[3]), int(sys.argv[4]); out = sys.argv[5]
DU, Z = int(sys.argv[6]) if len(sys.argv) > 6 else 50, 5
pg = Image.open(WS + "/packet/p0014.png").convert("L")
dg = Image.open(WS + "/out/FA-6/degrid.png").convert("L").filter(ImageFilter.GaussianBlur(0.6))
box = (u - DU, v0, u + DU, v1)
W, H = (box[2] - box[0]) * Z, (box[3] - box[1]) * Z
canvas = Image.new("RGB", (2 * W + 70, H + 20), (255, 255, 255))
for k, im in enumerate((pg, dg)):
    c = im.crop(box).resize((W, H), Image.NEAREST if k == 0 else Image.LANCZOS).convert("RGB")
    d = ImageDraw.Draw(c)
    x = DU * Z
    d.line([(x, 0), (x, 12)], fill=(255, 0, 0), width=2); d.line([(x, H - 12), (x, H)], fill=(255, 0, 0), width=2)
    for vv in range((v0 // 5 + 1) * 5, v1, 5):
        y = (vv - v0) * Z
        d.line([(0, y), (8 if vv % 10 else 16, y)], fill=(0, 0, 255), width=1)
        d.line([(W - (8 if vv % 10 else 16), y), (W, y)], fill=(0, 0, 255), width=1)
    for uu in range(((u - DU) // 10 + 1) * 10, u + DU, 10):
        xx = (uu - u + DU) * Z
        d.line([(xx, H - 6), (xx, H)], fill=(255, 0, 0))
    canvas.paste(c, (k * (W + 70), 0))
d = ImageDraw.Draw(canvas)
try:
    f = ImageFont.truetype("arial.ttf", 13)
except OSError:
    f = ImageFont.load_default()
for vv in range((v0 // 10 + 1) * 10, v1, 10):
    d.text((W + 8, (vv - v0) * Z - 7), str(vv), fill=(0, 0, 200), font=f)
d.text((5, H + 3), f"u={u} (red ticks); page left, de-gridded right; u ticks every 10 from {((u - DU)//10+1)*10}", fill=(0, 0, 0), font=f)
canvas.save(out)
