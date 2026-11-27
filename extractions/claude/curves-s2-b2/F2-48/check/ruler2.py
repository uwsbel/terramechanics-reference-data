"""Rulers along the solid trace (lpt87) between 3 and 7 in."""
from PIL import Image, ImageDraw
u0, v0, u1, v1, z = 1150, 1700, 1850, 3000, 2
im = Image.open("packet/p0109.png").convert("RGB").crop((u0, v0, u1, v1)).resize(((u1-u0)*z, (v1-v0)*z), Image.NEAREST)
d = ImageDraw.Draw(im)
def ruler(a, b, ext, col):
    (ua, va), (ub, vb) = a, b
    p = [((ua + t*(ub-ua) - u0)*z, (va + t*(vb-va) - v0)*z) for t in (-ext, 1 + ext)]
    d.line(p, fill=col, width=1)
ruler((1801.5, 2918.0), (1521.5, 2362.0), 0.6, (255, 0, 0))   # samples at 3.0 and 4.75
ruler((1480.5, 2291.0), (1252.5, 1902.0), 0.5, (0, 160, 0))   # samples at 5.0 and 6.25
im.save("out/F2-48/check/ruler2.png")
