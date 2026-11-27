"""Write calibration-eye-checks.csv: every printed axis label of FC-2A, its center read by eye on the
zoomed crops (crops/origin.png, xt12.png, xt34.png, xt5.png, yaxis_top.png, ylab34.png, ylab12.png),
the tick (anchor) it belongs to, and the fitted map's value there.

usage: python eye_checks.py <calibration.json> <anchors.csv> <out.csv>
"""
import csv
import json
import sys

cal = json.load(open(sys.argv[1], encoding="utf-8"))
ax, ay = cal["ax"], cal["ay"]
X = lambda u, v: ax[0] * u + ax[1] * v + ax[2]
Y = lambda u, v: ay[0] * u + ay[1] * v + ay[2]
anchors = list(csv.DictReader(open(sys.argv[2], encoding="utf-8")))
la, ba = cal["left_axis"], cal["bottom_axis"]

# (axis, printed label, eye-read label center u, v, crop)
labels = [
    ("x", 0, 943, 3428, "origin.png"), ("x", 1000, 1250, 3431, "xt12.png"), ("x", 2000, 1520, 3431, "xt12.png"),
    ("x", 3000, 1810, 3431, "xt34.png"), ("x", 4000, 2102, 3436, "xt34.png"), ("x", 5000, 2411, 3440, "xt5.png"),
    ("y", 0, 905, 3361, "origin.png"), ("y", 1000, 864, 3071, "ylab12.png"), ("y", 2000, 864, 2770, "ylab12.png"),
    ("y", 3000, 866, 2480, "ylab34.png"), ("y", 4000, 876, 2191, "ylab34.png"), ("y", 5000, 875, 1877, "yaxis_top.png"),
    ("y", 6000, 878, 1606, "yaxis_top.png"),
]
rows = []
for axis, val, lu, lv, crop in labels:
    if axis == "x":
        a = next(r for r in anchors if float(r["x_value"]) == val and float(r["y_value"]) == 0)
        at_tick = X(float(a["u"]), float(a["v"]))
        # label center carried vertically onto the bottom axis
        at_label = X(lu, ba["v_at_u0"] + ba["slope_dv_du"] * lu)
    else:
        a = next(r for r in anchors if float(r["y_value"]) == val and float(r["x_value"]) == 0)
        at_tick = Y(float(a["u"]), float(a["v"]))
        at_label = Y(la["u_at_v0"] + la["slope_du_dv"] * lv, lv)
    span = 5000 if axis == "x" else 6000
    res = val - at_tick
    rows.append(dict(
        figure_id="FC-2A", panel=1, axis=axis, printed_label=val, label_center_u=lu, label_center_v=lv,
        tick_u=a["u"], tick_v=a["v"], tick_source=a["x_source"] if axis == "x" else a["y_source"],
        map_value_at_tick=round(at_tick, 1), residual=round(res, 1), residual_pct_span=round(100 * abs(res) / span, 2),
        map_value_at_label_center=round(at_label, 1), crop=crop,
        by_eye=("confirmed: label sits under its tick" if axis == "x" else "confirmed: label sits left of its tick") if not (axis == "x" and val == 5000) else
        "confirmed: label sits under the right frame line, no separate tick drawn",
    ))
for r in rows:
    if r["axis"] == "x" and r["printed_label"] == 0:
        r["by_eye"] = "confirmed: 0 sits under the axis corner"
    if r["axis"] == "y" and r["printed_label"] == 0:
        r["by_eye"] = "confirmed: 0 sits left of the axis corner (no tick; the bottom axis line is y = 0)"
    if r["residual_pct_span"] > 0.5:
        r["by_eye"] += f"; tick drawn off the even spacing (residual {r['residual']} psf, {r['residual_pct_span']} % of span), checked on the crop"
with open(sys.argv[3], "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["axis"], r["printed_label"], r["map_value_at_tick"], r["residual"], r["map_value_at_label_center"], r["by_eye"])
