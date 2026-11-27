"""Column scan across the diagonal band of FC-6A: for each u, the dark runs (v center, thickness)
in v from 3888-u to 4090-u, with a flag on runs that fall on a horizontal grid line. Reader's aid."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
cal = json.loads((HERE.parent / "cal-p1" / "calibration.json").read_text())
ax, ay = cal["ax"], cal["ay"]
u0, u1, st = map(int, sys.argv[1:4])
lo = int(sys.argv[4]) if len(sys.argv) > 4 else 3888
hi = int(sys.argv[5]) if len(sys.argv) > 5 else 4090
for u in range(u0, u1 + 1, st):
    a, b = lo - u, hi - u
    col = g[a:b, u] < 160
    idx = np.where(col)[0]
    runs = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                runs.append((s, p)); s = i
            p = i
        runs.append((s, p))
    out = []
    for s, p in runs:
        c = a + (s + p) / 2
        flag = ""
        for l in cal["horizontal_lines"]:
            if abs(c - (l["v_at_u0"] + l["slope_dv_du"] * u)) < 6:
                flag = "g"
        y = ay[0] * u + ay[1] * c + ay[2]
        out.append(f"{c:.1f}/{p-s+1}{flag}(y{y:.0f})")
    x = ax[0] * u + ax[1] * (a + b) / 2 + ax[2]
    print(f"u {u} (x~{x:.0f}): " + "  ".join(out))
