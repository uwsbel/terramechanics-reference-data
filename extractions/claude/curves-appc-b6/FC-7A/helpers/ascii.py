"""Print a region of the page as ASCII ink map (# dark, . light) with u/v labels.
Usage: ascii.py image u0 v0 u1 v1 [dark]"""
import sys
import numpy as np
from PIL import Image
img = sys.argv[1]
u0, v0, u1, v1 = map(int, sys.argv[2:6])
dark = int(sys.argv[6]) if len(sys.argv) > 6 else 160
g = np.asarray(Image.open(img).convert("L"))
print("      " + "".join(str((u // 10) % 10) if u % 10 == 0 else " " for u in range(u0, u1)))
for v in range(v0, v1):
    print(f"{v:5d} " + "".join("#" if g[v, u] < dark else "." for u in range(u0, u1)))
