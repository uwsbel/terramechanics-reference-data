"""Write calibration-eye-checks.csv: fitted pixel position of each labeled gridline from the
affine map (v of a horizontal line at the column where it was read by eye, u of a vertical line
at the row where it was read), next to the eye reading (center of the gridline's ink band, read
on 1:1 text crops and zoom-3 image crops next to the printed label)."""
import csv, json
from pathlib import Path
H = Path(__file__).parent.parent
def cal(p):
    c = json.loads((H / p / "calibration.json").read_text(encoding="utf-8"))
    return c["ax"], c["ay"], c
# (panel, axis, label, value, read_at, eye, note)
checks = [
 (1, "y", "5000 (printed '500' with a smudged last digit)", 5000, 680, 954, "top frame"),
 (1, "y", "4000 (printed '4( 00')", 4000, 680, 1240.5, ""),
 (1, "y", "3000", 3000, 680, 1537.5, ""),
 (1, "y", "2000", 2000, 680, 1828.5, ""),
 (1, "y", "1000", 1000, 680, 2125.5, ""),
 (1, "y", "0", 0, 680, 2420, "bottom frame"),
 (1, "x", "50 (printed under the lower panel; same gridline)", 50, 2398, 956, ""),
 (1, "x", "100 (printed under the lower panel)", 100, 2398, 1245.5, ""),
 (1, "x", "150 (printed under the lower panel)", 150, 2398, 1536.5, ""),
 (1, "x", "200 (printed under the lower panel)", 200, 2398, 1830.5, ""),
 (1, "x", "250 (printed under the lower panel)", 250, 2398, 2115.5, ""),
 (2, "y", "+100", 100, 690, 2568, "top frame"),
 (2, "y", "0 (no printed label; midline between +100 and -100)", 0, 690, 2862.5, ""),
 (2, "y", "-100", -100, 690, 3156.5, "bottom frame"),
 (2, "x", "50", 50, 3138, 965.5, ""),
 (2, "x", "100", 100, 3138, 1254.5, ""),
 (2, "x", "150", 150, 3138, 1545.5, ""),
 (2, "x", "200", 200, 3138, 1839.5, ""),
 (2, "x", "250", 250, 3138, 2125.5, ""),
]
rows = []
for panel, axis, label, val, at, eye, note in checks:
    ax, ay, c = cal(f"cal-p{panel}")
    if axis == "y":   # v where y(u=at, v) = val
        fit = (val - ay[0] * at - ay[2]) / ay[1]; span = abs(ay[1]) * 1.0
        resid_val = (ay[0] * at + ay[1] * eye + ay[2]) - val
        span_axis = 5000 if panel == 1 else 200
    else:             # u where x(u, v=at) = val
        fit = (val - ax[1] * at - ax[2]) / ax[0]
        resid_val = (ax[0] * eye + ax[1] * at + ax[2]) - val
        span_axis = 250
    rows.append(dict(figure_id="FC-6C", panel=panel, axis=axis, printed_label=label,
                     read_at=("u=%d" % at) if axis == "y" else ("v=%d" % at),
                     fitted_pixel=round(fit, 1), eye_pixel=eye, eye_minus_fitted_px=round(eye - fit, 1),
                     eye_value_minus_label=round(resid_val, 2), pct_of_axis_span=round(100 * abs(resid_val) / span_axis, 2), note=note))
cols = list(rows[0].keys())
with open(H / "calibration-eye-checks.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
for r in rows: print(r["panel"], r["axis"], r["printed_label"][:6], r["fitted_pixel"], r["eye_pixel"], r["eye_minus_fitted_px"], r["eye_value_minus_label"], r["pct_of_axis_span"])
