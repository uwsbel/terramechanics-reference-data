"""calibration-eye-checks.csv: each printed label read by eye on zoomed crops (crops/xlab_*.png, crops/ylab_bot_*.png)
against the line the calibration anchored for it (cal-p1, piecewise lines, at the label's side of the plot)."""
import csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import calib
base = Path(__file__).resolve().parents[1]
# grain size labels: printed right of the plot, rotated; position = v of the label's decimal point (or centre)
X = [("0.02", 0.02, "3758-3855", 3806.5, "label centre (decimal point at 3816); bottom frame line, the frame carries the label 0.02, printed about 9 px below it; no other line within 90 px"),
     ("0.05", 0.05, "3369-3465", 3417, "label centre (decimal point at 3427)"),
     ("0.1", 0.1, "3089-3154", 3119, "decimal point"),
     ("0.2", 0.2, "2810-2845", 2827, "decimal point"),
     ("0.5", 0.5, "2425-2475", 2442, "decimal point"),
     ("1.0", 1.0, "2125-2170", 2150, "decimal point"),
     ("1.5", 1.5, "1948-2007", 1978, "decimal point"),
     ("2.0", 2.0, "1831-1897", 1860, "decimal point"),
     ("3.0", 3.0, "1660-1726", 1691, "decimal point"),
     ("4.0", 4.0, "1525-1602", 1565, "decimal point"),
     ("5.0", 5.0, "1438-1501", 1467, "decimal point"),
     ("9.0", 9.0, "1182-1250", 1216, "label centre (decimal point 1213); label sits on the line at v 1218, not on the top frame (v 1172, unlabelled, about 10 mm, not anchored)")]
Y = [("100", 100, "558-593", 576, "left frame line; the frame carries the label 100"),
     ("90", 90, "700-733", 717, ""), ("80", 80, "843-880", 862, ""), ("70", 70, "990-1025", 1008, ""),
     ("60", 60, "1133-1168", 1150, ""), ("50", 50, "1285-1320", 1302, ""), ("40", 40, "1430-1467", 1448, ""),
     ("30", 30, "1575-1612", 1593, ""), ("20", 20, "1720-1755", 1738, ""), ("10", 10, "1863-1900", 1882, ""),
     ("0", 0, "2012-2047", 2029, "right frame line; the frame carries the label 0")]
rows = []
for lab, val, ext, pos, note in X:
    line = calib.v_at(2040, val)
    rows.append({"axis": "x (grain size, mm, log)", "printed_label": lab, "label_extent_px": f"v {ext}", "label_position_px": pos,
                 "anchored_value": val, "fitted_line_px": round(line, 1), "label_minus_line_px": round(pos - line, 1),
                 "where": "right of the plot, u 2085-2125; line evaluated at u 2040", "verdict": "label on its line", "note": note})
for lab, val, ext, pos, note in Y:
    line = calib.u_at(3797, val)
    rows.append({"axis": "y (percent finer)", "printed_label": lab, "label_extent_px": f"u {ext}", "label_position_px": pos,
                 "anchored_value": val, "fitted_line_px": round(line, 1), "label_minus_line_px": round(pos - line, 1),
                 "where": "below the plot, v 3830-3870; line evaluated at v 3797", "verdict": "label on its line", "note": note})
with (base / "calibration-eye-checks.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["axis"][:1], r["printed_label"], r["label_position_px"], r["fitted_line_px"], r["label_minus_line_px"])
