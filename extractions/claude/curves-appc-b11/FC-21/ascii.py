import sys
import numpy as np
from PIL import Image
img, u0, u1, v0, v1 = sys.argv[1], *map(int, sys.argv[2:6])
thr = int(sys.argv[6]) if len(sys.argv) > 6 else 128
g = np.asarray(Image.open(img).convert("L"))
print("unique levels sample:", np.unique(g[v0:v1, u0:u1])[:10], len(np.unique(g[v0:v1, u0:u1])))
print("      " + "".join(str((u // 10) % 10) if u % 10 == 0 else " " for u in range(u0, u1)))
print("      " + "".join(str(u % 10) for u in range(u0, u1)))
for v in range(v0, v1):
    print(f"{v:5d} " + "".join("#" if g[v, u] < thr else "." for u in range(u0, u1)))
