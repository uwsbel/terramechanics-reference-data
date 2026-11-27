"""Reader helper: for each sample row k in k0..k1, a crop of +-hv px around the row (zoom z), u window
centred on the curves (+-hu), with the sample row in cyan and a pixel scale (ticks every 2 px, labels every
10 px, light guide lines every 10 px); crops stacked into one image. Optional points CSV overlaid.
usage: rowcrops.py k0 k1 out.png [z] [hu] [hv] [points.csv] [ushift]"""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw
from calmap import c, v_of_g, IMAGE
k0, k1 = int(sys.argv[1]), int(sys.argv[2]); out = sys.argv[3]
z = int(sys.argv[4]) if len(sys.argv) > 4 else 6
hu = int(sys.argv[5]) if len(sys.argv) > 5 else 55
hv = int(sys.argv[6]) if len(sys.argv) > 6 else 14
pts = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7] != "-" else None
ush = int(sys.argv[8]) if len(sys.argv) > 8 else 0
G = np.asarray(Image.open(IMAGE).convert("L"))
P = []
if pts:
    with open(pts, encoding="utf-8-sig") as f: P = list(csv.DictReader(f))
tiles = []
for k in range(k1, k0 - 1, -1):
    gs = 10 ** (0.05 * k); v = 2000.0
    for _ in range(5): v = v_of_g(gs, c(v))
    uc = int(round(c(v))) + ush; vc = int(round(v))
    u0, u1, v0, v1 = uc - hu, uc + hu, vc - hv, vc + hv
    g = G[v0:v1, u0:u1]
    rgb = np.stack([g] * 3, -1).astype(np.uint8)
    rgb[g < 128] = (40, 40, 40)
    im = Image.fromarray(rgb).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for u in range(u0, u1):
        x = (u - u0) * z
        if u % 10 == 0:
            d.line([(x, 0), (x, im.height)], fill=(255, 150, 150)); d.text((x + 2, 2), str(u), fill=(220, 0, 0))
        elif u % 2 == 0:
            d.line([(x, 0), (x, 5)], fill=(255, 0, 0)); d.line([(x, im.height - 5), (x, im.height)], fill=(255, 0, 0))
    for vv in range(v0, v1):
        y = (vv - v0) * z
        if vv % 10 == 0:
            d.line([(0, y), (im.width, y)], fill=(150, 150, 255)); d.text((2, y + 1), str(vv), fill=(0, 0, 220))
        elif vv % 2 == 0:
            d.line([(0, y), (5, y)], fill=(0, 0, 255)); d.line([(im.width - 5, y), (im.width, y)], fill=(0, 0, 255))
    ya, yb = (v_of_g(gs, u0) - v0) * z, (v_of_g(gs, u1) - v0) * z
    d.line([(0, ya), (im.width, yb)], fill=(0, 210, 240), width=2)
    d.text((im.width - 140, max(ya - 14, 0)), f"k{k} g={gs:.4f} v={v:.1f}", fill=(0, 140, 200))
    colors = {"average": (0, 190, 0), "upper": (255, 0, 0), "lower": (0, 110, 255)}
    for r in P:
        x, y = (float(r["pixel_u"]) - u0) * z, (float(r["pixel_v"]) - v0) * z
        if 0 <= x < im.width and 0 <= y < im.height:
            cl = colors.get(r["series_id"], (255, 140, 0)); bu, bv = float(r["u_bound_px"]) * z, float(r["v_bound_px"]) * z
            d.rectangle([x - bu, y - bv, x + bu, y + bv], outline=cl, width=2)
            d.line([(x, y - 6), (x, y + 6)], fill=cl, width=3)
    tiles.append(im)
W = max(t.width for t in tiles); H = sum(t.height + 6 for t in tiles)
canvas = Image.new("RGB", (W, H), (255, 255, 255)); y = 0
for t in tiles:
    canvas.paste(t, (0, y)); y += t.height + 6
canvas.save(out); print("wrote", out, canvas.size)
