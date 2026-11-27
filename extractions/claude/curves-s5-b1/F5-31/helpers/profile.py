"""Depth against time along the clean rows of rows.csv, with the local slope (reader helper, F5-31)."""
import csv, sys
from pathlib import Path
import numpy as np
ws = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ws / "tools"))
import calibrate_axes as ca

cal, X, Y = ca.piecewise_maps(str(ws / "out" / "F5-31" / "cal-p1"))
rows = [r for r in csv.DictReader(open(ws / "out" / "F5-31" / "helpers" / "rows.csv")) if r["clean"] == "1"]
V = np.array([float(r["v"]) for r in rows]); U = np.array([float(r["center"]) for r in rows]); W = np.array([float(r["width"]) for r in rows])
T = np.array([X.value(u, v)[0] for u, v in zip(U, V)]); D = np.array([Y.value(u, v)[0] for u, v in zip(U, V)])
np.save(ws / "out" / "F5-31" / "helpers" / "profile.npy", np.vstack([V, U, W, T, D]))
step = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0025
print(" t       depth   slope(in/s, fit over +-0.002 s)  width  rows")
for t0 in np.arange(0, 0.1001, step):
    m = np.abs(T - t0) <= 0.002
    if m.sum() < 5:
        print(f"{t0:.4f}  (few clean rows: {m.sum()})")
        continue
    k, c = np.polyfit(T[m], D[m], 1)
    print(f"{t0:.4f}  {k * t0 + c:6.3f}  {k:7.1f}   {np.median(W[m]):4.1f}  {m.sum()}")
