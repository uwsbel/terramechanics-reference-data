"""Print, for each tick of FB-6, the ink run across the tick at every step along it (from the frame
centre line inward), so the stub's extent, width and tilt can be seen."""
import sys
import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128
LEFT = (603.97, 0.03117)     # u = c + k v
BOTTOM = (4052.17, -0.02779) # v = c + k u
ytick_v = [1096, 1364, 1633, 1900, 2168, 2432, 2699, 2968, 3234, 3498, 3764]
xtick_u = [996, 1262, 1530, 1798, 2066, 2334]

def runs(idx):
    return np.split(idx, np.where(np.diff(idx) != 1)[0] + 1) if len(idx) else []

which = sys.argv[2]
if which == "y":
    for v0 in ytick_v:
        uf = LEFT[0] + LEFT[1] * v0
        out = []
        for d in range(0, 46, 3):
            u = int(round(uf + d))
            col = dark[v0 - 14:v0 + 15, u]
            rs = runs(np.where(col)[0])
            out.append(f"{d}:" + "/".join(f"{v0 - 14 + (r[0] + r[-1]) / 2:.1f}w{len(r)}" for r in rs))
        print(f"tick v~{v0} (frame u {uf:.1f}): " + "  ".join(out))
else:
    for u0 in xtick_u:
        vf = BOTTOM[0] + BOTTOM[1] * u0
        out = []
        for d in range(0, 46, 3):
            v = int(round(vf - d))
            row = dark[v, u0 - 14:u0 + 15]
            rs = runs(np.where(row)[0])
            out.append(f"{d}:" + "/".join(f"{u0 - 14 + (r[0] + r[-1]) / 2:.1f}w{len(r)}" for r in rs))
        print(f"tick u~{u0} (frame v {vf:.1f}): " + "  ".join(out))
