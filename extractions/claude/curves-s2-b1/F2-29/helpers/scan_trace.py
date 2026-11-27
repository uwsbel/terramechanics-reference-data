"""Scan the trace ink of Figure 2-29 along rows of constant penetration (tilted per the
calibration), with the grid lines and the frame masked out. Prints, per row, the dark runs
found (u range, centre) so the reader can pick the trace. Also measures the vertical ink run
at the chosen column. Nothing here chooses a value: the reader looks at every row."""
import json, sys
import numpy as np
from PIL import Image

cal = json.load(open("out/F2-29/cal-p1/calibration.json"))
g = np.asarray(Image.open("packet/p0080.png").convert("L"))
dark = g < 160
H, W = g.shape
ax, ay = cal["ax"], cal["ay"]

# grid mask: every calibrated line, half-width 12 px (lines are 6 to 21 px thick)
mask = np.zeros_like(dark)
vv, uu = np.mgrid[0:H, 0:W]
for l in cal["vertical_lines"]:
    upred = l["u_at_v0"] + l["slope_du_dv"] * vv
    mask |= np.abs(uu - upred) <= 13
for l in cal["horizontal_lines"]:
    vpred = l["v_at_u0"] + l["slope_dv_du"] * uu
    mask |= np.abs(vv - vpred) <= 13
# top frame (penetration 9, unlabelled, not calibrated): mask it too
mask |= np.abs(vv - (1016.5 + 20 - 0.0111 * uu)) <= 15   # roughly; checked below
ink = dark & ~mask

def v_of(p, u):
    return (p - ax[0] * u - ax[2]) / ax[1]

def runs(arr):
    out, start = [], None
    for i, d in enumerate(arr):
        if d and start is None: start = i
        if not d and start is not None: out.append((start, i - 1)); start = None
    if start is not None: out.append((start, len(arr) - 1))
    return out

def scan_row(p, u0=470, u1=2340):
    us = np.arange(u0, u1)
    vs = np.round(v_of(p, us)).astype(int)
    # combine 3 rows (v-1, v, v+1) so a 1 px gap does not split a run
    d = ink[vs, us] | ink[vs - 1, us] | ink[vs + 1, us]
    rr = [(us[a], us[b]) for a, b in runs(d) if b - a >= 1]
    # merge runs separated by <= 3 px
    merged = []
    for a, b in rr:
        if merged and a - merged[-1][1] <= 3: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    return merged

def col_run(u, v, dark_only=False):
    src = dark if dark_only else ink
    a = v
    while a - 1 >= 0 and src[a - 1, u]: a -= 1
    b = v
    while b + 1 < H and src[b + 1, u]: b += 1
    return a, b

if __name__ == "__main__":
    ps = [float(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [i * 0.25 for i in range(0, 33)]
    for p in ps:
        rr = scan_row(p)
        parts = []
        for a, b in rr:
            uc = (a + b) / 2
            vc = int(round(v_of(p, uc)))
            va, vb = col_run(int(round(uc)), vc)
            parts.append(f"u {a}-{b} (c {uc:.1f}, w {b-a+1}) v {va}-{vb} (c {(va+vb)/2:.1f}, h {vb-va+1})")
        print(f"p={p:5.2f}: " + " | ".join(parts))
