"""Fit the two drawn lines of FC-3A from column ink centers on line-only components (helper)."""
import sys, json, numpy as np
lab = np.load(sys.argv[1]); u0, v0 = 924, 1468
# line-only components (dashes and solid parts) and marker-contaminated ones handled by u exclusion
line_comps = {"L47": [135, 132, 130, 128, 127, 117, 95, 63, 50, 23],
              "L38": [138, 137, 136, 134, 133, 125, 115, 110, 104, 101, 100, 99]}
# u windows around markers that touch a line (excluded from the fit and flagged)
marker_u = {"L47": [(1112, 1152), (1405, 1448), (2004, 2042), (2258, 2300)],
            "L38": [(1116, 1154)]}
out = {}
for name, comps in line_comps.items():
    m = np.isin(lab, comps)
    pts = []
    for j in range(m.shape[1]):
        u = u0 + j
        if any(a <= u <= b for a, b in marker_u[name]): continue
        idx = np.where(m[:, j])[0]
        if len(idx) == 0: continue
        # split into runs; keep the single run (lines do not overlap in a column)
        br = np.where(np.diff(idx) > 1)[0]
        rs = np.split(idx, br + 1)
        for r in rs:
            pts.append((u, v0 + (r[0] + r[-1]) / 2, len(r)))
    p = np.array(pts)
    # robust straight fit
    keep = np.ones(len(p), bool)
    for it in range(3):
        c = np.polyfit(p[keep, 0], p[keep, 1], 1)
        r = p[:, 1] - np.polyval(c, p[:, 0])
        s = np.std(r[keep]); keep = np.abs(r) < 3 * max(s, 0.5)
    print(name, "fit v = %.3f + %.6f u ; n=%d kept=%d ; resid std %.2f px ; max |r| %.2f" % (c[1], c[0], len(p), keep.sum(), np.std(r[keep]), np.abs(r[keep]).max()))
    L = p[keep, 2]
    print("   column run length median %.1f (p10 %.1f, p90 %.1f) -> perpendicular thickness ~ %.1f px" % (np.median(L), np.percentile(L, 10), np.percentile(L, 90), np.median(L) / np.sqrt(1 + c[0] ** 2)))
    out[name] = {"slope": c[0], "icpt": c[1], "pts": p.tolist(), "keep": keep.tolist()}
json.dump(out, open(sys.argv[2], "w"))
