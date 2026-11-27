import csv, json
import numpy as np
cal = json.load(open("out/FC-4A/cal-p1/calibration.json"))
H = {l["y_value"]: l for l in cal["horizontal_lines"]}
V = {l["x_value"]: l for l in cal["vertical_lines"]}
ypx = cal["y_per_px"]; xpx = cal["x_per_px"]
# measured: tick centers (outside part, u 900-914 for y; v 3496-3512 for x), label centers
yt = {1000: (3193.5, 3186.0), 2000: (2902.5, 2895.0), 3000: (2611.0, 2599.0), 4000: (2320.0, 2309.0),
      5000: (2027.5, 2017.5), 6000: (1734.0, 1726.0), 7000: (1442.5, 1434.5)}
xt = {1000: (1214.5, 1223.5), 2000: (1511.5, 1512.5), 3000: (1801.5, 1802.5), 4000: (2092.0, 2093.5), 5000: (2375.0, 2385.0)}
eye_y = {2000, 5000, 7000, 8000}
eye_x = {1000, 3000, 5000}
rows = []
for y in [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]:
    l = H[y]; fit = l["v_at_u0"] + l["slope_dv_du"] * 921
    if y in yt:
        tick, lab = yt[y]; d = tick - fit
        note = "tick mark outside and inside the frame"
    else:
        tick = fit if y == 0 else 1160.9; lab = {0: float("nan"), 8000: 1152.5}[y]; d = tick - fit
        note = "frame line (bottom) carries 0; printed 0 sits at the lower-left corner below the frame" if y == 0 else "frame line (top) carries 8000; no separate tick; label 8000 centered 8.4 px above the frame line, like the other labels (7.5 to 12 px above their ticks)"
    rows.append({"axis": "y", "printed_label": y, "label_center_px": "" if lab != lab else lab, "tick_or_frame_px": round(tick, 1),
                 "fitted_px": round(fit, 1), "diff_px": round(d, 1), "tool_value_at_tick_minus_printed": round(-d * ypx, 1) + 0.0,
                 "diff_pct_span": round(abs(d * ypx) / 8000 * 100, 2), "checked_by_eye": "yes" if y in eye_y else "measured", "note": note})
for x in [0, 1000, 2000, 3000, 4000, 5000]:
    l = V[x]; fit = l["u_at_v0"] + l["slope_du_dv"] * 3500
    if x in xt and x != 5000:
        tick, lab = xt[x]; note = "tick mark below and above the bottom frame"
    elif x == 5000:
        tick, lab = xt[x]; note = "tick below the frame continues the right frame line (2375-2381); right frame carries 5000"
    else:
        tick, lab = fit, 879.5; note = "left frame line carries 0; printed 0 is at the lower-left corner, 43 px left of the axis (shared corner label)"
    d = tick - fit
    rows.append({"axis": "x", "printed_label": x, "label_center_px": lab, "tick_or_frame_px": round(tick, 1),
                 "fitted_px": round(fit, 1), "diff_px": round(d, 1), "tool_value_at_tick_minus_printed": round(d * xpx, 1),
                 "diff_pct_span": round(abs(d * xpx) / 5000 * 100, 2), "checked_by_eye": "yes" if x in eye_x else "measured", "note": note})
with open("out/FC-4A/calibration-eye-checks.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
# sensitivity: tick-based 1-D maps
yv = np.array([0] + list(yt.keys())); vv = np.array([H[0]["v_at_u0"] + H[0]["slope_dv_du"] * 921] + [yt[k][0] for k in yt])
by, ay_ = np.polyfit(vv, yv, 1)
xv = np.array([0] + list(xt.keys())); uu = np.array([V[0]["u_at_v0"] + V[0]["slope_du_dv"] * 3500] + [xt[k][0] for k in xt])
bx, ax_ = np.polyfit(uu, xv, 1)
print("tick-based y = %.4f v + %.1f (resid rms %.1f psf); x = %.4f u + %.1f (resid rms %.1f psf)" % (by, ay_, np.std(yv - (by*vv+ay_)), bx, ax_, np.std(xv - (bx*uu+ax_))))
A = cal["ax"]; B = cal["ay"]
for r in csv.DictReader(open("out/FC-4A/points-p1.csv", encoding="utf-8")):
    if r["point_kind"] in ("marker", "feature"):
        u, v = float(r["pixel_u"]), float(r["pixel_v"])
        sl_h = np.mean([l["slope_dv_du"] for l in cal["horizontal_lines"]]); sl_v = np.mean([l["slope_du_dv"] for l in cal["vertical_lines"]])
        va = v - sl_h * (u - 921); ua = u - sl_v * (v - 3500)   # carry the point to the tick columns/rows along the page tilt
        x1 = A[0]*u + A[1]*v + A[2]; y1 = B[0]*u + B[1]*v + B[2]
        print(r["series_id"], r["point_kind"], r["sequence"], "tool (%.0f, %.0f)  tick-based (%.0f, %.0f)  diff (%.0f, %.0f)" % (x1, y1, bx*ua+ax_, by*va+ay_, bx*ua+ax_-x1, by*va+ay_-y1))
