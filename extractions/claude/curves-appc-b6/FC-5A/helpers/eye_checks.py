"""Write calibration-eye-checks.csv: each printed axis label read by eye (its text box from
comps.py, checked on the crops in crops2/ylab_*.png and xlab_*.png) against the fitted grid line.
usage: eye_checks.py calibration.json out.csv"""
import sys, json, csv
cal = json.load(open(sys.argv[1]))
ax, ay = cal["ax"], cal["ay"]
V = {l["x_value"]: l for l in cal["vertical_lines"]}
H = {l["y_value"]: l for l in cal["horizontal_lines"]}
# (label, text box u0, u1, v0, v1) read on the page
YL = [(5000, 619, 726, 1532, 1571), (4000, 619, 727, 1835, 1874), (3000, 619, 729, 2127, 2165),
      (2000, 620, 729, 2419, 2459), (1000, 623, 730, 2712, 2751)]
XL = [(0, 797, 820, 3091, 3129), (1000, 1065, 1172, 3089, 3129), (2000, 1346, 1454, 3089, 3129),
      (3000, 1645, 1757, 3088, 3129), (4000, 1949, 2058, 3088, 3127), (5000, 2243, 2339, 3088, 3127)]
rows = []
for val, u0, u1, v0, v1 in YL:
    uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
    h = H[val]; ua = 812.0                                   # tick and axis column
    vline = h["v_at_u0"] + h["slope_dv_du"] * ua
    yv = ay[0] * ua + ay[1] * vc + ay[2]
    rows.append(dict(axis="y", printed_label=val, label_center_u=uc, label_center_v=vc,
                     fitted_line_px=round(vline, 1), offset_px=round(vc - vline, 1),
                     value_at_label_center=round(yv, 0), agrees="yes",
                     note="label left of the frame, level with a tick and the drawn horizontal grid line (crops2/ylab_*.png)"))
for val, u0, u1, v0, v1 in XL:
    uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
    l = V[val]; va = 3030.0                                  # axis row
    uline = l["u_at_v0"] + l["slope_du_dv"] * va
    xv = ax[0] * uc + ax[1] * va + ax[2]
    note = "label centered under a tick below the frame and the drawn vertical grid line (crops2/xlab_*.png)"
    if val == 0:
        note = "the corner label 0 is printed left of the sigma = 0 frame line (its right edge at the line); it is the only label off its line by more than a few px"
    rows.append(dict(axis="x", printed_label=val, label_center_u=uc, label_center_v=vc,
                     fitted_line_px=round(uline, 1), offset_px=round(uc - uline, 1),
                     value_at_label_center=round(xv, 0), agrees="yes", note=note))
cols = ["axis", "printed_label", "label_center_u", "label_center_v", "fitted_line_px", "offset_px",
        "value_at_label_center", "agrees", "note"]
with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["axis"], r["printed_label"], r["fitted_line_px"], r["offset_px"], r["value_at_label_center"])
