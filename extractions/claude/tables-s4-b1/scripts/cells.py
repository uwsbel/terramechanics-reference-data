"""Make a contact sheet of single cells, upright, zoom with NEAREST (raw pixels), each labeled.
Usage: cells.py out.png zoom 'label:u0,v0,u1,v1' ..."""
import sys
from PIL import Image, ImageDraw, ImageFont
out, zoom = sys.argv[1], int(sys.argv[2])
src = Image.open("packet/p0193.png").convert("RGB")
try:
    font = ImageFont.truetype("arial.ttf", 16)
except OSError:
    font = ImageFont.load_default()
tiles = []
for spec in sys.argv[3:]:
    lab, box = spec.split(":")
    u0, v0, u1, v1 = map(int, box.split(","))
    t = src.crop((u0, v0, u1, v1)).transpose(Image.ROTATE_270)
    t = t.resize((t.width * zoom, t.height * zoom), Image.NEAREST)
    canvas = Image.new("RGB", (t.width + 10, t.height + 26), (235, 235, 235))
    canvas.paste(t, (5, 24))
    ImageDraw.Draw(canvas).text((5, 3), f"{lab}  u{u0}-{u1} v{v0}-{v1}", fill=(200, 0, 0), font=font)
    tiles.append(canvas)
W = max(t.width for t in tiles); H = sum(t.height for t in tiles)
sheet = Image.new("RGB", (W, H), (255, 255, 255))
y = 0
for t in tiles:
    sheet.paste(t, (0, y)); y += t.height
sheet.save(out); print(out, W, H)
