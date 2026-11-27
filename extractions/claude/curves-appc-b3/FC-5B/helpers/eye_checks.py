"""Write calibration-eye-checks.csv: gridline positions read by eye on zoomed crops (crops/y*.png,
x_up_*.png, l_*.png) against the fitted gridline and the affine map, at the stated location."""
import csv, json
import numpy as np

EYE = [  # panel, axis, label value, printed label, eye pixel, cross-coordinate, note
 (1, "y", 5000, "5000", 982.5, 660, "label centered at v~978"),
 (1, "y", 3000, "3000", 1572.8, 660, "label centered at v~1572"),
 (1, "y", 1000, "1000", 2159.0, 660, "label centered at v~2154"),
 (1, "y", 0, "0", 2453.0, 700, "bottom frame; the printed 0 sits about 53 px below it (v~2506), between the panels"),
 (1, "x", 0, "0", 672.5, 2400, "left frame; x labels are printed only under the lower panel"),
 (1, "x", 50, "50", 986.0, 2400, ""),
 (1, "x", 100, "100", 1277.0, 2400, ""),
 (1, "x", 150, "150", 1570.0, 2400, ""),
 (1, "x", 200, "200", 1861.5, 2400, ""),
 (1, "x", 250, "250", 2157.0, 2400, ""),
 (2, "y", 100, "+100", 2600.5, 700, "top frame; label centered at v~2605"),
 (2, "y", 0, "0", 2896.5, 700, "label centered at v~2894"),
 (2, "y", -100, "-100", 3191.5, 700, "bottom frame; label centered at v~3182"),
 (2, "x", 0, "0", 676.5, 3180, "left frame; label centered at u~681"),
 (2, "x", 50, "50", 989.0, 3180, "label centered at u~989"),
 (2, "x", 100, "100", 1284.0, 3180, "label centered at u~1279; a row scan puts the line center at 1282.5"),
 (2, "x", 150, "150", 1575.0, 3180, "label centered at u~1570"),
 (2, "x", 200, "200", 1867.0, 3180, "label centered at u~1860"),
 (2, "x", 250, "250", 2162.0, 3180, "label centered at u~2154"),
]
rows = []
for panel, axis, val, lab, eye, cross, note in EYE:
    cal = json.load(open(f"cal-p{panel}/calibration.json"))
    if axis == "y":
        l = [h for h in cal["horizontal_lines"] if h["y_value"] == val][0]
        fitted = l["v_at_u0"] + l["slope_dv_du"] * cross
        a = cal["ay"]  # y = a0 u + a1 v + a2 -> v = (y - a0 u - a2) / a1
        aff = (val - a[0] * cross - a[2]) / a[1]
        loc = f"u={cross}"
        span = cal["y_per_px"]
    else:
        l = [h for h in cal["vertical_lines"] if h["x_value"] == val][0]
        fitted = l["u_at_v0"] + l["slope_du_dv"] * cross
        a = cal["ax"]
        aff = (val - a[1] * cross - a[2]) / a[0]
        loc = f"v={cross}"
        span = cal["x_per_px"]
    rows.append({"figure": "FC-5B", "panel": panel, "axis": axis, "printed_label": lab,
                 "fitted_pixel": round(fitted, 1), "eye_pixel": eye, "eye_minus_fitted_px": round(eye - fitted, 1),
                 "affine_pixel": round(aff, 1), "eye_minus_affine_value": round((eye - aff) * span, 3),
                 "check_location": loc, "note": note})
with open("calibration-eye-checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader(); w.writerows(rows)
for r in rows: print(r)
