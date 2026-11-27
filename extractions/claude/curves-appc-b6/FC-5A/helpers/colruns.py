"""For each fitted line (helpers/linefit.json) list, per column, the dark run nearest the fitted
center: run top, bottom, length, center, residual to the fit. Prints binned residual summaries
to check straightness. usage: colruns.py image linefit.json [line u0 u1]"""
import sys, json
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
L = json.load(open(sys.argv[2]))

def run_at(u, vp, win=25):
    v0, v1 = int(vp) - win, int(vp) + win
    col = g[v0:v1, u]
    idx = np.where(col)[0]
    runs = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                runs.append((s + v0, p + v0)); s = i
            p = i
        runs.append((s + v0, p + v0))
    best = None
    for t, b in runs:
        if t - 1 <= vp <= b + 1 or abs((t + b) / 2 - vp) < 8:
            c = (t + b) / 2
            if best is None or abs(c - vp) < abs(best[2] - vp):
                best = (t, b, c)
    return best, runs

if len(sys.argv) > 3:
    name, u0, u1 = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    a, b = L[name]["a"], L[name]["b"]
    for u in range(u0, u1 + 1):
        vp = a * u + b
        best, runs = run_at(u, vp)
        s = f"{u}: fit {vp:7.1f}  "
        if best:
            t, bb, c = best
            s += f"run {t}-{bb} len {bb-t+1:2d} c {c:7.1f} res {c-vp:+5.1f}"
        else:
            s += "no run"
        print(s)
    sys.exit()
for name, d in L.items():
    a, b, nom = d["a"], d["b"], d["median_run"]
    print(name, "nominal run", nom)
    for u0 in range(850, 2300, 50):
        res = []
        for u in range(u0, u0 + 50):
            best, _ = run_at(u, a * u + b)
            if best and abs((best[1] - best[0] + 1) - nom) <= 2:
                res.append(best[2] - (a * u + b))
        if res:
            print(f"   u {u0}-{u0+49}: n {len(res):2d} mean res {np.mean(res):+5.2f}")
