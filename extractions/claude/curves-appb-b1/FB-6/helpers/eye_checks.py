"""calibration-eye-checks.csv for FB-6: printed axis labels read by eye on zoomed crops (crops/lab_*.png),
their ink boxes measured on the page, against the line (tick or frame) each one is anchored to."""
import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image

W = Path(sys.argv[1])
sys.path.insert(0, str(W / "tools"))
import calibrate_axes as ca  # noqa: E402

img = W / "packet" / "p0112.png"
dark = np.asarray(Image.open(img).convert("L")) < 128
cal, X, Y = ca.piecewise_maps(str(W / "out" / "FB-6" / "cal-p1"), str(img))
F = cal["frames"]


def box(u0, v0, u1, v1):
    sub = dark[v0:v1, u0:u1]
    r, c = np.where(sub.any(axis=1))[0], np.where(sub.any(axis=0))[0]
    return u0 + c.min(), v0 + r.min(), u0 + c.max(), v0 + r.max()


# (axis, label, search window for the label's ink, line kind, crop)
CHECKS = [
    ("y", "29", (530, 800, 605, 870), "top frame line (y = 29)", "crops/lab_y29_27.png"),
    ("y", "27", (540, 1070, 615, 1130), "tick at the left frame", "crops/lab_y29_27.png"),
    ("y", "25", (550, 1360, 625, 1420), "tick at the left frame", "crops/lab_y25.png"),
    ("y", "17", (585, 2410, 660, 2470), "tick at the left frame", "crops/lab_y17.png"),
    ("y", "7", (660, 3740, 700, 3790), "tick at the left frame", "crops/lab_y7_5.png"),
    ("y", "5", (670, 3995, 705, 4050), "bottom frame line (y = 5)", "crops/lab_y7_5.png"),
    ("x", "0", (700, 4050, 745, 4100), "left frame line (x = 0)", "crops/lab_y7_5.png"),
    ("x", "2", (975, 4036, 1012, 4090), "tick at the bottom frame, seen only inside the hole of a plotted circle", "crops/x2b.png"),
    ("x", "4", (1240, 4036, 1290, 4085), "tick at the bottom frame", "crops/lab_x4_8.png"),
    ("x", "8", (1785, 4030, 1830, 4075), "tick at the bottom frame", "crops/lab_x4_8.png"),
    ("x", "12", (2300, 3998, 2375, 4050), "tick at the bottom frame", "crops/lab_x12_14.png"),
    ("x", "14", (2575, 3995, 2650, 4045), "right frame line (x = 14)", "crops/lab_x12_14.png"),
]

rows = []
for axis, lab, win, kind, crop in CHECKS:
    u0, v0, u1, v1 = box(*win)
    uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
    val = float(lab)
    if axis == "y":
        hl = next(h for h in cal["horizontal_lines"] if h["y_value"] == val)
        line_pos = hl["v_at_u0"] + hl["slope_dv_du"] * uc       # the line, extended to the label's column
        off = vc - line_pos
        at = Y.value(uc, vc)[0]
        desc = f"label centre v {vc:.1f}; line at v {line_pos:.1f} in the label's column"
    else:
        vl = next(l for l in cal["vertical_lines"] if l["x_value"] == val)
        line_pos = vl["u_at_v0"] + vl["slope_du_dv"] * vc
        off = uc - line_pos
        at = X.value(uc, vc)[0]
        desc = f"label centre u {uc:.1f}; line at u {line_pos:.1f} in the label's row"
    seq_ok = "yes"
    rows.append({"figure_id": "FB-6", "panel": 1, "axis": axis, "printed_label": lab,
                 "label_ink_box": f"{u0} {v0} {u1} {v1}", "label_centre_u": round(uc, 1), "label_centre_v": round(vc, 1),
                 "anchored_to": kind, "line_position_px": round(line_pos, 1),
                 "label_minus_line_px": round(off, 1), "map_value_at_label_centre": round(at, 3),
                 "fits_printed_sequence": seq_ok, "crop": crop, "verdict": "", "note": desc})

V = {
    ("y", "29"): ("ok", "label sits on the top frame line; the frame is 3.9 px below where the tick regression puts 29 (interval 27 to 29 is 261 px against 267 for the others); the top frame is the knot"),
    ("y", "27"): ("ok", "label centred on its tick"),
    ("y", "25"): ("ok", "label printed about 25 px below its tick (top of the digits below the tick); the nearest tick, and the tick spacing confirms 25"),
    ("y", "17"): ("ok", "label about 4 px below its tick"),
    ("y", "7"): ("ok", "label centred on its tick"),
    ("y", "5"): ("ok", "label at the bottom-left corner, about 9 px above the bottom frame line; no other line near; tick spacing puts 5 within 1.3 px of the frame"),
    ("x", "0"): ("ok", "label below the bottom-left corner, about 9 px left of the left frame line; tick spacing puts 0 within 1.5 px of the frame"),
    ("x", "2"): ("ok", "label centred within 5 px of the tick seen inside the circle's hole; the tick sits 0.15 px from the midpoint of the x = 0 frame and the x = 4 tick"),
    ("x", "4"): ("ok", "label centred on its tick"),
    ("x", "8"): ("ok", "label about 10 px right of its tick"),
    ("x", "12"): ("ok", "label centred on its tick"),
    ("x", "14"): ("ok", "label below the bottom-right corner, about 4 px right of the right frame line; tick spacing puts 14 within 2.2 px of the frame"),
}
for r in rows:
    r["verdict"], extra = V[(r["axis"], r["printed_label"])]
    r["note"] = extra + "; " + r["note"]

out = W / "out" / "FB-6" / "calibration-eye-checks.csv"
with out.open("w", encoding="utf-8", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    wr.writeheader()
    wr.writerows(rows)
for r in rows:
    print(r["axis"], r["printed_label"], r["label_ink_box"], r["label_minus_line_px"], r["map_value_at_label_centre"])
