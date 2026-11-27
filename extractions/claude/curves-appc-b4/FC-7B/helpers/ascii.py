import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"))
u0, v0, u1, v1 = map(int, sys.argv[2:6])
print("      " + "".join(str((u // 10) % 10) if u % 10 == 0 else " " for u in range(u0, u1)))
print("      " + "".join(str(u % 10) for u in range(u0, u1)))
for v in range(v0, v1):
    print(f"{v:5d} " + "".join("#" if g[v, u] < 128 else "." for u in range(u0, u1)))
