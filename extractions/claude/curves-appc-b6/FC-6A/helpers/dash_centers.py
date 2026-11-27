"""Measured centers of a line's ink by column (run within +-win px of the fitted line), with the
offset from the fit, for u in [u0, u1]. Reader's aid to check dashed parts against the solid fit."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
fits = json.loads((HERE / "fit_lines.json").read_text())
name = sys.argv[1]; u0, u1 = int(sys.argv[2]), int(sys.argv[3]); win = int(sys.argv[4]) if len(sys.argv) > 4 else 12
a, b = fits[name]
for u in range(u0, u1 + 1):
    vp = a + b * u
    lo, hi = int(vp) - win, int(vp) + win + 1
    col = g[lo:hi, u] < 160
    idx = np.where(col)[0]
    runs = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                runs.append((s, p)); s = i
            p = i
        runs.append((s, p))
    print(f"u {u} fit {vp:.1f}: " + " ".join(f"[{lo+s}-{lo+p} c{lo+(s+p)/2:.1f} d{lo+(s+p)/2-vp:+.1f}]" for s, p in runs))
