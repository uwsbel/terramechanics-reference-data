"""Crop with straight rulers through chosen dots, extended, to see a bend by eye."""
import sys
from PIL import Image, ImageDraw
u0, v0, u1, v1, z = 1350, 1800, 1950, 3000, 2
im = Image.open("packet/p0109.png").convert("RGB").crop((u0, v0, u1, v1)).resize(((u1-u0)*z, (v1-v0)*z), Image.NEAREST)
d = ImageDraw.Draw(im)
def ruler(a, b, ext, col):
    (ua, va), (ub, vb) = a, b
    for t0, t1 in ((-ext, 1 + ext),):
        p = [((ua + t*(ub-ua) - u0)*z, (va + t*(vb-va) - v0)*z) for t in (t0, t1)]
        d.line(p, fill=col, width=1)
ruler((1876.5, 2902.8), (1664.2, 2361.6), 0.9, (255, 0, 0))     # dots at x 3.0 and 4.75, extended
ruler((1637.0, 2299.4), (1436.1, 1905.6), 0.6, (0, 160, 0))     # dots at x 4.95 and 6.24, extended
im.save("out/F2-48/check/ruler.png")
