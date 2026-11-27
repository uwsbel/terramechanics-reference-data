"""A view of the curve region with the printed grid blanked, to tell the three curves apart.

Only an aid for seeing: every reading is made on the original page image. Grid rows are rows whose
dark fraction exceeds a threshold over a 300 px stretch of u; grid columns are columns whose dark
fraction exceeds a threshold over v 1230 to 2100, where no curve is drawn. Writes cleaned.png (page
size, white where blanked) and crops of it with a pixel grid on request."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

base = Path(__file__).resolve().parents[1]
page = base.parents[1] / "packet" / "p0054.png"
g = np.array(Image.open(page).convert("L")) < 128
H, W = g.shape
mask = np.zeros_like(g)
U0, U1, V0, V1 = 520, 2045, 2050, 3100
seg = 300
segs = [(a, min(a + seg, U1)) for a in range(U0, U1, seg)]
cand = np.array([g[V0:V1, a:b].mean(axis=1) > 0.33 for a, b in segs])   # segments x rows
# a grid row spans the plot: dark in at least 3 of the segments (a flat stretch of curve covers one or two);
# within each segment, the row (or a neighbour, for the tilt) must itself be dark there to be blanked
grid = cand.sum(axis=0) >= 3
for r in np.where(grid)[0]:
    for k, (a, b) in enumerate(segs):
        lo, hi = max(r - 2, 0), min(r + 3, cand.shape[1])
        if cand[k, lo:hi].any():
            mask[V0 + r - 1:V0 + r + 2, a:b] = True
fc = g[1230:2100, U0:U1].mean(axis=0)
cols = np.where(fc > 0.33)[0] + U0
for c in cols:
    mask[V0:V1, c - 1:c + 2] = True
clean = g & ~mask
img = np.where(clean, 0, 255).astype(np.uint8)
img[mask & g] = 200   # blanked grid ink shown light grey
Image.fromarray(img).save(base / "crops" / "cleaned.png")

def crop(box, out, zoom=3, step=10):
    u0, v0, u1, v1 = box
    im = Image.fromarray(img[v0:v1, u0:u1]).convert("RGB").resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for u in range((u0 // step + 1) * step, u1, step):
        x = (u - u0) * zoom
        d.line([(x, 0), (x, im.size[1])], fill=(255, 160, 160) if u % (4 * step) else (255, 0, 0), width=1)
        if u % (4 * step) == 0:
            d.text((x + 2, 2), str(u), fill=(255, 0, 0))
    for v in range((v0 // step + 1) * step, v1, step):
        y = (v - v0) * zoom
        d.line([(0, y), (im.size[0], y)], fill=(160, 160, 255) if v % (4 * step) else (0, 0, 255), width=1)
        if v % (4 * step) == 0:
            d.text((2, y + 2), str(v), fill=(0, 0, 255))
    im.save(out)

if len(sys.argv) > 1:
    for spec in sys.argv[1:]:
        name, *nums = spec.split(":")
        u0, v0, u1, v1, zoom = (int(x) for x in nums)
        crop((u0, v0, u1, v1), base / "crops" / f"{name}.png", zoom)
        print("wrote", name)
