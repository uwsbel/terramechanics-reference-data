"""Fit each circle marker of FC-16 from its ring: along rays every 3 degrees from a seed, the dark run
nearest the nominal radius gives an edge point (its center); a least-squares circle is fitted with
iterative rejection of rays whose run is disturbed by a crossing line, a frame or a curve."""
import sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")).astype(float)
seeds = [("p1L", 643, 2458), ("p1R", 794, 2453), ("p2L", 1563, 1919), ("p2R", 1679, 1923),
         ("p3L", 1921, 1848), ("p3R", 2147, 1848), ("p4L", 2345, 1534), ("p4R", 2550, 1529),
         ("sTop", 2499, 1390), ("sMid", 2501, 1616), ("sLow", 2501, 1847)]
def sample(u, v):
    u0, v0 = int(np.floor(u)), int(np.floor(v)); fu, fv = u - u0, v - v0
    return (g[v0, u0]*(1-fu)*(1-fv) + g[v0, u0+1]*fu*(1-fv) + g[v0+1, u0]*(1-fu)*fv + g[v0+1, u0+1]*fu*fv)
def fit(cu, cv, R0=18.0):
    for rnd in range(3):
        pts = []
        for th in np.radians(np.arange(0, 360, 3)):
            rs = np.arange(8, 30, 0.5)
            prof = np.array([sample(cu + r*np.cos(th), cv + r*np.sin(th)) for r in rs])
            d = prof < 128
            # runs
            runs = []; i = 0
            while i < len(rs):
                if d[i]:
                    j = i
                    while j + 1 < len(rs) and d[j+1]: j += 1
                    runs.append((rs[i], rs[j])); i = j + 1
                else: i += 1
            if not runs: continue
            a, b = min(runs, key=lambda ab: abs((ab[0]+ab[1])/2 - R0))
            if b - a > 8: continue      # long run: a line along the ray
            rc = (a + b) / 2
            pts.append((cu + rc*np.cos(th), cv + rc*np.sin(th), np.degrees(th)))
        P = np.array(pts)
        keep = np.ones(len(P), bool)
        for it in range(6):
            x, y = P[keep, 0], P[keep, 1]
            A = np.c_[2*x, 2*y, np.ones(len(x))]
            sol, *_ = np.linalg.lstsq(A, x**2 + y**2, rcond=None)
            xc, yc = sol[0], sol[1]; R = np.sqrt(sol[2] + xc**2 + yc**2)
            res = np.hypot(P[:, 0] - xc, P[:, 1] - yc) - R
            keep = np.abs(res) < max(1.0, 2.5 * np.std(res[keep]))
        cu, cv, R0 = xc, yc, R
    return xc, yc, R, keep.sum(), len(P), float(np.sqrt(np.mean(res[keep]**2))), P[~keep, 2]
for name, u, v in seeds:
    xc, yc, R, nk, n, rms, rej = fit(u, v)
    rej_s = ",".join(str(int(a)) for a in rej)
    print(f"{name}: center ({xc:.1f}, {yc:.1f}) R {R:.1f}  rays kept {nk}/{n} rms {rms:.2f}  rejected angles [{rej_s}]")
