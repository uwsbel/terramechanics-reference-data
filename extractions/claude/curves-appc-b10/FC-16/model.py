"""Fit a smooth model per curve to clean tracker ink (away from grid lines and circles); print residuals."""
import sys, json
import numpy as np
cal = json.load(open("out/FC-16/cal-p1/calibration.json"))
V = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
Hh = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
# frames: left ~645, right ~2504..2515; top 1211, bottom 3517 (approximate)
tr = json.load(open("out/FC-16/track.json"))
circles = [(642, 2458), (794, 2453), (1563, 1919), (1679, 1923), (1921, 1848), (2147, 1848), (2345, 1534), (2550, 1529), (2499, 1390), (2501, 1616), (2501, 1847)]
models = {}
for name, pts in tr.items():
    U, Vv = [], []
    for u, st, a, b, c in pts:
        if st != "ink": continue
        if any(abs(u - (u0 + k * c)) <= 6 for u0, k in V): continue
        if any(abs(c - (v0 + k * u)) <= 7 for v0, k in Hh): continue
        if any(np.hypot(u - cu, c - cv) <= 26 for cu, cv in circles): continue
        if u < 655 or u > 2490: continue
        U.append(u); Vv.append(c)
    U, Vv = np.array(U, float), np.array(Vv)
    keep = np.ones(len(U), bool)
    for it in range(4):
        p = np.polyfit(U[keep], Vv[keep], 4)
        r = Vv - np.polyval(p, U)
        keep = np.abs(r) < 2.5
    models[name] = p.tolist()
    rr = r[keep]
    print(name, "n", len(U), "kept", keep.sum(), "rms", round(float(np.sqrt(np.mean(rr**2))), 2))
    bad = U[~keep]
    if len(bad): print("  rejected u:", sorted(set((bad // 10 * 10).astype(int).tolist())))
json.dump(models, open("out/FC-16/models.json", "w"))
