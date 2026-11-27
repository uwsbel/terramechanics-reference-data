"""Writes calibration-eye-checks.csv for FC-19: each printed axis label, read by eye on zoomed crops
(crops/ylab*.png, crops/xlabA.png, crops/xlabB.png), against the fitted grid line of cal-p1."""
import csv, json
from pathlib import Path
OUT = Path(__file__).resolve().parents[1]
cal = json.loads((OUT / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
V = {l["x_value"]: l for l in cal["vertical_lines"]}
H = {l["y_value"]: l for l in cal["horizontal_lines"]}
# label centers read by eye on the crops (page pixels)
ylab = {50: (765, 1677, "crops/ylab50.png"), 45: (771, 2059, "crops/ylab45.png"), 40: (775, 2448, "crops/ylab40.png"),
        35: (782, 2832, "crops/ylab35.png"), 30: (788, 3205, "crops/ylab30.png")}
xlab = {0.0: (982, "0"), 0.1: (1141, "0.1"), 0.2: (1288, "0.2"), 0.3: (1443, "0.3"), 0.4: (1589, "0.4"),
        0.5: (1755, "0.5"), 0.6: (1911, "0.6"), 0.7: (2077, "0.7"), 0.8: (2222, "0.8"), 0.9: (2376, "0.9"),
        1.0: (2534, "1.0")}
rows = []
for val, (u, v, crop) in ylab.items():
    l = H[float(val)]
    line_v = l["v_at_u0"] + l["slope_dv_du"] * u
    rows.append({"figure_id": "FC-19", "panel": 1, "axis": "y", "printed_label": str(val), "value": val,
                 "label_center_u": u, "label_center_v": v, "line_position_px": round(line_v, 1),
                 "label_minus_line_px": round(v - line_v, 1), "line_source": l["source"], "crop": crop,
                 "outcome": "confirmed", "note": "label printed left of the frame, level with the horizontal line it names (line spacing 383 px)"})
for val, (u, lab) in xlab.items():
    l = V[val]
    v = 3640
    line_u = l["u_at_v0"] + l["slope_du_dv"] * v
    crop = "crops/xlabA.png" if val <= 0.4 else "crops/xlabB.png"
    note = "label printed below the frame, under the vertical line it names (line spacing 153 to 162 px)"
    if lab == "0.4":
        note += "; printed 16 px left of its line, still unambiguous"
    if lab == "0.7":
        note += "; a short stray stroke follows the label (0.7-), not part of it"
    if lab == "0":
        note += "; the frame extends a further 0.09 in Dr to the left of this line, unlabelled"
    if lab == "1.0":
        note += "; the frame extends a further 0.10 in Dr to the right of this line, unlabelled"
    rows.append({"figure_id": "FC-19", "panel": 1, "axis": "x", "printed_label": lab, "value": val,
                 "label_center_u": u, "label_center_v": v, "line_position_px": round(line_u, 1),
                 "label_minus_line_px": round(u - line_u, 1), "line_source": l["source"], "crop": crop,
                 "outcome": "confirmed", "note": note})
with (OUT / "calibration-eye-checks.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader(); w.writerows(rows)
for r in rows: print(r["axis"], r["printed_label"], r["label_minus_line_px"])
