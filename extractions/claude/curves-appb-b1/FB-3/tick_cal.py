"""Tick calibration of Figure B-3 (FB-3, p0109.png): a frame with ticks and printed labels, no grid.

Measures on the page, independently of any other reading:
  1. the four frame lines, each fitted with its own tilt to the centre of its ink core at many
     positions along it (rows or columns near a tick or a curve are skipped, outliers beyond 3 MAD set
     aside);
  2. every interior tick: the centre of the tick's ink at every row (x ticks, which rise from the
     bottom frame) or column (y ticks, which run right from the left frame), fitted with the tick's
     own tilt, and the anchor where that fitted tick line meets the fitted frame centreline.
The frame lines are knots only where a printed label sits on them (x = 0 left, x = 14 right, y = 7
bottom, y = 18 top; checked by eye, see calibration-eye-checks.csv). Anchors are written to
anchors.csv in the layout of tools/calibrate_axes.py (a row may anchor one axis only); the affine
map is fitted per axis by least squares, as a diagnostic, and written to calibration.json in the
layout of `calibrate_axes.py detect`, with `box`.

Usage: python tick_cal.py <image> <out_dir>
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

IMG, OUT = sys.argv[1], Path(sys.argv[2])
g = np.asarray(Image.open(IMG).convert("L"), dtype=float)
BOX = [500, 780, 2580, 3980]
X_VALUES = [0, 2, 4, 6, 8, 10, 12, 14]
Y_VALUES = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]


def core(prof):
    """centre (index units) and width of the dark core around the darkest point of a profile of
    darkness (0 white); None when there is no ink."""
    if prof.max() < 60:
        return None
    c = prof >= 0.5 * prof.max()
    i = int(np.argmax(prof))
    lo = hi = i
    while lo > 0 and c[lo - 1]:
        lo -= 1
    while hi < len(c) - 1 and c[hi + 1]:
        hi += 1
    w = prof[lo:hi + 1]
    return float(np.sum(np.arange(lo, hi + 1) * w) / w.sum()), hi - lo + 1


def robust_fit(t, s):
    t, s = np.asarray(t, float), np.asarray(s, float)
    k, s0 = np.polyfit(t, s, 1)
    r = s - (s0 + k * t)
    mad = 1.4826 * np.median(np.abs(r - np.median(r)))
    keep = np.abs(r) <= max(1.0, 3 * mad)
    k, s0 = np.polyfit(t[keep], s[keep], 1)
    r = s[keep] - (s0 + k * t[keep])
    return float(k), float(s0), keep, float(np.sqrt(np.mean(r ** 2))), float(np.abs(r).max())


def vline_center(v, u_lo, u_hi, half=3):
    prof = 255 - g[v - half:v + half + 1, u_lo:u_hi].mean(axis=0)
    r = core(prof)
    return None if r is None else (u_lo + r[0], r[1])


def hline_center(u, v_lo, v_hi, half=3):
    prof = 255 - g[v_lo:v_hi, u - half:u + half + 1].mean(axis=1)
    r = core(prof)
    return None if r is None else (v_lo + r[0], r[1])


def frame(kind, positions, lo, hi, skip):
    pts = []
    for p in positions:
        if any(abs(p - q) <= 15 for q in skip):
            continue
        r = (vline_center if kind == "v" else hline_center)(int(p), lo, hi)
        if r is not None and 3 <= r[1] <= 14:
            pts.append((float(p), r[0], r[1]))
    t = [q[0] for q in pts]
    s = [q[1] for q in pts]
    k, s0, keep, rms, mx = robust_fit(t, s)
    return {"k": k, "s0": s0, "rms": rms, "max": mx,
            "pts": [(a, b) for (a, b, _), kp in zip(pts, keep) if kp],
            "dropped": [(a, round(b, 1)) for (a, b, _), kp in zip(pts, keep) if not kp],
            "width": float(np.median([q[2] for q in pts]))}


# ---- first pass: frames without skips, to predict the ticks
left0 = frame("v", range(870, 3900, 20), 530, 580, [])
bot0 = frame("h", range(580, 2500, 20), 3895, 3945, [])
right0 = frame("v", range(870, 3900, 20), 2495, 2540, [])
top0 = frame("h", range(580, 2500, 20), 810, 860, [])
fl = lambda f, t: f["s0"] + f["k"] * t


def nearest_run(dark, pred, half):
    """the dark run (centre, width) nearest `pred` within `half` px in a 1-D darkness profile; specks
    and label strokes farther from the predicted tick are ignored."""
    lo = int(pred) - half
    idx = np.where(dark[lo:int(pred) + half + 1] >= 128)[0]
    if len(idx) == 0:
        return None
    runs, s = [], idx[0]
    for a, b in zip(idx, idx[1:]):
        if b != a + 1:
            runs.append((s, a)); s = b
    runs.append((s, idx[-1]))
    a, b = min(runs, key=lambda r: abs(lo + (r[0] + r[1]) / 2 - pred))
    return lo + (a + b) / 2, b - a + 1


def xtick(pred_u):
    """x tick rising from the bottom frame near pred_u: centre u per row above the frame."""
    vb = fl(bot0, pred_u)
    rows = []
    for v in range(int(vb - 40), int(vb - 7)):
        r = nearest_run(255 - g[v, :], pred_u, 25)
        if r is not None and r[1] <= 8:
            rows.append((v, r[0], r[1]))
    return rows


def ytick(pred_v):
    ul = fl(left0, pred_v)
    cols = []
    for u in range(int(ul + 7), int(ul + 45)):
        r = nearest_run(255 - g[:, u], pred_v, 25)
        if r is not None and r[1] <= 8:
            cols.append((u, r[0], r[1]))
    return cols


def corner(fv, fh):
    """intersection of a vertical frame u = s0 + k v and a horizontal one v = s0 + k u"""
    u = (fv["s0"] + fv["k"] * fh["s0"]) / (1 - fv["k"] * fh["k"])
    return u, fh["s0"] + fh["k"] * u


bl, br, tl, tr = corner(left0, bot0), corner(right0, bot0), corner(left0, top0), corner(right0, top0)
xticks, yticks = {}, {}
for i, xv in enumerate(X_VALUES[1:-1], 1):
    pu = bl[0] + (br[0] - bl[0]) * i / 7
    rows = xtick(pu)
    # keep the contiguous run of rows nearest the frame (the tick), rows from the bottom up
    vs = np.array([q[0] for q in rows]); us = np.array([q[1] for q in rows])
    k, s0, keep, rms, mx = robust_fit(vs, us)
    vb = fl(bot0, s0 + k * fl(bot0, s0))
    # tick line u = s0 + k v meets the frame v = b0 + bk u
    u_a = (s0 + k * bot0["s0"]) / (1 - k * bot0["k"])
    v_a = fl(bot0, u_a)
    xticks[xv] = {"u": u_a, "v": v_a, "k": k, "s0": s0, "rms": rms, "max": mx, "n": int(keep.sum()),
                  "v_top": float(vs[keep].min()), "width": float(np.median([q[2] for q in rows])), "pred_u": pu}
for i, yv in enumerate(Y_VALUES[1:-1], 1):
    pv = bl[1] + (tl[1] - bl[1]) * i / 11
    cols = ytick(pv)
    us = np.array([q[0] for q in cols]); vs = np.array([q[1] for q in cols])
    k, s0, keep, rms, mx = robust_fit(us, vs)
    # tick line v = s0 + k u meets the left frame u = l0 + lk v
    u_a = (left0["s0"] + left0["k"] * s0) / (1 - left0["k"] * k)
    v_a = s0 + k * u_a
    yticks[yv] = {"u": u_a, "v": v_a, "k": k, "s0": s0, "rms": rms, "max": mx, "n": int(keep.sum()),
                  "u_end": float(us[keep].max()), "width": float(np.median([q[2] for q in cols])), "pred_v": pv}

# ---- second pass: frames with the ticks (and their junction blobs) skipped
left = frame("v", range(870, 3900, 20), 530, 580, [t["v"] for t in yticks.values()])
bot = frame("h", range(580, 2500, 20), 3895, 3945, [t["u"] for t in xticks.values()])
right = frame("v", range(870, 3900, 20), 2495, 2540, [])
top = frame("h", range(580, 2500, 20), 810, 860, [])

for name, f in (("left (x=0)", left), ("right (x=14)", right), ("bottom (y=7)", bot), ("top (y=18)", top)):
    print(f"frame {name:13s}: s = {f['s0']:.2f} + {f['k']:+.5f} t  rms {f['rms']:.2f} max {f['max']:.2f} px, "
          f"{len(f['pts'])} pts, width {f['width']:.0f}, dropped {f['dropped']}")
for xv, t in xticks.items():
    print(f"x tick {xv:>3}: anchor ({t['u']:.1f}, {t['v']:.1f}) pred u {t['pred_u']:.1f}  own tilt du/dv {t['k']:+.4f} "
          f"rms {t['rms']:.2f} max {t['max']:.2f}, {t['n']} rows, top v {t['v_top']:.0f}, width {t['width']:.0f}")
for yv, t in yticks.items():
    print(f"y tick {yv:>3}: anchor ({t['u']:.1f}, {t['v']:.1f}) pred v {t['pred_v']:.1f}  own tilt dv/du {t['k']:+.4f} "
          f"rms {t['rms']:.2f} max {t['max']:.2f}, {t['n']} cols, end u {t['u_end']:.0f}, width {t['width']:.0f}")

# ---- anchors
anchors = []
for (vv, uu) in left["pts"]:
    anchors.append({"x_value": 0, "y_value": "", "u": round(uu, 2), "v": round(vv, 2), "x_source": "frame left, measured ink centre (label 0)", "y_source": ""})
for (vv, uu) in right["pts"]:
    anchors.append({"x_value": 14, "y_value": "", "u": round(uu, 2), "v": round(vv, 2), "x_source": "frame right, measured ink centre (label 14)", "y_source": ""})
for (uu, vv) in bot["pts"]:
    anchors.append({"x_value": "", "y_value": 7, "u": round(uu, 2), "v": round(vv, 2), "x_source": "", "y_source": "frame bottom, measured ink centre (label 7)"})
for (uu, vv) in top["pts"]:
    anchors.append({"x_value": "", "y_value": 18, "u": round(uu, 2), "v": round(vv, 2), "x_source": "", "y_source": "frame top, measured ink centre (label 18)"})
for xv, t in xticks.items():
    anchors.append({"x_value": xv, "y_value": "", "u": round(t["u"], 2), "v": round(t["v"], 2),
                    "x_source": f"tick measured in {t['n']} rows, meets bottom frame centreline", "y_source": ""})
for yv, t in yticks.items():
    src = f"tick measured in {t['n']} columns, meets left frame centreline"
    if yv == 8:
        src += " (printed label reads 3; value from tick spacing)"
    anchors.append({"x_value": "", "y_value": yv, "u": round(t["u"], 2), "v": round(t["v"], 2), "x_source": "", "y_source": src})


def fit(col):
    A = [a for a in anchors if a[col] != ""]
    U = np.array([[a["u"], a["v"], 1.0] for a in A])
    Z = np.array([float(a[col]) for a in A])
    c, *_ = np.linalg.lstsq(U, Z, rcond=None)
    r = Z - U @ c
    return c.tolist(), float(np.sqrt(np.mean(r ** 2))), float(np.abs(r).max()), r, A


ax, rmsx, maxx, rx, Ax = fit("x_value")
ay, rmsy, maxy, ry, Ay = fit("y_value")
print(f"affine x: {ax}  rms {rmsx:.4f} max {maxx:.4f} psi ({rmsx / 14 * 100:.3f} % / {maxx / 14 * 100:.3f} % of span)")
print(f"affine y: {ay}  rms {rmsy:.4f} max {maxy:.4f} ksi ({rmsy / 11 * 100:.3f} % / {maxy / 11 * 100:.3f} % of span)")
# residual per value (mean over its anchors)
for col, A, r in (("x_value", Ax, rx), ("y_value", Ay, ry)):
    byv = {}
    for a, rr in zip(A, r):
        byv.setdefault(float(a[col]), []).append(rr)
    print(col, "  ".join(f"{k:g}:{np.mean(v):+.4f}" for k, v in sorted(byv.items())))

OUT.mkdir(parents=True, exist_ok=True)
with (OUT / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader()
    w.writerows(anchors)

line = lambda f_, val, key: {key: val, "slope": f_["k"], "intercept": f_["s0"], "rms_px": f_["rms"], "max_px": f_["max"],
                             "n_samples": len(f_["pts"]), "source": "frame, measured"}
cal = {
    "image": IMG, "box": BOX, "method": "ticks on a frame without grid lines (reader's helper tick_cal.py); frames are knots only where a printed label sits on them",
    "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the tick and frame anchors, per axis)",
    "ax": ax, "ay": ay,
    "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
    "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
    "n_anchors": len(anchors),
    "vertical_lines": [
        {"x_value": 0, "slope_du_dv": left["k"], "u_at_v0": left["s0"], "source": f"frame left, measured at {len(left['pts'])} rows, rms {left['rms']:.2f} px"},
        *[{"x_value": xv, "slope_du_dv": t["k"], "u_at_v0": t["s0"], "source": f"tick, measured in {t['n']} rows (own tilt; anchor where it meets the bottom frame), rms {t['rms']:.2f} px",
           "anchor": [round(t["u"], 2), round(t["v"], 2)]} for xv, t in xticks.items()],
        {"x_value": 14, "slope_du_dv": right["k"], "u_at_v0": right["s0"], "source": f"frame right, measured at {len(right['pts'])} rows, rms {right['rms']:.2f} px"},
    ],
    "horizontal_lines": [
        {"y_value": 18, "slope_dv_du": top["k"], "v_at_u0": top["s0"], "source": f"frame top, measured at {len(top['pts'])} columns, rms {top['rms']:.2f} px"},
        *[{"y_value": yv, "slope_dv_du": t["k"], "v_at_u0": t["s0"], "source": f"tick, measured in {t['n']} columns (own tilt; anchor where it meets the left frame), rms {t['rms']:.2f} px",
           "anchor": [round(t["u"], 2), round(t["v"], 2)]} for yv, t in sorted(yticks.items(), reverse=True)],
        {"y_value": 7, "slope_dv_du": bot["k"], "v_at_u0": bot["s0"], "source": f"frame bottom, measured at {len(bot['pts'])} columns, rms {bot['rms']:.2f} px"},
    ],
}
(OUT / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print("wrote", OUT / "anchors.csv", "and", OUT / "calibration.json", len(anchors), "anchors")
