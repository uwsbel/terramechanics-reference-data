"""Report a calibration: affine residuals in pixels and percent of span, and the D-025 ink check
of every line (verified knots and rejected lines). Usage: calcheck.py <tools_dir> <cal_dir> <image>"""
import sys, json
from pathlib import Path
import numpy as np
sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca

cal_dir, image = sys.argv[2], sys.argv[3]
cal = json.loads((Path(cal_dir) / "calibration.json").read_text(encoding="utf-8"))
an = ca.load_anchors(cal_dir)
tx, ty = ca.axis_transforms(cal)
ax, ay = np.array(cal["ax"]), np.array(cal["ay"])
U = np.array([[float(a["u"]), float(a["v"]), 1.0] for a in an])
X = np.array([ca.forward(tx, float(a["x_value"])) for a in an])
Y = np.array([ca.forward(ty, float(a["y_value"])) for a in an])
rx, ry = X - U @ ax, Y - U @ ay
xpp, ypp = np.hypot(*ax[:2]), np.hypot(*ay[:2])
spanx, spany = np.ptp(X), np.ptp(Y)
print(f"affine x: rms {np.sqrt((rx**2).mean())/xpp:.2f} px, max {np.abs(rx).max()/xpp:.2f} px; "
      f"rms {100*np.sqrt((rx**2).mean())/spanx:.3f} % of span, max {100*np.abs(rx).max()/spanx:.3f} %")
print(f"affine y (q): rms {np.sqrt((ry**2).mean())/ypp:.2f} px, max {np.abs(ry).max()/ypp:.2f} px; "
      f"rms {100*np.sqrt((ry**2).mean())/spany:.3f} % of span, max {100*np.abs(ry).max()/spany:.3f} %")
cal_, KX, KY = ca.piecewise_maps(cal_dir, image)
s = ca.knots_summary(KX, KY)
for k in ("x", "y", "rejected_x", "rejected_y"):
    for l in s[k]:
        c = l["ink_check"]
        print(f"{k:11s} {l['value']:>7g} err {l['location_error_px']:.2f} px  found {len(c.get('found', []))}/{c.get('positions')}"
              f"  ink_line_offset {c.get('ink_line_offset_px')} scatter {c.get('ink_scatter_px')} {l.get('reason','')}")
