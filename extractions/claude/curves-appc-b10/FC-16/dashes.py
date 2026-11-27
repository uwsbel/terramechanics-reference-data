"""Per curve, classify every column as ink / none / unknown (under a grid line, frame or circle) around a
local prediction from clean ink, and list the dashes (ink stretches separated by 3 or more 'none' columns)."""
import json, sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open("packet/p0152.png").convert("L")).astype(float)
cal = json.load(open("out/FC-16/cal-p1/calibration.json"))
VL = [(l["x_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
HL = [(l["y_value"], l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
CIRC = {"p1L": (642.2, 2458.4), "p1R": (793.5, 2453.0), "p2L": (1563.6, 1919.4), "p2R": (1679.0, 1921.8),
        "p3L": (1923.7, 1848.3), "p3R": (2146.5, 1847.0), "p4L": (2345.2, 1532.3), "p4R": (2547.7, 1528.6),
        "sTop": (2498.5, 1391.8), "sMid": (2501.3, 1617.0), "sLow": (2500.2, 1846.6)}
clean = {k: np.array(v) for k, v in json.load(open("out/FC-16/clean.json")).items()}
def pred(name, u, half=40):
    A = clean[name]
    for h in (half, 100, 200, 400):
        w = np.abs(A[:, 0] - u) <= h
        if w.sum() >= 8:
            k, b = np.polyfit(A[w, 0], A[w, 1], 1); return k * u + b, k
    raise ValueError
def zone(u, v):
    z = []
    for val, u0, k in VL:
        if abs(u - (u0 + k * v)) <= 5: z.append(f"vline {val:g}")
    for val, v0, k in HL:
        if abs(v - (v0 + k * u)) <= 7: z.append(f"hline {val:g}")
    for n, (cu, cv) in CIRC.items():
        if np.hypot(u - cu, v - cv) <= 23: z.append(f"circle {n}")
    if u <= 652 or 2488 <= u <= 2507: z.append("frame")
    return z
def present(u, v):
    col = g[int(v) - 3:int(v) + 5, u]
    return bool((col < 128).any())
cls = {}
for name in clean:
    rows = []
    for u in range(645, 2560):
        v, k = pred(name, u)
        z = zone(u, v)
        p = present(u, v)
        rows.append((u, round(v, 2), "unk" if z else ("ink" if p else "none"), p, z))
    cls[name] = rows
    # dashes
    dashes = []; cur = None; nnone = 0
    for u, v, st, p, z in rows:
        if st == "ink":
            if cur is None: cur = [u, u]
            cur[1] = u; nnone = 0
        elif st == "none":
            nnone += 1
            if nnone >= 3 and cur is not None:
                dashes.append(cur); cur = None
    if cur: dashes.append(cur)
    print(f"== {name}: {len(dashes)} ink stretches")
    for a, b in dashes:
        # unknown columns adjacent to the ends
        za = [r[4] for r in rows if a - 8 <= r[0] < a and r[2] == "unk"]
        zb = [r[4] for r in rows if b < r[0] <= b + 8 and r[2] == "unk"]
        fa = sorted(set(x for z in za for x in z)); fb = sorted(set(x for z in zb for x in z))
        print(f"   {a:5d} .. {b:5d}  ({b-a+1:4d} px)  v {pred(name,a)[0]:.1f}..{pred(name,b)[0]:.1f}"
              + (f"  start next to {fa}" if fa else "") + (f"  end next to {fb}" if fb else ""))
json.dump({k: [(r[0], r[1], r[2], r[3], r[4]) for r in v] for k, v in cls.items()}, open("out/FC-16/columns.json", "w"))
