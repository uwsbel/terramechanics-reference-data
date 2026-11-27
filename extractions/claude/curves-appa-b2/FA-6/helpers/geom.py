"""Geometry from the reader's own calibration (cal-p1), via the tool's piecewise map (read-only import):
where a given grain size or percent lies on the page. Used to place sampling locations, never for values."""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3] / "tools"))
import calibrate_axes as ca

WS = HERE.parents[3]
CAL = WS / "out" / "FA-6" / "cal-p1"
IMG = WS / "out" / "FA-6" / "p0014-table-masked.png"
_cal, X, Y = ca.piecewise_maps(str(CAL), str(IMG))

def xval(u, v):
    return X.value(u, v)[0]

def yval(u, v):
    return Y.value(u, v)[0]

def v_of_x(x, u, lo=1100.0, hi=3800.0):
    """page v where grain size x lies at column u (x decreases with v)."""
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if xval(u, m) > x:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)

def u_of_y(y, v, lo=760.0, hi=2290.0):
    """page u where percent y lies at row v (y decreases with u)."""
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if yval(m, v) > y:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)

if __name__ == "__main__":
    for k in range(-18, 13):
        x = 10 ** (k * 0.05)
        print(f"{k*0.05:+.2f} x={x:.4f}  v@u800={v_of_x(x, 800):.1f} v@u1500={v_of_x(x, 1500):.1f} v@u2200={v_of_x(x, 2200):.1f}")
    for y in range(0, 101, 5):
        print(f"y={y}: u@v1500={u_of_y(y, 1500):.1f} u@v1900={u_of_y(y, 1900):.1f} u@v2600={u_of_y(y, 2600):.1f}")
