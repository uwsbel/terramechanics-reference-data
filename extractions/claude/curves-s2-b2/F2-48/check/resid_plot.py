"""Residual of each trace from a straight line over 1.3 to 8 in: shows knees and wiggles."""
import csv, sys
sys.path.insert(0, "out/F2-48")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from trace_lib import x_of, y_of
cl = [d for d in csv.DictReader(open("out/F2-48/solid-centerline.csv")) if d["u"] and d["v"] and d["flag"] == ""]
X = np.array([x_of(float(d["u"]), float(d["v"])) for d in cl]); Y = np.array([y_of(float(d["u"]), float(d["v"])) for d in cl])
dots = list(csv.DictReader(open("out/F2-48/dots.csv")))
DX = np.array([float(d["x"]) for d in dots]); DY = np.array([float(d["y"]) for d in dots])
fig, ax = plt.subplots(2, 1, figsize=(16, 9))
for a, (x, y, st) in zip(ax, ((X, Y, "k."), (DX, DY, "bo"))):
    m = (x > 1.3)
    p = np.polyfit(x[m], y[m], 1)
    a.plot(x[m], y[m] - np.polyval(p, x[m]), st, ms=2)
    a.set_xticks(np.arange(1.25, 8.01, 0.25)); a.grid(True, alpha=.4)
    a.set_title(f"slope {p[0]:.1f} lb/in")
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=60)
