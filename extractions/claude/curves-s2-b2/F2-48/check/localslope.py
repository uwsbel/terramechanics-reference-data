"""Local slope (lb/in) of the solid centerline and the dots, by linear fit in windows of 0.15 in."""
import csv, sys
sys.path.insert(0, "out/F2-48")
import numpy as np
from trace_lib import x_of, y_of
cl = [d for d in csv.DictReader(open("out/F2-48/solid-centerline.csv")) if d["u"] and d["v"] and d["flag"] == ""]
SX = np.array([x_of(float(d["u"]), float(d["v"])) for d in cl]); SY = np.array([y_of(float(d["u"]), float(d["v"])) for d in cl])
SU = np.array([float(d["u"]) for d in cl]); SV = np.array([float(d["v"]) for d in cl])
dots = [d for d in csv.DictReader(open("out/F2-48/dots.csv")) if d["flag"] == ""]
DX = np.array([float(d["x"]) for d in dots]); DY = np.array([float(d["y"]) for d in dots])
for name, X, Y, rng in (("solid", SX, SY, np.arange(0.95, 2.0, 0.05)), ("solid", SX, SY, np.arange(4.3, 5.4, 0.05)), ("dots", DX, DY, np.arange(4.4, 5.4, 0.1))):
    print(name)
    for c in rng:
        m = np.abs(X - c) <= 0.075
        if m.sum() >= 3:
            p = np.polyfit(X[m], Y[m], 1)
            print(f"  x {c:.2f}: slope {p[0]:6.0f}  y {np.polyval(p, c):6.1f}  n {m.sum()}")
# pixel of the solid centerline at a few x
for xt in (1.45, 1.5, 1.55, 4.65, 4.7, 4.75):
    i = np.argmin(np.abs(SX - xt)); print("solid at x", xt, "->", SU[i], SV[i], round(SY[i], 1))
