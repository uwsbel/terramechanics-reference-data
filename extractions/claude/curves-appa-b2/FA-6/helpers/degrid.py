"""Visual aid only: a copy of the page with grid-line ink erased where the line passes through white
(pixels just beyond the line on both sides are white), so the drawn curves stand out. Lines are found per
window as rows/columns whose dark fraction exceeds a threshold. Erased pixels are drawn light grey,
so nothing is hidden. Pixel coordinates unchanged. Not used for any value."""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
U0, V0, U1, V1 = 778, 1120, 2275, 3762
WIN, THR, GAP = 160, 0.45, 2
g = np.asarray(Image.open(src).convert("L"))
dark = g < 128
erase = np.zeros_like(dark)

def runs(idx):
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

# horizontal lines, windows along u
for u in range(U0, U1, WIN // 2):
    ua, ub = u, min(u + WIN, U1)
    frac = dark[V0:V1, ua:ub].mean(axis=1)
    for s, e in runs(np.where(frac >= THR)[0]):
        s += V0; e += V0
        if e - s > 14:
            continue
        above = dark[max(s - GAP - 1, 0), ua:ub] | dark[max(s - GAP, 0), ua:ub]
        below = dark[e + GAP, ua:ub] | dark[e + GAP + 1, ua:ub]
        clear = ~above & ~below
        cols = np.arange(ua, ub)[clear]
        erase[s - 1:e + 2, cols] |= True
# vertical lines, windows along v
for v in range(V0, V1, WIN // 2):
    va, vb = v, min(v + WIN, V1)
    frac = dark[va:vb, U0:U1].mean(axis=0)
    for s, e in runs(np.where(frac >= THR)[0]):
        s += U0; e += U0
        if e - s > 14:
            continue
        left = dark[va:vb, max(s - GAP - 1, 0)] | dark[va:vb, max(s - GAP, 0)]
        right = dark[va:vb, e + GAP] | dark[va:vb, e + GAP + 1]
        clear = ~left & ~right
        rows = np.arange(va, vb)[clear]
        erase[rows, s - 1:e + 2] |= True
out = np.where(dark & ~erase, 0, 255).astype(np.uint8)
rgb = np.stack([out] * 3, axis=-1)
rgb[dark & erase] = (215, 215, 215)
Image.fromarray(rgb).save(dst)
print("wrote", dst)
