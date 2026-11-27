"""Helper for the F2-48 reading: strip the grid from the page ink inside the plot frame and
label the remaining connected components (the solid trace, the dots of the dotted trace, the
printed labels). Writes out/F2-48/components.csv (id, area, bbox, centroid) and a mask PNG.
Pixel coordinates are those of packet/p0109.png (u right, v down)."""
import json, sys, csv
from collections import deque
import numpy as np
from PIL import Image

IMG = "packet/p0109.png"
CAL = "out/F2-48/cal-p1/calibration.json"
DARK = 160
BOX = (400, 1040, 2290, 3775)   # u0 v0 u1 v1, a little inside the outer frame lines

g = np.array(Image.open(IMG).convert("L"))
ink = g < DARK
cal = json.load(open(CAL))
H, W = g.shape
vv, uu = np.mgrid[0:H, 0:W]
gridmask = np.zeros_like(ink)
for L in cal["vertical_lines"]:
    uc = L["u_at_v0"] + L["slope_du_dv"] * vv
    hw = 6 if L["y_value"] in (0.0, 1200.0) else 5
    gridmask |= np.abs(uu - uc) <= hw
for L in cal["horizontal_lines"]:
    vc = L["v_at_u0"] + L["slope_dv_du"] * uu
    hw = 7 if L["x_value"] == 0.0 else 5
    gridmask |= np.abs(vv - vc) <= hw
# top frame (unlabelled, about v = 1053 + tilt)
gridmask |= np.abs(vv - (1049.5 + 0.0046 * uu)) <= 7
u0, v0, u1, v1 = BOX
inside = (uu >= u0) & (uu < u1) & (vv >= v0) & (vv < v1)
rem = ink & ~gridmask & inside
Image.fromarray((~rem * 255).astype(np.uint8)).save("out/F2-48/ink-nogrid.png")

# connected components (8-connected) by flood fill
lab = np.zeros(rem.shape, dtype=np.int32)
comps = []
ys, xs = np.nonzero(rem)
nid = 0
for y, x in zip(ys, xs):
    if lab[y, x]:
        continue
    nid += 1
    q = deque([(y, x)]); lab[y, x] = nid
    pts = []
    while q:
        cy, cx = q.popleft(); pts.append((cy, cx))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and rem[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = nid; q.append((ny, nx))
    p = np.array(pts)
    comps.append((nid, len(p), p[:, 1].min(), p[:, 0].min(), p[:, 1].max(), p[:, 0].max(), p[:, 1].mean(), p[:, 0].mean()))
np.save("out/F2-48/labels.npy", lab)
with open("out/F2-48/components.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "area", "u_min", "v_min", "u_max", "v_max", "u_c", "v_c"])
    for c in comps:
        w.writerow([c[0], c[1], c[2], c[3], c[4], c[5], f"{c[6]:.1f}", f"{c[7]:.1f}"])
print(len(comps), "components")
big = sorted(comps, key=lambda c: -c[1])[:40]
for c in big:
    print(c[0], c[1], "bbox u %d..%d v %d..%d" % (c[2], c[4], c[3], c[5]))
