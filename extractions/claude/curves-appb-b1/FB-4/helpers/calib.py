"""Tick calibration of FB-4 (Fig. B-4, p0110.png): frame lines fitted on their ink, ticks located
on their stubs, anchors written in the calibration.json/anchors.csv layout of
tools/calibrate_axes.py (hand-made tick calibration, with `box` and `anchors`).

x (sigma_3, psi): ticks at 2..12 on the bottom frame (pointing up, inside); 0 = left frame, 14 = right
frame (labels "0" and "14" printed under them; tick spacing confirms both).
y (E, kips/in.^2): ticks at 1..9 on the left frame (pointing right, inside); 0 = bottom frame,
10 = top frame (labels "0" and "10" printed beside them; tick spacing confirms both)."""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

img, outdir = sys.argv[1], Path(sys.argv[2])
D = np.asarray(Image.open(img).convert("L")) < 128


def runs(mask):
    idx = np.where(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s, p))
            s = i
        p = i
    out.append((s, p))
    return out


def robust_fit(ts, cs):
    ts, cs = np.array(ts, float), np.array(cs, float)
    keep = np.ones(len(ts), bool)
    for _ in range(4):
        k, c0 = np.polyfit(ts[keep], cs[keep], 1)
        r = cs - (c0 + k * ts)
        mad = np.median(np.abs(r[keep] - np.median(r[keep]))) * 1.4826
        keep = np.abs(r) <= max(1.0, 3 * mad)
    k, c0 = np.polyfit(ts[keep], cs[keep], 1)
    r = cs[keep] - (c0 + k * ts[keep])
    return float(c0), float(k), float(np.sqrt(np.mean(r ** 2))), int(keep.sum()), len(ts)


def frame_h(vlo, vhi, ulo, uhi, maxw=14):
    ts, cs = [], []
    for u in range(ulo, uhi, 2):
        rr = runs(D[vlo:vhi, u])
        if not rr:
            continue
        s, p = max(rr, key=lambda x: x[1] - x[0])
        if 3 <= p - s + 1 <= maxw:
            ts.append(u); cs.append(vlo + (s + p) / 2)
    return robust_fit(ts, cs)


def frame_v(ulo, uhi, vlo, vhi, maxw=12):
    ts, cs = [], []
    for v in range(vlo, vhi, 2):
        rr = runs(D[v, ulo:uhi])
        if not rr:
            continue
        s, p = max(rr, key=lambda x: x[1] - x[0])
        if 3 <= p - s + 1 <= maxw:
            ts.append(v); cs.append(ulo + (s + p) / 2)
    return robust_fit(ts, cs)


# frame lines: position = c0 + k t (bottom/top: v(u); left/right: u(v))
F = {"bottom": frame_h(3880, 3935, 640, 2520), "top": frame_h(1085, 1140, 640, 2520),
     "left": frame_v(570, 630, 1150, 3870), "right": frame_v(2530, 2590, 1150, 3870)}
for name, (c0, k, rms, n, N) in F.items():
    print(f"frame {name:6s}: {c0:.2f} {k:+.6f} t   rms {rms:.2f} px, {n}/{N} samples")


def hv(name, t):
    c0, k = F[name][:2]
    return c0 + k * t


def corner(vname, hname):
    """intersection of vertical frame u = a + b v and horizontal frame v = c + d u"""
    a, b = F[vname][:2]
    c, d = F[hname][:2]
    u = (a + b * c) / (1 - b * d)
    return u, c + d * u


# x ticks on the bottom frame: centre of the tick's run in each row of its stub, 7 to 20 px above
# the frame centre (the frame is 10 px thick, so its top edge is about 5 px above the centre)
xticks = {2: 874, 4: 1151.5, 6: 1432.5, 8: 1715.5, 10: 1995.5, 12: 2272.5}
yticks = {9: 1385, 8: 1668.5, 7: 1947.5, 6: 2226.5, 5: 2507, 4: 2787.5, 3: 3066.5, 2: 3346.5, 1: 3625.5}
anchors, tick_rec = [], []
for val, u0 in xticks.items():
    vb = hv("bottom", u0)
    rows, cents, widths = [], [], []
    length = None
    for dv in range(7, 60):
        v = int(round(vb - dv))
        rr = runs(D[v, int(u0) - 12:int(u0) + 13])
        if not rr:
            length = dv
            break
        s, p = max(rr, key=lambda x: x[1] - x[0])
        if dv <= 20:
            rows.append(v); cents.append(int(u0) - 12 + (s + p) / 2); widths.append(p - s + 1)
    c0, k, rms, n, N = robust_fit(rows, cents)
    u_at = c0 + k * vb      # the tick's centre line at the frame centre
    u_mean = float(np.mean(cents))
    va = hv("bottom", u_mean)
    tick_rec.append({"axis": "x", "value": val, "u_mean": round(u_mean, 2), "u_fit_at_frame": round(u_at, 2),
                     "tilt_du_dv": round(k, 4), "width_px": float(np.median(widths)),
                     "ink_ends_px_above_frame_centre": length, "scatter_px": round(float(np.std(cents)), 2)})
    anchors.append({"x_value": val, "y_value": "", "u": round(u_mean, 2), "v": round(va, 2),
                    "x_source": f"tick on the bottom frame, stub rows {len(rows)}", "y_source": ""})

for val, v0 in yticks.items():
    ul = hv("left", v0)
    cols, cents, widths = [], [], []
    length = None
    for du in range(6, 60):
        u = int(round(ul + du))
        rr = runs(D[int(v0) - 12:int(v0) + 13, u])
        if not rr:
            length = du
            break
        s, p = max(rr, key=lambda x: x[1] - x[0])
        if du <= 20:
            cols.append(u); cents.append(int(v0) - 12 + (s + p) / 2); widths.append(p - s + 1)
    c0, k, rms, n, N = robust_fit(cols, cents)
    v_mean = float(np.mean(cents))
    ua = hv("left", v_mean)
    tick_rec.append({"axis": "y", "value": val, "v_mean": round(v_mean, 2), "v_fit_at_frame": round(c0 + k * ul, 2),
                     "tilt_dv_du": round(k, 4), "width_px": float(np.median(widths)),
                     "ink_ends_px_right_of_frame_centre": length, "scatter_px": round(float(np.std(cents)), 2)})
    anchors.append({"x_value": "", "y_value": val, "u": round(ua, 2), "v": round(v_mean, 2),
                    "x_source": "", "y_source": f"tick on the left frame, stub columns {len(cols)}"})

# frame lines as lines of constant value: anchors along each frame at the tick positions and corners
cBL, cTL, cBR, cTR = corner("left", "bottom"), corner("left", "top"), corner("right", "bottom"), corner("right", "top")
for (u, v), xv, yv in ((cBL, 0, 0), (cTL, 0, 10), (cBR, 14, 0), (cTR, 14, 10)):
    anchors.append({"x_value": xv, "y_value": yv, "u": round(u, 2), "v": round(v, 2),
                    "x_source": f"frame ({'left' if xv == 0 else 'right'}), labelled {xv}",
                    "y_source": f"frame ({'bottom' if yv == 0 else 'top'}), labelled {yv}"})
ytick_v = [a["v"] for a in anchors if a["y_value"] != "" and a["x_value"] == ""]
xtick_u = [a["u"] for a in anchors if a["x_value"] != "" and a["y_value"] == ""]
for v in ytick_v:
    anchors.append({"x_value": 0, "y_value": "", "u": round(hv("left", v), 2), "v": v,
                    "x_source": "frame (left), labelled 0", "y_source": ""})
    anchors.append({"x_value": 14, "y_value": "", "u": round(hv("right", v), 2), "v": v,
                    "x_source": "frame (right), labelled 14", "y_source": ""})
for u in xtick_u:
    anchors.append({"x_value": "", "y_value": 0, "u": u, "v": round(hv("bottom", u), 2),
                    "x_source": "", "y_source": "frame (bottom), labelled 0"})
    anchors.append({"x_value": "", "y_value": 10, "u": u, "v": round(hv("top", u), 2),
                    "x_source": "", "y_source": "frame (top), labelled 10"})


def fit_axis(col):
    A = [a for a in anchors if a[col] != ""]
    U = np.array([[a["u"], a["v"], 1.0] for a in A])
    X = np.array([float(a[col]) for a in A])
    c, *_ = np.linalg.lstsq(U, X, rcond=None)
    r = X - U @ c
    return (c.tolist(), float(np.sqrt(np.mean(r ** 2))), float(np.abs(r).max()),
            [(float(a[col]), round(a["u"], 1), round(a["v"], 1), round(float(ri), 4)) for a, ri in zip(A, r)])


ax, rmsx, maxx, resx = fit_axis("x_value")
ay, rmsy, maxy, resy = fit_axis("y_value")
outdir.mkdir(parents=True, exist_ok=True)
with (outdir / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader()
    w.writerows(anchors)
cal = {
    "image": img, "box": [560, 1060, 2610, 3950],
    "method": ("hand-made tick calibration (helpers/calib.py): frame lines fitted on the centre of their ink; "
               "ticks located on their stubs (x: rows 7-20 px above the bottom frame centre; y: columns 6-20 px "
               "right of the left frame centre), anchored on the frame centre line; frames used as the lines of "
               "value 0 and 14 (x) and 0 and 10 (y), where the printed labels sit and the tick spacing confirms them"),
    "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the anchors of each axis)",
    "ax": ax, "ay": ay,
    "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
    "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
    "n_anchors": len(anchors),
    "frames": {k: {"pos_at_t0": round(v[0], 3), "slope": round(v[1], 6), "rms_px": round(v[2], 3), "n": v[3]} for k, v in F.items()},
    "ticks": tick_rec,
    "residuals_x": resx, "residuals_y": resy,
    "anchors": anchors,
}
(outdir / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(f"x: {cal['x_per_px']:.5f} psi/px, rms {rmsx:.4f}, max {maxx:.4f} psi; "
      f"y: {cal['y_per_px']:.5f} ksi/px, rms {rmsy:.4f}, max {maxy:.4f}")
for t in tick_rec:
    print(" ", t)
print("corners", [tuple(round(c, 1) for c in p) for p in (cBL, cTL, cBR, cTR)])
for name, res in (("x", resx), ("y", resy)):
    print(name, "residuals (value, u, v, residual):")
    for r in res:
        print("   ", r)
