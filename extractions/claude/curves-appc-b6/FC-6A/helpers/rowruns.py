"""Row runs: for each row v in [v0, v1), the dark runs (u start-end) within [u0, u1). Reader's aid."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
WS = Path(__file__).resolve().parents[3]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
u0, u1, v0, v1 = map(int, sys.argv[1:5])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 1
for v in range(v0, v1, step):
    row = g[v, u0:u1] < 160
    idx = np.where(row)[0]
    runs = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                runs.append((s, p)); s = i
            p = i
        runs.append((s, p))
    print(f"{v}: " + " ".join(f"{u0+s}-{u0+p}" for s, p in runs))
