"""ASCII dump of a page region (u0 u1 v0 v1): '#' dark (<100), '+' (<160), '.' (<220). Reader's aid."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
WS = Path(__file__).resolve().parents[3]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
u0, u1, v0, v1 = map(int, sys.argv[1:5])
print("      " + "".join(str((u // 10) % 10) if u % 10 == 0 else ("|" if u % 5 == 0 else " ") for u in range(u0, u1)))
for v in range(v0, v1):
    print(f"{v:5d} " + "".join("#" if p < 100 else ("+" if p < 160 else ("." if p < 220 else " ")) for p in g[v, u0:u1]))
