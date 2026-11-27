"""Contact sheet of small zoomed crops around approximate marker positions, each with a fine
labeled pixel grid (minor every 5 px, labeled every 10 px), so marker extents can be read by eye.
python sheet.py <image> <out.png> --half 35 --zoom 4 --cols 4 "label:u,v" ..."""
import argparse
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("image"); ap.add_argument("out")
ap.add_argument("--half", type=int, default=35)
ap.add_argument("--zoom", type=int, default=4)
ap.add_argument("--cols", type=int, default=4)
ap.add_argument("items", nargs="+")
a = ap.parse_args()
im = Image.open(a.image).convert("RGB")
try:
    font = ImageFont.truetype("arial.ttf", 13)
except OSError:
    font = ImageFont.load_default()
h, z = a.half, a.zoom
cell = 2 * h * z
pad_l, pad_t = 44, 34
W = a.cols * (cell + pad_l + 6)
rows = (len(a.items) + a.cols - 1) // a.cols
H = rows * (cell + pad_t + 6)
sheet = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(sheet)
for k, it in enumerate(a.items):
    lab, uv = it.split(":")
    u, v = [int(round(float(t))) for t in uv.split(",")]
    u0, v0 = u - h, v - h
    c = im.crop((u0, v0, u0 + 2 * h, v0 + 2 * h)).resize((cell, cell), Image.NEAREST)
    cd = ImageDraw.Draw(c)
    for t in range(0, 2 * h + 1):
        if (u0 + t) % 5 == 0:
            x = t * z
            col = (255, 0, 0) if (u0 + t) % 10 == 0 else (255, 170, 170)
            cd.line([(x, 0), (x, cell)], fill=col, width=1)
        if (v0 + t) % 5 == 0:
            y = t * z
            col = (0, 0, 255) if (v0 + t) % 10 == 0 else (170, 170, 255)
            cd.line([(0, y), (cell, y)], fill=col, width=1)
    r, q = divmod(k, a.cols)
    ox, oy = q * (cell + pad_l + 6) + pad_l, r * (cell + pad_t + 6) + pad_t
    sheet.paste(c, (ox, oy))
    d.text((ox, oy - 32), lab, fill=(0, 0, 0), font=font)
    for t in range(0, 2 * h + 1):
        if (u0 + t) % 10 == 0 and (u0 + t) % 20 == 0:
            d.text((ox + t * z - 12, oy - 16), str(u0 + t), fill=(200, 0, 0), font=font)
        if (v0 + t) % 10 == 0 and (v0 + t) % 20 == 0:
            d.text((ox - 42, oy + t * z - 7), str(v0 + t), fill=(0, 0, 200), font=font)
sheet.save(a.out)
print(f"wrote {a.out} {sheet.size}")
