"""Tick-mark calibration for FC-2A (a frame with tick marks only, no interior grid lines).

Why this exists: tools/calibrate_axes.py assumes grid lines, with frame lines at the first and last
printed values. FC-2A has no interior grid lines and its top frame line (about 6450 psf, unlabeled)
is not at a printed value; the tool took the legend box edge as y = 6000 (see
cal-tool-attempt/). Here the anchors are the drawn tick marks instead:

1. The left axis (x = 0) and the bottom axis (y = 0) are fitted as straight lines from the centers
   of their ink in many rows/columns away from ticks and curves.
2. Each y tick is a short horizontal stroke through the left axis; its v center is measured in the
   columns just left of the axis (the stroke itself, not the label). Anchor: (x=0, y=value) on
   the axis line at that v.
3. Each x tick is a short vertical stroke through the bottom axis; its u center is measured in the
   rows just below the axis. Anchor: (x=value, y=0) on the axis line at that u.
4. The origin (axis intersection) is an anchor (0, 0). The right frame line meets the bottom axis
   where the 5000 label sits and no separate tick is drawn there; it is taken as x = 5000 (checked:
   the 0 to 4000 ticks extrapolate to within a few pixels of it).
5. An affine map value = A [u v 1] is fitted by least squares to all anchors, in the same JSON
   layout as tools/calibrate_axes.py so `calibrate_axes.py apply` can use it.

usage: python tick_calibrate.py <page.png> <out_dir> [--no-right-frame]
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

img = sys.argv[1]
out = Path(sys.argv[2])
use_right = "--no-right-frame" not in sys.argv
out.mkdir(parents=True, exist_ok=True)
g = np.asarray(Image.open(img).convert("L")) < 128


def center_of_run(arr, off, near=None):
    idx = np.where(arr)[0]
    if len(idx) == 0:
        return None
    runs, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i != p + 1:
            runs.append((s, p))
            s = i
        p = i
    runs.append((s, p))
    if near is None:
        r = max(runs, key=lambda r: r[1] - r[0])
    else:
        r = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 + off - near))
    return (r[0] + r[1]) / 2 + off, r[1] - r[0] + 1


tick_rows_guess = [1611, 1890, 2200, 2490, 2775, 3080]   # 6000 .. 1000, from the crops
tick_cols_guess = [1250, 1526, 1813, 2113]               # 1000 .. 4000

# 1. left axis
left = []
for v in range(1480, 3180, 4):
    if any(abs(v - t) < 30 for t in tick_rows_guess):
        continue
    c = center_of_run(g[v, 930:990], 930, near=958)
    if c and c[1] <= 9:
        left.append((v, c[0]))
left = np.array(left)
bl, al = np.polyfit(left[:, 0], left[:, 1], 1)       # u = al + bl v
resl = left[:, 1] - (al + bl * left[:, 0])
# bottom axis
bot = []
for u in range(1000, 2390, 4):
    if any(abs(u - t) < 30 for t in tick_cols_guess):
        continue
    c = center_of_run(g[3340:3400, u], 3340, near=3372)
    if c and c[1] <= 10:
        bot.append((u, c[0]))
bot = np.array(bot)
bb, ab = np.polyfit(bot[:, 0], bot[:, 1], 1)         # v = ab + bb u
resb = bot[:, 1] - (ab + bb * bot[:, 0])
# right frame
right = []
for v in range(1520, 3370, 4):
    c = center_of_run(g[v, 2380:2440], 2380, near=2410)
    if c and c[1] <= 10:
        right.append((v, c[0]))
right = np.array(right)
br, ar = np.polyfit(right[:, 0], right[:, 1], 1)


def axis_u(v):
    return al + bl * v


def axis_v(u):
    return ab + bb * u


# y ticks
yticks = []
for val, vg in zip([6000, 5000, 4000, 3000, 2000, 1000], tick_rows_guess):
    cs = []
    ua = axis_u(vg)
    for u in range(int(round(ua - 18)), int(round(ua - 7))):
        c = center_of_run(g[vg - 25:vg + 25, u], vg - 25, near=vg)
        if c and c[1] <= 10:
            cs.append((u, c[0], c[1]))
    cs = np.array(cs)
    vc = float(np.median(cs[:, 1]))
    yticks.append({"value": val, "v_center": vc, "n_cols": len(cs), "thick_px": float(np.median(cs[:, 2])),
                   "v_spread": float(cs[:, 1].max() - cs[:, 1].min()), "u_at_axis": float(axis_u(vc))})
# x ticks
xticks = []
for val, ug in zip([1000, 2000, 3000, 4000], tick_cols_guess):
    cs = []
    va = axis_v(ug)
    for v in range(int(round(va + 7)), int(round(va + 20))):
        c = center_of_run(g[v, ug - 25:ug + 25], ug - 25, near=ug)
        if c and c[1] <= 10:
            cs.append((v, c[0], c[1]))
    cs = np.array(cs)
    uc = float(np.median(cs[:, 1]))
    vmid = float(np.median(cs[:, 0]))
    va = axis_v(uc)
    u_at_axis = uc + bl * (va - vmid)     # carry the tick to the axis parallel to the left axis
    xticks.append({"value": val, "u_center_below": uc, "v_probe_mid": vmid, "n_rows": len(cs),
                   "thick_px": float(np.median(cs[:, 2])), "u_spread": float(cs[:, 1].max() - cs[:, 1].min()),
                   "u_at_axis": float(u_at_axis), "v_at_axis": float(axis_v(u_at_axis))})

u0 = (al + bl * ab) / (1 - bl * bb)
v0 = ab + bb * u0
u5 = (ar + br * ab) / (1 - br * bb)
v5 = ab + bb * u5

anchors = [{"x_value": 0.0, "y_value": 0.0, "u": u0, "v": v0, "x_source": "origin (axis intersection)",
            "y_source": "origin (axis intersection)"}]
for t in xticks:
    anchors.append({"x_value": float(t["value"]), "y_value": 0.0, "u": t["u_at_axis"], "v": t["v_at_axis"],
                    "x_source": "x tick", "y_source": "bottom axis"})
if use_right:
    anchors.append({"x_value": 5000.0, "y_value": 0.0, "u": u5, "v": v5,
                    "x_source": "right frame line (no tick; 5000 label below it)", "y_source": "bottom axis"})
for t in yticks:
    anchors.append({"x_value": 0.0, "y_value": float(t["value"]), "u": t["u_at_axis"], "v": t["v_center"],
                    "x_source": "left axis", "y_source": "y tick"})

U = np.array([[a["u"], a["v"], 1.0] for a in anchors])
X = np.array([a["x_value"] for a in anchors])
Y = np.array([a["y_value"] for a in anchors])
ax, *_ = np.linalg.lstsq(U, X, rcond=None)
ay, *_ = np.linalg.lstsq(U, Y, rcond=None)
rx, ry = X - U @ ax, Y - U @ ay
for a, ex, ey in zip(anchors, rx, ry):
    a["u"] = round(float(a["u"]), 2)
    a["v"] = round(float(a["v"]), 2)
    a["res_x"] = round(float(ex), 2)
    a["res_y"] = round(float(ey), 2)
with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(anchors[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(anchors)
cal = {
    "image": img,
    "method": "tick marks (out/FC-2A/helpers/tick_calibrate.py, see its docstring); tools/calibrate_axes.py "
              "detect does not apply (no grid lines, top frame not at a printed value)",
    "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on tick anchors)",
    "ax": ax.tolist(), "ay": ay.tolist(),
    "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
    "rms_residual_x": float(np.sqrt((rx ** 2).mean())), "rms_residual_y": float(np.sqrt((ry ** 2).mean())),
    "max_residual_x": float(np.abs(rx).max()), "max_residual_y": float(np.abs(ry).max()),
    "n_anchors": len(anchors),
    "left_axis": {"u_at_v0": float(al), "slope_du_dv": float(bl), "n": len(left), "rms_px": float(np.sqrt((resl ** 2).mean()))},
    "bottom_axis": {"v_at_u0": float(ab), "slope_dv_du": float(bb), "n": len(bot), "rms_px": float(np.sqrt((resb ** 2).mean()))},
    "right_frame": {"u_at_v0": float(ar), "slope_du_dv": float(br), "n": len(right), "used_as_x5000": use_right},
    "x_ticks": xticks, "y_ticks": yticks,
}
(out / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(json.dumps({k: cal[k] for k in ["ax", "ay", "x_per_px", "y_per_px", "rms_residual_x", "rms_residual_y",
                                      "max_residual_x", "max_residual_y", "left_axis", "bottom_axis", "right_frame"]}, indent=1))
for a in anchors:
    print(a)
for t in xticks:
    print(t)
for t in yticks:
    print(t)
