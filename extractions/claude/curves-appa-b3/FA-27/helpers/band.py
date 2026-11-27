"""Print the dark pixels of a plotted line's band, column by column: rows c-7 .. c+7 around the
line's centre c = a + b (u - uref). Usage: band.py <image> uref a b u0 u1"""
import sys
import numpy as np
from PIL import Image
G = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
uref, a, b = map(float, sys.argv[2:5])
for u in range(int(sys.argv[5]), int(sys.argv[6]) + 1):
    c = a + b * (u - uref)
    r0 = int(round(c)) - 7
    print(u, f"{c:.1f}", "".join("#" if G[r, u] else "." for r in range(r0, r0 + 15)))
