"""Refit the grid lines of a `calibrate_axes.py detect` run, setting aside band samples that are not
the grid line's ink, then rebuild anchors.csv and calibration.json in the same layout.

Why (FA-2, page p0007): the grain-size parameter table is pasted over the grid (u 862..1482,
v 2262..3668). Under it the percent lines 50 to 90 are hidden, and the table's own vertical border
at u 1131..1141 lies a few pixels from the 70 percent line, so detect's track for 70 ran onto the
table border below v 2262 (fitted tilt 0.0047 against 0.010 for every other percent line; 9 px off
at the bottom labels). And the three curves run along the 0 percent frame line between about
v 2600 and 3200, widening the dark run there, which pulls two band samples of the frame inward.

Rule applied to every line, in this order:
1. a sample whose band overlaps the table box and whose position lies inside the table's span
   across the lines is set aside (the table hides the grid there);
2. of the remaining samples, those that agree on one straight line are kept: the pair of samples
   with the most others within 1.5 px of the line through them (the consensus rule of the tool's
   `recover`), and the line is refitted on them by least squares (a plain least-squares first fit
   was pulled by the two curve-widened samples of the 0 line and set aside two good ones);
3. an anchor (crossing of two fitted lines) is dropped where the table hides the grid: inside the
   table's u span from its top edge down to the frame. The lines 50 to 90 were measured above the
   table only, so their crossings below it would be extrapolations, not observations; under the
   table the ink check finds the table's border and text instead of grid ink.
Lines are never moved by hand; the tool's own band samples are reused.

Usage: python refit_cal.py <detect_dir> <out_dir> <image> <bands> <box u0 v0 u1 v1>
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
import calibrate_axes as ca  # noqa: E402  (read only; the tool is not modified)

TABLE = (862, 2262, 1482, 3668)   # u0, v0, u1, v1 of the parameter table, read on the page


def refit(samples, axis, half_band):
    """samples: [(t, pos)]; axis 'v' (vertical line: t = v, pos = u) or 'h' (t = u, pos = v)."""
    u0, v0, u1, v1 = TABLE
    keep, aside = [], []
    for t, p in samples:
        if axis == "v":
            hit = (t + half_band > v0 and t - half_band < v1) and (u0 <= p <= u1)
        else:
            hit = (t + half_band > u0 and t - half_band < u1) and (v0 <= p <= v1)
        (aside if hit else keep).append((t, p, "table"))
    pts = np.array([(t, p) for t, p, _ in keep])
    if len(pts) >= 3:
        T, S = pts[:, 0], pts[:, 1]
        best = None
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                k = (S[j] - S[i]) / (T[j] - T[i])
                inl = np.abs(S - (S[i] + k * (T - T[i]))) <= 1.5
                if best is None or inl.sum() > best.sum():
                    best = inl
        c1, c0 = np.polyfit(T[best], S[best], 1)
        res = S - (c0 + c1 * T)
        aside += [(t, p, f"off the consensus line by {r:+.1f} px") for (t, p, _), r, k in zip(keep, res, best) if not k]
        keep = [k for k, o in zip(keep, best) if o]
        pts = np.array([(t, p) for t, p, _ in keep])
    slope, intercept = np.polyfit(pts[:, 0], pts[:, 1], 1)
    return float(slope), float(intercept), [[t, p] for t, p, _ in keep], aside


def main():
    src, out, image, bands = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    box = [int(x) for x in sys.argv[5:9]]
    cal = json.loads((src / "calibration.json").read_text(encoding="utf-8"))
    tx, ty = ca.axis_transforms(cal)
    hb_v = (box[3] - box[1]) / bands / 2   # half a band along a vertical line
    hb_h = (box[2] - box[0]) / bands / 2
    vkey = [k for k in cal["vertical_lines"][0] if k.endswith("_value")][0]
    hkey = [k for k in cal["horizontal_lines"][0] if k.endswith("_value")][0]
    vlines, hlines, log = [], [], []
    for ln in cal["vertical_lines"]:
        s, i, kept, aside = refit([tuple(x) for x in ln["samples"]], "v", hb_v)
        src_txt = f"detected in {len(kept)}/{bands} bands" + (f"; {len(aside)} set aside (refit_cal.py)" if aside else "")
        vlines.append((ln[vkey], s, i, src_txt, kept))
        log += [f"{vkey[0]}={ln[vkey]:g}: sample v={t:.0f} u={p:.1f} set aside ({why})" for t, p, why in aside]
    for ln in cal["horizontal_lines"]:
        s, i, kept, aside = refit([tuple(x) for x in ln["samples"]], "h", hb_h)
        src_txt = f"detected in {len(kept)}/{bands} bands" + (f"; {len(aside)} set aside (refit_cal.py)" if aside else "")
        hlines.append((ln[hkey], s, i, src_txt, kept))
        log += [f"{hkey[0]}={ln[hkey]:g}: sample u={t:.0f} v={p:.1f} set aside ({why})" for t, p, why in aside]
    on_v_is_x = vkey == "x_value"
    anchors = []
    for h in hlines:
        for v in vlines:
            u, vv = ca.intersect(h, v)
            xl, yl = (v, h) if on_v_is_x else (h, v)
            anchors.append({"x_value": xl[0], "y_value": yl[0], "u": round(u, 1), "v": round(vv, 1),
                            "x_source": xl[3], "y_source": yl[3]})
    hidden = [a for a in anchors if TABLE[0] <= a["u"] <= TABLE[2] and a["v"] >= TABLE[1]]
    anchors = [a for a in anchors if a not in hidden]
    log.append(f"{len(hidden)} anchors dropped under the table (u {TABLE[0]}..{TABLE[2]}, v >= {TABLE[1]}): "
               + ", ".join(f"({a['x_value']:g}, {a['y_value']:g})" for a in hidden))
    ax, ay, rmsx, rmsy, maxx, maxy = ca.fit_affine(anchors, tx, ty)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
        w.writeheader()
        w.writerows(anchors)
    new = dict(cal)
    new.update({"ax": ax, "ay": ay, "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
                "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
                "n_anchors": len(anchors),
                "vertical_lines": [{vkey: l[0], "slope_du_dv": l[1], "u_at_v0": l[2], "source": l[3], "samples": l[4]} for l in vlines],
                "horizontal_lines": [{hkey: l[0], "slope_dv_du": l[1], "v_at_u0": l[2], "source": l[3], "samples": l[4]} for l in hlines],
                "refit": {"by": "out/FA-2/refit_cal.py", "from": str(src).replace("\\", "/"), "table_box": list(TABLE),
                          "set_aside": log}})
    (out / "calibration.json").write_text(json.dumps(new, indent=1), encoding="utf-8")
    print(f"{len(anchors)} anchors; x rms {rmsx:.4f} max {maxx:.4f} (q); y rms {rmsy:.4f} max {maxy:.4f}")
    for line in log:
        print("  " + line)
    for l in vlines:
        print(f"  vertical   {vkey[0]}={l[0]:>8g}  u = {l[2]:.1f} + {l[1]:+.4f} v   ({l[3]})")
    for l in hlines:
        print(f"  horizontal {hkey[0]}={l[0]:>8g}  v = {l[2]:.1f} + {l[1]:+.4f} u   ({l[3]})")
    # the ink check of the piecewise map (D-025)
    c, X, Y = ca.piecewise_maps(out, image)
    summ = ca.knots_summary(X, Y)
    (out / "knots-check.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    for k in ("x", "y"):
        print(f"  {k}: verified " + ", ".join(f"{d['value']:g}({d['location_error_px']})" for d in summ[k]))
        for d in summ["rejected_" + k]:
            print(f"  {k}: REJECTED {d['value']:g}: {d['reason']}")


if __name__ == "__main__":
    main()
