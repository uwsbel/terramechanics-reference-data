"""Write cal-p<n>/ (anchors.csv, calibration.json) for each panel of Figure 5-25 from the lines
measured on the ink by measure_lines.py, in the layout of tools/calibrate_axes.py detect.

Why not `detect` itself: the time lines (constant x) are dash-dot lines drawn only at the left of
panel 1 (u 745 to 965) and as short segments at the right of panel 3 (u 2195 to 2268); inside the
panels they are absent, so `detect` cannot find them in bands across any panel box and would only
predict them from the frame. Here each time line is measured where it is drawn and fitted as one
straight line across the figure (the same physical line for all three panels); each load line is
measured in bands along its whole length. Anchors are the measured ink points themselves, one axis
per row (the other value blank, which the piecewise map reads as anchoring one axis only), so the
tool's ink check runs where the ink is. The affine map, a diagnostic only, is fitted to the
intersections of the fitted lines inside the panel.
"""
import csv
import json
import sys
from pathlib import Path
import numpy as np

lines = json.load(open(sys.argv[1], encoding="utf-8"))
outroot = Path(sys.argv[2])
image = sys.argv[3]
# the time lines: anchors and fits from time_anchors.py (measured along the drawn dashes)
TL = {round(T["value"], 3): T for T in json.load(open(sys.argv[4], encoding="utf-8"))}
for L in lines["horizontal"]:
    T = TL[round(L["value"], 3)]
    L["anchors"] = T["anchors"]
    L["v_at_u0"], L["slope_dv_du"] = T["v_at_u0"], T["slope_dv_du"]
    if L["value"] != 0:
        L["n"], L["n_all"], L["rms"] = len(T["anchors"]), len(T["anchors"]), T["rms"]
PANELS = {1: {"loads": [0, 20, 40, 60], "ydir": "left", "box": [975, 1810, 1265, 3540]},
          2: {"loads": [0, 20, 40, 60], "ydir": "left", "box": [1405, 1810, 1690, 3540]},
          3: {"loads": [0, -20, -40, -60, -80, -100], "ydir": "right", "box": [1830, 1810, 2300, 3540]}}
SRC = "measured on the ink (helpers/measure_lines.py)"

for p, P in PANELS.items():
    d = outroot / f"cal-p{p}"
    d.mkdir(parents=True, exist_ok=True)
    V = [L for L in lines["vertical"] if L["panel"] == p and L["value"] in P["loads"]]
    H = lines["horizontal"]
    rows = []
    for L in H:
        # anchors along the drawn dashes, about 16 px apart in a long dash, so that the tool's ink-check
        # positions, placed between consecutive anchors, fall on the ink
        anchors = L["anchors"]
        if L["value"] == 0:
            # the baseline (t = 0, the bottom frame) is slightly bent across the figure (v 3525 at the left of
            # panel 1, 3531.5 at the right of panel 3): each panel keeps the stretch under it, every third
            # band measurement (18 px apart)
            u_lo = min(vl["u_at_v0"] + vl["slope_du_dv"] * 3528 for vl in V) - 12
            u_hi = max(vl["u_at_v0"] + vl["slope_du_dv"] * 3528 for vl in V) + 12
            anchors = [a for a in sorted(anchors) if u_lo <= a[0] <= u_hi][::3]
            A = np.array(anchors)
            k1, k0 = np.polyfit(A[:, 0], A[:, 1], 1)
            L = dict(L, v_at_u0=float(k0), slope_dv_du=float(k1), n=len(anchors), n_all=len(anchors),
                     rms=float(np.sqrt(np.mean((A[:, 1] - k0 - k1 * A[:, 0]) ** 2))), anchors=anchors)
            H = [L if h["value"] == 0 else h for h in H]
        for u, v in anchors:
            rows.append({"x_value": L["value"], "y_value": "", "u": round(u, 2), "v": round(v, 2),
                         "x_source": SRC, "y_source": ""})
    for L in V:
        for u, v in sorted(L["samples"], key=lambda s: s[1]):
            rows.append({"x_value": "", "y_value": L["value"], "u": round(u, 2), "v": round(v, 2),
                         "x_source": "", "y_source": SRC})
    with (d / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    # affine diagnostic from intersections of the fitted lines
    inter = []
    for h in H:
        for vl in V:
            sh, ih = h["slope_dv_du"], h["v_at_u0"]
            sv, iv = vl["slope_du_dv"], vl["u_at_v0"]
            u = (iv + sv * ih) / (1 - sv * sh)
            v = ih + sh * u
            inter.append({"x_value": h["value"], "y_value": vl["value"], "u": round(u, 2), "v": round(v, 2)})
    U = np.array([[a["u"], a["v"], 1.0] for a in inter])
    X = np.array([a["x_value"] for a in inter], float)
    Y = np.array([a["y_value"] for a in inter], float)
    ax, *_ = np.linalg.lstsq(U, X, rcond=None)
    ay, *_ = np.linalg.lstsq(U, Y, rcond=None)
    rx, ry = X - U @ ax, Y - U @ ay
    cal = {"image": image, "box": P["box"], "bands": "per line (see helpers/measure_lines.py)", "dark": 128,
           "min_frac": "per line", "snap": None,
           "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the grid intersections)",
           "ax": ax.tolist(), "ay": ay.tolist(),
           "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
           "rms_residual_x": float(np.sqrt((rx ** 2).mean())), "rms_residual_y": float(np.sqrt((ry ** 2).mean())),
           "max_residual_x": float(np.abs(rx).max()), "max_residual_y": float(np.abs(ry).max()),
           "n_anchors": len(rows), "n_affine_anchors": len(inter),
           "anchors_note": ("anchors.csv holds the measured ink points of each line, one axis per row; the affine "
                            "map is fitted to the intersections of the fitted lines (affine_anchors)"),
           "affine_anchors": inter,
           "vertical_lines": [{"y_value": L["value"], "slope_du_dv": L["slope_du_dv"], "u_at_v0": L["u_at_v0"],
                               "source": f"measured on the ink in {L['n']}/{L['n_all']} bands, rms {L['rms']:.2f} px",
                               "samples": L["samples"]} for L in V],
           "horizontal_lines": [{"x_value": L["value"], "slope_dv_du": L["slope_dv_du"], "v_at_u0": L["v_at_u0"],
                                 "source": f"measured on the ink at {len(L['anchors'])} places along its drawn dashes, rms {L['rms']:.2f} px",
                                 "samples": L["anchors"]} for L in H],
           "x_direction": "up", "y_direction": P["ydir"]}
    (d / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
    span_x, span_y = 0.10, abs(max(P["loads"]) - min(P["loads"]))
    print(f"panel {p}: {len(rows)} anchors, {len(inter)} intersections; x {cal['x_per_px']:.6f} s/px rms {cal['rms_residual_x']:.6f} "
          f"(max {cal['max_residual_x']:.6f}, {100 * cal['max_residual_x'] / span_x:.2f}% of span); "
          f"y {cal['y_per_px']:.4f} lb/px rms {cal['rms_residual_y']:.3f} (max {cal['max_residual_y']:.3f}, {100 * cal['max_residual_y'] / span_y:.2f}% of span)")
