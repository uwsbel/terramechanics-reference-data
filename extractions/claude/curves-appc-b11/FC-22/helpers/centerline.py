"""Column-wise centerline of the three curves of FC-22 (reader helper; reads the page only).
For each column u, dark runs in v are found; pixels within a few px of a grid line (from this
reader's calibration) are masked; each run is assigned to the curve whose rough line is nearest."""
import sys, json
import numpy as np
from PIL import Image
img, caljson, out = sys.argv[1], sys.argv[2], sys.argv[3]
g = np.asarray(Image.open(img).convert("L"), dtype=float)
cal = json.load(open(caljson))
vl = [(l["x_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
hl = [(l["y_value"], l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
rough = {"upper": ((866, 2451), (2405, 1464)), "mean": ((866, 2542), (2412, 1550)), "lower": ((866, 2645), (2405, 1646))}
def rough_v(name, u):
    (u0, v0), (u1, v1) = rough[name]
    return v0 + (v1 - v0) * (u - u0) / (u1 - u0)
DARK = 140
res = {k: [] for k in rough}
for u in range(820, 2470):
    # near a vertical grid line?
    near_v = any(abs(u - (i0 + s * 2000)) <= 7 for _, i0, s in vl)  # crude; refined per v below
    col = g[1350:2750, u]
    dark = col < DARK
    idx = np.where(dark)[0]
    if len(idx) == 0:
        continue
    runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    for r in runs:
        v0, v1 = r[0] + 1350, r[-1] + 1350
        vc = (v0 + v1) / 2
        # vertical grid line at this v?
        on_vline = any(abs(u - (i0 + s * vc)) <= 6 for _, i0, s in vl)
        # horizontal grid line inside the run?
        on_hline = any(v0 - 4 <= (i0 + s * u) <= v1 + 4 for _, i0, s in hl)
        name = min(rough, key=lambda n: abs(rough_v(n, u) - vc))
        if abs(rough_v(name, u) - vc) > 40:
            continue
        w = 255 - g[v0:v1 + 1, u]
        vw = float(np.sum(np.arange(v0, v1 + 1) * w) / np.sum(w))
        res[name].append([u, round(vw, 2), int(v0), int(v1), int(on_vline), int(on_hline)])
json.dump(res, open(out, "w"))
for k, v in res.items():
    print(k, len(v))
