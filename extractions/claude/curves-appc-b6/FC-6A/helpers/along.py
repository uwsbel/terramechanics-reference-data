"""Ink along a fitted line: for each u in [u0, u1], is there ink within +-tol px (vertical) of the
fitted line v = a + b u (fit_lines.json)? Prints the runs of u with ink (gaps of 1 px merged), with
psf. Reader's aid."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
cal = json.loads((HERE.parent / "cal-p1" / "calibration.json").read_text())
ax, ay = cal["ax"], cal["ay"]
fits = json.loads((HERE / "fit_lines.json").read_text())
name = sys.argv[1]; u0, u1 = int(sys.argv[2]), int(sys.argv[3]); tol = int(sys.argv[4])
a, b = fits[name]
on = []
for u in range(u0, u1 + 1):
    v = a + b * u
    vi = int(round(v))
    on.append(bool((g[vi - tol: vi + tol + 1, u] < 160).any()))
runs = []
i = 0
us = list(range(u0, u1 + 1))
while i < len(on):
    if on[i]:
        j = i
        while j + 1 < len(on) and (on[j + 1] or (j + 2 < len(on) and on[j + 2])):
            j += 1
        runs.append((us[i], us[j])); i = j + 1
    else:
        i += 1
for s, e in runs:
    vs, ve = a + b * s, a + b * e
    xs = ax[0]*s + ax[1]*vs + ax[2]; ys = ay[0]*s + ay[1]*vs + ay[2]
    xe = ax[0]*e + ax[1]*ve + ax[2]; ye = ay[0]*e + ay[1]*ve + ay[2]
    print(f"{name} ink u {s}-{e} (len {e-s+1})  v {vs:.1f}-{ve:.1f}  sigma {xs:.0f}-{xe:.0f}  tau {ys:.0f}-{ye:.0f}")
