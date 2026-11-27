"""Slope of the trace samples and shear stress at the intercept, against the printed box values."""
import csv, sys, math
import numpy as np
f, tan_p, coh_p = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
R = list(csv.DictReader(open(f, encoding="utf-8")))
T = [(float(r["x_native"]), float(r["y_native"])) for r in R if r["point_kind"] == "trace"]
M = [(float(r["x_native"]), float(r["y_native"])) for r in R if r["point_kind"] == "marker"]
I = [r for r in R if r["point_kind"] == "feature" and r["note"].startswith("intercept")]
T, M = np.array(T), np.array(M)
s, c = np.polyfit(T[:, 0], T[:, 1], 1)
si, ci = np.polyfit(T[1:-1, 0], T[1:-1, 1], 1)
e = (T[-1, 1] - T[0, 1]) / (T[-1, 0] - T[0, 0])
print(f"trace LS slope (all {len(T)} samples) {s:.4f}, intercept {c:.1f} psf; interior only {si:.4f}, {ci:.1f}; end to end {e:.4f}")
print(f"  printed tan theta {tan_p:.4f}: LS slope differs by {s - tan_p:+.4f} ({100 * (s - tan_p) / tan_p:+.1f} %); angle {math.degrees(math.atan(s)):.2f} deg")
if I:
    yi, bi = float(I[0]["y_native"]), float(I[0]["y_read_bound"])
    print(f"intercept feature: y {yi:.1f} +- {bi:.1f} psf (x {float(I[0]['x_native']):.1f}); printed cohesion {coh_p:.2f}: differs by {yi - coh_p:+.1f} psf")
sm, cm = np.polyfit(M[:, 0], M[:, 1], 1)
print(f"markers LS (as read): slope {sm:.4f}, intercept {cm:.1f} psf, n {len(M)}; angle {math.degrees(math.atan(sm)):.2f} deg")
