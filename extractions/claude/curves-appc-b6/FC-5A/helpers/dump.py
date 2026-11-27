"""Print a page region as ASCII ('#' dark, '.' light) with u and v labels, for reading pixels.
usage: dump.py image u0 v0 u1 v1"""
import sys
import numpy as np
from PIL import Image
img, u0, v0, u1, v1 = sys.argv[1], *map(int, sys.argv[2:6])
g = np.asarray(Image.open(img).convert("L"))
sub = g[v0:v1, u0:u1] < 128
hdr1 = "".join(str((u // 100) % 10) if u % 10 == 0 else " " for u in range(u0, u1))
hdr2 = "".join(str((u // 10) % 10) if u % 10 == 0 else ("|" if u % 5 == 0 else " ") for u in range(u0, u1))
print("      " + hdr1)
print("      " + hdr2)
for i, row in enumerate(sub):
    print(f"{v0 + i:5d} " + "".join("#" if b else "." for b in row))
