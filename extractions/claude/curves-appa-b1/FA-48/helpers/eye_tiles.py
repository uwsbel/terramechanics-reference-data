"""Label check tiles: each fitted grid line marked in red next to its printed label.
usage: eye_tiles.py <image> <calibration.json> <out_prefix> <u_ylabels_left> <v_xlabels_top>"""
import json, sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert("RGB")
cal = json.load(open(sys.argv[2]))
pre, uy, vx = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
tiles = []
for l in cal["horizontal_lines"]:
    v = l["v_at_u0"] + l["slope_dv_du"] * (uy + 80)
    t = im.crop((uy, int(v) - 40, uy + 160, int(v) + 40)).resize((480, 240), Image.NEAREST)
    d = ImageDraw.Draw(t); y = (v - (int(v) - 40)) * 3
    d.line([(0, y), (60, y)], fill=(255, 0, 0), width=1); d.text((2, 2), "y=%g v=%.0f" % (l["y_value"], v), fill=(255, 0, 0))
    tiles.append(t)
out = Image.new("RGB", (480, sum(t.height for t in tiles)), "white"); y = 0
for t in tiles:
    out.paste(t, (0, y)); y += t.height
out.save(pre + "-ylabels.png")
tiles = []
for l in cal["vertical_lines"]:
    u = l["u_at_v0"] + l["slope_du_dv"] * (vx + 70)
    t = im.crop((int(u) - 60, vx, int(u) + 60, vx + 140)).resize((360, 420), Image.NEAREST)
    d = ImageDraw.Draw(t); x = (u - (int(u) - 60)) * 3
    d.line([(x, 300), (x, 420)], fill=(255, 0, 0), width=1); d.text((2, 2), "x=%g u=%.0f" % (l["x_value"], u), fill=(255, 0, 0))
    tiles.append(t)
out = Image.new("RGB", (360 * len(tiles), 420), "white")
for i, t in enumerate(tiles):
    out.paste(t, (360 * i, 0))
out.save(pre + "-xlabels.png")
print("ok")
