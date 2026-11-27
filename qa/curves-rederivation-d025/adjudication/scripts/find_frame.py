"""Measure the left frame (x = 0) of a panel on the page, independently of either reading's anchors.

The search starts from the reading's own lines (x = 0 extrapolated from its two lowest x lines), looks
+-60 px around that for the darkest column in bands of the panel's height, and refines each band's
position with the ink check of tools/calibrate_axes.py. Prints knots.csv rows."""
import csv
import sys
sys.path.insert(0, "tools")
import numpy as np
from PIL import Image
import calibrate_axes as ca

fig, page, cal_dir, panel, reader = sys.argv[1:6]
gray = np.asarray(Image.open(page).convert("L"), dtype=float)
cal, X, Y = ca.piecewise_maps(cal_dir)
k1, k2 = sorted(X.knots, key=lambda k: k["value"])[:2]
assert k1["value"] > 0, "the reading has an x = 0 line already"
yk = sorted(Y.knots, key=lambda k: k["value"])
vtop, vbot = cal["box"][1], cal["box"][3]   # the reading's box spans the panel's height
rows = []
for vc in np.arange(vtop + 25, vbot - 24, 50):
    t = X.coords(0, vc)[1]
    s_pred = X.line_s(k1, t) - (k1["value"] - 0) / (k2["value"] - k1["value"]) * (X.line_s(k2, t) - X.line_s(k1, t))
    p_pred = s_pred * X.e_s + t * X.e_t
    best = None
    for ds in np.arange(-60, 60.5, 1.0):
        p = p_pred + ds * X.e_s
        u, v = int(round(p[0])), int(round(p[1]))
        g = gray[v - 20:v + 21, u].mean()
        if best is None or g < best[0]:
            best = (g, p)
    if best[0] > 100:          # no long dark line in this band (a gap in the frame)
        continue
    off = ca.ink_offset(gray, best[1], X.e_s, X.e_t)
    if off is None:
        continue
    q = best[1] + off * X.e_s
    rows.append((round(float(q[0]), 2), round(float(q[1]), 1)))
us = np.array([r[0] for r in rows])
vv = np.array([r[1] for r in rows])
fit = np.polyfit(vv, us, 1)
res = us - np.polyval(fit, vv)
print(f"{fig} p{panel} {reader}: {len(rows)} frame points, u = {fit[1]:.2f} + {fit[0]:.5f} v, residual RMS {np.sqrt(np.mean(res**2)):.2f} px, "
      f"max {np.abs(res).max():.2f}; the reading's map puts x = {X.value(rows[len(rows)//2][0], rows[len(rows)//2][1])[0]:.3f} there", file=sys.stderr)
w = csv.writer(sys.stdout, lineterminator="\n")
for u, v in rows:
    w.writerow([fig, panel, reader, 0, "", u, v,
                "left frame, measured on the page (value 0 inferred: the first lower-panel symbols sit on it; D-025)", "",
                "the reader's calibration box left the frame out; recovered by Claude 2026-10-14, independently of the other reading"])
