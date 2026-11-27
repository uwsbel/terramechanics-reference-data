"""Build calibration-eye-checks.csv from eye readings (recorded here) and the fitted maps."""
import csv, sys
sys.path.insert(0, "out/FC-3B")
from helpers import load_cal, fitted_pixel
# (panel, axis, label, other_pixel, eye_pixel)  eye pixels read on zoom-4 crops (crops/*.png)
eye = [
 (1,"y",5000,720,1270.0), (1,"y",3000,720,1854.0), (1,"y",0,720,2733.0),
 (1,"x",50,1290,978.0), (1,"x",100,2700,1271.0), (1,"x",250,2700,2143.0),
 (2,"y",50,720,2872.0), (2,"y",0,720,3017.0), (2,"y",-150,720,3454.5),
 (2,"x",150,3420,1563.5), (2,"x",200,2910,1853.5), (2,"x",250,3420,2143.5),
]
rows = []
for p, ax, lab, other, eyepx in eye:
    cal = load_cal(f"out/FC-3B/cal-p{p}/calibration.json")
    fit = fitted_pixel(cal, ax, lab, other)
    scale = cal["x_per_px"] if ax == "x" else cal["y_per_px"]
    span = 250 if ax == "x" else (5000 if p == 1 else 200)
    rows.append(dict(figure_id="FC-3B", panel=p, axis=ax, printed_label=lab, other_pixel=other,
                     fitted_pixel=round(fit,1), eye_pixel=eyepx, diff_px=round(eyepx-fit,1),
                     diff_pct_span=round(abs(eyepx-fit)*scale/span*100,3)))
with open("out/FC-3B/calibration-eye-checks.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
