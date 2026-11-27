"""calibration-eye-checks.csv for FB-5: every printed axis label against the line it anchors (label
ink extents measured on the page; the verdicts were made by eye on the zoomed crops in out/FB-5/crops).
Usage: python eye_checks.py <cal_dir> <out.csv>"""
import csv, json, sys
import numpy as np
cal = json.load(open(sys.argv[1] + "/calibration.json"))
F = cal["frame_lines"]
an = {(a["x_value"], a["y_value"]): a for a in cal["anchors"]}
kx, ky = cal["frame_tilt_x_du_dv"], cal["frame_tilt_y_dv_du"]
# label ink extents (u0, u1, v0, v1), from the page (components below the bottom frame / left of the left frame)
XL = {0: (703, 732, 4015, 4059), 2: (1058, 1082, 4010, 4053), 4: (1413, 1440, 4010, 4047), 6: (1773, 1797, 4010, 4041),
      8: (2128, 2152, 4010, 4035), 10: (2451, 2509, 4010, 4032), 12: (2773, 2829, 4010, 4026)}
YL = {40: (533, 598, 871, 916), 35: (547, 606, 1314, 1358), 30: (557, 618, 1765, 1808), 25: (563, 624, 2207, 2251),
      20: (572, 633, 2636, 2677), 15: (581, 640, 3095, 3139), 10: (590, 649, 3526, 3570), 5: (634, 658, 3966, 4008)}
rows = []
def xline_u(x, v):
    if x == 0:
        return F["left"]["intercept"] + F["left"]["slope"] * v, "left frame line"
    if x == 12:
        return F["right"]["intercept"] + F["right"]["slope"] * v, "right frame line"
    a = an[(x, 5)]
    return a["u"] + kx * (v - a["v"]), "tick on the bottom frame"
def yline_v(y, u):
    if y == 5:
        return F["bottom"]["intercept"] + F["bottom"]["slope"] * u, "bottom frame line"
    if y == 40:
        return F["top"]["intercept"] + F["top"]["slope"] * u, "top frame line"
    a = an[(0, y)]
    return a["v"] + ky * (u - a["u"]), "tick on the left frame"
prev = None
for x, (u0, u1, v0, v1) in XL.items():
    cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    lu, kind = xline_u(x, 3990)
    lu_c, _ = xline_u(x, cv)
    sp = "" if prev is None else round(lu - prev, 1)
    prev = lu
    rows.append(["FB-5", 1, "x", str(x), x, kind, round(lu, 1), round(cu, 1), round(cv, 1), round(cu - lu_c, 1), sp])
prev = None
for y, (u0, u1, v0, v1) in YL.items():
    cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    lv, kind = yline_v(y, 680)
    lv_c, _ = yline_v(y, cu)
    sp = "" if prev is None else round(lv - prev, 1)
    prev = lv
    rows.append(["FB-5", 1, "y", str(y), y, kind, round(lv, 1), round(cu, 1), round(cv, 1), round(cv - lv_c, 1), sp])
VERDICT = {
    ("x", "0"): ("ok", "label under the lower left corner, centred 14 px right of the left frame line, like the single-digit labels 2 to 8 (13 to 15 px right of their ticks); spacing to the 2 tick 354 px, within the 354 to 359 px of the tick intervals"),
    ("x", "2"): ("ok", "single digit 13 px right of its tick (the speck at u 1093 to 1097 beside it is not part of the digit)"),
    ("x", "4"): ("ok", "15 px right of its tick"),
    ("x", "6"): ("ok", "15 px right of its tick"),
    ("x", "8"): ("ok", "14 px right of its tick"),
    ("x", "10"): ("ok", "two digits centred on the tick (3 px left of it)"),
    ("x", "12"): ("off its line; value confirmed by the tick spacing", "printed 33 px left of the right frame line (the '10' sits centred on its tick, so '12' is about 31 px out of the pattern, 0.17 psi); the right frame is 351 px past the 10 tick, against 354 to 359 px for the other 2 psi intervals (mean 356, so 1.4 percent short, within the drafting scatter), so the right frame is x = 12 and is used as that line"),
    ("y", "40"): ("ok", "label beside the top frame line, its centre 12 px below it; spacing 35 to 40 is 447 px against 443 to 449 px for the other 5 ksi intervals, so the top frame is y = 40 (no tick of its own)"),
    ("y", "35"): ("ok", "7 px below its tick"),
    ("y", "30"): ("ok", "9 px below its tick"),
    ("y", "25"): ("ok", "7 px below its tick"),
    ("y", "20"): ("ok", "10 px above its tick"),
    ("y", "15"): ("ok", "6 px below its tick"),
    ("y", "10"): ("ok", "6 px above its tick"),
    ("y", "5"): ("ok", "label beside the lower left corner, its centre 12 px above the bottom frame line; spacing 5 to 10 is 445 px, so the bottom frame is y = 5"),
}
with open(sys.argv[2], "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "axis", "printed_label", "value_used", "line_anchored", "line_position_px",
                "label_centre_u", "label_centre_v", "label_offset_px", "spacing_from_previous_px", "verdict", "note"])
    for r in rows:
        verdict, note = VERDICT[(r[2], r[3])]
        w.writerow(r + [verdict, note])
for r in rows:
    print(r)
