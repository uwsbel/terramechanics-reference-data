"""Write calibration-eye-checks.csv: printed label, fitted pixel (inverse of the final affine map at
the stated column or row) and the pixel read by eye (line center on a zoomed crop, confirmed with
plot_grid scan / lines), with the residual in printed units and in percent of the axis span."""
import csv
import json

cal = {1: json.load(open("cal-p1/calibration.json")), 2: json.load(open("cal-p2/calibration.json"))}
span = {(1, "x"): 250, (1, "y"): 5000, (2, "x"): 250, (2, "y"): 300}


def fitted(p, axis, value, at):
    ax, ay = cal[p]["ax"], cal[p]["ay"]
    if axis == "y":
        return (value - ay[0] * at - ay[2]) / ay[1]
    return (value - ax[1] * at - ax[2]) / ax[0]


rows = [
    # panel, axis, label, at (u for y, v for x), eye pixel, note
    (1, "y", "0", 760, 2211.0, "bottom frame line; label 0 printed at it"),
    (1, "y", "1000", 760, 1926.5, "gridline"),
    (1, "y", "2000", 760, 1633.5, "gridline"),
    (1, "y", "3000", 760, 1341.5, "gridline"),
    (1, "y", "4000", 760, 1043.5, "gridline"),
    (1, "y", "5000", 760, 751.5, "top frame line, hidden behind the legend box for u 795 to 2010; not an anchor of the fit"),
    (1, "y", "0", 2210, 2193.5, "bottom frame line, right end"),
    (1, "y", "1000", 2210, 1909.5, "gridline, right end"),
    (1, "y", "4000", 2210, 1027.5, "gridline, right end"),
    (1, "y", "5000", 2210, 733.0, "top frame line, right end; not an anchor"),
    (1, "x", "50", 2130, 1063.5, "gridline (labels printed under the lower panel only)"),
    (1, "x", "100", 2130, 1355.5, "gridline"),
    (1, "x", "150", 2130, 1649.5, "gridline"),
    (1, "x", "200", 2130, 1943.5, "gridline"),
    (1, "x", "250", 2130, 2236.5, "gridline"),
    (1, "x", "50", 890, 1042.5, "gridline, top of panel"),
    (1, "x", "150", 890, 1632.5, "gridline, top of panel"),
    (1, "x", "250", 890, 2220.5, "gridline, top of panel"),
    (1, "x", "0 (not printed)", 2130, 746.5, "left frame line: NOT at x = 0 of the 50-250 grid (frame to 50 line 317 px, other intervals 293.5 px); not an anchor"),
    (2, "x", "50", 3190, 1082.5, "gridline; label 50 text centered at u 1090"),
    (2, "x", "100", 3190, 1374.5, "gridline"),
    (2, "x", "150", 3190, 1667.5, "gridline; label text centered at u 1660"),
    (2, "x", "200", 3190, 1961.5, "gridline; label text centered at u 1962"),
    (2, "x", "250", 3190, 2254.0, "gridline; label text centered at u 2260"),
    (2, "x", "0 (not printed)", 3190, 763.5, "left frame line: NOT at x = 0 of the 50-250 grid (frame to 50 line 319 px, other intervals 292 to 294 px); not an anchor"),
    (2, "y", "0 (not printed)", 760, 2354.2, "top frame line; value 0 inferred (three 293 px divisions above the -300 frame), not printed"),
    (2, "y", "-300", 760, 3235.0, "bottom frame line; label -300 text center at v 3230 (u 675)"),
    (2, "y", "-100", 670, 2626.5, "NO gridline in the lower panel: eye pixel is the center of the printed label text; 22 px above the fitted -100 (upper-panel labels sit within 6 px of their lines)"),
    (2, "y", "-200", 670, 2934.5, "NO gridline in the lower panel: eye pixel is the center of the printed label text"),
    (2, "y", "-300", 670, 3230.0, "center of the printed label text (the frame line itself is checked in the row above)"),
]
with open("calibration-eye-checks.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure", "panel", "axis", "printed_label", "measured_at", "fitted_pixel", "eye_pixel", "residual_px", "residual_units", "residual_pct_span", "note"])
    for p, axis, lab, at, eye, note in rows:
        val = float(lab.split()[0])
        fp = fitted(p, axis, val, at)
        per = cal[p]["y_per_px"] if axis == "y" else cal[p]["x_per_px"]
        r_px = eye - fp
        r_u = r_px * per * (-1 if axis == "y" else 1)
        where = f"u={at}" if axis == "y" else f"v={at}"
        w.writerow(["FC-6D", p, axis, lab, where, f"{fp:.1f}", f"{eye:.1f}", f"{r_px:+.1f}", f"{r_u:+.2f}", f"{100 * abs(r_u) / span[(p, axis)]:.2f}", note])
print(open("calibration-eye-checks.csv", encoding="utf-8").read())
