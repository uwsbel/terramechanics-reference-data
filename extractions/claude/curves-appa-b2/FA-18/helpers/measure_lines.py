"""Claude reader helper (FA-18): measure each labelled grid line on the page and write a calibration
directory in the layout of tools/calibrate_axes.py detect (anchors.csv, calibration.json).

Why a helper: on this sideways log sheet the grid is dense (2 percent lines every 29 px, log
subdivisions, dashed sieve lines 20 px from some labelled lines) and the table hides the middle of
many lines; the band tracker of `detect` mixed tracks (max residual 1.9 percent in a trial run).
Here each labelled line is predicted from two positions read by eye on the page, and its ink is
located with the tool's own ink_offset (darkness-weighted core centre across the line) every `step`
px along it; offsets far from a robust straight-line fit (the curve, the table, a crossing line) are
set aside, and the line is the least-squares fit of the rest. Anchors are the intersections of the
fitted lines, as in `detect`, and the affine map is fitted by the tool's fit_affine.
"""
import csv, json, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3] / "tools"))
import calibrate_axes as ca  # noqa: E402

img = sys.argv[1]
out = Path(sys.argv[2])
gray = np.asarray(Image.open(img).convert("L"), dtype=float)

# horizontal lines carry grain size x (mm): rough v at u=725 and at u=1925 (read on profiles and crops)
H = {9.0: (1162.7, 1138.7), 5.0: (1412.4, 1389.0), 4.0: (1509.0, 1485.3), 3.0: (1632.0, 1608.0),
     2.0: (1804.0, 1781.4), 1.5: (1926.0, 1902.5), 1.0: (2094.5, 2073.7), 0.5: (2388.2, 2365.0),
     0.2: (2772.5, 2748.5), 0.1: (3061.9, 3039.7), 0.05: (3353.0, 3332.0), 0.02: (3739.4, 3719.0)}
# vertical lines carry percent finer y: rough u at v=1225 and v=3675
V = {100: (587.6, 642.9), 90: (734.4, 788.4), 80: (880.0, 932.3), 70: (1026.4, 1079.0),
     60: (1170.3, 1223.6), 50: (1316.8, 1371.2), 40: (1464.0, 1517.3), 30: (1610.8, 1663.3),
     20: (1756.5, 1808.3), 10: (1901.7, 1953.7), 0: (2049.0, 2101.6)}


def measure(axis, t1, s1, t2, s2, t_lo, t_hi, step=10):
    """axis 'h': s=v, t=u; 'v': s=u, t=v. Returns (slope, intercept, used [(t,s)], set aside n, positions n)."""
    k0 = (s2 - s1) / (t2 - t1)
    if axis == "h":
        e_s, e_t = np.array([0.0, 1.0]), np.array([1.0, 0.0])
    else:
        e_s, e_t = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    pts = []
    n_pos = 0
    for t in np.arange(t_lo, t_hi + 0.1, step):
        n_pos += 1
        s_pred = s1 + k0 * (t - t1)
        p = s_pred * e_s + t * e_t
        off = ca.ink_offset(gray, p, e_s, e_t)
        if off is None or abs(off) > 4.5:
            continue
        pts.append((t, s_pred + off))
    P = np.array(pts)
    keep = np.ones(len(P), bool)
    for _ in range(5):
        k, c = np.polyfit(P[keep, 0], P[keep, 1], 1)
        r = P[:, 1] - (c + k * P[:, 0])
        mad = 1.4826 * np.median(np.abs(r[keep] - np.median(r[keep])))
        new = np.abs(r) <= max(1.0, 3 * mad)
        if (new == keep).all():
            break
        keep = new
    k, c = np.polyfit(P[keep, 0], P[keep, 1], 1)
    r = P[keep, 1] - (c + k * P[keep, 0])
    return float(k), float(c), P[keep].tolist(), int((~keep).sum()), n_pos, float(np.sqrt(np.mean(r ** 2)))


hl, vl = [], []
for val, (a, b) in H.items():
    k, c, used, aside, npos, rms = measure("h", 725, a, 1925, b, 600, 2090)
    hl.append((val, k, c, f"measured at {len(used)}/{npos} positions (helper, ink_offset), {aside} set aside, rms {rms:.2f} px", used))
for val, (a, b) in V.items():
    k, c, used, aside, npos, rms = measure("v", 1225, a, 3675, b, 1150, 3730)
    vl.append((val, k, c, f"measured at {len(used)}/{npos} positions (helper, ink_offset), {aside} set aside, rms {rms:.2f} px", used))

anchors = []
for h in hl:
    for v in vl:
        u, vv = ca.intersect(h, v)
        anchors.append({"x_value": h[0], "y_value": v[0], "u": round(u, 1), "v": round(vv, 1),
                        "x_source": h[3], "y_source": v[3]})
ax, ay, rmsx, rmsy, maxx, maxy = ca.fit_affine(anchors, "log10", "linear")
out.mkdir(parents=True, exist_ok=True)
with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader(); w.writerows(anchors)
cal = {
    "image": img, "box": [565, 1100, 2125, 3755], "bands": None, "dark": None, "min_frac": None, "snap": None,
    "method": "Claude reader helper out/FA-18/helpers/measure_lines.py: each labelled line measured with calibrate_axes.ink_offset every 10 px along it, robust straight-line fit; anchors are intersections of the fitted lines",
    "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the grid intersections) (D-027: x and y here are the plotting coordinates T(value) of the axes' transforms)",
    "ax": ax, "ay": ay,
    "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
    "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
    "n_anchors": len(anchors),
    "vertical_lines": [{"y_value": l[0], "slope_du_dv": l[1], "u_at_v0": l[2], "source": l[3], "samples": [[round(a, 1), round(b, 2)] for a, b in l[4]]} for l in vl],
    "horizontal_lines": [{"x_value": l[0], "slope_dv_du": l[1], "v_at_u0": l[2], "source": l[3], "samples": [[round(a, 1), round(b, 2)] for a, b in l[4]]} for l in hl],
    "x_direction": "up", "y_direction": "left", "x_transform": "log10",
}
(out / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(f"{len(anchors)} anchors; x (log10 mm): {cal['x_per_px']:.6f} per px, rms {rmsx:.5f}, max {maxx:.5f}; "
      f"y: {cal['y_per_px']:.4f} per px, rms {rmsy:.3f}, max {maxy:.3f}")
for l in vl:
    print(f"  vertical   y={l[0]:>6g}  u = {l[2]:.2f} + {l[1]:+.5f} v   ({l[3]})")
for l in hl:
    print(f"  horizontal x={l[0]:>6g}  v = {l[2]:.2f} + {l[1]:+.5f} u   ({l[3]})")
