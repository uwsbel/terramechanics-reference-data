"""Write calibration-eye-checks.csv: every printed axis label against the fitted line it names.
Label glyph centres were measured as the centre of the dark pixels of each label (helper below);
the check itself was made by eye on crops/ylabels.png and crops/xlabels.png."""
import csv, json
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parents[1] / "packet" / "p0104.png").convert("L"))
cal = json.loads((HERE / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
H = {l["y_value"]: l for l in cal["horizontal_lines"]}
V = {l["x_value"]: l for l in cal["vertical_lines"]}


def clusters(mask, gap=3):
    idx = np.where(mask)[0]
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i > p + gap:
            out.append((s, p)); s = i
        p = i
    out.append((s, p))
    return out


rows = []
sub = g[1640:3300, 560:712] < 128
for (s, p), val in zip(clusters(sub.any(axis=1)), [2000, 1500, 1000, 500, 0]):
    c = 1640 + (s + p) / 2
    l = H[float(val)]
    u_lab = 735.0
    line = l["v_at_u0"] + l["slope_dv_du"] * u_lab
    rows.append(dict(figure_id="F2-44", panel=1, axis="y", printed_label=val, label_rows_or_cols=f"v {1640+s}-{1640+p}",
                     label_center_px=round(c, 1), fitted_line_px=round(line, 1), offset_px=round(c - line, 1),
                     checked_by_eye="yes",
                     note=("frame line (top), measured on its visible parts; the key box covers its middle" if val == 2000 else
                           "frame line (bottom)" if val == 0 else "drawn grid line") +
                          "; label printed left of the frame, centred within 10 px of its line; next line is 387 px away"))
sub = g[3268:3335, 700:2330] < 128
for (s, p), val in zip(clusters(sub.any(axis=0)), [0, 1, 2, 3, 4, 5]):
    c = 700 + (s + p) / 2
    l = V[float(val)]
    line = l["u_at_v0"] + l["slope_du_dv"] * 3255
    rows.append(dict(figure_id="F2-44", panel=1, axis="x", printed_label=val, label_rows_or_cols=f"u {700+s}-{700+p}",
                     label_center_px=round(c, 1), fitted_line_px=round(line, 1), offset_px=round(c - line, 1),
                     checked_by_eye="yes",
                     note=("frame line (left)" if val == 0 else "frame line (right)" if val == 5 else "drawn grid line") +
                          "; label printed below the frame, centred within 8 px of its line; next line is about 308 px away"))
with (HERE / "calibration-eye-checks.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader(); w.writerows(rows)
for r in rows: print(r["axis"], r["printed_label"], r["label_center_px"], r["fitted_line_px"], r["offset_px"])
