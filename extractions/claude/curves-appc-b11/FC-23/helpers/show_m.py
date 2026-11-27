"""Draw guided measurements (tracks/<name>_m.json) over a zoomed crop (reading aid).
usage: show_m.py <image> u0 v0 u1 v1 zoom out.png names"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
COL = {"rc2": (230, 0, 0), "ps": (0, 160, 0), "rs": (0, 0, 230), "rsmb": (200, 0, 200), "rsma": (230, 130, 0), "ss": (0, 170, 170)}
img, u0, v0, u1, v1, z, out = sys.argv[1], *map(int, sys.argv[2:7]), sys.argv[7]
names = sys.argv[8].split(",")
im = Image.open(img).convert("RGB").crop((u0, v0, u1, v1))
im = im.point(lambda x: 150 + x * 105 // 255)
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range((u0 // 10 + 1) * 10, u1, 10):
    d.line([((u - u0) * z, 0), ((u - u0) * z, 4 if u % 50 else 10)], fill=(0, 0, 0))
    if u % 50 == 0: d.text(((u - u0) * z + 2, 10), str(u), fill=(200, 0, 0))
for v in range((v0 // 10 + 1) * 10, v1, 10):
    d.line([(0, (v - v0) * z), (4 if v % 50 else 10, (v - v0) * z)], fill=(0, 0, 0))
    if v % 50 == 0: d.text((12, (v - v0) * z - 5), str(v), fill=(0, 0, 200))
for n in names:
    recs = json.loads((HERE.parent / "tracks" / f"{n}_m.json").read_text())
    c = COL[n]
    for r in recs:
        u = r["u"]
        if not (u0 <= u < u1): continue
        x = (u - u0 + 0.5) * z
        if "v" in r:
            y = (r["v"] - v0 + 0.5) * z
            if r["status"] == "ink":
                d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=c)
            else:
                d.rectangle([x - 2, y - 2, x + 2, y + 2], outline=c)
        elif r["status"] == "gap" and u % 3 == 0:
            y = (r["g"] - v0 + 0.5) * z
            d.point((x, y), fill=c)
im.save(out); print("wrote", out, im.size)
