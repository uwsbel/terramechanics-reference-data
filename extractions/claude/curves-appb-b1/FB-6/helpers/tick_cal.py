"""Tick calibration of FB-6 (Fig. B-6, p0112.png): no grid lines, ticks inside the left and bottom
frame lines only, labels 0 and 14 on the left and right frame lines, 5 and 29 on the bottom and top
frame lines. Writes cal-p1/anchors.csv and cal-p1/calibration.json in the layout of
tools/calibrate_axes.py detect, so `piecewise` and `apply` read it.

1. Frame lines: at every sample along each frame line, the ink run nearest a rough position (runs
   wider than the line, where a tick or label touches it, set aside), robust straight-line fit.
2. Each tick line gets its own tilt (the frame is skewed, the two frame lines of an axis are not
   parallel): interpolated by value between the two frame lines of constant value of that axis
   (x: left frame x=0 and right frame x=14; y: bottom frame y=5 and top frame y=29). The tick's own
   stub (30 to 35 px long) is also fitted with a free tilt as a check, but a tilt from 30 px of ink
   cannot be carried across 1900 to 3200 px of plot, so it is reported, not used.
3. The tick line's position: the stub's ink centre at every pixel along it (from 6 px off the frame
   centre line, past the frame's own ink, to 2 px short of the stub's end), fitted with the tilt of
   step 2 fixed. Its foot (intersection with the frame centre line) is an anchor carrying both
   values; a second anchor 22 px along the tick from the foot gives the line its tilt in the
   piecewise map and puts the ink check of calibrate_axes.py on the stub.
4. Frame lines are knots: anchors at the four corners and every 300 px along the right and top
   frame lines (the left and bottom ones carry the tick feet).
5. Affine diagnostic: least squares on every anchor that carries both values (tick feet, corners).
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

img_path, out_dir = sys.argv[1], Path(sys.argv[2])
g = np.asarray(Image.open(img_path).convert("L"))
dark = g < 128
BOX = [560, 740, 2680, 4110]
TIP_PX = 22.0


def runs_of(idx):
    return np.split(idx, np.where(np.diff(idx) != 1)[0] + 1) if len(idx) else []


def frame_fit(orient, rough, t_range, maxw, half=25, step=5):
    c0, k0 = rough
    pts = []
    for t in range(t_range[0], t_range[1], step):
        p = c0 + k0 * t
        lo = int(round(p - half))
        prof = dark[t, lo:lo + 2 * half + 1] if orient == "v" else dark[lo:lo + 2 * half + 1, t]
        rs = runs_of(np.where(prof)[0])
        if not rs:
            continue
        r = min(rs, key=lambda r: abs(lo + (r[0] + r[-1]) / 2 - p))
        pts.append((t, lo + (r[0] + r[-1]) / 2, len(r)))
    t, p, w = np.array(pts, dtype=float).T
    keep = w <= maxw
    for _ in range(6):
        k, c = np.polyfit(t[keep], p[keep], 1)
        res = p - (c + k * t)
        s = 1.4826 * np.median(np.abs(res[keep]))
        keep = (w <= maxw) & (np.abs(res) <= max(1.5, 3 * s))
    res = p[keep] - (c + k * t[keep])
    q = np.polyfit(t[keep], p[keep], 2)
    tt = np.linspace(t[keep].min(), t[keep].max(), 50)
    bow = float(np.max(np.abs(np.polyval(q, tt) - (c + k * tt))))
    return {"c": float(c), "k": float(k), "n": int(keep.sum()), "n_samples": len(t), "rms_px": float(np.sqrt(np.mean(res ** 2))),
            "max_px": float(np.abs(res).max()), "width_px": float(np.median(w[keep])),
            "t_range": [float(t[keep].min()), float(t[keep].max())], "bow_px": bow}


F = {
    "left": frame_fit("v", (604.0, 0.0312), (880, 4000), 11),     # u = c + k v
    "right": frame_fit("v", (2485.0, 0.0298), (800, 3950), 11),
    "top": frame_fit("h", (852.1, -0.0256), (650, 2490), 13),     # v = c + k u
    "bottom": frame_fit("h", (4052.2, -0.0278), (740, 2590), 14),
}


def cross(vl, hl):
    """vertical u = cv + kv v, horizontal v = ch + kh u"""
    u = (vl[0] + vl[1] * hl[0]) / (1 - vl[1] * hl[1])
    return u, hl[0] + hl[1] * u


LF, RF = (F["left"]["c"], F["left"]["k"]), (F["right"]["c"], F["right"]["k"])
TF, BF = (F["top"]["c"], F["top"]["k"]), (F["bottom"]["c"], F["bottom"]["k"])
k_x = lambda x: LF[1] + (RF[1] - LF[1]) * x / 14.0      # du/dv of the line x = const
k_y = lambda y: BF[1] + (TF[1] - BF[1]) * (y - 5) / 24.0  # dv/du of the line y = const

YT = {27: 1096, 25: 1364, 23: 1633, 21: 1900, 19: 2168, 17: 2432, 15: 2699, 13: 2968, 11: 3234, 9: 3498, 7: 3764}
XT = {2: 996, 4: 1262, 6: 1530, 8: 1798, 10: 2066, 12: 2334}
# x = 2: the tick is under a plotted circle sitting on the bottom frame; it shows only inside the
# circle's hole, about 18 to 27 px above the frame centre line. Only that stretch is used.
X2_ONLY = (17, 28)

ticks = []
for y, v0 in YT.items():
    uf0 = LF[0] + LF[1] * v0
    pts = []
    for d in range(6, 50):
        u = int(round(uf0 + d))
        col = dark[v0 - 12:v0 + 13, u]
        rs = [r for r in runs_of(np.where(col)[0]) if len(r) <= 9]
        if not rs:
            if d > 12:
                break
            continue
        r = min(rs, key=lambda r: abs(v0 - 12 + (r[0] + r[-1]) / 2 - v0))
        pts.append((u, v0 - 12 + (r[0] + r[-1]) / 2, len(r)))
    pts = np.array(pts[:-2], dtype=float)   # 2 px short of the stub's end (a ragged tip)
    ticks.append(("y", y, pts))
for x, u0 in XT.items():
    vf0 = BF[0] + BF[1] * u0
    pts = []
    for d in range(6, 50):
        if x == 2 and not (X2_ONLY[0] <= d <= X2_ONLY[1]):
            continue
        v = int(round(vf0 - d))
        row = dark[v, u0 - 12:u0 + 13]
        rs = [r for r in runs_of(np.where(row)[0]) if len(r) <= 9]
        if not rs:
            if d > 12 and x != 2:
                break
            continue
        r = min(rs, key=lambda r: abs(u0 - 12 + (r[0] + r[-1]) / 2 - u0))
        if abs(u0 - 12 + (r[0] + r[-1]) / 2 - u0) > 4:
            continue
        pts.append((v, u0 - 12 + (r[0] + r[-1]) / 2, len(r)))
    pts = np.array(pts if x == 2 else pts[:-2], dtype=float)
    ticks.append(("x", x, pts))

anchors, tick_rec = [], []
for axis, val, pts in ticks:
    t, p, w = pts.T          # y tick: t = u, p = v ; x tick: t = v, p = u
    kf = k_y(val) if axis == "y" else k_x(val)
    c_fixed = float(np.mean(p - kf * t))
    res_fixed = p - (c_fixed + kf * t)
    k_free, c_free = np.polyfit(t, p, 1)
    res_free = p - (c_free + k_free * t)
    se = float(np.sqrt(np.sum(res_free ** 2) / max(1, len(t) - 2) / np.sum((t - t.mean()) ** 2)))
    if axis == "y":
        u = (LF[0] + LF[1] * c_fixed) / (1 - LF[1] * kf)
        v = c_fixed + kf * u
        n = math.hypot(1, kf)
        ut, vt = u + TIP_PX / n, v + kf * TIP_PX / n
        anchors.append({"x_value": 0, "y_value": val, "u": u, "v": v, "x_source": "left frame (label 0)",
                        "y_source": f"tick foot: stub ink fitted with its own tilt dv/du {kf:+.5f}"})
        anchors.append({"x_value": "", "y_value": val, "u": ut, "v": vt, "x_source": "",
                        "y_source": f"tick, {TIP_PX:g} px along the stub from its foot (tilt dv/du {kf:+.5f})"})
        ext = [float(t.min() - u), float(t.max() - u)]
    else:
        v = (BF[0] + BF[1] * c_fixed) / (1 - BF[1] * kf)
        u = c_fixed + kf * v
        n = math.hypot(1, kf)
        foot = {"x_value": val, "y_value": 5, "u": u, "v": v,
                "x_source": f"tick foot: stub ink fitted with its own tilt du/dv {kf:+.5f}", "y_source": "bottom frame (label 5)"}
        if val == 2:
            # Only the stretch inside the circle's hole shows the tick: the line is anchored there
            # (15 and 31 px up the tick from its foot), so the ink check looks at the visible stub and
            # not at the circle's ring or the frame. The foot enters the affine diagnostic only.
            foot["affine_only"] = True
            for d in (15.0, 31.0):
                anchors.append({"x_value": val, "y_value": "", "u": u - kf * d / n, "v": v - d / n,
                                "x_source": f"tick, {d:g} px up the stub from its foot, inside the hole of a plotted circle (tilt du/dv {kf:+.5f})",
                                "y_source": ""})
        else:
            anchors.append({"x_value": val, "y_value": "", "u": u - kf * TIP_PX / n, "v": v - TIP_PX / n,
                            "x_source": f"tick, {TIP_PX:g} px along the stub from its foot (tilt du/dv {kf:+.5f})", "y_source": ""})
        anchors.append(foot)
        ext = [float(v - t.max()), float(v - t.min())]
    tick_rec.append({"axis": axis, "value": val, "foot_u": round(u, 2), "foot_v": round(v, 2), "n_ink_samples": len(t),
                     "stub_ink_used_px_from_frame_centre": [round(e, 1) for e in ext],
                     "stub_width_px": float(np.median(w)),
                     "tilt_used": round(kf, 5), "rms_px_with_tilt_used": round(float(np.sqrt(np.mean(res_fixed ** 2))), 2),
                     "tilt_own_stub": round(float(k_free), 4), "tilt_own_stub_se": round(se, 4),
                     "rms_px_own_tilt": round(float(np.sqrt(np.mean(res_free ** 2))), 2)})

# corners and frame lines
corners = {(0, 5): cross(LF, BF), (0, 29): cross(LF, TF), (14, 5): cross(RF, BF), (14, 29): cross(RF, TF)}
for (x, y), (u, v) in corners.items():
    anchors.append({"x_value": x, "y_value": y, "u": u, "v": v,
                    "x_source": "left frame (label 0)" if x == 0 else "right frame (label 14)",
                    "y_source": "bottom frame (label 5)" if y == 5 else "top frame (label 29)"})
(u0, v0), (u1, v1) = corners[(14, 5)], corners[(14, 29)]
for vv in np.arange(v0 - 300, v1 + 150, -300):
    anchors.append({"x_value": 14, "y_value": "", "u": RF[0] + RF[1] * vv, "v": float(vv),
                    "x_source": "right frame (label 14), on its fitted line", "y_source": ""})
(u0, v0), (u1, v1) = corners[(0, 29)], corners[(14, 29)]
for uu in np.arange(u0 + 300, u1 - 150, 300):
    anchors.append({"x_value": "", "y_value": 29, "u": float(uu), "v": TF[0] + TF[1] * uu, "x_source": "",
                    "y_source": "top frame (label 29), on its fitted line"})

for a in anchors:
    a["u"], a["v"] = round(float(a["u"]), 2), round(float(a["v"]), 2)

both = [a for a in anchors if a["x_value"] != "" and a["y_value"] != ""]
anchors = [a for a in anchors if not a.get("affine_only")]
U = np.array([[a["u"], a["v"], 1.0] for a in both])
X = np.array([float(a["x_value"]) for a in both])
Y = np.array([float(a["y_value"]) for a in both])
ax, *_ = np.linalg.lstsq(U, X, rcond=None)
ay, *_ = np.linalg.lstsq(U, Y, rcond=None)
rx, ry = X - U @ ax, Y - U @ ay

out_dir.mkdir(parents=True, exist_ok=True)
with (out_dir / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    wr.writeheader()
    wr.writerows(anchors)


def spacing(axis):
    """Each axis's tick feet against a straight line in value, and the frame lines against it."""
    rows = [r for r in tick_rec if r["axis"] == axis]
    vals = np.array([r["value"] for r in rows], dtype=float)
    pos = np.array([r["foot_v"] if axis == "y" else r["foot_u"] for r in rows])
    k, c = np.polyfit(vals, pos, 1)
    rec = {"px_per_unit": round(float(k), 3),
           "tick_residual_px": {f"{v:g}": round(float(p - (c + k * v)), 2) for v, p in zip(vals, pos)}}
    if axis == "x":
        rec["frames_minus_tick_line_px"] = {"x=0 (left frame, at the bottom)": round(float(corners[(0, 5)][0] - c), 2),
                                            "x=14 (right frame, at the bottom)": round(float(corners[(14, 5)][0] - (c + 14 * k)), 2)}
    else:
        rec["frames_minus_tick_line_px"] = {"y=5 (bottom frame, at the left)": round(float(corners[(0, 5)][1] - (c + 5 * k)), 2),
                                            "y=29 (top frame, at the left)": round(float(corners[(0, 29)][1] - (c + 29 * k)), 2)}
    return rec


cal = {
    "image": img_path, "box": BOX,
    "method": "ticks (no grid lines), out/FB-6/helpers/tick_cal.py: frame lines and tick stubs measured on the ink; each tick line's tilt interpolated between the two frame lines of its axis",
    "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the anchors that carry both values: tick feet and frame corners); a diagnostic: values come from `calibrate_axes.py piecewise` on anchors.csv",
    "ax": [float(c) for c in ax], "ay": [float(c) for c in ay],
    "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
    "rms_residual_x": float(np.sqrt(np.mean(rx ** 2))), "rms_residual_y": float(np.sqrt(np.mean(ry ** 2))),
    "max_residual_x": float(np.abs(rx).max()), "max_residual_y": float(np.abs(ry).max()),
    "n_anchors": len(both),
    "affine_residuals": [{"x_value": a["x_value"], "y_value": a["y_value"], "res_x": round(float(r1), 4), "res_y": round(float(r2), 4)}
                         for a, r1, r2 in zip(both, rx, ry)],
    "frames": {n: {kk: (round(vv, 5) if isinstance(vv, float) else vv) for kk, vv in d.items()} for n, d in F.items()},
    "frame_note": "left, right: u = c + k v; top, bottom: v = c + k u; bow_px: largest gap between a quadratic and the straight fit",
    "frame_angles_deg": {"left_from_vertical": round(math.degrees(math.atan(LF[1])), 3), "right_from_vertical": round(math.degrees(math.atan(RF[1])), 3),
                         "top_from_horizontal": round(math.degrees(math.atan(TF[1])), 3), "bottom_from_horizontal": round(math.degrees(math.atan(BF[1])), 3)},
    "corners": {f"x={x},y={y}": [round(u, 2), round(v, 2)] for (x, y), (u, v) in corners.items()},
    "ticks": tick_rec,
    "tick_spacing": {"x": spacing("x"), "y": spacing("y")},
    "vertical_lines": [{"x_value": 0, "slope_du_dv": LF[1], "u_at_v0": LF[0], "source": "left frame, measured"}]
                      + [{"x_value": r["value"], "slope_du_dv": r["tilt_used"], "u_at_v0": round(r["foot_u"] - r["tilt_used"] * r["foot_v"], 2),
                          "source": "tick, measured; tilt interpolated between the frame lines"} for r in tick_rec if r["axis"] == "x"]
                      + [{"x_value": 14, "slope_du_dv": RF[1], "u_at_v0": RF[0], "source": "right frame, measured"}],
    "horizontal_lines": [{"y_value": 5, "slope_dv_du": BF[1], "v_at_u0": BF[0], "source": "bottom frame, measured"}]
                        + [{"y_value": r["value"], "slope_dv_du": r["tilt_used"], "v_at_u0": round(r["foot_v"] - r["tilt_used"] * r["foot_u"], 2),
                            "source": "tick, measured; tilt interpolated between the frame lines"}
                           for r in sorted(tick_rec, key=lambda r: r["value"]) if r["axis"] == "y"]
                        + [{"y_value": 29, "slope_dv_du": TF[1], "v_at_u0": TF[0], "source": "top frame, measured"}],
}
(out_dir / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(json.dumps({k: cal[k] for k in ("x_per_px", "y_per_px", "rms_residual_x", "rms_residual_y", "max_residual_x", "max_residual_y",
                                      "n_anchors", "frame_angles_deg", "corners", "tick_spacing")}, indent=1))
for n, d in F.items():
    print(n, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items()})
for r in tick_rec:
    print(r)
print("affine residuals:", cal["affine_residuals"])
