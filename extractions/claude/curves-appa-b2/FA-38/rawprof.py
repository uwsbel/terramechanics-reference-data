"""Reader helper: raw ink runs on rows around a sample row; runs lying entirely within a grid column (+-1 px)
are dropped and listed as grid; rows on a horizontal grid line are skipped. usage: rawprof.py k [half] [hu] [ushift]"""
import sys
import numpy as np
from PIL import Image
from calmap import c, v_of_g, IMAGE
from rowprof_lib import gridcols, is_gridrow
G = np.asarray(Image.open(IMAGE).convert("L")) < 128
k = int(sys.argv[1]); hr = int(sys.argv[2]) if len(sys.argv) > 2 else 8
hu = int(sys.argv[3]) if len(sys.argv) > 3 else 55; ush = int(sys.argv[4]) if len(sys.argv) > 4 else 0
gs = 10 ** (0.05 * k); v = 2000.0
for _ in range(5): v = v_of_g(gs, c(v))
vt = int(round(v)); uc = int(round(c(v))) + ush; a, b = uc - hu, uc + hu
gc = gridcols(a, b, vt)
print(f"== k {k} g {gs:.4f} v_target {v:.2f} (at u {uc}); grid cols " + " ".join(f"{p}-{q}" for p, q in gc))
for vv in range(vt - hr, vt + hr + 1):
    if is_gridrow(vv): print(f"  v {vv} G"); continue
    row = G[vv, a:b]; out, s = [], None
    for i, d in enumerate(list(row) + [False]):
        if d and s is None: s = i
        if not d and s is not None:
            p, q = a + s, a + i - 1; s = None
            if any(p >= gp - 1 and q <= gq + 1 for gp, gq in gc): continue
            tag = "*" if any(not (q < gp or p > gq) for gp, gq in gc) else ""
            out.append(f"{p}-{q}({q - p + 1}){tag}")
    print(f"  v {vv}   " + " ".join(out))
