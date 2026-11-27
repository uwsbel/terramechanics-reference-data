"""Write calibration-eye-checks.csv: fitted pixel of each printed label (from the affine map)
against the pixel read by eye on zoomed crops / row and column scans."""
import csv, json
cal = {p: json.load(open(f"cal-p{p}/calibration.json")) for p in (1, 2)}

def u_of(p, x, v):
    ax = cal[p]["ax"]; return (x - ax[1] * v - ax[2]) / ax[0]
def v_of(p, y, u):
    ay = cal[p]["ay"]; return (y - ay[0] * u - ay[2]) / ay[1]
def x_at(p, u, v):
    ax = cal[p]["ax"]; return ax[0] * u + ax[1] * v + ax[2]
def y_at(p, u, v):
    ay = cal[p]["ay"]; return ay[0] * u + ay[1] * v + ay[2]

# (panel, axis, label, eye pixel, other coordinate, span, note)
checks = [
 (1, "x", 50, 959.0, 2085, 200, "gridline center at v=2085 (row scan, crop)"),
 (1, "x", 100, 1247.0, 2085, 200, "gridline center at v=2085"),
 (1, "x", 150, 1528.5, 2085, 200, "gridline center at v=2085"),
 (1, "x", 200, 1821.5, 2085, 200, "gridline center at v=2085"),
 (1, "x", 250, 2113.5, 2085, 200, "gridline center at v=2085; x labels are printed under the lower panel only"),
 (1, "y", 4000, 925.5, 700, 4000, "gridline at u=700 and tick left of frame at u=625 (925.5)"),
 (1, "y", 3000, 1215.5, 700, 4000, "gridline at u=700; tick left of frame 1213.5"),
 (1, "y", 2000, 1511.5, 700, 4000, "gridline at u=700; tick 1511.5"),
 (1, "y", 1000, 1802.0, 700, 4000, "gridline at u=700; tick 1801.5"),
 (1, "y", 0, 2101.5, 700, 4000, "bottom frame at u=700"),
 (2, "x", 50, 962.5, 3295, 200, "gridline tick below the frame at v=3295, label 50 centered under it"),
 (2, "x", 100, 1250.5, 3295, 200, "tick below frame"),
 (2, "x", 150, 1533.5, 3295, 200, "tick below frame"),
 (2, "x", 200, 1825.5, 3295, 200, "tick below frame"),
 (2, "x", 250, 2114.5, 2300, 200, "gridline at v=2300 (no tick below the frame)"),
 (2, "y", 50, 2245.5, 700, 350, "top frame at u=700; label +50 leader at v=2258"),
 (2, "y", 0, 2392.0, 700, 350, "drawn zero line at u=700; leader at v=2403"),
 (2, "y", -300, 3276.0, 700, 350, "bottom frame at u=700; leader at v=3287.5"),
 (2, "y", -100, 2649.0, 620, 350, "NO drawn gridline; eye pixel = label leader (v=2660.5) minus the 11.5 px leader offset seen on +50, 0, -300; label sits about 13 units high of the linear scale defined by the drawn lines"),
 (2, "y", -200, 2974.0, 620, 350, "NO drawn gridline; eye pixel = label leader (v=2985.5) minus the 11.5 px leader offset"),
]
rows = []
for p, axis, lab, eye, other, span, note in checks:
    if axis == "x":
        fit = u_of(p, lab, other); val_eye = x_at(p, eye, other)
    else:
        fit = v_of(p, lab, other); val_eye = y_at(p, other, eye)
    res_px = eye - fit
    res_val = val_eye - lab
    rows.append(dict(figure_id="FC-6B", panel=p, axis=axis, printed_label=lab, fitted_pixel=round(fit, 1),
                     eye_pixel=eye, checked_at=("v=" if axis == "x" else "u=") + str(other),
                     residual_px=round(res_px, 1), residual_value=round(res_val, 2),
                     residual_pct_span=round(100 * abs(res_val) / span, 2), note=note))
# frame left edges (unlabeled): value by extrapolation
for p, u, v in ((1, 641.5, 2085), (2, 642.5, 2300)):
    rows.append(dict(figure_id="FC-6B", panel=p, axis="x", printed_label="(left frame, unlabeled)", fitted_pixel="",
                     eye_pixel=u, checked_at=f"v={v}", residual_px="", residual_value=round(x_at(p, u, v), 2),
                     residual_pct_span="", note="left frame is not a labeled gridline; residual_value column holds the x value the 50-250 calibration gives it"))
rows.append(dict(figure_id="FC-6B", panel=1, axis="y", printed_label="(top frame, unlabeled)", fitted_pixel="",
                 eye_pixel=784.0, checked_at="u=1300", residual_px="", residual_value=round(y_at(1, 1300, 784.0), 1),
                 residual_pct_span="", note="top frame not labeled; residual_value column holds the y value the calibration gives it"))
with open("calibration-eye-checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader(); w.writerows(rows)
for r in rows: print(r)
