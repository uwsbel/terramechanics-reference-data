"""Pixel <-> value through the piecewise map of cal-p1 (tools/calibrate_axes.py, read only)."""
import sys, math
from pathlib import Path
base = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base.parents[1] / "tools"))
import calibrate_axes as ca
_cal, X, Y = ca.piecewise_maps(str(base / "cal-p1"), str(base.parents[1] / "packet" / "p0054.png"))
def val(u, v):
    return X.value(u, v)[0], Y.value(u, v)[0]
def v_at(u, x):
    lo, hi = 1100.0, 3950.0   # grain size decreases downward
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if X.value(u, m)[0] > x: lo = m
        else: hi = m
    return 0.5 * (lo + hi)
def u_at(v, y):
    lo, hi = 500.0, 2100.0    # percent decreases to the right
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if Y.value(m, v)[0] > y: lo = m
        else: hi = m
    return 0.5 * (lo + hi)
if __name__ == "__main__":
    for k in range(-17, 0):
        x = 10 ** (k * 0.05)
        print(f"{x:.4f} mm: v at u=600 {v_at(600, x):.1f}, u=1300 {v_at(1300, x):.1f}, u=2000 {v_at(2000, x):.1f}")
    for p in range(0, 101, 5):
        print(f"{p}%: u at v=2250 {u_at(2250, p):.1f}, v=2500 {u_at(2500, p):.1f}, v=2950 {u_at(2950, p):.1f}")
