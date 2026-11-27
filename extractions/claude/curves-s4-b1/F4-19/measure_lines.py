"""Measure the grid lines of one panel on the page and write a calibration directory in the layout of
tools/calibrate_axes.py detect (anchors.csv, calibration.json).

Why a helper: on Figure 4-19 panel 1 the left frame (t = 0) is touched by the near-vertical rising
traces of all three runs from about v = 1250 down, so the tool's band detection merges frame and trace
ink and places the frame 15 to 20 px to the right; several dashed force lines (350 to 550 lb) are also
left as `predicted`. Here every line is followed from an initial guess: at every `step` px along the
line the profile across it is read (mean of 5 px along the line), and the dark run nearest the guess is
kept only when it is isolated (white on both sides within the window) and no wider than `wmax` px, so a
crossing grid line, a trace touching the line, or a dash gap gives no sample. The center is the
darkness-weighted centroid of the run. A straight line is fitted with iterative rejection of outliers
(more than max(1 px, 3 MAD)). Lines with `anchor: false` are measured and recorded but give no anchors
(their value is not certain on the page). The anchors are the intersections of the anchored lines.

Usage: python measure_lines.py <config.json>
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def measure(g, kind, guess, t0, t1, step, half, wmax, dark, maxdist=4, skip=()):
    """kind 'v': vertical line u = a + b v (t = v); kind 'h': horizontal v = a + b u (t = u)."""
    a, b = guess
    pts = []
    n = 0
    for t in np.arange(t0, t1 + 0.1, step):
        t = int(round(t))
        if any(s0 <= t <= s1 for s0, s1 in skip):
            continue   # a stretch where the line is not drawn (legend box): text there is not the line
        p = a + b * t
        lo, hi = int(np.floor(p - half)), int(np.ceil(p + half))
        if kind == "v":
            prof = g[t - 2:t + 3, lo:hi + 1].mean(axis=0)
        else:
            prof = g[lo:hi + 1, t - 2:t + 3].mean(axis=1)
        n += 1
        d = prof < dark
        if not d.any():
            continue
        # runs
        runs = []
        i = 0
        while i < len(d):
            if d[i]:
                j = i
                while j < len(d) and d[j]:
                    j += 1
                runs.append((i, j - 1))
                i = j
            else:
                i += 1
        c = p - lo
        best = min(runs, key=lambda r: 0 if r[0] <= c <= r[1] else min(abs(r[0] - c), abs(r[1] - c)))
        dist = 0 if best[0] <= c <= best[1] else min(abs(best[0] - c), abs(best[1] - c))
        if dist > maxdist:
            continue
        if best[0] == 0 or best[1] == len(d) - 1:
            continue  # not isolated: merged with other ink at the window edge
        w = best[1] - best[0] + 1
        if w > wmax:
            continue
        r0, r1 = max(0, best[0] - 1), min(len(d) - 1, best[1] + 1)
        wt = np.clip(255.0 - prof[r0:r1 + 1], 0, None)
        pos = lo + float(np.sum(np.arange(r0, r1 + 1) * wt) / np.sum(wt))
        pts.append((float(t), pos))
    if len(pts) < 3:
        return None, pts, n
    P = np.array(pts)
    keep = np.ones(len(P), bool)
    for _ in range(10):
        bb, aa = np.polyfit(P[keep, 0], P[keep, 1], 1)
        res = P[:, 1] - (aa + bb * P[:, 0])
        mad = 1.4826 * np.median(np.abs(res[keep] - np.median(res[keep])))
        new = np.abs(res) <= max(1.0, 3 * mad)
        if (new == keep).all():
            break
        keep = new
    bb, aa = np.polyfit(P[keep, 0], P[keep, 1], 1)
    res = P[keep, 1] - (aa + bb * P[keep, 0])
    fit = {"intercept": float(aa), "slope": float(bb), "n_used": int(keep.sum()), "n_found": len(P), "n_positions": n,
           "rms_px": float(np.sqrt(np.mean(res ** 2))),
           "span_fraction": float((P[keep, 0].max() - P[keep, 0].min()) / (t1 - t0))}
    return fit, [(t, p) for (t, p), k in zip(pts, keep) if k], n


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    g = np.asarray(Image.open(cfg["image"]).convert("L"), dtype=float)
    step, half, dark = cfg.get("step", 10), cfg.get("half", 10), cfg.get("dark", 160)
    out = {"vertical": [], "horizontal": []}
    for kind, key in (("v", "vertical"), ("h", "horizontal")):
        for L in cfg[key]:
            fit, pts, n = measure(g, kind, L["guess"], L["t0"], L["t1"], step, half, L.get("wmax", 10), dark, maxdist=8, skip=L.get("skip", ()))
            if fit is not None:   # second pass from the first fit, tighter
                fit, pts, n = measure(g, kind, (fit["intercept"], fit["slope"]), L["t0"], L["t1"], step, half, L.get("wmax", 10), dark, maxdist=3, skip=L.get("skip", ()))
            if fit is None:
                print(f"{key} {L['value']}: not found ({len(pts)} of {n})")
                continue
            rec = dict(L, **fit, samples=[[round(t, 1), round(p, 2)] for t, p in pts])
            out[key].append(rec)
            print(f"{key:10s} {L['label']:>8s} value={str(L['value']):>6s} anchor={L.get('anchor', True)!s:5s} "
                  f"pos = {fit['intercept']:.2f} {fit['slope']:+.5f} t  used {fit['n_used']}/{fit['n_found']} of {n} "
                  f"span {fit['span_fraction']:.2f} rms {fit['rms_px']:.2f}")
    # anchors: intersections of anchored lines. vertical: u = av + bv v; horizontal: v = ah + bh u
    anchors = []
    for h in out["horizontal"]:
        if not h.get("anchor", True):
            continue
        for vl in out["vertical"]:
            if not vl.get("anchor", True):
                continue
            u = (vl["intercept"] + vl["slope"] * h["intercept"]) / (1 - vl["slope"] * h["slope"])
            v = h["intercept"] + h["slope"] * u
            src = lambda L: f"measured at {L['n_used']} of {L['n_positions']} positions (reader's helper measure_lines.py)"
            anchors.append({"x_value": vl["value"], "y_value": h["value"], "u": round(u, 2), "v": round(v, 2),
                            "x_source": src(vl), "y_source": src(h)})
    U = np.array([[a["u"], a["v"], 1.0] for a in anchors])
    X = np.array([a["x_value"] for a in anchors], float)
    Y = np.array([a["y_value"] for a in anchors], float)
    ax, *_ = np.linalg.lstsq(U, X, rcond=None)
    ay, *_ = np.linalg.lstsq(U, Y, rcond=None)
    rx, ry = X - U @ ax, Y - U @ ay
    od = Path(cfg["out"])
    od.mkdir(parents=True, exist_ok=True)
    with (od / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
        w.writeheader()
        w.writerows(anchors)
    cal = {
        "image": cfg["image"], "box": cfg["box"], "bands": None, "dark": dark, "min_frac": None, "snap": None,
        "method": "lines measured by out/F4-19/measure_lines.py (profile across each line every "
                  f"{step} px, isolated run no wider than wmax, robust straight-line fit); config {sys.argv[1]}",
        "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the grid intersections)",
        "ax": ax.tolist(), "ay": ay.tolist(),
        "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
        "rms_residual_x": float(np.sqrt((rx ** 2).mean())), "rms_residual_y": float(np.sqrt((ry ** 2).mean())),
        "max_residual_x": float(np.abs(rx).max()), "max_residual_y": float(np.abs(ry).max()),
        "n_anchors": len(anchors),
        "vertical_lines": [{"x_value": L["value"], "label_printed": L["label"], "anchored": L.get("anchor", True),
                            "slope_du_dv": L["slope"], "u_at_v0": L["intercept"],
                            "source": f"measured at {L['n_used']} of {L['n_positions']} positions, span {L['span_fraction']:.2f}, rms {L['rms_px']:.2f} px",
                            "note": L.get("note", ""), "samples": L["samples"]} for L in out["vertical"]],
        "horizontal_lines": [{"y_value": L["value"], "label_printed": L["label"], "anchored": L.get("anchor", True),
                              "slope_dv_du": L["slope"], "v_at_u0": L["intercept"],
                              "source": f"measured at {L['n_used']} of {L['n_positions']} positions, span {L['span_fraction']:.2f}, rms {L['rms_px']:.2f} px",
                              "note": L.get("note", ""), "samples": L["samples"]} for L in out["horizontal"]],
    }
    (od / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
    print(f"{len(anchors)} anchors; x rms {cal['rms_residual_x']:.4f} max {cal['max_residual_x']:.4f} "
          f"({cal['x_per_px']:.5f} per px); y rms {cal['rms_residual_y']:.4f} max {cal['max_residual_y']:.4f} ({cal['y_per_px']:.5f} per px)")


if __name__ == "__main__":
    main()
