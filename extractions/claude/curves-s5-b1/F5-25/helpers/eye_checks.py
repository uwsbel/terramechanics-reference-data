"""calibration-eye-checks.csv: every printed axis label of Figure 5-25 as printed, the value its line is
anchored at, the fitted line's position at the label, the label's measured center (label_boxes.py), and
the by-eye verdict (labels read on crops at zoom 3 to 8)."""
import csv
import json
LINES = json.load(open("lines.json", encoding="utf-8"))
TL = {round(T["value"], 3): T for T in json.load(open("time_lines.json", encoding="utf-8"))}
cal3 = json.load(open("../cal-p3/calibration.json", encoding="utf-8"))
base3 = [h for h in cal3["horizontal_lines"] if h["x_value"] == 0][0]


def vline(panel, value, v=3575):
    L = [l for l in LINES["vertical"] if l["panel"] == panel and l["value"] == value][0]
    return L["u_at_v0"] + L["slope_du_dv"] * v


rows = []
LOAD = [  # panel, printed, anchored, label center u, verdict, note
    (1, "+60", 60, 992.0, "ok", "plus sign whole"),
    (1, "+40", 40, 1082.0, "ok", "label printed 5 px toward +60 from its line (line spacing 86 px); names this line unambiguously"),
    (1, "+20", 20, 1163.0, "ok", "plus sign incomplete: read upright, the lower half of its vertical stroke is missing, so at low zoom it can pass for -20; read +20 at zoom 8, and +20 is also what the sequence gives"),
    (1, "0", 0, 1248.0, "ok", "this line is also the left boundary of panel 2"),
    (2, "-60", 60, 1418.0, "slip, anchored from the sequence", "printed with a minus sign (read upright, a bare horizontal bar with 1 px bumps at its middle, unlike the full plus of +40 and +20 beside it); the sequence 0, +20, +40 and the (Tension) title make it +60; anchored at +60"),
    (2, "+40", 40, 1502.0, "ok", ""),
    (2, "+20", 20, 1586.0, "ok", ""),
    (2, "0", 0, 1671.0, "ok", "this line is also the left boundary of panel 3"),
    (3, "-100", -100, 1842.0, "ok", ""),
    (3, "-80", -80, 1928.0, "ok", ""),
    (3, "-60", -60, 2012.5, "ok", ""),
    (3, "-40", -40, 2102.0, "ok", ""),
    (3, "-20", -20, 2187.0, "ok", ""),
    (3, "0", 0, 2271.0, "ok", "this 0 line is the right frame of the figure (6 px thick)"),
]
for panel, printed, val, lab, verdict, note in LOAD:
    pos = vline(panel, val)
    rows.append({"figure_id": "F5-25", "panel": panel, "axis": "y (load, lb)", "label_as_printed": printed, "value_anchored": val,
                 "line_px": f"u = {pos:.1f} at v 3575", "label_center_px": f"u = {lab:.1f}", "offset_px": round(lab - pos, 1),
                 "check": verdict, "note": note})
TIME = [  # printed, anchored, label center v, verdict, note
    ("0", 0.0, 3531.0, "ok", "the t = 0 line is the baseline (bottom frame), 5 to 9 px thick and slightly bent across the figure; each panel uses the stretch under it"),
    (".01", 0.01, 3362.0, "ok", ""), (".02", 0.02, 3192.0, "ok", ""), (".03", 0.03, 3022.0, "ok", ""),
    (".04", 0.04, 2850.5, "ok", ""), (".05", 0.05, 2680.5, "ok", ""), (".06", 0.06, 2510.5, "ok", ""),
    (".07", 0.07, 2340.0, "ok", ""), (".08", 0.08, 2168.5, "ok", ""),
    ("(damaged: fragments only)", 0.09, 2000.5, "damaged label, anchored from the sequence",
     "the label's ink is mostly missing: a small hook (v 1983 to 1990), a curved stroke (v 1998 to 2010) and the decimal point (v 2015 to 2018), at u 2316 to 2323; its line (dashes at u 747 to 809 and 2208 to 2239) sits one spacing above .08 and below .10, so it is the .09 line; anchored at 0.09"),
    (".10", 0.10, 1830.0, "ok", "the last time line: the load lines of panels 2 and 3 stop at it; the frame continues above it around the inset"),
]
for printed, val, lab, verdict, note in TIME:
    if val == 0:
        pos = base3["v_at_u0"] + base3["slope_dv_du"] * 2307
    else:
        T = TL[round(val, 3)]
        pos = T["v_at_u0"] + T["slope_dv_du"] * 2310
    rows.append({"figure_id": "F5-25", "panel": "1-3", "axis": "x (time, s)", "label_as_printed": printed, "value_anchored": val,
                 "line_px": f"v = {pos:.1f} at u 2310", "label_center_px": f"v = {lab:.1f}", "offset_px": round(lab - pos, 1),
                 "check": verdict, "note": ("printed once, right of panel 3, for all three panels" + ("; " + note if note else ""))})
with open("../calibration-eye-checks.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["panel"], r["axis"][:1], r["label_as_printed"][:12], r["line_px"], r["label_center_px"], r["offset_px"], r["check"])
