"""ASCII dump of the bilevel page: rows v0..v1, columns u0..u1 (step s); '#' ink, '.' paper.
Usage: ascii.py image u0 u1 v0 v1 [step]"""
import sys
import numpy as np
from PIL import Image
img, u0, u1, v0, v1 = sys.argv[1], *map(int, sys.argv[2:6])
s = int(sys.argv[6]) if len(sys.argv) > 6 else 1
g = np.asarray(Image.open(img).convert("L"))
us = list(range(u0, u1 + 1, s))
# header: u every 10
hdr = "".join(("|" if u % 10 == 0 else " ") for u in us)
print("      " + hdr)
for v in range(v0, v1 + 1, s):
    print(f"{v:5d} " + "".join("#" if g[v, u] < 128 else "." for u in us))
print("u0=", u0, "each '|' marks u divisible by 10")
