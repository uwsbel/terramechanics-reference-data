"""Ink bounding boxes of the printed axis labels, and the fitted line positions next to them."""
import json
import numpy as np
from PIL import Image
g = np.array(Image.open("packet/p0109.png").convert("L")) < 128
cal = json.load(open("out/F2-48/cal-p1/calibration.json"))
H = {L["x_value"]: L for L in cal["horizontal_lines"]}
V = {L["y_value"]: L for L in cal["vertical_lines"]}
def bbox(u0, v0, u1, v1):
    s = g[v0:v1, u0:u1]; vv, uu = np.nonzero(s)
    return uu.min() + u0, vv.min() + v0, uu.max() + u0, vv.max() + v0
print("penetration labels (right of the frame, u 2278-2335)")
for val, (v0, v1) in {0: (3745, 3790), 1: (3515, 3565), 4: (2580, 2630), 8: (1345, 1400)}.items():
    b = bbox(2284, v0, 2335, v1); cu, cv = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    L = H[val]; lv = L["v_at_u0"] + L["slope_dv_du"] * cu
    print(f"  {val}: glyph u {b[0]}-{b[2]} v {b[1]}-{b[3]}, center v {cv:.1f}; fitted line v {lv:.1f} at u {cu:.0f}; offset {cv-lv:+.1f} px")
print("load labels (below the frame, v 3785-3895)")
for val, (u0, u1) in {0: (2225, 2276), 200: (1915, 1985), 600: (1305, 1365), 1200: (385, 445)}.items():
    b = bbox(u0, 3785, u1, 3895); cu, cv = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    L = V[val]; lu = L["u_at_v0"] + L["slope_du_dv"] * cv
    print(f"  {val}: glyph u {b[0]}-{b[2]} v {b[1]}-{b[3]}, center u {cu:.1f}; fitted line u {lu:.1f} at v {cv:.0f}; offset {cu-lu:+.1f} px")
