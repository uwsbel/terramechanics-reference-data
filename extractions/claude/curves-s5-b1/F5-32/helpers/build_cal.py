"""Write cal-p<n>/anchors.csv and cal-p<n>/calibration.json for the three panels of Figure 5-32, in the
layout of tools/calibrate_axes.py detect, from the lines measured on the page (grid_measured.json,
time_lines.json). Pixel coordinates of the unrotated page image.

Why a helper and not `detect`: the time grid lines of this figure are printed only as short dashes at the
right frame (and longer dashes across panel 3 for some of them); across panels 1 and 2 only remnants of the
dashed lines survive (dots, thickenings at the crossings with the load lines). `detect` needs a line in
half of its bands inside the panel's box and fails on every time line ("fewer than two grid lines").

design "ticks" (used): each time line t = .01 to .10 is a tick anchored once, on its dash at the right frame
(x-only anchor, y_value empty); it takes the tilt of the panel's affine map, as calibrate_axes.py does for
a lone tick. t = 0 is the bottom frame, a solid drawn line, anchored at its crossings with the panel's
load lines. The load lines are drawn lines, anchored (y-only) at their crossings with the time lines
fitted across the figure (time_lines.json), so their own tilt is kept. The affine map (a diagnostic, and the
direction of the tick lines) is fitted on the crossings of the panel's load lines with the time lines
fitted across the figure, which are listed in calibration.json as `affine_anchors`.

design "fullwidth": each time line is the straight line fitted to its ink across the figure, anchored at
its crossings with the panel's load lines and with every measured load line to the right of the panel
(x-only), so that the ink check of calibrate_axes.py sees the stretch where the line is drawn.

usage: build_cal.py <grid_measured.json> <time_lines.json> <out_dir> <design> [<image>]
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

PANELS = {1: {"values": [-60, -40, -20, 0], "ydir": "right"},
          2: {"values": [60, 40, 20, 0], "ydir": "left"},
          3: {"values": [-80, -60, -40, -20, 0], "ydir": "right"}}
TIMES = [round(0.01 * k, 2) for k in range(11)]


def intersect(tl, ll):
    """time line v = a + b u, load line u = c + d v"""
    a, b = tl["v_at_u0"], tl["slope_dv_du"]
    c, d = ll["u_at_v0"], ll["slope_du_dv"]
    u = (c + d * a) / (1 - d * b)
    return u, a + b * u


def fit_affine(rows):
    U = np.array([[r["u"], r["v"], 1.0] for r in rows])
    X = np.array([r["x_value"] for r in rows], float)
    Y = np.array([r["y_value"] for r in rows], float)
    ax, *_ = np.linalg.lstsq(U, X, rcond=None)
    ay, *_ = np.linalg.lstsq(U, Y, rcond=None)
    rx, ry = X - U @ ax, Y - U @ ay
    return ax, ay, rx, ry


def main():
    gm, tl, out_dir, design = sys.argv[1:5]
    G = json.load(open(gm, encoding="utf-8"))
    TL = json.load(open(tl, encoding="utf-8"))
    tlines = {round(0.01 * int(k), 2): v for k, v in TL.items()}
    all_load = [(int(p), l) for p, lines in G["load_lines"].items() for l in lines]
    for pn, P in PANELS.items():
        lines = G["load_lines"][str(pn)]
        # affine diagnostic on the crossings of the panel's load lines with the time lines fitted across the figure
        aff = []
        for t in TIMES:
            for ll in lines:
                u, v = intersect(tlines[t], ll)
                aff.append({"x_value": t, "y_value": ll["value"], "u": round(u, 2), "v": round(v, 2)})
        ax, ay, rx, ry = fit_affine(aff)
        anchors = []
        src_load = lambda ll: (f"drawn load line, ink centre fitted in {ll['n_rows']} rows over v {ll['v_span'][0]}.."
                               f"{ll['v_span'][1]} (rms {ll['rms_px']:.2f} px); anchored at its crossings with the "
                               f"time lines fitted across the figure")
        for ll in lines:
            for t in TIMES:
                u, v = intersect(tlines[t], ll)
                anchors.append({"x_value": "", "y_value": ll["value"], "u": round(u, 2), "v": round(v, 2),
                                "x_source": "", "y_source": src_load(ll)})
        f0 = tlines[0.0]
        for ll in lines:
            u, v = intersect(f0, ll)
            anchors.append({"x_value": 0.0, "y_value": "", "u": round(u, 2), "v": round(v, 2),
                            "x_source": f"bottom frame (t = 0), solid, fitted in {f0['n']} columns (rms {f0['rms_px']:.2f} px)",
                            "y_source": ""})
        if design == "ticks":
            for k in range(1, 11):
                tk = G["ticks"][str(k)]
                anchors.append({"x_value": tk["t"], "y_value": "", "u": tk["u"], "v": tk["v"],
                                "x_source": (f"tick: centre of the dash drawn at the right frame, ink in {tk['n_cols']} "
                                             f"columns over u {tk['u_span'][0]}..{tk['u_span'][1]}; one anchor, the line "
                                             f"takes the affine tilt"), "y_source": ""})
        else:
            umin = min(l["u_at_v0"] + l["slope_du_dv"] * 2600 for l in lines) - 5
            others = [l for p, l in all_load if p > pn]
            for t in TIMES[1:]:
                for ll in lines + others:
                    u, v = intersect(tlines[t], ll)
                    anchors.append({"x_value": t, "y_value": "", "u": round(u, 2), "v": round(v, 2),
                                    "x_source": "time line fitted to its ink across the figure", "y_source": ""})
        od = Path(out_dir) / f"cal-p{pn}"
        od.mkdir(parents=True, exist_ok=True)
        with (od / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
            w.writeheader()
            w.writerows(anchors)
        us = [a["u"] for a in aff]
        vs = [a["v"] for a in aff]
        cal = {
            "image": "packet/p0337.png",
            "box": [int(min(us)) - 12, int(min(vs)) - 12, int(max(us)) + 12, int(max(vs)) + 12],
            "made_by": f"out/F5-32/helpers/build_cal.py, design '{design}' (see the helper's docstring)",
            "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the grid intersections in affine_anchors)",
            "ax": ax.tolist(), "ay": ay.tolist(),
            "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
            "rms_residual_x": float(np.sqrt(np.mean(rx ** 2))), "rms_residual_y": float(np.sqrt(np.mean(ry ** 2))),
            "max_residual_x": float(np.abs(rx).max()), "max_residual_y": float(np.abs(ry).max()),
            "n_anchors": len(aff),
            "x_direction": "up", "y_direction": P["ydir"],
            "vertical_lines": [{"y_value": l["value"], "slope_du_dv": l["slope_du_dv"], "u_at_v0": l["u_at_v0"],
                                "source": f"detected: ink centre in {l['n_rows']} rows, rms {l['rms_px']:.2f} px, width {l['width_px_median']} px"}
                               for l in lines],
            "horizontal_lines": [{"x_value": t, "slope_dv_du": tlines[t]["slope_dv_du"], "v_at_u0": tlines[t]["v_at_u0"],
                                  "source": (tlines[t]["source"] + f"; {tlines[t]['n']} ink columns, rms {tlines[t]['rms_px']} px")}
                                 for t in TIMES],
            "ticks": {G["ticks"][str(k)]["t"]: G["ticks"][str(k)] for k in range(1, 11)},
            "affine_anchors": aff,
        }
        (od / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
        print(f"panel {pn}: {len(anchors)} anchors; affine x {cal['x_per_px']:.3e} s/px rms {cal['rms_residual_x']:.2e} "
              f"(max {cal['max_residual_x']:.2e}); y {cal['y_per_px']:.4f} lb/px rms {cal['rms_residual_y']:.3f} "
              f"(max {cal['max_residual_y']:.3f})")


if __name__ == "__main__":
    main()
