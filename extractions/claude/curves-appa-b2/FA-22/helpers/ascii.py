"""Print the page around (u, v): '#' ink, '|' ink on vertical grid runs, '=' ink on horizontal grid
runs, '.' white; a '^' row marks u. Usage: python ascii.py u v [hu hv]"""
import sys
import numpy as np
import fa22lib as L
INK = L.page() < 128
VL = np.load(L.OUT / "helpers" / "vline.npy"); HL = np.load(L.OUT / "helpers" / "hline.npy")
u, v = int(round(float(sys.argv[1]))), int(round(float(sys.argv[2])))
hu = int(sys.argv[3]) if len(sys.argv) > 3 else 22; hv = int(sys.argv[4]) if len(sys.argv) > 4 else 14
print("      " + "".join(str((c // 10) % 10) if c % 10 == 0 else " " for c in range(u - hu, u + hu + 1)))
for r in range(v - hv, v + hv + 1):
    row = "".join("=" if HL[r, c] else "|" if VL[r, c] else "#" if INK[r, c] else "." for c in range(u - hu, u + hu + 1))
    print(f"{r:5d}{'>' if r == v else ' '}{row}")
print("      " + "".join("^" if c == u else ("+" if c % 10 == 0 else " ") for c in range(u - hu, u + hu + 1)))
