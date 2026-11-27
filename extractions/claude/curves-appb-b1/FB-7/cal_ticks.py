"""Tick calibration of Fig. B-7 (FB-7), p0113.png, written in the calibration.json layout of
tools/calibrate_axes.py (anchors kept inside calibration.json, one axis per anchor).

The plot has a frame with inward ticks on the left (y) and bottom (x) sides only, no grid lines.
Knots:
  x = 0  : left frame line (label "0" printed at the lower-left corner), measured along its length
  x = 2..14 : bottom ticks, one anchor each on the tick's centre line
  x = 16 : right frame line (label "16" printed under it), measured along its length
  y = 0  : bottom frame line (label "0" printed at its left end)
  y = 1..10 : left ticks, one anchor each on the tick's centre line
  y = 11 : top frame line (label "11" printed at its left end)
The ticks point into the plot only (none outside the frame), so a tick anchor is placed at the middle
of the stretch of the tick that was measured (about 17 px inside the frame's centre line), not where the
tick meets the frame: the ink check of tools/calibrate_axes.py reads a lone tick on stubs 6 to 14 px
either side of its anchor, and with the anchor on the frame the outer stubs fall below the frame, on the
tops of the printed labels and on specks (x = 14 was then rejected as 2.24 px from the ink and x = 10 and
12 had 3.5 to 4 px errors from that stray ink). The anchor's position along the tick does not change the
line's value position. The y = 1, 2, 3 ticks are crossed by a symbol or a curve near the frame, so they
are measured on the clean columns only.
Each frame line is fitted with its own tilt from its ink (rows or columns where the frame's run is
isolated and of normal width), with outliers above 1.5 px set aside.

usage: python cal_ticks.py <image> <out_dir>
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def runs(idx):
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


def robust_fit(t, p, tol=1.5):
    t, p = np.asarray(t, float), np.asarray(p, float)
    c = np.polyfit(t, p, 1)
    keep = np.abs(p - np.polyval(c, t)) <= tol
    c = np.polyfit(t[keep], p[keep], 1)
    res = p[keep] - np.polyval(c, t[keep])
    return c, keep, float(np.sqrt(np.mean(res ** 2))), int(keep.sum()), len(t)


def frame_vertical(g, v_range, guess, maxw=10):
    """Centre u of a vertical frame line per row, where its run is isolated and of normal width."""
    ts, ps = [], []
    for v in range(*v_range):
        c0 = int(round(guess(v)))
        row = g[v, c0 - 25:c0 + 26]
        rr = [(s + c0 - 25, e + c0 - 25) for s, e in runs(np.where(row)[0].tolist())]
        near = [r for r in rr if r[0] - 4 <= guess(v) <= r[1] + 4]
        if len(near) != 1 or len(rr) != 1:
            continue
        s, e = near[0]
        if e - s + 1 > maxw:
            continue
        ts.append(v)
        ps.append((s + e) / 2)
    return ts, ps


def frame_horizontal(g, u_range, guess, maxw=13):
    ts, ps = [], []
    for u in range(*u_range):
        c0 = int(round(guess(u)))
        col = g[c0 - 25:c0 + 26, u]
        rr = [(s + c0 - 25, e + c0 - 25) for s, e in runs(np.where(col)[0].tolist())]
        near = [r for r in rr if r[0] - 4 <= guess(u) <= r[1] + 4]
        if len(near) != 1 or len(rr) != 1:
            continue
        s, e = near[0]
        if e - s + 1 > maxw:
            continue
        ts.append(u)
        ps.append((s + e) / 2)
    return ts, ps


def main():
    image, out = sys.argv[1], Path(sys.argv[2])
    g = np.asarray(Image.open(image).convert("L")) < 128
    box = [470, 830, 2775, 3960]

    # frame lines
    lt, lp = frame_vertical(g, (870, 3925, 5), lambda v: 490.5 + (v - 950) * 0.0054)
    rt, rp = frame_vertical(g, (870, 3925, 5), lambda v: 2737.5 + (v - 860) * 0.0052)
    bt, bp = frame_horizontal(g, (520, 2740, 5), lambda u: 3936 - (u - 520) * 0.0014)
    tt, tp = frame_horizontal(g, (500, 2730, 5), lambda u: 852.0)
    fits = {}
    for name, t, p in (("left", lt, lp), ("right", rt, rp), ("bottom", bt, bp), ("top", tt, tp)):
        c, keep, rms, nk, n = robust_fit(t, p)
        fits[name] = c
        print(f"frame {name:6s}: pos = {c[1]:.2f} + {c[0]:+.5f} t   rms {rms:.2f} px, {nk}/{n} samples kept")
    L = lambda v: np.polyval(fits["left"], v)
    R = lambda v: np.polyval(fits["right"], v)
    B = lambda u: np.polyval(fits["bottom"], u)
    T = lambda u: np.polyval(fits["top"], u)

    # x ticks (bottom, pointing up into the plot): centre u per row above the frame
    xt = {}
    for val, u0 in ((2, 793), (4, 1071), (6, 1351), (8, 1632), (10, 1911), (12, 2192), (14, 2474)):
        vb = B(u0)
        cs, vs = [], []
        for v in range(int(vb) - 26, int(vb) - 7):
            idx = np.where(g[v, u0 - 9:u0 + 10])[0] + u0 - 9
            rr = runs(idx.tolist())
            if len(rr) == 1 and 2 <= rr[0][1] - rr[0][0] + 1 <= 8:
                cs.append((rr[0][0] + rr[0][1]) / 2)
                vs.append(v)
        uc = float(np.mean(cs))
        vm = float(np.mean(vs))   # anchor at the middle of the tick's measured stretch (see module docstring)
        xt[val] = (uc, vm, len(cs), float(np.std(cs)), float(B(uc)))
        print(f"x tick {val:>2}: u = {uc:.2f} (rows {len(cs)}, sd {np.std(cs):.2f}), anchor v = {vm:.1f}, meets frame at v = {B(uc):.2f}")
    # y ticks (left, pointing right into the plot): centre v per column right of the frame
    yt = {}
    for val, v0 in ((10, 1138.5), (9, 1419.5), (8, 1701.5), (7, 1978.5), (6, 2260), (5, 2539),
                    (4, 2819.5), (3, 3101), (2, 3377.5), (1, 3658.5)):
        ul = L(v0)
        cs, us = [], []
        for u in range(int(ul) + 7, int(ul) + 24):
            idx = np.where(g[int(v0) - 9:int(v0) + 10, u])[0] + int(v0) - 9
            rr = runs(idx.tolist())
            if len(rr) == 1 and 2 <= rr[0][1] - rr[0][0] + 1 <= 8:
                cs.append((rr[0][0] + rr[0][1]) / 2)
                us.append(u)
        vc = float(np.mean(cs))
        um = float(np.mean(us))   # anchor at the middle of the tick's measured stretch (see module docstring)
        yt[val] = (um, vc, len(cs), float(np.std(cs)), float(L(vc)))
        print(f"y tick {val:>2}: v = {vc:.2f} (cols {len(cs)}, sd {np.std(cs):.2f}), anchor u = {um:.1f}, meets frame at u = {L(vc):.2f}")

    anchors = []
    # frame anchors: the fitted frame line at the other axis' tick levels and at the corners
    v_levels = [T(L(852)) * 0 + 852.0] + [yt[k][1] for k in sorted(yt, reverse=True)] + [float(B(507))]
    for v in v_levels:
        anchors.append({"x_value": 0.0, "y_value": None, "u": round(float(L(v)), 2), "v": round(v, 2),
                        "x_source": "left frame line (label 0), fitted on its ink", "y_source": ""})
        anchors.append({"x_value": 16.0, "y_value": None, "u": round(float(R(v)), 2), "v": round(v, 2),
                        "x_source": "right frame line (label 16), fitted on its ink", "y_source": ""})
    u_levels = [507.0] + [xt[k][0] for k in sorted(xt)] + [2752.0]
    for u in u_levels:
        anchors.append({"x_value": None, "y_value": 0.0, "u": round(u, 2), "v": round(float(B(u)), 2),
                        "x_source": "", "y_source": "bottom frame line (label 0), fitted on its ink"})
        anchors.append({"x_value": None, "y_value": 11.0, "u": round(u, 2), "v": round(float(T(u)), 2),
                        "x_source": "", "y_source": "top frame line (label 11), fitted on its ink"})
    for val in sorted(xt):
        u, v, n, sd, _ = xt[val]
        anchors.append({"x_value": float(val), "y_value": None, "u": round(u, 2), "v": round(v, 2),
                        "x_source": f"tick measured ({n} rows, sd {sd:.2f} px)", "y_source": ""})
    for val in sorted(yt):
        u, v, n, sd, _ = yt[val]
        anchors.append({"x_value": None, "y_value": float(val), "u": round(u, 2), "v": round(v, 2),
                        "x_source": "", "y_source": f"tick measured ({n} columns, sd {sd:.2f} px)"})

    def fit(col):
        A = [a for a in anchors if a[col] is not None]
        U = np.array([[a["u"], a["v"], 1.0] for a in A])
        X = np.array([a[col] for a in A])
        c, *_ = np.linalg.lstsq(U, X, rcond=None)
        r = X - U @ c
        return c.tolist(), float(np.sqrt(np.mean(r ** 2))), float(np.abs(r).max()), A, r

    ax, rmsx, maxx, AX, rx = fit("x_value")
    ay, rmsy, maxy, AY, ry = fit("y_value")
    print(f"affine x: rms {rmsx:.4f} psi, max {maxx:.4f} psi (span 16, {100 * maxx / 16:.3f}%)")
    print(f"affine y: rms {rmsy:.4f} ksi, max {maxy:.4f} ksi (span 11, {100 * maxy / 11:.3f}%)")
    for a, r in zip(AX, rx):
        a["x_residual"] = round(float(r), 4)
    for a, r in zip(AY, ry):
        a["y_residual"] = round(float(r), 4)

    cal = {
        "image": image, "box": box,
        "method": "ticks and labelled frame lines measured by out/FB-7/cal_ticks.py (no grid lines on this plot)",
        "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the tick and frame anchors, each axis on its own anchors)",
        "ax": ax, "ay": ay,
        "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
        "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
        "n_anchors": len(anchors),
        "vertical_lines": (
            [{"x_value": 0.0, "slope_du_dv": fits["left"][0], "u_at_v0": fits["left"][1], "source": "frame, detected"}]
            + [{"x_value": float(k), "slope_du_dv": None, "u_at_v0": xt[k][0], "source": "tick, detected", "samples": []} for k in sorted(xt)]
            + [{"x_value": 16.0, "slope_du_dv": fits["right"][0], "u_at_v0": fits["right"][1], "source": "frame, detected"}]),
        "horizontal_lines": (
            [{"y_value": 11.0, "slope_dv_du": fits["top"][0], "v_at_u0": fits["top"][1], "source": "frame, detected"}]
            + [{"y_value": float(k), "slope_dv_du": None, "v_at_u0": yt[k][1], "source": "tick, detected", "samples": []} for k in sorted(yt, reverse=True)]
            + [{"y_value": 0.0, "slope_dv_du": fits["bottom"][0], "v_at_u0": fits["bottom"][1], "source": "frame, detected"}]),
        "anchors": anchors,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
    print(f"wrote {out / 'calibration.json'}: {len(anchors)} anchors")


if __name__ == "__main__":
    main()
