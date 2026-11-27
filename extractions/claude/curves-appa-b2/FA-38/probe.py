"""Reader helper: along a predicted line u = u0 + s (v - v0), print for each row v in [v0-n, v0+n] whether there is
ink at the predicted centre (+-2 px), the run containing it (raw ink, grid cols marked), and grid-row flags.
usage: probe.py u0 v0 slope n"""
import sys
import numpy as np
from PIL import Image
from calmap import IMAGE
from rowprof_lib import is_gridrow, gridcols
G = np.asarray(Image.open(IMAGE).convert("L")) < 128
u0, v0, s, n = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
for v in range(int(v0) - n, int(v0) + n + 1):
    u = u0 + s * (v - v0); ui = int(round(u))
    hit = G[v, ui - 2:ui + 3].any()
    p = q = None
    if G[v, ui]:
        p = ui
        while G[v, p - 1]: p -= 1
        q = ui
        while G[v, q + 1]: q += 1
    gc = gridcols(ui - 15, ui + 15, v)
    print(f"v {v} {'G' if is_gridrow(v) else ' '} pred {u:7.1f} ink {'#' if hit else '.'} run {'' if p is None else f'{p}-{q}({q-p+1})'}  gridcols {gc}")
