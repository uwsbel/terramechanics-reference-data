"""Text crop of the page at 1:1: '#' dark (< dark), '.' light. Rows labeled with v, a ruler of u
on top (tens digit row and units digit row). usage: ascii.py <image> u0 v0 u1 v1 [dark=128]"""
import sys
import numpy as np
from PIL import Image
img = sys.argv[1]; u0, v0, u1, v1 = map(int, sys.argv[2:6]); dark = int(sys.argv[6]) if len(sys.argv) > 6 else 128
g = np.asarray(Image.open(img).convert("L"))
us = range(u0, u1)
print("      " + "".join(str((u // 100) % 10) for u in us))
print("      " + "".join(str((u // 10) % 10) for u in us))
print("      " + "".join(str(u % 10) for u in us))
for v in range(v0, v1):
    print(f"{v:5d} " + "".join("#" if g[v, u] < dark else "." for u in us))
