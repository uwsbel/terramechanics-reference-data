"""Calibration of F2-44 (p0104.png), Claude reader, batch curves-s2-b3.

The key box at the top covers the middle of the 2000 lb frame line, and its bottom edge (v ~1750)
is a long dark line that `calibrate_axes.py detect` takes for the 2000 line when the box reaches the
top frame. So:
1. `detect` is run on a box below the key box (y lines 0 to 1500, x lines 0 to 5): out/F2-44/cal-detect-lower.
2. This helper measures the 2000 line only on the parts that show (left of the key box, u 752 to 1036,
   and right of it, u 1980 to 2276): in each column the centre of the dark run of the thick frame line
   near v = 1700, then a straight line fitted to those centres.
3. The 2000 line is anchored at its crossings with the x = 0, 1, 4 and 5 lines (all visible on the
   page); the crossings with x = 2 and x = 3 lie under the key box and are not anchors.
4. cal-p1/anchors.csv and cal-p1/calibration.json are written in the layout of `detect`, with the
   affine map refitted on all anchors.
"""
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[1]
IMG = WS / "packet" / "p0104.png"
LOWER = HERE / "cal-detect-lower"
OUT = HERE / "cal-p1"

g = np.asarray(Image.open(IMG).convert("L"), dtype=float)
cal = json.loads((LOWER / "calibration.json").read_text(encoding="utf-8"))

# --- 2. measure the 2000 line on its visible parts
DARK = 200
cols = list(range(752, 1037, 4)) + list(range(1980, 2277, 4))
pts = []
for u in cols:
    prof = g[1675:1726, u]
    d = prof < DARK
    idx = np.where(d)[0]
    if len(idx) == 0:
        continue
    # longest run of dark pixels: the frame line
    runs, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i != p + 1:
            runs.append((s, p)); s = i
        p = i
    runs.append((s, p))
    s, p = max(runs, key=lambda r: r[1] - r[0])
    w = 255.0 - prof[s:p + 1]
    vc = 1675 + float(np.sum(np.arange(s, p + 1) * w) / np.sum(w))
    pts.append((u, vc, p - s + 1))
P = np.array(pts)
b, a = np.polyfit(P[:, 0], P[:, 1], 1)           # v = a + b u
res = P[:, 1] - (a + b * P[:, 0])
keep = np.abs(res) <= max(1.5, 3 * 1.4826 * np.median(np.abs(res - np.median(res))))
b, a = np.polyfit(P[keep, 0], P[keep, 1], 1)
res = P[keep, 1] - (a + b * P[keep, 0])
print(f"2000 line: v = {a:.2f} + {b:+.5f} u from {keep.sum()} of {len(P)} columns; "
      f"rms {np.sqrt(np.mean(res**2)):.2f} px, max {np.abs(res).max():.2f} px; "
      f"thickness median {np.median(P[:, 2]):.0f} px")
left, right = P[P[:, 0] < 1500], P[P[:, 0] > 1500]
for name, Q in (("left", left), ("right", right)):
    bb, aa = np.polyfit(Q[:, 0], Q[:, 1], 1)
    print(f"  {name} part alone: v = {aa:.2f} + {bb:+.5f} u ({len(Q)} columns); "
          f"at u=1500 {aa + bb * 1500:.2f} vs joint {a + b * 1500:.2f}")

src2000 = (f"measured on the visible parts (u 752 to 1036 and 1980 to 2276, {int(keep.sum())} columns); "
           "the key box covers the middle")
samples2000 = [[float(u), round(float(v), 2)] for (u, v, _), k in zip(pts, keep) if k]


def intersect(hs, hi, vs, vi):
    u = (vi + vs * hi) / (1 - vs * hs)
    return u, hi + hs * u


# --- 3. anchors
anchors = []
with (LOWER / "anchors.csv").open(encoding="utf-8") as f:
    lower = list(csv.DictReader(f))
vl = {l["x_value"]: l for l in cal["vertical_lines"]}
for xv in (0.0, 1.0, 4.0, 5.0):
    l = vl[xv]
    u, v = intersect(b, a, l["slope_du_dv"], l["u_at_v0"])
    anchors.append({"x_value": xv, "y_value": 2000.0, "u": round(u, 1), "v": round(v, 1),
                    "x_source": l["source"], "y_source": src2000})
anchors += lower

# --- 4. affine refit and output
U = np.array([[float(r["u"]), float(r["v"]), 1.0] for r in anchors])
X = np.array([float(r["x_value"]) for r in anchors])
Y = np.array([float(r["y_value"]) for r in anchors])
ax, *_ = np.linalg.lstsq(U, X, rcond=None)
ay, *_ = np.linalg.lstsq(U, Y, rcond=None)
rx, ry = X - U @ ax, Y - U @ ay
OUT.mkdir(parents=True, exist_ok=True)
with (OUT / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader()
    w.writerows(anchors)
new = dict(cal)
new["image"] = "packet/p0104.png"
new["box"] = [725, 1675, 2300, 3270]
new["note"] = ("detect run on box 725 1790 2300 3270 (below the key box) for x = 0..5 and y = 0..1500; "
               "the y = 2000 frame line measured by out/F2-44/cal_helper.py on its visible parts and anchored "
               "at x = 0, 1, 4, 5 only (x = 2, 3 cross it under the key box); affine map refitted on all anchors")
new["ax"], new["ay"] = ax.tolist(), ay.tolist()
new["x_per_px"], new["y_per_px"] = float(np.hypot(ax[0], ax[1])), float(np.hypot(ay[0], ay[1]))
new["rms_residual_x"], new["rms_residual_y"] = float(np.sqrt((rx**2).mean())), float(np.sqrt((ry**2).mean()))
new["max_residual_x"], new["max_residual_y"] = float(np.abs(rx).max()), float(np.abs(ry).max())
new["n_anchors"] = len(anchors)
new["horizontal_lines"] = [{"y_value": 2000.0, "slope_dv_du": float(b), "v_at_u0": float(a),
                            "source": src2000, "samples": samples2000}] + cal["horizontal_lines"]
(OUT / "calibration.json").write_text(json.dumps(new, indent=1), encoding="utf-8")
print(f"{len(anchors)} anchors; x rms {new['rms_residual_x']:.4f} max {new['max_residual_x']:.4f}; "
      f"y rms {new['rms_residual_y']:.3f} max {new['max_residual_y']:.3f}")
for r, xr, yr in zip(anchors, rx, ry):
    print(f"  x={r['x_value']} y={r['y_value']} u={r['u']} v={r['v']} res x {xr:+.4f} y {yr:+.2f}")
