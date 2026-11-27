"""Clean ink centers per curve (tracker 'ink' columns away from grid lines, frames and circles) and the
local slope profile along each curve (straight fits over 120 px windows)."""
import json, numpy as np
cal = json.load(open("out/FC-16/cal-p1/calibration.json"))
V = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
H = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
C = [(642.2, 2458.4), (793.5, 2453.0), (1563.6, 1919.4), (1679.0, 1921.8), (1923.7, 1848.3), (2146.5, 1847.0),
     (2345.2, 1532.3), (2547.7, 1528.6), (2498.5, 1391.8), (2501.3, 1617.0), (2500.2, 1846.6)]
tr = json.load(open("out/FC-16/track.json"))
out = {}
for name, pts in tr.items():
    keep = []
    for u, st, a, b, c in pts:
        if st != "ink": continue
        if any(abs(u - (u0 + k * c)) <= 6 for u0, k in V): continue
        if any(abs(c - (v0 + k * u)) <= 7 for v0, k in H): continue
        if any(np.hypot(u - cu, c - cv) <= 23 for cu, cv in C): continue
        if u < 652 or (2486 <= u <= 2520): continue      # frames
        keep.append((u, c, b - a + 1))
    # second pass: drop points far from a local fit (captured grid line or stray ink)
    A = np.array(keep, float)
    good = np.ones(len(A), bool)
    for i in range(len(A)):
        w = (np.abs(A[:, 0] - A[i, 0]) <= 30)
        if w.sum() >= 8:
            k, b0 = np.polyfit(A[w, 0], A[w, 1], 1)
            if abs(A[i, 1] - (k * A[i, 0] + b0)) > 2.5: good[i] = False
    A = A[good]
    out[name] = A.tolist()
    print(f"== {name}: {len(A)} clean columns ({(~good).sum()} dropped as off the local line)")
    for u0 in range(660, 2560, 100):
        w = (A[:, 0] >= u0) & (A[:, 0] < u0 + 120)
        if w.sum() >= 20:
            k, b0 = np.polyfit(A[w, 0], A[w, 1], 1)
            print(f"   u {u0}..{u0+120}: slope dv/du {k:+.4f}  n {w.sum()}  vthick med {np.median(A[w,2]):.0f}")
json.dump(out, open("out/FC-16/clean.json", "w"))
