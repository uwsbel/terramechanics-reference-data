"""Ring-model centres of the FB-3 circles: each symbol an annulus (radii fitted on the clean circles),
the union of the annuli of a cluster compared pixel by pixel with the page in a window, the drawn
lines' ink (within 6 px of a fitted segment centreline, outside the annuli) masked out; centres found
by coordinate search (0.25 px). Clean circles are fitted too, as a check against their hole centroid."""
import json, sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
S = json.load(open(sys.argv[2]))
lines = [(np.array(s["point"]), np.array(s["dir"])) for s in S.values()]

def line_dist(U, V):
    d = np.full(U.shape, 1e9)
    for p, e in lines:
        n = np.array([-e[1], e[0]])
        d = np.minimum(d, np.abs((U - p[0]) * n[0] + (V - p[1]) * n[1]))
    return d

def model(U, V, cs, ri, ro):
    m = np.zeros(U.shape, bool)
    for c in cs:
        r = np.hypot(U - c[0], V - c[1])
        m |= (r >= ri) & (r <= ro)
    return m

def fit(cs, ri, ro, half=40, mask_lines=True):
    cs = [np.array(c, float) for c in cs]
    cu, cv = np.mean([c[0] for c in cs]), np.mean([c[1] for c in cs])
    us = np.arange(int(cu) - half, int(cu) + half + 1); vs = np.arange(int(cv) - half, int(cv) + half + 1)
    U, V = np.meshgrid(us + 0.0, vs + 0.0)   # pixel centres at integer coordinates
    I = g[vs[0]:vs[-1] + 1, us[0]:us[-1] + 1]
    keep = np.ones(U.shape, bool)
    if mask_lines:
        keep &= line_dist(U, V) > 6.5
    # only judge pixels near some ring
    for it in range(4):
        for k in range(len(cs)):
            best = None
            for du in np.arange(-3, 3.01, 0.25):
                for dv in np.arange(-3, 3.01, 0.25):
                    trial = [c if j != k else c + (du, dv) for j, c in enumerate(cs)]
                    M = model(U, V, trial, ri, ro)
                    near = np.zeros(U.shape, bool)
                    for c in trial:
                        near |= np.hypot(U - c[0], V - c[1]) <= ro + 6
                    sel = keep & near
                    err = np.sum(M[sel] != I[sel])
                    if best is None or err < best[0]:
                        best = (err, trial[k].copy(), sel.sum())
            cs[k] = best[1]
    return cs, best[0], best[2]

if __name__ == "__main__":
    # radii from the clean circles: scan ri, ro on the 2.3-psi lower dense circle and the 6-psi loose circle
    for name, c in (("d23l", (862.69, 3124.86)), ("l6", (1384.09, 3232.59)), ("d99u", (1938.43, 889.48))):
        best = None
        for ri in np.arange(11.5, 14.01, 0.25):
            for ro in np.arange(19, 22.01, 0.25):
                cs, err, n = fit([c], ri, ro, half=30)
                if best is None or err < best[0]:
                    best = (err, ri, ro, cs[0], n)
        print(f"{name}: best ri {best[1]} ro {best[2]} centre ({best[3][0]:.2f},{best[3][1]:.2f}) mismatch {best[0]}/{best[4]}")
