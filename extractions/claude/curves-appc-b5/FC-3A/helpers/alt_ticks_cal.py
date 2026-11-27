"""Sensitivity check, not the reading's calibration: an affine map fitted by least squares to the printed
tick marks of FC-3A (each tick where it meets its axis) and the axis corner, instead of to the frame lines.
Written in the calibrate_axes.py format so that `calibrate_axes.py apply` can use it."""
import csv, json, sys, numpy as np
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
A = []
for r in rows:
    val = float(r["printed_label"]); u, v = float(r["mark_u"]), float(r["mark_v"])
    if r["axis"] == "x":
        if val == 0: A.append((0.0, 0.0, u, v)); continue          # the axis corner, once
        A.append((val, 0.0, u, v))
    elif val != 0:
        A.append((0.0, val, u, v))
U = np.array([[a[2], a[3], 1.0] for a in A]); Xv = np.array([a[0] for a in A]); Yv = np.array([a[1] for a in A])
ax, *_ = np.linalg.lstsq(U, Xv, rcond=None); ay, *_ = np.linalg.lstsq(U, Yv, rcond=None)
rx, ry = Xv - U @ ax, Yv - U @ ay
cal = {"image": "packet/p0123.png", "model": "affine least squares on printed tick marks (sensitivity check only)",
       "ax": ax.tolist(), "ay": ay.tolist(), "x_per_px": float(np.hypot(*ax[:2])), "y_per_px": float(np.hypot(*ay[:2])),
       "rms_residual_x": float(np.sqrt((rx ** 2).mean())), "rms_residual_y": float(np.sqrt((ry ** 2).mean())),
       "max_residual_x": float(np.abs(rx).max()), "max_residual_y": float(np.abs(ry).max()), "n_anchors": len(A),
       "anchors": [{"x_value": a[0], "y_value": a[1], "u": a[2], "v": a[3], "res_x": float(e), "res_y": float(f)} for a, e, f in zip(A, rx, ry)]}
json.dump(cal, open(sys.argv[2], "w"), indent=1)
print("x per px %.4f rms %.2f max %.2f ; y per px %.4f rms %.2f max %.2f" % (cal["x_per_px"], cal["rms_residual_x"], cal["max_residual_x"], cal["y_per_px"], cal["rms_residual_y"], cal["max_residual_y"]))
for a, e, f in zip(A, rx, ry): print("  anchor x=%5g y=%5g  res x %+6.1f  y %+6.1f" % (a[0], a[1], e, f))
