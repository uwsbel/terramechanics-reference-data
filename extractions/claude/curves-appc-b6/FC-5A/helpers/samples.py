"""Locate the trace sample columns (every 250 psf of normal stress) on each fitted line and report
the ink found in that column: the run nearest the fit, its length vs the line's nominal run, and
all runs within +-25 px. usage: samples.py image calibration.json linefit.json"""
import sys, json
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
cal = json.load(open(sys.argv[2]))
L = json.load(open(sys.argv[3]))
ax, ay = cal["ax"], cal["ay"]
ENDS = {"L1_41.5": 2930, "L2_36.9": 3900, "L3_32.8": 4600, "L4_29": 5000}

def runs(u, v0, v1):
    col = g[v0:v1, u]
    idx = np.where(col)[0]
    out = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                out.append((s + v0, p + v0)); s = i
            p = i
        out.append((s + v0, p + v0))
    return out

for name, d in L.items():
    a, b, nom = d["a"], d["b"], d["median_run"]
    print(name, "nominal", nom)
    for sig in range(250, ENDS[name], 250):
        # solve x(u, v(u)) = sig
        u = (sig - ax[2] - ax[1] * b) / (ax[0] + ax[1] * a)
        uc = int(round(u)); vp = a * uc + b
        rr = runs(uc, int(vp) - 25, int(vp) + 25)
        near = [r for r in rr if r[0] - 1 <= vp <= r[1] + 1]
        txt = " ".join(f"{t}-{bb}({bb-t+1})" for t, bb in rr)
        flag = ""
        if not near:
            flag = "NO INK AT FIT"
        else:
            t, bb = near[0]; ln = bb - t + 1; c = (t + bb) / 2
            if abs(ln - nom) > 2 or abs(c - vp) > 3:
                flag = f"CHECK len {ln} c {c:.1f} res {c-vp:+.1f}"
            else:
                flag = f"ok c {c:.1f} res {c-vp:+.1f}"
        print(f"  sig {sig:5d}: u {u:7.1f} col {uc} fit v {vp:7.1f} | {flag} | runs {txt}")
