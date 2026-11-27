"""Two-segment (continuous) least-squares fits in value space to locate a bend, solid centerline and dots."""
import csv, sys
sys.path.insert(0, "out/F2-48")
import numpy as np
from trace_lib import x_of, y_of
cl = [d for d in csv.DictReader(open("out/F2-48/solid-centerline.csv")) if d["u"] and d["v"] and d["flag"] == ""]
SX = np.array([x_of(float(d["u"]), float(d["v"])) for d in cl]); SY = np.array([y_of(float(d["u"]), float(d["v"])) for d in cl])
SU = np.array([float(d["u"]) for d in cl]); SV = np.array([float(d["v"]) for d in cl])
dots = [d for d in csv.DictReader(open("out/F2-48/dots.csv")) if d["flag"] == ""]
DX = np.array([float(d["x"]) for d in dots]); DY = np.array([float(d["y"]) for d in dots])
def fit(x, y, lo, hi):
    m = (x >= lo) & (x <= hi); x, y = x[m], y[m]
    p1 = np.polyfit(x, y, 1); r1 = np.sqrt(np.mean((y - np.polyval(p1, x))**2))
    best = None
    for b in np.arange(lo + 0.2, hi - 0.2, 0.01):
        A = np.c_[np.ones_like(x), x, np.maximum(x - b, 0)]
        c, *_ = np.linalg.lstsq(A, y, rcond=None)
        r = np.sqrt(np.mean((y - A @ c)**2))
        if best is None or r < best[0]:
            best = (r, b, c)
    r, b, c = best
    print(f"  {lo}-{hi}: one line rms {r1:.2f} lb; break at {b:.2f} in, rms {r:.2f} lb, slopes {c[1]:.0f} -> {c[1]+c[2]:.0f} lb/in, y at break {c[0]+c[1]*b:.1f}")
    return b
print("solid lpt87")
for lo, hi in ((3.0, 6.0), (4.0, 5.6), (3.5, 6.2), (5.2, 7.5), (5.6, 8.0), (1.0, 2.5), (0.2, 0.9)):
    fit(SX, SY, lo, hi)
print("dotted lpt85")
for lo, hi in ((3.0, 6.5), (2.5, 7.0), (4.0, 6.0), (0.2, 1.2), (0.8, 2.0), (6.0, 8.0)):
    fit(DX, DY, lo, hi)
print("stability")
for lo, hi in ((0.9, 1.8), (1.0, 2.2), (0.75, 1.75), (1.1, 2.5), (0.95, 3.0)):
    print(" solid"); fit(SX, SY, lo, hi)
for lo, hi in ((0.9, 1.8), (1.0, 2.2), (0.75, 1.75), (1.0, 3.0)):
    print(" dots"); fit(DX, DY, lo, hi)
for lo, hi in ((0.25, 0.7), (0.3, 0.8), (0.15, 0.65)):
    print(" solid"); fit(SX, SY, lo, hi)
for lo, hi in ((0.3, 1.0), (0.4, 0.9), (0.25, 1.1)):
    print(" dots"); fit(DX, DY, lo, hi)
for lo, hi in ((4.2, 5.6), (3.8, 6.0), (4.4, 5.4)):
    print(" dots"); fit(DX, DY, lo, hi)
