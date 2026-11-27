"""Runs along a row (v fixed) or column (u fixed) and its neighbours.
Usage: cutruns.py row|col center lo hi [offsets]  (offsets comma list, default -6,-4,-2,0,2,4,6)"""
import sys
import numpy as np
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
mode, c, lo, hi = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
offs = [int(x) for x in (sys.argv[5].split(",") if len(sys.argv) > 5 else "-6,-4,-2,0,2,4,6".split(","))]
for o in offs:
    a = int(round(c + o))
    line = g[a, lo:hi + 1] if mode == "row" else g[lo:hi + 1, a]
    runs, s = [], None
    for i, d in enumerate(line):
        if d and s is None: s = i
        if not d and s is not None: runs.append((lo + s, lo + i - 1)); s = None
    if s is not None: runs.append((lo + s, hi))
    print(f"{'*' if o == 0 else ' '}{a}: " + " ".join(f"{x}-{y}" for x, y in runs))
