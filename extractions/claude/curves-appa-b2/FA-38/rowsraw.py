"""Reader helper: raw ink runs (grid columns marked with *) on rows v0..v1 within u window centred on c(v).
usage: rowsraw.py v0 v1 [hu] [ushift] [step]"""
import sys
import numpy as np
from PIL import Image
from calmap import c, IMAGE
from rowprof_lib import is_gridrow, gridcols
G = np.asarray(Image.open(IMAGE).convert("L")) < 128
v0, v1 = int(sys.argv[1]), int(sys.argv[2]); hu = int(sys.argv[3]) if len(sys.argv) > 3 else 40
ush = int(sys.argv[4]) if len(sys.argv) > 4 else 0; st = int(sys.argv[5]) if len(sys.argv) > 5 else 1
for v in range(v0, v1 + 1, st):
    uc = int(round(c(v))) + ush; a, b = uc - hu, uc + hu
    gc = gridcols(a, b, v)
    if is_gridrow(v): print(f"v {v} G"); continue
    row = G[v, a:b]; out, s = [], None
    for i, d in enumerate(list(row) + [False]):
        if d and s is None: s = i
        if not d and s is not None:
            p, q = a + s, a + i - 1; s = None
            if any(p >= gp - 1 and q <= gq + 1 for gp, gq in gc): continue
            tag = "*" if any(not (q < gp or p > gq) for gp, gq in gc) else ""
            out.append(f"{p}-{q}({q - p + 1}){tag}")
    print(f"v {v} [{a}..{b}] gc {' '.join(f'{p}-{q}' for p, q in gc)} | " + " ".join(out))
