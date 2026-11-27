"""Shared helpers for reading the traces of Figure 5-25: the page, the grid masks and the
piecewise maps of the tool (tools/calibrate_axes.py), with inverse lookups."""
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]                       # the workspace (F5-25/)
sys.path.insert(0, str(WS / "tools"))
import calibrate_axes as ca                # noqa: E402

IMG = WS / "packet" / "p0330.png"
GRAY = np.asarray(Image.open(IMG).convert("L"))
DARK = GRAY < 128
LINES = json.load(open(HERE / "lines.json", encoding="utf-8"))

# vertical opening: removes ink thinner than 5 px vertically (the time-line dashes, 1 to 3 px thick)
def _vopen(mask, k=5):
    h = mask.shape[0]
    er = mask.copy()
    for s in range(1, k):
        er[:h - s] &= mask[s:]
    er[h - k + 1:] = False
    out = er.copy()
    for s in range(1, k):
        out[s:] |= er[:h - s]
    return out

THICK = _vopen(DARK)


def vline_band(u, v, half=3.5):
    """True where (u, v) lies on a measured vertical grid line (any panel, frames included)."""
    for L in LINES["vertical"]:
        if abs(u - (L["u_at_v0"] + L["slope_du_dv"] * v)) <= half:
            return True
    # the left frame of panel 1 and the line at u 825 are far from the traces; not needed
    return False


class Panel:
    def __init__(self, n):
        self.n = n
        self.cal, self.X, self.Y = ca.piecewise_maps(str(HERE.parent / f"cal-p{n}"))
        self.urange = {1: (985, 1266), 2: (1395, 1690), 3: (1835, 2300)}[n]

    def xy(self, u, v):
        return self.X.value(u, v)[0], self.Y.value(u, v)[0]

    def v_at_t(self, u, t):
        lo, hi = 1700.0, 3600.0                # x decreases with v
        for _ in range(60):
            m = 0.5 * (lo + hi)
            if self.X.value(u, m)[0] > t:
                lo = m
            else:
                hi = m
        return 0.5 * (lo + hi)

    def u_at_y(self, v, y):
        lo, hi = self.urange[0] - 60.0, self.urange[1] + 60.0
        inc = self.Y.value(hi, v)[0] > self.Y.value(lo, v)[0]
        for _ in range(60):
            m = 0.5 * (lo + hi)
            if (self.Y.value(m, v)[0] < y) == inc:
                lo = m
            else:
                hi = m
        return 0.5 * (lo + hi)
