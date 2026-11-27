"""Grid row and column bands of page 54 near the curves (same rules as clean2.py), saved to gridbands.json."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
base = Path(__file__).resolve().parents[1]
g = np.array(Image.open(base.parents[1] / "packet" / "p0054.png").convert("L")) < 128
U0, U1, V0, V1 = 520, 2045, 2050, 3100
def bands(flags, off):
    idx = np.where(flags)[0]; out = []
    if len(idx) == 0: return out
    s = p = idx[0]
    for i in list(idx[1:]) + [None]:
        if i is None or i != p + 1:
            out.append((int(s + off), int(p + off))); s = i
        p = i if i is not None else p
    return out
segs = [(a, min(a + 300, U1)) for a in range(U0, U1, 300)]
cand = np.array([g[V0:V1, a:b].mean(axis=1) > 0.33 for a, b in segs])
rows = bands(cand.sum(axis=0) >= 3, V0)
fc = g[1230:2100, U0:U1].mean(axis=0)
cols = bands(fc > 0.2, U0)
(base / "helpers" / "gridbands.json").write_text(json.dumps({"rows": rows, "cols": cols}), encoding="utf-8")
print("rows", rows)
print("cols", cols)
