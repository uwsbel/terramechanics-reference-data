"""Tick calibration of FB-5 (p0111.png), written for this reading (the plot has a frame with ticks and
no grid lines). Writes <out>/anchors.csv and <out>/calibration.json in the layout of
tools/calibrate_axes.py detect (anchors also kept inside calibration.json, with `box`).

Measured on the page, nothing predicted:
  1. the four frame lines, each fitted to the centre of its ink every 5 px (frame.fit_line);
  2. each tick: the centre of its ink across it, in rows (x ticks) or columns (y ticks) from 8 px
     off the frame line's centre to its far end, fitted as a straight line; its anchor is where that
     line meets the frame line's centre line.
Which lines carry which value (checked by eye, see calibration-eye-checks.csv):
  x = 0 the left frame (label "0" under it), x = 2, 4, 6, 8, 10 the ticks on the bottom frame,
  x = 12 the right frame (label "12" printed about 32 px left of it; the tick spacing confirms it);
  y = 5 the bottom frame (label "5" beside it), y = 10 to 35 the ticks on the left frame,
  y = 40 the top frame (label "40" beside it). There are no ticks on the top and right frames.
Anchors: the corners and the tick anchors carry the values of both lines through them; the right and
top frames also get one-axis anchors on their fitted lines (every ~1/6 of their length), so each frame
line keeps its own tilt.
Usage: python calibrate_ticks.py <image> <out_dir>"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from frame import fit_line, runs  # noqa: E402

img, out = sys.argv[1], Path(sys.argv[2])
g = np.asarray(Image.open(img).convert("L"))
dark = g < 128
TL, TR, BR, BL = (652, 880), (2783, 852), (2834, 3966), (700, 3995)
F = {
    "bottom": fit_line(dark, (BL[0] + 40, BL[1]), (BR[0] - 40, BR[1]), True),
    "top": fit_line(dark, (TL[0] + 40, TL[1]), (TR[0] - 40, TR[1]), True),
    "left": fit_line(dark, (TL[0], TL[1] + 40), (BL[0], BL[1] - 40), False),
    "right": fit_line(dark, (TR[0], TR[1] + 40), (BR[0], BR[1] - 40), False),
}


def hv(h, vline):
    """Intersection of horizontal v = ch + kh u and vertical u = cv + kv v."""
    u = (vline["intercept"] + vline["slope"] * h["intercept"]) / (1 - vline["slope"] * h["slope"])
    return u, h["intercept"] + h["slope"] * u


def tick(frame, guess, dists, horizontal_frame):
    """A tick on `frame` near position `guess` along it. For a horizontal frame (x tick) sample rows at
    distances `dists` (negative: above the frame centre) and find the tick's centre u; returns the
    fitted tick line u = c + k v, its samples and the anchor on the frame centre line."""
    f = F[frame]
    pts = []
    for d in dists:
        if horizontal_frame:
            v = int(round(f["intercept"] + f["slope"] * guess + d))
            lo = int(guess) - 15
            rr = [r for r in runs(dark[v, lo:lo + 30], lo) if r[1] <= 12]
            if rr:
                c, w = min(rr, key=lambda r: abs(r[0] - guess))
                pts.append((v, c, w))
        else:
            u = int(round(f["intercept"] + f["slope"] * guess + d))
            lo = int(guess) - 15
            rr = [r for r in runs(dark[lo:lo + 30, u], lo) if r[1] <= 12]
            if rr:
                c, w = min(rr, key=lambda r: abs(r[0] - guess))
                pts.append((u, c, w))
    P = np.array(pts, dtype=float)
    k, c = np.polyfit(P[:, 0], P[:, 1], 1)
    res = P[:, 1] - (c + k * P[:, 0])
    line = {"slope": float(k), "intercept": float(c)}
    if horizontal_frame:   # tick u = c + k v, frame v = ...
        u, v = hv(f, line)
    else:                  # tick v = c + k u (a horizontal-ish line), frame u = ...
        u, v = hv(line, f)
    return {"u": u, "v": v, "tilt": float(k), "rms": float(np.sqrt(np.mean(res ** 2))), "n": len(P),
            "width": float(np.median(P[:, 2])), "extent": [float(P[:, 0].min()), float(P[:, 0].max())]}


def tick_extent(frame, guess, horizontal_frame, maxd=60):
    """How far the tick's ink reaches from the frame centre (first distance with no ink near guess)."""
    f = F[frame]
    last = None
    sign = -1 if horizontal_frame else 1
    for d in range(5, maxd):
        dd = sign * d
        if horizontal_frame:
            v = int(round(f["intercept"] + f["slope"] * guess + dd))
            seg = dark[v, int(guess) - 6:int(guess) + 7]
        else:
            u = int(round(f["intercept"] + f["slope"] * guess + dd))
            seg = dark[int(guess) - 6:int(guess) + 7, u]
        if seg.any():
            last = d
        elif last is not None and d - last > 2:
            break
    return last


xt = {2: 1056, 4: 1410.5, 6: 1768.5, 8: 2125.5, 10: 2481.5}
yt = {35: 1328, 30: 1776.5, 25: 2221, 20: 2664.5, 15: 3109.5, 10: 3553}
ticks_x, ticks_y = {}, {}
for val, gu in xt.items():
    L = tick_extent("bottom", gu, True)
    ticks_x[val] = tick("bottom", gu, [-d for d in range(8, L - 1)], True)
    ticks_x[val]["length_from_centre"] = L
for val, gv in yt.items():
    L = tick_extent("left", gv, False)
    ticks_y[val] = tick("left", gv, list(range(7, L - 1)), False)
    ticks_y[val]["length_from_centre"] = L

anchors = []


def add(xv, yv, u, v, xs, ys):
    anchors.append({"x_value": "" if xv is None else xv, "y_value": "" if yv is None else yv,
                    "u": round(u, 2), "v": round(v, 2), "x_source": xs, "y_source": ys})


fsrc = lambda n: f"frame line ({n}), fitted to its ink every 5 px, rms {F[n]['rms']:.2f} px"
tsrc = lambda t: f"tick measured on its ink ({t['n']} rows/cols, tilt {t['tilt']:+.4f}, rms {t['rms']:.2f} px)"
# corners
for (h, vname, xv, yv) in (("bottom", "left", 0, 5), ("bottom", "right", 12, 5), ("top", "left", 0, 40), ("top", "right", 12, 40)):
    u, v = hv(F[h], F[vname])
    add(xv, yv, u, v, fsrc(vname), fsrc(h))
# x ticks on the bottom frame (y = 5)
for val, t in ticks_x.items():
    add(val, 5, t["u"], t["v"], tsrc(t), fsrc("bottom"))
# y ticks on the left frame (x = 0)
for val, t in ticks_y.items():
    add(0, val, t["u"], t["v"], fsrc("left"), tsrc(t))
# one-axis anchors along the right frame (x = 12) and the top frame (y = 40), between the corners
uTR, vTR = hv(F["top"], F["right"])
uBR, vBR = hv(F["bottom"], F["right"])
uTL, vTL = hv(F["top"], F["left"])
for f in np.linspace(0, 1, 7)[1:-1]:
    v = vTR + f * (vBR - vTR)
    add(12, None, F["right"]["intercept"] + F["right"]["slope"] * v, v, fsrc("right"), "")
    u = uTL + f * (uTR - uTL)
    add(None, 40, u, F["top"]["intercept"] + F["top"]["slope"] * u, "", fsrc("top"))


def fit_axis(col):
    """Unconstrained affine fit of one axis on its anchors (diagnostic only, see below)."""
    A = [a for a in anchors if a[col] != ""]
    U = np.array([[a["u"], a["v"], 1.0] for a in A])
    X = np.array([float(a[col]) for a in A])
    c, *_ = np.linalg.lstsq(U, X, rcond=None)
    r = X - U @ c
    return c.tolist(), float(np.sqrt(np.mean(r ** 2))), float(np.abs(r).max()), [(a[col], round(float(rr), 4)) for a, rr in zip(A, r)]


def fit_axis_frame_tilt(col, k):
    """Affine fit whose lines of constant value have the mean tilt of the two frame lines of that
    axis: x = A (u - k v) + B with k = du/dv of the left and right frames, or y = A (v - k u) + B with
    k = dv/du of the bottom and top frames; A and B by least squares on all anchors of the axis.
    Why: the ticks sit on one side of the plot only (x on the bottom, y on the left), so an
    unconstrained fit turns the map to absorb the uneven tick spacing (y lines at dv/du -0.0154
    against -0.0145 and -0.0139 for the bottom and top frames), and tools/calibrate_axes.py gives a
    lone tick the tilt of the affine map: about 2 px of error in v at the right of the plot."""
    A_ = [a for a in anchors if a[col] != ""]
    if col == "x_value":
        q = np.array([a["u"] - k * a["v"] for a in A_])
    else:
        q = np.array([a["v"] - k * a["u"] for a in A_])
    X = np.array([float(a[col]) for a in A_])
    s, b = np.polyfit(q, X, 1)
    r = X - (s * q + b)
    c = [float(s), float(-s * k), float(b)] if col == "x_value" else [float(-s * k), float(s), float(b)]
    return c, float(np.sqrt(np.mean(r ** 2))), float(np.abs(r).max()), [(a[col], round(float(rr), 4)) for a, rr in zip(A_, r)]


ax_free, rmsx_free, maxx_free, _ = fit_axis("x_value")
ay_free, rmsy_free, maxy_free, _ = fit_axis("y_value")
kx = (F["left"]["slope"] + F["right"]["slope"]) / 2
ky = (F["bottom"]["slope"] + F["top"]["slope"]) / 2
ax, rmsx, maxx, resx = fit_axis_frame_tilt("x_value", kx)
ay, rmsy, maxy, resy = fit_axis_frame_tilt("y_value", ky)
out.mkdir(parents=True, exist_ok=True)
with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader()
    w.writerows(anchors)
cal = {
    "image": img, "box": [600, 800, 2900, 4050], "method": "ticks and frame lines measured on the ink (out/FB-5/calibrate_ticks.py); no grid lines on this plot",
    "model": ("x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine; the lines of constant x have the mean "
              "tilt of the left and right frame lines, those of constant y the mean tilt of the bottom and top frame lines; "
              "scale and offset by least squares on the anchors of each axis)"),
    "frame_tilt_x_du_dv": kx, "frame_tilt_y_dv_du": ky,
    "ax": ax, "ay": ay, "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
    "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
    "affine_unconstrained": {"ax": ax_free, "ay": ay_free, "rms_residual_x": rmsx_free, "rms_residual_y": rmsy_free,
                             "max_residual_x": maxx_free, "max_residual_y": maxy_free,
                             "x_line_tilt_du_dv": -ax_free[1] / ax_free[0], "y_line_tilt_dv_du": -ay_free[0] / ay_free[1],
                             "note": "diagnostic only: its y lines lean more than either horizontal frame line"},
    "n_anchors": len(anchors), "residuals_x": resx, "residuals_y": resy,
    "frame_lines": {k: {kk: vv for kk, vv in v.items() if kk != "samples"} for k, v in F.items()},
    "frame_line_convention": "bottom/top: v = intercept + slope*u; left/right: u = intercept + slope*v",
    "ticks_x": {str(k): v for k, v in ticks_x.items()}, "ticks_y": {str(k): v for k, v in ticks_y.items()},
    "tick_convention": "x ticks: u = c + tilt*v (tilt du/dv); y ticks: v = c + tilt*u (tilt dv/du); u, v: anchor on the frame centre line",
    "anchors": anchors,
}
(out / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(f"{len(anchors)} anchors; x {cal['x_per_px']:.5f}/px rms {rmsx:.4f} max {maxx:.4f}; y {cal['y_per_px']:.5f}/px rms {rmsy:.4f} max {maxy:.4f}")
print(f"  unconstrained affine (diagnostic): x rms {rmsx_free:.4f} max {maxx_free:.4f}; y rms {rmsy_free:.4f} max {maxy_free:.4f}; "
      f"tilts x {-ax_free[1] / ax_free[0]:+.5f} y {-ay_free[0] / ay_free[1]:+.5f}; frame tilts used x {kx:+.5f} y {ky:+.5f}")
for k, v in F.items():
    print(f"  frame {k:6s} slope {v['slope']:+.5f} intercept {v['intercept']:.2f} rms {v['rms']:.2f} width {v['width']}")
for k, t in ticks_x.items():
    print(f"  x tick {k:>3}: anchor ({t['u']:.1f}, {t['v']:.1f}) tilt {t['tilt']:+.4f} rms {t['rms']:.2f} n {t['n']} width {t['width']} reach {t['length_from_centre']}")
for k, t in ticks_y.items():
    print(f"  y tick {k:>3}: anchor ({t['u']:.1f}, {t['v']:.1f}) tilt {t['tilt']:+.4f} rms {t['rms']:.2f} n {t['n']} width {t['width']} reach {t['length_from_centre']}")
print("  residuals x:", resx)
print("  residuals y:", resy)
