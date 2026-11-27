"""By-eye label check support for FC-6A: the center of each printed axis label (bounding box of its
digits, found in label strips outside the frame) against the calibrated grid line it names. The
reader confirmed on crops (crops2/xlabels.png, ylabels.png, yl_top.png) that each label sits at
the grid line or frame line it names; this script measures how far apart they are. Writes
out/FC-6A/calibration-eye-checks.csv."""
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
cal = json.loads((OUT / "cal-p1" / "calibration.json").read_text())
ax, ay = cal["ax"], cal["ay"]
dark = g < 160


def bbox(u0, v0, u1, v1):
    sub = dark[v0:v1, u0:u1]
    rows_ = np.where(sub.sum(axis=1) >= 4)[0]      # rows and columns with at least 4 dark pixels: digits,
    cols_ = np.where(sub.sum(axis=0) >= 4)[0]      # not isolated specks
    return u0 + cols_.min(), v0 + rows_.min(), u0 + cols_.max(), v0 + rows_.max()


rows = []
# x labels: strip below the frame, v 3045-3095; label windows around each grid line
for xv, (u0, u1) in {1000: (1160, 1300), 2000: (1450, 1600), 3000: (1745, 1880), 4000: (2040, 2190),
                     5000: (2330, 2470)}.items():
    bu0, bv0, bu1, bv1 = bbox(u0, 3040, u1, 3100)
    uc, vc = (bu0 + bu1) / 2, (bv0 + bv1) / 2
    l = [l for l in cal["vertical_lines"] if l["x_value"] == xv][0]
    v_axis = 3005.0
    u_line = l["u_at_v0"] + l["slope_du_dv"] * v_axis
    x_at_label = ax[0] * uc + ax[1] * v_axis + ax[2]
    rows.append({"figure_id": "FC-6A", "panel": 1, "axis": "x", "printed_label": xv,
                 "label_center_u": uc, "label_center_v": vc,
                 "grid_line_position_px": round(u_line, 1), "offset_px": round(uc - u_line, 1),
                 "value_at_label_center": round(x_at_label, 1),
                 "result": "confirmed: label centered under the grid line it names" if xv < 5000
                 else "confirmed: label centered under the right frame line"})
# y labels: strip left of the frame, u 740-870
for yv, (v0, v1) in {1000: (2680, 2745), 2000: (2385, 2450), 3000: (2090, 2160), 4000: (1795, 1860),
                     5000: (1505, 1565), 6000: (1215, 1275)}.items():
    bu0, bv0, bu1, bv1 = bbox(740, v0, 880, v1)
    uc, vc = (bu0 + bu1) / 2, (bv0 + bv1) / 2
    l = [l for l in cal["horizontal_lines"] if l["y_value"] == yv][0]
    u_axis = 925.0
    v_line = l["v_at_u0"] + l["slope_dv_du"] * u_axis
    y_at_label = ay[0] * u_axis + ay[1] * vc + ay[2]
    rows.append({"figure_id": "FC-6A", "panel": 1, "axis": "y", "printed_label": yv,
                 "label_center_u": uc, "label_center_v": vc,
                 "grid_line_position_px": round(v_line, 1), "offset_px": round(vc - v_line, 1),
                 "value_at_label_center": round(y_at_label, 1),
                 "result": ("confirmed: label level with the grid line it names" if yv < 6000
                            else "confirmed: label level with the top frame line")
                 + ("; this line is hidden behind the legend inside the frame and was measured on its two visible "
                    "segments (stub left of the frame, segment right of the legend)" if yv == 5000 else "")})
cols = ["figure_id", "panel", "axis", "printed_label", "label_center_u", "label_center_v", "grid_line_position_px",
        "offset_px", "value_at_label_center", "result"]
with (OUT / "calibration-eye-checks.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r)
