"""Locate the bends of the trace objectively (reader helper, F5-31): for each bend, straight lines are fitted
(in page pixels) to the clean center rows of the stretch before and the stretch after it; the knee is the
point of the center line nearest the intersection of the two lines. Prints the result for sample.py."""
import sys
from pathlib import Path
import numpy as np
ws = Path(__file__).resolve().parents[3]
V, U, W, T, D = np.load(ws / "out" / "F5-31" / "helpers" / "profile.npy")

BENDS = {   # name: (before t0, t1), (after t0, t1)
    "A ~0.03": ((0.016, 0.027), (0.033, 0.040)),
    "B ~0.06": ((0.048, 0.055), (0.063, 0.069)),
    "C ~0.09": ((0.082, 0.086), (0.094, 0.099)),
}
for name, (b, a) in BENDS.items():
    fits = []
    for t0, t1 in (b, a):
        m = (T >= t0) & (T <= t1)
        k, c = np.polyfit(V[m], U[m], 1)          # u = k v + c
        res = U[m] - (k * V[m] + c)
        fits.append((k, c, float(np.sqrt(np.mean(res ** 2)))))
    (k1, c1, r1), (k2, c2, r2) = fits
    vx = (c2 - c1) / (k1 - k2)
    ux = k1 * vx + c1
    # nearest center row (clean) to the intersection
    dist = np.hypot(U - ux, V - vx)
    i = int(np.argmin(dist))
    ang = np.degrees(np.arctan(k1) - np.arctan(k2))
    print(f"{name}: before du/dv {k1:.3f} (rms {r1:.2f} px), after {k2:.3f} (rms {r2:.2f} px), turn {ang:.1f} deg; "
          f"lines meet at u {ux:.1f} v {vx:.1f}; nearest clean center row v {V[i]:.0f} u {U[i]:.1f} "
          f"({dist[i]:.1f} px away), t {T[i]:.4f} depth {D[i]:.3f}")
