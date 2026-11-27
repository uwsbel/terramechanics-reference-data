"""Write calibration-eye-checks.csv for FB-7: printed axis labels against the lines they were anchored to.
The by-eye verdicts were made on the zoomed crops crop_bl, crop_tl, crop_br, crop_x8_10, crop_y6_5,
crop_l1, crop_l2 (zoom 3); the numbers here are the label ink's bounding-box centres and the fitted lines."""
import json, csv, sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert('L')) < 128
cal = json.load(open(sys.argv[2] + '/calibration.json', encoding='utf-8'))
ax, ay = cal['ax'], cal['ay']
X = lambda u, v: ax[0]*u + ax[1]*v + ax[2]
Y = lambda u, v: ay[0]*u + ay[1]*v + ay[2]
def bb(u0, u1, v0, v1):
    sub = g[v0:v1, u0:u1]; ys, xs = np.where(sub)
    assert sub[0].sum() == 0 and sub[-1].sum() == 0 and sub[:, 0].sum() == 0 and sub[:, -1].sum() == 0, (u0, u1, v0, v1)
    return (xs.min()+xs.max())/2+u0, (ys.min()+ys.max())/2+v0
L = lambda v: 486.40+0.00561*v; R = lambda v: 2733.34+0.00432*v; B = lambda u: 3938.51-0.00185*u; T = lambda u: 852.78-0.00004*u
rows = []
xl = [("0", 0, (503, 545, 3944, 4010), "left frame line", L(3936), "printed 13 px right of the frame line, under the corner; the next line (tick 2) is 284 px away, so the label can only belong to the frame; the frame carries the x = 0 symbols"),
      ("2", 2, (750, 795, 3944, 4010), "tick", 792.89, "printed 22 px left of its tick, the largest offset on the axis; still 260 px from any other line"),
      ("8", 8, (1605, 1660, 3944, 4010), "tick", 1632.66, "centred under its tick"),
      ("10", 10, (1890, 1965, 3944, 4010), "tick", 1911.50, "the '1' of '10' sits under the tick"),
      ("16", 16, (2710, 2790, 3944, 4010), "right frame line", R(3934), "centred under the right frame line; tick spacing 2 to 14 (mean 280.3 px) puts 16 at 2754.8, 4.5 px from the frame")]
for lab, val, w, kind, lu, note in xl:
    cu, cv = bb(*w); vline = B(lu)
    rows.append({"axis": "x", "printed_label": lab, "value": val, "anchored_to": kind, "line_u": round(lu, 1), "line_v": round(vline, 1),
                 "label_center_u": round(cu, 1), "label_center_v": round(cv, 1), "label_offset_px": round(cu-lu, 1),
                 "affine_value_at_line": round(X(lu, vline), 4), "by_eye": "agrees", "note": note})
yl = [("0", 0, (462, 502, 3905, 3962), "bottom frame line", B(507), "level with the bottom frame line at the corner"),
      ("1", 1, (440, 480, 3630, 3685), "tick", 3659.50, "level with its tick (the dr77 polyline crosses the tick near the frame)"),
      ("3", 3, (440, 475, 3075, 3130), "tick", 3101.22, "level with its tick (a square and an open circle at sigma3 = 0 sit just above the tick)"),
      ("6", 6, (425, 465, 2230, 2285), "tick", 2259.94, "level with its tick"),
      ("10", 10, (380, 452, 1118, 1176), "tick", 1138.21, "printed 8 px below its tick"),
      ("11", 11, (375, 450, 835, 892), "top frame line", T(500), "printed 10 px below the top frame line, at its left end; tick spacing 1 to 10 (mean 280.0 px) puts 11 at 858, 5 px from the frame")]
for lab, val, w, kind, lv, note in yl:
    cu, cv = bb(*w); uline = L(lv)
    rows.append({"axis": "y", "printed_label": lab, "value": val, "anchored_to": kind, "line_u": round(uline, 1), "line_v": round(lv, 1),
                 "label_center_u": round(cu, 1), "label_center_v": round(cv, 1), "label_offset_px": round(cv-lv, 1),
                 "affine_value_at_line": round(Y(uline, lv), 4), "by_eye": "agrees", "note": note})
with open(sys.argv[3], 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n'); w.writeheader(); w.writerows(rows)
for r in rows: print(r['axis'], r['printed_label'], r['label_center_u'], r['label_center_v'], r['label_offset_px'], r['affine_value_at_line'])
