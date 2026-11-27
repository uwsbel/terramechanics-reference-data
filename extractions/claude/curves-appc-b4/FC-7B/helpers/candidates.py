"""Candidate symbol blobs inside the plot frame: grid-line pixels removed, connected components,
fragments split by a grid line merged back. Candidates only; every point is checked by eye."""
import json, sys, csv
from collections import deque
import numpy as np
from PIL import Image

img, calp, out = sys.argv[1], sys.argv[2], sys.argv[3]
g = np.asarray(Image.open(img).convert("L")).astype(int)
cal = json.load(open(calp))
U0, V0, U1, V1 = 600, 1330, 2306, 3284   # inside the frame lines
dark = g < 170
H, W = g.shape
removed = np.zeros_like(dark)
HALF = 4
for ln in cal["vertical_lines"]:
    a, b = ln["u_at_v0"], ln["slope_du_dv"]
    for v in range(V0 - 10, V1 + 10):
        uc = a + b * v
        for u in range(int(round(uc - HALF)), int(round(uc + HALF)) + 1):
            removed[v, u] = True
for ln in cal["horizontal_lines"]:
    a, b = ln["v_at_u0"], ln["slope_dv_du"]
    for u in range(U0 - 10, U1 + 10):
        vc = a + b * u
        for v in range(int(round(vc - HALF)), int(round(vc + HALF)) + 1):
            removed[v, u] = True
m = dark & ~removed
m[:V0, :] = False; m[V1:, :] = False; m[:, :U0] = False; m[:, U1:] = False
lab = np.zeros(m.shape, int)
comps = []
ys, xs = np.nonzero(m)
for y0, x0 in zip(ys, xs):
    if lab[y0, x0]:
        continue
    k = len(comps) + 1
    q = deque([(y0, x0)]); lab[y0, x0] = k
    pts = []
    while q:
        y, x = q.popleft(); pts.append((y, x))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                yy, xx = y + dy, x + dx
                if m[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = k; q.append((yy, xx))
    p = np.array(pts)
    comps.append(dict(vmin=p[:, 0].min(), vmax=p[:, 0].max(), umin=p[:, 1].min(), umax=p[:, 1].max(), n=len(p)))
# merge fragments whose boxes are within GAP px (grid-line removal splits symbols)
GAP = 10
def close(a, b):
    du = max(0, max(a["umin"], b["umin"]) - min(a["umax"], b["umax"]))
    dv = max(0, max(a["vmin"], b["vmin"]) - min(a["vmax"], b["vmax"]))
    return du <= GAP and dv <= GAP and max(a["umax"], b["umax"]) - min(a["umin"], b["umin"]) < 45 and max(a["vmax"], b["vmax"]) - min(a["vmin"], b["vmin"]) < 45
comps = [c for c in comps if c["n"] >= 4]
changed = True
while changed:
    changed = False
    for i in range(len(comps)):
        for j in range(i + 1, len(comps)):
            if close(comps[i], comps[j]):
                a, b = comps[i], comps[j]
                comps[i] = dict(vmin=min(a["vmin"], b["vmin"]), vmax=max(a["vmax"], b["vmax"]), umin=min(a["umin"], b["umin"]), umax=max(a["umax"], b["umax"]), n=a["n"] + b["n"])
                del comps[j]; changed = True; break
        if changed:
            break
comps.sort(key=lambda c: (-(c["vmin"] + c["vmax"]), c["umin"]))
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["cid", "uc", "vc", "umin", "umax", "vmin", "vmax", "w", "h", "n"])
    for i, c in enumerate(comps, 1):
        w.writerow([i, (c["umin"] + c["umax"]) / 2, (c["vmin"] + c["vmax"]) / 2, c["umin"], c["umax"], c["vmin"], c["vmax"], c["umax"] - c["umin"] + 1, c["vmax"] - c["vmin"] + 1, c["n"]])
print(len(comps), "candidates")
