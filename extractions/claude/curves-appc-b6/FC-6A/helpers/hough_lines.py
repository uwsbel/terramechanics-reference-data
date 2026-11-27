"""Find the diagonal drawn lines of FC-6A by a Hough-type projection (reader's aid, not a reading).

Dark pixels inside the plot frame, minus the grid lines and frame (masked +-6 px around the
calibrated lines), are projected on the normal of a trial direction; peaks of the histogram are
straight lines. Prints, for the best angles, the peaks and the along-line extents of ink.
"""
import json, sys
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
U0, V0, U1, V1 = 935, 1540, 2380, 3060
mask[V0:V1, U0:U1] = True
vv, uu = np.mgrid[0:H, 0:W]
for l in cal["vertical_lines"]:
    uline = l["u_at_v0"] + l["slope_du_dv"] * vv
    mask &= np.abs(uu - uline) > 6
for l in cal["horizontal_lines"]:
    vline = l["v_at_u0"] + l["slope_dv_du"] * uu
    mask &= np.abs(vv - vline) > 6
# exclude legend box region
mask[0:1660, 0:2185] = False
pts = np.argwhere(dark & mask)
v = pts[:, 0].astype(float); u = pts[:, 1].astype(float)
print("dark pts", len(u))
best = []
for a in np.arange(40.0, 50.0, 0.05):
    r = np.radians(a)
    rho = u * np.sin(r) + v * np.cos(r)
    h, e = np.histogram(rho, bins=np.arange(rho.min(), rho.max() + 1, 1.0))
    best.append((h.max(), a))
best.sort(reverse=True)
print("top angles", best[:10])
for a in [float(sys.argv[1])] if len(sys.argv) > 1 else [best[0][1]]:
    r = np.radians(a)
    rho = u * np.sin(r) + v * np.cos(r)
    h, e = np.histogram(rho, bins=np.arange(np.floor(rho.min()), rho.max() + 1, 1.0))
    sm = np.convolve(h, np.ones(5), mode="same")
    peaks = [i for i in range(2, len(sm) - 2) if sm[i] == sm[i-2:i+3].max() and sm[i] > 150]
    print(f"angle {a:.2f}")
    for i in peaks:
        print(f"  rho {e[i]:.0f}  count5 {sm[i]:.0f}")
