"""Runs of ink along each fitted time line: columns u with a dark pixel within 2 px of the line."""
import json, sys
import numpy as np
from PIL import Image
dark = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
lines = json.load(open(sys.argv[2]))
for L in lines["horizontal"]:
    on = []
    for u in range(744, 2268):
        v = L["v_at_u0"] + L["slope_dv_du"] * u
        vi = int(round(v))
        on.append(dark[vi - 2:vi + 3, u].any())
    runs, s = [], None
    for i, f in enumerate(on + [False]):
        if f and s is None: s = i
        if not f and s is not None:
            if i - s >= 3: runs.append((744 + s, 744 + i - 1))
            s = None
    left = [r for r in runs if r[1] < 1000]; right = [r for r in runs if r[0] > 2150]
    print(L["value"], "left", left, "right", right)
