"""Write calibration-eye-checks.csv: for each printed label (axis, value, label centre u v, line
value it names, note), the fitted line's position at the label (a horizontal line's v at the
label's u, a vertical line's u at the frame's bottom v) and the offset label minus line, px.
Usage: eyecheck.py <cal_dir> <checks.json> <out.csv>; checks.json: {"figure_id", "v_bottom",
"checks": [[axis, printed, line_value, u, v, verdict, note], ...]}"""
import sys
import json
import csv

cal = json.load(open(sys.argv[1] + "/calibration.json", encoding="utf-8"))
spec = json.load(open(sys.argv[2], encoding="utf-8"))
H = {round(l["y_value"], 6): l for l in cal["horizontal_lines"]}
V = {round(l["x_value"], 6): l for l in cal["vertical_lines"]}
rows = []
for axis, printed, val, u, v, verdict, note in spec["checks"]:
    if axis == "y":
        l = H[round(val, 6)]
        pos = l["v_at_u0"] + l["slope_dv_du"] * u
        off = v - pos
        where = f"v = {pos:.1f} at u = {u}"
    else:
        l = V[round(val, 6)]
        vb = spec["v_bottom"]
        pos = l["u_at_v0"] + l["slope_du_dv"] * vb
        off = u - pos
        where = f"u = {pos:.1f} at v = {vb} (bottom frame)"
    rows.append({"figure_id": spec["figure_id"], "panel": 1, "axis": axis, "printed_label": printed,
                 "line_value": val, "line_source": l["source"], "label_center_u": u, "label_center_v": v,
                 "fitted_line_at_label": where, "label_minus_line_px": round(off, 1), "verdict": verdict, "note": note})
with open(sys.argv[3], "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["axis"], r["printed_label"], r["fitted_line_at_label"], r["label_minus_line_px"])
