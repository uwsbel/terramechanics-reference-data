"""Bounding boxes of the printed axis labels of FB-6 (ink outside the frame, grouped by gaps), with the
position of the line each label is checked against (from cal-p1/calibration.json)."""
import json
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
cal = json.loads(open(sys.argv[2], encoding="utf-8").read())
dark = g < 128


def groups(mask_1d, gap):
    idx = np.where(mask_1d)[0]
    if not len(idx):
        return []
    parts = np.split(idx, np.where(np.diff(idx) > gap)[0] + 1)
    return [(int(p[0]), int(p[-1])) for p in parts]


F = cal["frames"]
# y labels: left of the left frame (frame centre u = c + k v, label ink ends 15 px or more left of it)
print("y labels (v extent, centre; u extent)")
sub = dark[780:4070, 520:625]
for a, b in groups(sub.any(axis=1), 12):
    v0, v1 = a + 780, b + 780
    cols = np.where(sub[a:b + 1].any(axis=0))[0] + 520
    vc = (v0 + v1) / 2
    hl = min(cal["horizontal_lines"], key=lambda h: abs(h["v_at_u0"] + h["slope_dv_du"] * (cols.max() + 30) - vc))
    vl = hl["v_at_u0"] + hl["slope_dv_du"] * ((cols.min() + cols.max()) / 2)
    print(f"  v {v0}..{v1} centre {vc:.1f}; u {cols.min()}..{cols.max()}; nearest line y={hl['y_value']} at v {vl:.1f} (same u); label minus line {vc - vl:+.1f} px")
print("x labels (u extent, centre; v extent)")
sub = dark[4036:4100, 680:2680]
for a, b in groups(sub.any(axis=0), 20):
    u0, u1 = a + 680, b + 680
    rows = np.where(sub[:, a:b + 1].any(axis=1))[0] + 4036
    uc = (u0 + u1) / 2
    vline = min(cal["vertical_lines"], key=lambda l: abs(l["u_at_v0"] + l["slope_du_dv"] * rows.mean() - uc))
    ul = vline["u_at_v0"] + vline["slope_du_dv"] * ((rows.min() + rows.max()) / 2)
    print(f"  u {u0}..{u1} centre {uc:.1f}; v {rows.min()}..{rows.max()}; nearest line x={vline['x_value']} at u {ul:.1f} (same v); label minus line {uc - ul:+.1f} px")
