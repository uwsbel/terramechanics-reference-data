"""2D Hough-type search (angle, rho) for the diagonal lines of FC-6A, smoothed against binning
aliasing; prints the 2D local maxima. Reader's aid only."""
import json
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
cal = json.loads((HERE.parent / "cal-p1" / "calibration.json").read_text())
dark = g < 160
H, W = g.shape
mask = np.zeros_like(dark)
mask[1540:3060, 935:2380] = True
vv, uu = np.mgrid[0:H, 0:W]
for l in cal["vertical_lines"]:
    mask &= np.abs(uu - (l["u_at_v0"] + l["slope_du_dv"] * vv)) > 6
for l in cal["horizontal_lines"]:
    mask &= np.abs(vv - (l["v_at_u0"] + l["slope_dv_du"] * uu)) > 6
mask[0:1660, 0:2185] = False
pts = np.argwhere(dark & mask)
v = pts[:, 0].astype(float); u = pts[:, 1].astype(float)
angles = np.arange(42.0, 48.0, 0.1)
lo, hi = 2600, 3100
acc = np.zeros((len(angles), (hi - lo) * 4))
for k, a in enumerate(angles):
    r = np.radians(a)
    rho = u * np.sin(r) + v * np.cos(r)
    h, e = np.histogram(rho, bins=np.linspace(lo, hi, (hi - lo) * 4 + 1))
    acc[k] = np.convolve(h, np.ones(24), mode="same")  # 6 px window
# 2D maxima
from itertools import product
res = []
for k in range(1, len(angles) - 1):
    for j in range(12, acc.shape[1] - 12, 1):
        val = acc[k, j]
        if val < 900:
            continue
        if val >= acc[k-1:k+2, j-12:j+13].max():
            res.append((val, angles[k], lo + j / 4))
res.sort(reverse=True)
for val, a, rho in res[:25]:
    print(f"count {val:6.0f}  angle {a:5.2f}  rho {rho:7.2f}")
