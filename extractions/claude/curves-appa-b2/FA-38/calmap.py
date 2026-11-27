"""Reader helper: forward and inverse piecewise maps of cal-p1 (tools/calibrate_axes.py, unmodified)."""
import sys, math
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import calibrate_axes as ca
IMAGE = str(HERE.parents[1] / "packet" / "p0077.png")
_cal, X, Y = ca.piecewise_maps(str(HERE / "cal-p1"), IMAGE)
KV = [1250, 1300, 1340, 1420, 1500, 1580, 1660, 1740, 1820, 1900, 1980, 2100, 2220, 2340, 2460, 2580, 2700, 2780, 2860, 2940, 3020, 3100, 3180, 3240]
KU = [670, 690, 706, 724, 770, 822, 875, 912, 955, 995, 1022, 1050, 1080, 1110, 1145, 1178, 1213, 1246, 1274, 1308, 1345, 1383, 1420, 1450]
def c(v): return float(np.interp(v, KV, KU))
def xy(u, v): return X.value(u, v)[0], Y.value(u, v)[0]
def v_of_g(g, u):
    """v on column u where grain size = g (bisection; x increases upward)."""
    lo, hi = 1100.0, 3800.0
    for _ in range(60):
        m = (lo + hi) / 2
        if X.value(u, m)[0] > g: lo = m
        else: hi = m
    return (lo + hi) / 2
def u_of_p(p, v):
    lo, hi = 650.0, 2200.0
    for _ in range(60):
        m = (lo + hi) / 2
        if Y.value(m, v)[0] > p: lo = m
        else: hi = m
    return (lo + hi) / 2
if __name__ == "__main__":
    for k in range(-24, 18):
        g = 10 ** (0.05 * k)
        # v at the curve's column (iterate u = c(v))
        v = 2000.0
        for _ in range(5):
            v = v_of_g(g, c(v))
        print(f"k {k:4d} g {g:8.4f} v {v:7.1f} u_c {c(v):7.1f}")
