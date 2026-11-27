"""Raw ink runs (grid included) along columns (c) or rows (r) near a position; grid bands listed for reference.
usage: rawruns.py c u v0 v1 [du...]   |   rawruns.py r v u0 u1 [dv...]"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
base = Path(__file__).resolve().parents[1]
g = np.array(Image.open(base.parents[1] / "packet" / "p0054.png").convert("L")) < 128
gb = json.loads((base / "helpers" / "gridbands.json").read_text())
mode, a, b0, b1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
offs = [int(x) for x in sys.argv[5:]] or [-4, -2, 0, 2, 4]
def runs(line, off):
    idx = np.where(line)[0]; out = []
    if len(idx):
        s = p = idx[0]
        for i in list(idx[1:]) + [None]:
            if i is None or i != p + 1:
                out.append((int(s + off), int(p + off))); s = i
            p = i if i is not None else p
    return out
bands = gb["rows"] if mode == "c" else gb["cols"]
print("grid", " ".join(f"{x}-{y}" for x, y in bands if b0 - 3 <= y and x <= b1 + 3))
for d in offs:
    p = a + d
    line = g[b0:b1 + 1, p] if mode == "c" else g[p, b0:b1 + 1]
    print(f"{p}: " + " ".join(f"{s}-{e}" for s, e in runs(line, b0)))
