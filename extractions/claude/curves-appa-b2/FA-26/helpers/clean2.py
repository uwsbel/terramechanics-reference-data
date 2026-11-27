"""A view of the curve region with the printed grid greyed out, to tell the three curves apart.

Only an aid for seeing: every reading is made on the original page image. A dark pixel is taken as
grid when it lies in a grid row band (or column band) and its run across that band does not extend
beyond the band by more than 1 px: a curve crossing a grid line keeps its pixels, since its ink runs
on beyond the line. Row bands: rows dark over more than a third of a 300 px stretch of u in at least
3 of the 5 stretches; column bands: columns dark over a fifth of v 1230 to 2100, where no curve is."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

base = Path(__file__).resolve().parents[1]
page = base.parents[1] / "packet" / "p0054.png"
g = np.array(Image.open(page).convert("L")) < 128
H, W = g.shape
U0, U1, V0, V1 = 520, 2045, 2050, 3100

def bands(flags):
    idx = np.where(flags)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s, p)); s = i
        p = i
    out.append((s, p))
    return out

grid = np.zeros_like(g)
segs = [(a, min(a + 300, U1)) for a in range(U0, U1, 300)]
cand = np.array([g[V0:V1, a:b].mean(axis=1) > 0.33 for a, b in segs])
spans = (np.convolve(cand.sum(axis=0) >= 3, np.ones(3), "same") > 0)  # a row dark in 3 stretches, +-1 for tilt
for k, (a, b) in enumerate(segs):
    for r0, r1 in bands(cand[k] & spans):
        r0, r1 = r0 + V0, r1 + V0
        for u in range(a, b):
            col = g[:, u]
            for v in range(r0, r1 + 1):
                if col[v]:
                    # vertical run through (u, v)
                    t = v
                    while t > 0 and col[t - 1]:
                        t -= 1
                    bt = v
                    while bt < H - 1 and col[bt + 1]:
                        bt += 1
                    if t >= r0 - 1 and bt <= r1 + 1:
                        grid[t:bt + 1, u] = True
fc = g[1230:2100, U0:U1].mean(axis=0)
for c0, c1 in bands(fc > 0.2):
    c0, c1 = c0 + U0, c1 + U0
    for v in range(V0, V1):
        row = g[v]
        for u in range(c0, c1 + 1):
            if row[u]:
                l = u
                while l > 0 and row[l - 1]:
                    l -= 1
                r = u
                while r < W - 1 and row[r + 1]:
                    r += 1
                if l >= c0 - 1 and r <= c1 + 1:
                    grid[v, l:r + 1] = True
                break
np.save(base / "helpers" / "gridmask.npy", grid[V0:V1, U0:U1])
img = np.full(g.shape, 255, np.uint8)
img[g] = 0
img[g & grid] = 205
Image.fromarray(img).save(base / "crops" / "cleaned2.png")

def crop(box, out, zoom=4, step=10):
    u0, v0, u1, v1 = box
    im = Image.fromarray(img[v0:v1, u0:u1]).convert("RGB").resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for u in range((u0 // step + 1) * step, u1, step):
        x = (u - u0) * zoom
        d.line([(x, 0), (x, im.size[1])], fill=(255, 150, 150) if u % (4 * step) else (255, 0, 0), width=1)
        if u % (4 * step) == 0:
            d.text((x + 2, 2), str(u), fill=(255, 0, 0))
    for v in range((v0 // step + 1) * step, v1, step):
        y = (v - v0) * zoom
        d.line([(0, y), (im.size[0], y)], fill=(150, 150, 255) if v % (4 * step) else (0, 0, 255), width=1)
        if v % (4 * step) == 0:
            d.text((2, y + 2), str(v), fill=(0, 0, 255))
    im.save(out)

for spec in sys.argv[1:]:
    name, *nums = spec.split(":")
    u0, v0, u1, v1, zoom = (int(x) for x in nums)
    crop((u0, v0, u1, v1), base / "crops" / f"{name}.png", zoom)
    print("wrote", name)
