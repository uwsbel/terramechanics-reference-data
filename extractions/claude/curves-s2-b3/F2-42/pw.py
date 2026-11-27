"""Piecewise map of cal-p1 (D-025) as a helper for choosing sample locations and checking values.

usage:
  pw.py v <y> <u>      the row v at which load y is reached at column u
  pw.py u <x> <v>      the column u at which penetration x is reached at row v
  pw.py val <u> <v>    (x, y) at a pixel
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(str(HERE / "cal-p1"))

def solve(f, target, lo, hi):
    flo = f(lo) - target
    for _ in range(60):
        mid = 0.5 * (lo + hi); fm = f(mid) - target
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return 0.5 * (lo + hi)

def v_of(y, u): return solve(lambda v: Y.value(u, v)[0], y, 1200, 3500)
def u_of(x, v): return solve(lambda u: X.value(u, v)[0], x, 700, 1900)
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "v": print(f"{v_of(float(sys.argv[2]), float(sys.argv[3])):.1f}")
    elif c == "u": print(f"{u_of(float(sys.argv[2]), float(sys.argv[3])):.1f}")
    elif c == "val":
        u, v = float(sys.argv[2]), float(sys.argv[3]); print(f"x={X.value(u, v)[0]:.4f} y={Y.value(u, v)[0]:.2f}")
