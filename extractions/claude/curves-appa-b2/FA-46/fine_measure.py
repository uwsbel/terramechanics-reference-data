"""Per-row measurement in the fine part (v 2390..3192), u 2100..2205.
For each non-grid row: B edges where visible, A present + A left edge, C present + C right edge or merged into frame."""
import numpy as np
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
def run_at(v, u):
    if not g[v, u]: return None
    a = u
    while g[v, a - 1]: a -= 1
    b = u
    while g[v, b + 1]: b += 1
    return a, b
def bexp(v):
    if v <= 2600: return 2165.5
    if v >= 3060: return 2174.0
    return 2165.5 + (v - 2600) * (8.5 / 460)
def frame_c(v):
    return 2174.9 + 0.0060 * v
out = []
for v in range(2390, 3193):
    bc = bexp(v); fc = int(round(frame_c(v)))
    gridrow = run_at(v, 2130) is not None and run_at(v, 2130)[1] >= 2145
    if gridrow:
        print(f"{v} grid"); continue
    R = run_at(v, int(round(bc)))
    F = run_at(v, fc)
    aP = g[v, int(round(bc - 10))] and g[v, int(round(bc - 9))]
    cP = g[v, int(round(bc + 10))] and g[v, int(round(bc + 9))]
    s = f"{v} R={R} F={F} A={'Y' if aP else '-'} C={'Y' if cP else '-'}"
    # B left edge visible if A absent: left end of R; B right edge visible if C absent
    bl = R[0] if (R and not aP) else None
    br = R[1] if (R and not cP) else None
    al = run_at(v, int(round(bc - 10)))[0] if aP else None
    cr = None; cmerge = False
    if cP:
        rc = run_at(v, int(round(bc + 10)))
        if F and rc == F: cmerge = True
        else: cr = rc[1]
    print(s + f" Bl={bl} Br={br} Al={al} Cr={cr} Cmerge={cmerge}")
