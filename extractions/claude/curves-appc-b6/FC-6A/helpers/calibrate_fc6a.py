"""Calibration of FC-6A (p0131.png), panel 1.

Runs the same line detection as tools/calibrate_axes.py detect (imported, not modified) with
box 895 1215 2425 3025, bands 5, dark 200, min-frac 0.6. The tool finds every grid line except
y = 5000, which is hidden behind the legend box over most of its length; the tool would then
interpolate it from the frame (`predicted`). Instead, this helper measures that line on its two
visible segments (the tick/grid stub left of the legend, u 900 to 965, and the grid segment right
of the legend, u 2195 to 2380) column by column, fits v = a + b u through the run centers, and uses
the fitted line as a measured line. Anchors, affine fit and calibration.json layout are those of
the tool.
"""
import csv, json, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]
sys.path.insert(0, str(WS / "tools"))
import calibrate_axes as ca  # noqa: E402

IMG = WS / "packet" / "p0131.png"
BOX = [895, 1215, 2425, 3025]
BANDS, DARK, MINF, SNAP, FF = 5, 200, 0.6, 10, 0.5
XS = [0, 1000, 2000, 3000, 4000, 5000]
YS = [0, 1000, 2000, 3000, 4000, 5000, 6000]

g = np.asarray(Image.open(IMG).convert("L"))
vlines = ca.locate(g, BOX, [float(x) for x in XS], "v", BANDS, DARK, MINF, SNAP, FF)
hlines = ca.locate(g, BOX, [float(y) for y in reversed(YS)], "h", BANDS, DARK, MINF, SNAP, FF)

# measure y = 5000 on its visible segments
us = [u for u in range(900, 966) if not (911 <= u <= 924)] + list(range(2195, 2379))
pts = []
for u in us:
    col = g[1505:1550, u] < DARK
    idx = np.where(col)[0] + 1505
    if len(idx) == 0:
        continue
    # split into runs, keep the run nearest the expected line
    runs, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i != p + 1:
            runs.append((s, p)); s = i
        p = i
    runs.append((s, p))
    exp = 1535 - 0.0095 * (u - 930)
    s, p = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - exp))
    if p - s > 12:      # a vertical stroke, not the line
        continue
    pts.append((u, (s + p) / 2))
pts = np.array(pts, dtype=float)
b, a = np.polyfit(pts[:, 0], pts[:, 1], 1)
res = pts[:, 1] - (a + b * pts[:, 0])
print(f"y=5000 measured: v = {a:.1f} + {b:+.4f} u from {len(pts)} columns, rms {np.sqrt((res**2).mean()):.2f} px")
new_h = []
for l in hlines:
    if l[0] == 5000.0:
        if l[3] != "predicted":
            print("tool detected y=5000 itself:", l[3])
        new_h.append((5000.0, float(b), float(a), f"measured by out/FC-6A/helpers/calibrate_fc6a.py on visible segments u 900-965 and 2195-2378 ({len(pts)} columns)", pts[::10].tolist()))
    else:
        new_h.append(l)
hlines = new_h

anchors = []
for h in hlines:
    for v in vlines:
        u, vv = ca.intersect(h, v)
        anchors.append({"x_value": v[0], "y_value": h[0], "u": round(u, 1), "v": round(vv, 1), "x_source": v[3], "y_source": h[3]})
ax, ay, rmsx, rmsy, maxx, maxy = ca.fit_affine(anchors)
out = HERE.parent / "cal-p1"
out.mkdir(parents=True, exist_ok=True)
with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader(); w.writerows(anchors)
cal = {
    "image": "packet/p0131.png", "box": BOX, "bands": BANDS, "dark": DARK, "min_frac": MINF, "snap": SNAP,
    "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the grid intersections)",
    "ax": ax, "ay": ay,
    "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
    "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
    "n_anchors": len(anchors),
    "vertical_lines": [{"x_value": l[0], "slope_du_dv": l[1], "u_at_v0": l[2], "source": l[3], "samples": l[4]} for l in vlines],
    "horizontal_lines": [{"y_value": l[0], "slope_dv_du": l[1], "v_at_u0": l[2], "source": l[3], "samples": l[4]} for l in hlines],
    "helper": "out/FC-6A/helpers/calibrate_fc6a.py (tool detection imported from tools/calibrate_axes.py; y=5000 measured on its visible segments instead of predicted)",
}
(out / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(f"{len(anchors)} anchors; x: {cal['x_per_px']:.4f} per px, rms {rmsx:.3f}, max {maxx:.3f}; y: {cal['y_per_px']:.4f} per px, rms {rmsy:.3f}, max {maxy:.3f}")
for l in vlines:
    print(f"  vertical   x={l[0]:>6g}  u = {l[2]:.1f} + {l[1]:+.4f} v   ({l[3]})")
for l in hlines:
    print(f"  horizontal y={l[0]:>6g}  v = {l[2]:.1f} + {l[1]:+.4f} u   ({l[3]})")
