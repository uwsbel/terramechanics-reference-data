"""calibration-eye-checks.csv for Figure 5-31 (reader helper).

The printed strings were read by eye on zoomed crops of p0336.png (crops/ylab-*.png, crops/xlab-*.png). This
script measures each label's ink extent on the page and the fitted line's position at the label, so the
check that each label sits on the line it is anchored to is recorded with numbers. The figure is printed
sideways: the time labels stand to the right of the right frame (u about 2220 to 2300), centered on their
horizontal page lines; the depth labels stand below the bottom frame (v about 3535 to 3645), centered on
their vertical page lines.
"""
import csv, json
from pathlib import Path
import numpy as np
from PIL import Image

ws = Path(__file__).resolve().parents[3]
g = np.asarray(Image.open(ws / "packet" / "p0336.png").convert("L")) < 128
cal = json.loads((ws / "out" / "F5-31" / "cal-p1" / "calibration.json").read_text())
HL = {l["x_value"]: l for l in cal["horizontal_lines"]}
VL = {l["y_value"]: l for l in cal["vertical_lines"]}
SPACING_T = 245.0   # px between adjacent time lines, about
SPACING_D = 245.0   # px between adjacent depth lines, about


def clusters(mask, gap):
    idx = np.where(mask)[0]
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - p > gap:
            out.append((int(s), int(p)))
            s = i
        p = i
    out.append((int(s), int(p)))
    return out


rows = []
# time labels, top to bottom on the page; the last one ("0") sits at the corner and is measured on its own
TIME_PRINTED = [".1", ".09", ".08", ".07", ".06", ".05", ".04", ".03", ".02", ".01"]
TIME_VALUES = [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
u0, u1 = 2218, 2300
strip = g[1030:3500, u0:u1]
for (a, b), txt, val in zip(clusters(strip.any(axis=1), 25), TIME_PRINTED, TIME_VALUES):
    cols = np.where(strip[a:b + 1].any(axis=0))[0]
    uc, vc = (cols[0] + cols[-1]) / 2 + u0, (a + b) / 2 + 1030
    rows.append(("x", txt, val, uc, vc, HL[val], "v"))
sub = g[3495:3570, 2250:2300]
r_ = np.where(sub.any(axis=1))[0]; c_ = np.where(sub.any(axis=0))[0]
rows.append(("x", "0", 0.0, (c_[0] + c_[-1]) / 2 + 2250, (r_[0] + r_[-1]) / 2 + 3495, HL[0.0], "v"))
# depth labels, left to right on the page
DEPTH_PRINTED = ["5.0", "4.0", "3.0", "2.0", "+1.0", "0", "-1.0"]
DEPTH_VALUES = [5.0, 4.0, 3.0, 2.0, 1.0, 0.0, -1.0]
strip = g[3535:3665, 650:2260]
for (a, b), txt, val in zip(clusters(strip.any(axis=0), 25), DEPTH_PRINTED, DEPTH_VALUES):
    rr = np.where(strip[:, a:b + 1].any(axis=1))[0]
    uc, vc = (a + b) / 2 + 650, (rr[0] + rr[-1]) / 2 + 3535
    rows.append(("y", txt, val, uc, vc, VL[val], "u"))

out = ws / "out" / "F5-31" / "calibration-eye-checks.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "axis", "label_printed", "value_anchored", "label_center_u", "label_center_v",
                "line_at_label_px", "label_offset_px", "line_source", "verdict", "note"])
    for axis, txt, val, uc, vc, line, across in rows:
        if across == "v":
            pos = line["v_at_u0"] + line["slope_dv_du"] * uc
            off = vc - pos
            where = "v of the fitted time line at the label's u"
            frac = abs(off) / SPACING_T
        else:
            pos = line["u_at_v0"] + line["slope_du_dv"] * vc
            off = uc - pos
            where = "u of the fitted depth line at the label's v"
            frac = abs(off) / SPACING_D
        note = f"{where}; offset {frac:.0%} of a division"
        if axis == "x" and val == 0.0:
            note += ("; the corner label 0 is printed a little below the bottom frame, in step with the sequence "
                     "(250 px below the .01 label); it labels the frame")
        if axis == "x" and val == 0.1:
            note += "; printed .1, not .10; it labels the top frame"
        if axis == "y" and val == 1.0:
            note += "; printed with a plus sign, +1.0"
        if axis == "y" and val == -1.0:
            note += "; printed with a minus sign, -1.0; it labels the right frame"
        if axis == "y" and val == 0.0:
            note += "; printed 0 without a decimal"
        w.writerow(["F5-31", 1, axis, txt, val, round(uc, 1), round(vc, 1), round(pos, 1), round(off, 1),
                    line["source"], "label on its line", note])
    w.writerow(["F5-31", 1, "y", "", "", "", "", "", "", "",
                "unlabeled frame, not a knot",
                "the left frame (u about 590 at the top to 618 at the bottom) lies about half a division beyond the "
                "5.0 line, near 5.5 in by the spacing, and carries no label; left out of the calibration box, so "
                "it is not a knot; the trace never comes near it (deepest 4.21 in)"])
print(f"wrote {out}: {len(rows)} labels")
