import numpy as np
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
# fraction of ink per row in two windows away from most curve ink: u 1510..1580 and 1960..2020 are not enough; use whole width
fr = g[:, 745:2175].mean(axis=1)
rows = [v for v in range(1150, 3750) if fr[v] > 0.30]
# merge into runs
out = []
s = p = None
for v in rows:
    if s is None: s = p = v; continue
    if v == p + 1: p = v; continue
    out.append((s, p)); s = p = v
out.append((s, p))
print(" ".join(f"{a}-{b}({fr[a:b+1].max():.2f})" for a, b in out))
