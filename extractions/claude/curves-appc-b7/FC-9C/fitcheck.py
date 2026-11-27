"""Reader helper: slope and intercept of the trace samples of a native points file, and a least-squares
line through the markers (for comparison with the printed box values only; nothing is moved).
usage: fitcheck.py <points-native.csv> <tan_theta_printed> <cohesion_printed_psf>"""
import csv
import sys

import numpy as np

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
tp, cp = float(sys.argv[2]), float(sys.argv[3])
T = np.array([[float(r["x_native"]), float(r["y_native"])] for r in rows if r["point_kind"] == "trace"])
M = np.array([[float(r["x_native"]), float(r["y_native"])] for r in rows if r["point_kind"] == "marker"])
I = [float(r["y_native"]) for r in rows if r["point_kind"] == "feature" and "intercept" in r["note"]]
s, c = np.polyfit(T[:, 0], T[:, 1], 1)
print(f"trace samples: n={len(T)}, least-squares slope {s:.4f} (printed {tp}, diff {s - tp:+.4f}, {100 * (s - tp) / tp:+.2f}%), "
      f"intercept of that fit {c:.1f} psf")
s2 = (T[-2, 1] - T[1, 1]) / (T[-2, 0] - T[1, 0])
print(f"end-to-end slope of the interior samples (2nd to second-last): {s2:.4f}")
print(f"residuals of trace samples about their fit (psf): {np.round(T[:, 1] - (c + s * T[:, 0]), 1).tolist()}")
if I:
    print(f"intercept feature: {I[0]:.1f} psf (printed cohesion {cp}, diff {I[0] - cp:+.1f} psf)")
if len(M) >= 2:
    ms, mc = np.polyfit(M[:, 0], M[:, 1], 1)
    print(f"markers: n={len(M)}, least-squares through the read markers: slope {ms:.4f}, intercept {mc:.1f} psf "
          f"(atan {np.degrees(np.arctan(ms)):.2f} deg)")
print(f"printed tan theta {tp} -> {np.degrees(np.arctan(tp)):.2f} deg")
