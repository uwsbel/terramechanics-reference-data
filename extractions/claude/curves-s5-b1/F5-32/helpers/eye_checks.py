"""Write calibration-eye-checks.csv: every printed axis label of Figure 5-32 as printed, the value its line is
anchored at, the line's measured position next to the label and the label's centre (both measured on the
page; the labels were read by eye on rotated, enlarged crops).

usage: eye_checks.py <page.png> <grid_measured.json> <time_lines.json> <out.csv>
"""
import csv
import json
import sys

import numpy as np
from PIL import Image


def label_centre_u(g, u_guess, v0=3518, v1=3600, half=14):
    sub = g[v0:v1, int(u_guess) - half:int(u_guess) + half + 1]
    cols = np.where(sub.any(axis=0))[0]
    return (cols.min() + cols.max()) / 2 + int(u_guess) - half, (v0, v1)


def label_centre_v(g, v_guess, u0=2292, u1=2334, half=24):
    sub = g[int(v_guess) - half:int(v_guess) + half + 1, u0:u1]
    rows = np.where(sub.any(axis=1))[0]
    return (rows.min() + rows.max()) / 2 + int(v_guess) - half


def main():
    page, gm, tl, out = sys.argv[1:5]
    g = np.asarray(Image.open(page).convert("L")) < 128
    G = json.load(open(gm, encoding="utf-8"))
    T = json.load(open(tl, encoding="utf-8"))
    printed = {1: ["-60", "-40", "-20", "0"], 2: ["-60", "+40", "+20", "0"], 3: ["-80", "-60", "-40", "-20", "0"]}
    titles = {1: "(Compression) Load on Strut No. 3 (lbs.)", 2: "(Tension) Load on Strut No. 2 (lbs.)",
              3: "(Compression) Load on Strut No. 1 (lbs.)"}
    rows = []
    for pn in (1, 2, 3):
        for lab, l in zip(printed[pn], G["load_lines"][str(pn)]):
            u_line = l["u_at_v0"] + l["slope_du_dv"] * 3545
            uc, _ = label_centre_u(g, u_line - 3)
            res, note = "ok", ""
            if pn == 2 and lab == "-60":
                res = "slip"
                note = ("printed with a minus sign (a short dash, no vertical stroke, unlike the plus of +40 and +20); the "
                        "panel's own sequence 0, +20, +40 and its (Tension) title make it +60: anchored at 60")
            if pn == 3 and lab == "0":
                note = ("printed about 9 px off its line, towards the -20 line (85 px away); the line is the figure's right "
                        "frame, which the panel's own sequence (-80, -60, -40, -20 at 85 px) puts at 0: anchored there")
            if pn == 1 and lab == "-60":
                note = ("the panel's grid continues past -60 with three more unlabeled lines (u about 842, 928, 1013 near the "
                        "bottom frame) and the figure's left frame (u about 755); not used, the trace stays above -30")
            rows.append({"figure_id": "F5-32", "panel": pn, "axis": "y (load, lb)", "axis_title_as_printed": titles[pn],
                         "label_as_printed": lab, "value_anchored": l["value"], "line": f"u at v 3545 (extended to the labels)",
                         "line_px": round(u_line, 1), "label_centre_px": round(uc, 1), "offset_px": round(uc - u_line, 1),
                         "result": res, "note": note})
        tl_printed = ["0", ".01", ".02", ".03", ".04", ".05", ".06", ".07", ".08", ".09", ".10"]
        for k, lab in enumerate(tl_printed):
            L = T[str(k)]
            v_line = L["v_at_u0"] + L["slope_dv_du"] * 2320
            vc = label_centre_v(g, v_line - 3)
            res, note = "ok", ""
            if lab == "0":
                note = "the bottom frame of the figure"
            if lab == ".07":
                note = "the 7 is slightly malformed (reads like a ?), legible in the sequence"
            if lab == ".09":
                res = "slip"
                note = ("damaged: the point and the 0 are broken (reads like '(,9' or '?9'); anchored at 0.09 from the "
                        "sequence; its tick is drawn")
            if lab == ".10":
                res = "line not verified"
                note = ("label printed; its line is only a 3 px speck at u 2233 and 2 px stubs on the frame and the -20 line: "
                        "rejected by the tool's ink check, so not a knot; t beyond 0.09 is extrapolated from the 0.08 and "
                        "0.09 lines")
            if k in range(1, 10):
                note = (note + "; " if note else "") + "tick drawn as a dash at the right frame, the knot of every panel (the line is not drawn across panels 1 and 2)"
            rows.append({"figure_id": "F5-32", "panel": pn, "axis": "x (time, s)", "axis_title_as_printed": "Time - Seconds",
                         "label_as_printed": lab, "value_anchored": round(0.01 * k, 2), "line": "v at u 2320 (the time line near the labels)",
                         "line_px": round(v_line, 1), "label_centre_px": round(vc, 1), "offset_px": round(vc - v_line, 1),
                         "result": res, "note": note})
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        if r["panel"] == 1 or r["axis"].startswith("y"):
            print(r["panel"], r["axis"][:1], r["label_as_printed"], r["value_anchored"], r["line_px"], r["label_centre_px"], r["offset_px"], r["result"])


if __name__ == "__main__":
    main()
