"""Sampling geometry from the reader's own calibration (piecewise, verified lines only).
x_at(u, v), y_at(u, v); v_for_x(x, u): page v on the constant-x line at column u;
u_for_y(y, v): page u on the constant-y line at row v."""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
import calibrate_axes as ca
CAL = HERE / "cal-p1"
IMG = HERE.parent.parent / "packet" / "p0095.png"
cal, X, Y = ca.piecewise_maps(str(CAL), str(IMG))

def x_at(u, v):
    return X.value(u, v)[0]

def y_at(u, v):
    return Y.value(u, v)[0]

def v_for_x(x, u, lo=1000.0, hi=3900.0):
    # x decreases with v
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if x_at(u, m) > x:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)

def u_for_y(y, v, lo=650.0, hi=2300.0):
    # y decreases with u
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if y_at(m, v) > y:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)

if __name__ == "__main__":
    print("x knots:", [kn["value"] for kn in X.knots], "rejected:", [kn["value"] for kn in X.rejected])
    print("y knots:", [kn["value"] for kn in Y.knots], "rejected:", [kn["value"] for kn in Y.rejected])
    lg0 = math.log10(0.02)
    for k in range(0, 54):
        x = 10 ** (lg0 + 0.05 * k)
        if 0.06 < x < 10:
            print(f"k={k:2d} x={x:.4f}  v@u=760:{v_for_x(x, 760):7.1f}  v@u=1450:{v_for_x(x, 1450):7.1f}  v@u=2170:{v_for_x(x, 2170):7.1f}")
    for y in range(0, 101, 5):
        print(f"y={y:3d}  u@v=1500:{u_for_y(y, 1500):7.1f}  u@v=1800:{u_for_y(y, 1800):7.1f}  u@v=2100:{u_for_y(y, 2100):7.1f}")
