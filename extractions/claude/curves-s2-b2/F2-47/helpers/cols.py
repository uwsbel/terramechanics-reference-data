"""Print dark runs (threshold 128) of page columns: cols.py v0 v1 u1 u2 ... (F2-47 helper)."""
import sys
import numpy as np
from PIL import Image
img = np.array(Image.open('packet/p0108.png').convert('L')) < 128
v0, v1 = int(sys.argv[1]), int(sys.argv[2])
for u in [int(s) for s in sys.argv[3:]]:
    col = img[v0:v1, u]; out = []; i = 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]: j += 1
            out.append(f"{v0+i}-{v0+j-1}({j-i})"); i = j
        else: i += 1
    print(u, ' '.join(out))
