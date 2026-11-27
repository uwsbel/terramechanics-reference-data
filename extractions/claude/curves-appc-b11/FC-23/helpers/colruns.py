"""Print the dark runs (v0..v1) in columns u0..u1 step s (reading aid)."""
import sys
import numpy as np
from PIL import Image
img, u0, u1, s, v0, v1 = sys.argv[1], *map(int, sys.argv[2:7])
g = np.asarray(Image.open(img).convert("L"))
d = g < 150
for u in range(u0, u1 + 1, s):
    col = d[v0:v1, u]
    runs = []
    i = 0
    while i < len(col):
        if col[i]:
            j = i
            while j + 1 < len(col) and col[j + 1]:
                j += 1
            runs.append(f"{v0+i}-{v0+j}({j-i+1})")
            i = j + 1
        else:
            i += 1
    print(u, " ".join(runs))
