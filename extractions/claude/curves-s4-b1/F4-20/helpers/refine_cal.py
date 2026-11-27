"""Refine the grid lines of a `calibrate_axes.py detect` output on the ink of the page, then write a
calibration directory in the same layout (anchors.csv, calibration.json).

Why: on Fig. 4-20 the band search of `detect` took the legend's sample line of Run No. 12 for the
450 lb grid line in one band, and the 600 and 500 lb lines failed the tool's own ink check (2.7 to
3.4 px from the ink at one end). Here every line is measured on the ink at a dense set of positions
along it (every 6 px, away from the crossings with the other grid lines), the run of dark pixels
nearest the detected line is taken in a profile across it (search half width 12 px), and a straight
line is fitted robustly: the pair of positions with the most others within 1.5 px decides the
inliers (a curve crossing or running near the line is set aside), then a least-squares fit on those.
Anchors are the intersections of the refined lines; the affine map is fitted to them with the tool's
own fit_affine. tools/ is not modified.

usage: refine_cal.py <detect_dir> <image> <out_dir>
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3] / "tools"))
import calibrate_axes as ca  # noqa: E402

STEP = 6
SEARCH = 12
ALONG = 3
CROSS_KEEP = 10


def profile_center(gray, pos_pred, t, vertical):
    """Centre of the dark run nearest pos_pred across the line at t (vertical line: across = u, along = v)."""
    offs = np.arange(-SEARCH, SEARCH + 1)
    rows = []
    for dt in range(-ALONG, ALONG + 1):
        tt = int(round(t + dt))
        ps = np.round(pos_pred + offs).astype(int)
        rows.append(gray[tt, ps] if vertical else gray[ps, tt])
    prof = np.mean(rows, axis=0)
    dark = np.clip(prof.max() - prof, 0, None)
    if dark.max() < 60:
        return None, None
    core = dark >= 0.5 * dark.max()
    runs, i = [], 0
    while i < len(core):
        if core[i]:
            j = i
            while j + 1 < len(core) and core[j + 1]:
                j += 1
            w = dark[i:j + 1]
            c = float(np.sum(offs[i:j + 1] * w) / np.sum(w))
            runs.append((c, j - i + 1, i, j))
            i = j + 1
        else:
            i += 1
    runs = [r for r in runs if r[2] > 0 and r[3] < len(core) - 1]
    if not runs:
        return None, None
    c, width, _, _ = min(runs, key=lambda r: abs(r[0]))
    return pos_pred + c, width


def robust_line(T, P):
    T, P = np.asarray(T, float), np.asarray(P, float)
    best = None
    n = len(T)
    idx = list(range(n)) if n <= 120 else list(np.linspace(0, n - 1, 120).astype(int))
    for i in idx:
        for j in idx:
            if j <= i or abs(T[j] - T[i]) < 100:
                continue
            k = (P[j] - P[i]) / (T[j] - T[i])
            inl = np.abs(P - (P[i] + k * (T - T[i]))) <= 1.5
            if best is None or inl.sum() > best.sum():
                best = inl
    s, b = np.polyfit(T[best], P[best], 1)
    res = P[best] - (b + s * T[best])
    return float(s), float(b), best, float(np.sqrt(np.mean(res ** 2)))


def main():
    det, image, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    cal = json.loads((det / "calibration.json").read_text(encoding="utf-8"))
    gray = np.asarray(Image.open(image).convert("L"), dtype=float)
    V, H = cal["vertical_lines"], cal["horizontal_lines"]
    vkey = [k for k in V[0] if k.endswith("_value")][0]
    hkey = [k for k in H[0] if k.endswith("_value")][0]
    vs_frame = sorted(l["v_at_u0"] + l["slope_dv_du"] * 1300 for l in H)
    us_frame = sorted(l["u_at_v0"] + l["slope_du_dv"] * 2400 for l in V)
    report = []
    newV, newH = [], []
    for lines, vertical, newl in ((V, True, newV), (H, False, newH)):
        for l in lines:
            if vertical:
                s0, i0 = l["slope_du_dv"], l["u_at_v0"]
                t_lo, t_hi = vs_frame[0], vs_frame[-1]
                cross = [h["v_at_u0"] + h["slope_dv_du"] * (i0 + s0 * 2400) for h in H]
            else:
                s0, i0 = l["slope_dv_du"], l["v_at_u0"]
                t_lo, t_hi = us_frame[0], us_frame[-1]
                cross = [v_["u_at_v0"] + v_["slope_du_dv"] * (i0 + s0 * 1300) for v_ in V]
            T, P, W = [], [], []
            for t in np.arange(t_lo + CROSS_KEEP, t_hi - CROSS_KEEP + 0.1, STEP):
                if min(abs(t - c) for c in cross) < CROSS_KEEP:
                    continue
                p, w = profile_center(gray, i0 + s0 * t, t, vertical)
                if p is not None:
                    T.append(float(t))
                    P.append(p)
                    W.append(w)
            s, b, inl, rms = robust_line(T, P)
            T, P, W = np.array(T), np.array(P), np.array(W)
            tin = T[inl]
            span = (tin.max() - tin.min()) / (t_hi - t_lo)
            old_lo, old_hi = i0 + s0 * t_lo, i0 + s0 * t_hi
            new_lo, new_hi = b + s * t_lo, b + s * t_hi
            val = l[vkey] if vertical else l[hkey]
            report.append({"axis_line": "vertical" if vertical else "horizontal", "value": val,
                           "n_positions": int(len(T)), "n_inliers": int(inl.sum()), "inlier_span_frac": round(float(span), 2),
                           "rms_px": round(rms, 2), "median_width_px": float(np.median(W[inl])),
                           "detect_minus_refined_px_at_ends": [round(float(old_lo - new_lo), 2), round(float(old_hi - new_hi), 2)],
                           "slope": round(s, 5), "intercept": round(b, 2)})
            samples = [[round(float(t), 1), round(float(p), 2)] for t, p in zip(T[inl], P[inl])]
            src = (f"refined on ink: {int(inl.sum())}/{len(T)} positions, rms {rms:.2f} px "
                   f"(detect: {l['source']})")
            if vertical:
                newl.append({vkey: val, "slope_du_dv": s, "u_at_v0": b, "source": src, "samples": samples[::5]})
            else:
                newl.append({hkey: val, "slope_dv_du": s, "v_at_u0": b, "source": src, "samples": samples[::5]})
    on_v = vkey[0]
    anchors = []
    for h in newH:
        hl = (h[hkey], h["slope_dv_du"], h["v_at_u0"], h["source"], None)
        for v_ in newV:
            vl = (v_[vkey], v_["slope_du_dv"], v_["u_at_v0"], v_["source"], None)
            u, vv = ca.intersect(hl, vl)
            xl, yl = (vl, hl) if on_v == "x" else (hl, vl)
            anchors.append({"x_value": xl[0], "y_value": yl[0], "u": round(u, 1), "v": round(vv, 1),
                            "x_source": xl[3], "y_source": yl[3]})
    ax, ay, rmsx, rmsy, maxx, maxy = ca.fit_affine(anchors)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
        w.writeheader()
        w.writerows(anchors)
    newcal = dict(cal)
    newcal.update({
        "ax": ax, "ay": ay,
        "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
        "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
        "n_anchors": len(anchors), "vertical_lines": newV, "horizontal_lines": newH,
        "refinement": {"helper": "out/F4-20/helpers/refine_cal.py", "from": str(det).replace("\\", "/"),
                       "step_px": STEP, "search_half_width_px": SEARCH, "lines": report},
    })
    (out / "calibration.json").write_text(json.dumps(newcal, indent=1), encoding="utf-8")
    print(f"{len(anchors)} anchors; x: {newcal['x_per_px']:.5f} per px, rms {rmsx:.4f}, max {maxx:.4f}; "
          f"y: {newcal['y_per_px']:.4f} per px, rms {rmsy:.3f}, max {maxy:.3f}")
    for r in report:
        print(f"  {r['axis_line']:10s} {r['value']:>6g}  pos = {r['intercept']:8.2f} {r['slope']:+.5f} t  "
              f"inliers {r['n_inliers']}/{r['n_positions']} span {r['inlier_span_frac']} rms {r['rms_px']} "
              f"width {r['median_width_px']}  detect-refined at ends {r['detect_minus_refined_px_at_ends']}")


if __name__ == "__main__":
    main()
