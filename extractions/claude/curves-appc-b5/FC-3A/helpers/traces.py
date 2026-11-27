"""Trace samples, intercepts and line ends for the two drawn lines of FC-3A (helper for the Claude reading).
Samples are taken on the line's own ink: line components only, marker outlines masked, and a column is used
only where its ink run has the full cross-section of the line (not a dash tip, not cut by a marker mask)."""
import sys, json, numpy as np
lab = np.load(sys.argv[1]); cal = json.load(open(sys.argv[2])); ax = cal["ax"]
U0, V0 = 924, 1468
X = lambda u, v: ax[0] * u + ax[1] * v + ax[2]
lines = {
  "L47": dict(series="dr100-130", comps=[135, 132, 130, 128, 127, 117, 95, 63, 50, 23],
              masks=[(1117, 2800, 1149, 2832), (1409, 2463, 1440, 2495),
                     (2007, 1799, 2040, 1833), (2260, 1565, 2292, 1599)],
              dashed=lambda u: u < 1118 or u > 2266, bound=5.5, first=135, last=23),
  "L38": dict(series="dr0-15", comps=[138, 137, 136, 134, 133, 125, 115, 110, 104, 101, 100, 99],
              masks=[(1120, 2944, 1152, 2975)],
              dashed=lambda u: u < 1120 or u > 2237, bound=6.0, first=138, last=99),
}
def axis_u(v):   # left axis centre line (x = 0) from the calibration's vertical line for x=0
    l = [l for l in cal["vertical_lines"] if l["x_value"] == 0][0]
    return l["u_at_v0"] + l["slope_du_dv"] * v
out = {}
for name, L in lines.items():
    m = np.isin(lab, L["comps"])
    for (a, b, c, d) in L["masks"]:
        m[b - V0:d - V0 + 1, a - U0:c - U0 + 1] = False
    cols = {}
    for j in range(m.shape[1]):
        idx = np.where(m[:, j])[0]
        if len(idx) == 0: continue
        rs = np.split(idx, np.where(np.diff(idx) > 4)[0] + 1)   # pin-holes of up to 3 px inside the ink are bridged
        r = max(rs, key=len)
        cols[U0 + j] = (V0 + (r[0] + r[-1]) / 2, r[-1] - r[0] + 1, len(rs))
    L_med = np.median([c[1] for c in cols.values()])
    g0 = np.polyfit(list(cols), [cols[u][0] for u in cols], 1)
    # a column is near a symbol when the symbol's box (+3 px) overlaps the line's band in that column
    near_mask = lambda u: any(a - 3 <= u <= c + 3 and b - 3 <= np.polyval(g0, u) + 10 and np.polyval(g0, u) - 10 <= d + 3
                              for a, b, c, d in L["masks"])
    valid = {u: c for u, c in cols.items() if abs(c[1] - L_med) <= 4 and c[2] == 1 and not near_mask(u)}
    # a column is usable for a sample only if its +-4 neighbours are valid too (not a dash tip)
    usable = sorted(u for u in valid if all((u + k) in valid for k in range(-4, 5)))
    def centre(u):
        us = np.array([k for k in range(u - 5, u + 6) if k in valid])
        vs = np.array([valid[k][0] for k in us])
        c = np.polyfit(us, vs, 1); return float(np.polyval(c, u))
    gfit = np.polyfit(list(valid), [valid[u][0] for u in valid], 1)
    vline = lambda u: float(np.polyval(gfit, u))
    samples = []
    # left end on the shear-stress axis: centre line of the first dash meets the x=0 line
    us = [u for u in valid if (lab[:, u - U0] == L["first"]).any()]
    c1 = np.polyfit(us, [valid[u][0] for u in us], 1)
    u = 915.0
    for _ in range(20):
        v = np.polyval(c1, u); u = axis_u(v)
    left = (float(u), float(np.polyval(c1, u)))
    # right end: tip of the last dash along the line direction, pulled back 3 px onto the cap
    ys, xs = np.nonzero(lab == L["last"]); pu, pv = xs + U0, ys + V0
    cl = np.polyfit(pu, pv, 1); d = np.array([1, cl[0]]) / np.hypot(1, cl[0])
    t = pu * d[0] + pv * d[1]; tmax = t.max() - 3.0
    # point on the dash centre line (v = cl(u)) with projection tmax
    ur = tmax / (d[0] + d[1] * cl[0]) - (d[1] * cl[1]) / (d[0] + d[1] * cl[0])
    right = (float(ur), float(np.polyval(cl, ur)))
    samples.append(dict(u=left[0], v=left[1], note="dashed; left end on the shear-stress axis (line ink runs into the axis)"))
    xr = X(*right)
    target = 250.0
    while target < xr - 60:
        # u on the line where x = target
        u = 1000.0
        for _ in range(30):
            u += (target - X(u, vline(u))) / ax[0]
        ui = int(round(u))
        note = ""
        if ui not in usable:
            cand = [k for k in usable if abs(k - u) <= 40]
            if not cand:
                samples.append(dict(skip=True, target=target, u=u)); target += 250; continue
            k = min(cand, key=lambda k: abs(k - u))
            note = "moved from x=%g (u=%.0f, %s) to the nearest ink" % (target, u,
                   "on a symbol" if near_mask(ui) else "in a gap or at a dash tip")
            ui = k
        dash = L["dashed"](ui)
        samples.append(dict(u=float(ui), v=centre(ui), note=("dashed; " if dash else "") + ("x=%g" % target if not note else note)))
        target += 250
    samples.append(dict(u=right[0], v=right[1], note=("dashed; " if L["dashed"](right[0]) else "") + "right end: tip of the last dash, centre of its cap"))
    out[name] = dict(series=L["series"], bound=L["bound"], samples=samples, intercept=left,
                     gfit=list(map(float, gfit)), med_run=float(L_med))
    print(name, "median column run %.1f; global fit v = %.3f %+.6f u" % (L_med, gfit[1], gfit[0]))
    for s in samples:
        if s.get("skip"): print("   SKIPPED x=%g (u=%.0f): no usable ink within 40 px" % (s["target"], s["u"])); continue
        print("   u %7.1f v %7.1f  x %7.1f  |%s" % (s["u"], s["v"], X(s["u"], s["v"]), s["note"]))
json.dump(out, open(sys.argv[3], "w"), indent=1)
