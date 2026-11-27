import sys, numpy as np
from PIL import Image
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
u0, v0, u1, v1 = map(int, sys.argv[1:5]); th = int(sys.argv[5]) if len(sys.argv) > 5 else 160
print("      " + "".join(str((u // 10) % 10) if u % 10 == 0 else " " for u in range(u0, u1 + 1)))
for v in range(v0, v1 + 1):
    print("%5d " % v + "".join("#" if g[v, u] < th else ("+" if g[v, u] < 220 else ".") for u in range(u0, u1 + 1)))
print("u0 =", u0)
