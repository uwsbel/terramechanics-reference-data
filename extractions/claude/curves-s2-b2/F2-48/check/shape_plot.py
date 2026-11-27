"""Plot the solid centerline and the dot chain in value space with the points, to look for knees."""
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
pts = list(csv.DictReader(open(sys.argv[1])))
fig, axs = plt.subplots(3, 1, figsize=(14, 18))
for ax, (lo, hi) in zip(axs, ((0, 1.6), (1.4, 5), (4.8, 8.2))):
    m = (X >= lo) & (X <= hi); ax.plot(X[m], Y[m], "k.", ms=1)
    m2 = (DX >= lo) & (DX <= hi); ax.plot(DX[m2], DY[m2], "o", mfc="none", mec="gray", ms=4)
    for p in pts:
        x, y = float(p["x_native"]), float(p["y_native"])
        if lo <= x <= hi:
            c = "r" if p["series_id"] == "lpt87" else "b"
            ax.plot(x, y, "s" if p["point_kind"] == "feature" else "+", color=c, ms=8, mfc="none")
            ax.annotate(p["sequence"], (x, y), color=c, fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_xlim(lo, hi); ax.grid(True, alpha=.3)
plt.tight_layout(); plt.savefig(sys.argv[2], dpi=70)
