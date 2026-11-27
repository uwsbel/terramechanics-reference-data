"""Ink runs per row (or per column) of the bilevel page.
Usage: runs.py image row|col lo hi a0 a1 [step]
  row: for v in a0..a1 list runs in u over [lo, hi]; col: for u in a0..a1 list runs in v over [lo, hi]."""
import sys
import numpy as np
from PIL import Image
img, mode = sys.argv[1], sys.argv[2]
lo, hi, a0, a1 = map(int, sys.argv[3:7])
step = int(sys.argv[7]) if len(sys.argv) > 7 else 1
g = np.asarray(Image.open(img).convert("L")) < 128
prev = None
for a in range(a0, a1 + 1, step):
    line = g[a, lo:hi + 1] if mode == "row" else g[lo:hi + 1, a]
    runs, s = [], None
    for i, d in enumerate(line):
        if d and s is None:
            s = i
        if not d and s is not None:
            runs.append((lo + s, lo + i - 1)); s = None
    if s is not None:
        runs.append((lo + s, hi))
    txt = " ".join(f"{x}-{y}" for x, y in runs)
    if txt != prev:
        print(f"{a}: {txt}")
    prev = txt
