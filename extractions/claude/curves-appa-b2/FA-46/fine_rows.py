"""Fine part (v 2330..3195): per row, the runs in u 2120..2205; flags rows that are grid lines
(ink continuous from u<=2140 into the band). Prints compact per-row state for A, B, C."""
import numpy as np
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
def runs(v, lo=2120, hi=2205):
    line = g[v, lo:hi + 1]; out = []; s = None
    for i, d in enumerate(line):
        if d and s is None: s = i
        if not d and s is not None: out.append((lo + s, lo + i - 1)); s = None
    if s is not None: out.append((lo + s, hi))
    return out
for v in range(2330, 3196):
    r = runs(v)
    grid = any(a <= 2135 and b >= 2145 for a, b in r)
    # band runs: those overlapping 2145..2200
    band = [(a, b) for a, b in r if b >= 2145]
    s = " ".join(f"{a}-{b}" for a, b in band)
    print(f"{v} {'G' if grid else ' '} {s}")
