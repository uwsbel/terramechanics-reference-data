"""Fit each time line of Figure 5-32 (t = .01 to .10) as one straight line across the figure from its own ink:
the dash drawn at the right frame plus the remnants of the dashed line left across the panels (dots and short
dashes of the printed grid line). The t = 0 line is the bottom frame. Writes time_lines.json.

usage: fit_time_lines.py <page.png> <grid_measured.json> <out.json>
"""
import json
import sys

import numpy as np
from PIL import Image


def main():
    page, gm, out = sys.argv[1:4]
    g = np.asarray(Image.open(page).convert("L")) < 128
    G = json.load(open(gm, encoding="utf-8"))
    fr = G["frame_t0"]
    load = [l for lines in G["load_lines"].values() for l in lines]

    def on_load_line(u, v, pad=5):
        return any(abs(u - (l["u_at_v0"] + l["slope_du_dv"] * v)) <= pad for l in load)

    res = {"0": {"t": 0.0, "v_at_u0": fr["v_at_u0"], "slope_dv_du": fr["slope_dv_du"], "rms_px": fr["rms_px"],
                 "n": fr["n"], "u_range": [760, 2290], "source": "bottom frame, solid, fitted in every 5th column"}}
    for k in range(1, 11):
        T = G["ticks"][str(k)]
        a = T["v"] - fr["slope_dv_du"] * T["u"]
        b = fr["slope_dv_du"]
        for win, tol in ((6, 1.0), (3, 0.8), (2.5, 0.8)):
            pts = []
            for u in range(760, 2267):
                vp = a + b * u
                if on_load_line(u, vp):
                    continue
                if u < 1090 and vp < 1890:   # the inset's legend boxes and text, not a grid line
                    continue
                lo = int(round(vp - win))
                col = g[lo:int(round(vp + win)) + 1, u]
                idx = np.where(col)[0]
                if len(idx) == 0:
                    continue
                # a grid line's ink in one column is a short run (<= 6 px); taller ink is a trace, a label or a symbol
                full = g[lo - 6:int(round(vp + win)) + 7, u]
                fidx = np.where(full)[0]
                if fidx.max() - fidx.min() + 1 > 7:
                    continue
                pts.append((u, lo + idx.mean()))
            P = np.array(pts)
            if len(P) < 10 or np.ptp(P[:, 0]) < 300:
                # too little ink to fit a tilt (t = .10: a 3 px speck at u 2233 and stubs on the frame and on the
                # -20 line): the line through the tick with the tilt of the t = .09 line fitted before it
                prev = res[str(k - 1)]
                a, b = T["v"] - prev["slope_dv_du"] * T["u"], prev["slope_dv_du"]
                r = P[:, 1] - (a + b * P[:, 0])
                keep = np.abs(r) <= 1.0
                aa, bb = a, b
                tilt_note = "tilt of the t = .09 line (too little ink to fit its own)"
                break
            tilt_note = "own tilt"
            keep = np.ones(len(P), bool)
            for _ in range(8):
                bb, aa = np.polyfit(P[keep, 0], P[keep, 1], 1)
                r = P[:, 1] - (aa + bb * P[:, 0])
                new = np.abs(r) <= max(tol, 3 * float(np.std(r[keep])))
                if (new == keep).all():
                    break
                keep = new
            a, b = aa, bb
        rms = float(np.std(r[keep]))
        U = P[keep, 0]
        # coverage: ink columns per 100 px stretch, for the record
        cover = {f"{u0}-{u0 + 100}": int(((U >= u0) & (U < u0 + 100)).sum()) for u0 in range(700, 2300, 100)}
        res[str(k)] = {"t": round(0.01 * k, 2), "v_at_u0": float(a), "slope_dv_du": float(b), "rms_px": round(rms, 2),
                       "n": int(keep.sum()), "u_range": [int(U.min()), int(U.max())], "ink_columns_per_100px": cover,
                       "source": "dash at the right frame and the remnants of the printed line across the panels, "
                                 "one straight fit; " + tilt_note,
                       "points": [[int(u), round(float(v), 2)] for u, v in P[keep]]}
        print(f"t={0.01*k:.2f}: v = {a:.2f} {b:+.5f} u; rms {rms:.2f} px; {keep.sum()} ink columns over u "
              f"{U.min():.0f}..{U.max():.0f}; at u 1225 v {a + b*1225:.1f}, at u 1650 {a + b*1650:.1f}, "
              f"at u 2240 {a + b*2240:.1f}; columns left of 1800: {(U < 1800).sum()}, left of 1400: {(U < 1400).sum()}")
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
