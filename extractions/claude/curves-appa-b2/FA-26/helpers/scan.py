"""Dark runs of curve ink (grid greyed out by clean2.py) along rows or columns of the page image.
usage: scan.py rows v0 v1 step u0 u1   |   scan.py cols u0 u1 step v0 v1
Each run: start-end (centre). Runs of grid-only ink are left out; '*' marks a run touching grid ink."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
base = Path(__file__).resolve().parents[1]
g = np.array(Image.open(base.parents[1] / "packet" / "p0054.png").convert("L")) < 128
U0, V0 = 520, 2050
gm = np.load(base / "helpers" / "gridmask.npy")
grid = np.zeros_like(g); grid[V0:V0 + gm.shape[0], U0:U0 + gm.shape[1]] = gm
curve = g & ~grid
mode, a0, a1, st, b0, b1 = sys.argv[1], *map(int, sys.argv[2:7])
for a in range(a0, a1 + 1, st):
    line = curve[a, b0:b1 + 1] if mode == "rows" else curve[b0:b1 + 1, a]
    idx = np.where(line)[0]
    runs = []
    if len(idx):
        s = p = idx[0]
        for i in list(idx[1:]) + [None]:
            if i is None or i != p + 1:
                runs.append((s + b0, p + b0)); s = i
            p = i if i is not None else p
    txt = "  ".join(f"{s}-{e}({(s+e)/2:.0f})" for s, e in runs if e - s >= 1)
    print(f"{a}: {txt}")
