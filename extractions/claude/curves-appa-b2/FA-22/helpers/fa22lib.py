"""Shared helpers for the FA-22 reading: the piecewise maps of cal-p1 (via tools/calibrate_axes.py,
loaded read-only) and their inverses, used only to place sampling lines and to check positions."""
import importlib.util
from pathlib import Path
import numpy as np
from PIL import Image

WS = Path(__file__).resolve().parents[3]
OUT = WS / "out" / "FA-22"
spec = importlib.util.spec_from_file_location("cal", WS / "tools" / "calibrate_axes.py")
cal = importlib.util.module_from_spec(spec); spec.loader.exec_module(cal)
PAGE = WS / "packet" / "p0047.png"
C, X, Y = cal.piecewise_maps(str(OUT / "cal-p1"), str(PAGE))

def xy(u, v):
    return X.value(u, v)[0], Y.value(u, v)[0]

def v_of_x(x, u, v0=1100.0, v1=3900.0):
    """v on the page where grain size = x at column u (bisection; x decreases as v increases)."""
    lo, hi = v0, v1
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if X.value(u, m)[0] > x:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)

def u_of_y(y, v, u0=700.0, u1=2300.0):
    lo, hi = u0, u1
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if Y.value(m, v)[0] > y:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)

def page():
    return np.asarray(Image.open(PAGE).convert("L"))
