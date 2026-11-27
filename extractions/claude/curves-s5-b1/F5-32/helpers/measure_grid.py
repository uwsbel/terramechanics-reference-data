"""Measure the grid of Figure 5-32 (p0337.png) on the page: the bottom frame (t = 0), the time ticks
drawn at the right frame (t = .01 to .10), and the load lines of each panel. Prints the fits and
writes grid_measured.json next to this script's output folder. Pixel coordinates are those of the
unrotated page image (u right, v down).

usage: measure_grid.py <page.png> <out.json>
"""
import json
import sys

import numpy as np
from PIL import Image

DARK = 128


def runs(idx):
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append((s, p))
            s = i
        p = i
    out.append((s, p))
    return out


def robust_fit(x, y, it=5, k=3.0, floor=0.75):
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = np.ones(len(x), bool)
    for _ in range(it):
        b, a = np.polyfit(x[keep], y[keep], 1)
        r = y - (a + b * x)
        s = max(floor, float(np.std(r[keep])))
        new = np.abs(r) <= k * s
        if (new == keep).all():
            break
        keep = new
    b, a = np.polyfit(x[keep], y[keep], 1)
    r = y - (a + b * x)
    return float(a), float(b), keep, float(np.sqrt(np.mean(r[keep] ** 2)))


def main():
    page, out = sys.argv[1], sys.argv[2]
    g = np.asarray(Image.open(page).convert("L")) < DARK
    res = {"page": page, "dark_threshold": DARK}

    # 1. bottom frame, t = 0: centre of the 6 px line in each column, robust straight fit over the figure width
    pred = lambda u: 3494.7 - 0.008 * (u - 2285)
    U, V, W = [], [], []
    for u in range(760, 2291, 5):
        rr = [(3460 + (s + p) / 2, p - s + 1) for s, p in runs(np.where(g[3460:3540, u])[0])]
        rr = [r for r in rr if abs(r[0] - pred(u)) < 6 and r[1] <= 9]
        if rr:
            r = min(rr, key=lambda r: abs(r[0] - pred(u)))
            U.append(u); V.append(r[0]); W.append(r[1])
    a, b, keep, rms = robust_fit(U, V)
    res["frame_t0"] = {"v_at_u0": a, "slope_dv_du": b, "rms_px": rms, "n": int(keep.sum()),
                       "width_px_median": float(np.median(W))}
    print(f"t=0 frame: v = {a:.2f} + {b:+.5f} u, rms {rms:.2f} px, {keep.sum()} columns, width {np.median(W)} px")
    slope = b

    # 2. time ticks near the right frame: the dash of each line between u 2195 and 2266 (left of the frame line)
    ticks = {}
    for k in range(1, 11):
        v_guess = 3494.7 - 170.2 * k
        pts = []
        for u in range(2192, 2267):
            col = g[int(v_guess) - 10:int(v_guess) + 11, u]
            rr = [(int(v_guess) - 10 + (s + p) / 2, p - s + 1) for s, p in runs(np.where(col)[0])]
            rr = [r for r in rr if r[1] <= 6]
            if rr:
                r = min(rr, key=lambda r: abs(r[0] - v_guess))
                pts.append((u, r[0]))
        # drop the columns of the -20 load line (u ~ 2195..2206) where the vertical line is the run
        pts = [p for p in pts if not (2193 <= p[0] <= 2208)]
        P = np.array(pts)
        # fixed slope (the frame's): intercept by median, outliers beyond 2 px dropped
        c = P[:, 1] - slope * (P[:, 0] - 2240)
        med = float(np.median(c))
        ok = np.abs(c - med) <= 2
        c0 = float(np.mean(c[ok]))
        uc = float(np.mean(P[ok, 0]))
        # anchor at the centroid of the dash, on the fixed-slope line through it
        ticks[k] = {"t": round(k * 0.01, 2), "u": round(uc, 1), "v": round(c0 + slope * (uc - 2240), 2),
                    "n_cols": int(ok.sum()), "u_span": [int(P[ok, 0].min()), int(P[ok, 0].max())],
                    "scatter_px": round(float(np.std(c[ok])), 2)}
        print(f"tick t={k*0.01:.2f}: centroid u {uc:.1f}, v {ticks[k]['v']:.2f}; ink in {ok.sum()} columns "
              f"over u {P[ok,0].min()}..{P[ok,0].max()}, scatter {np.std(c[ok]):.2f} px")
    res["ticks"] = ticks

    # 3. load lines of each panel: centre of the thin line in each row, robust fit u = a + b v
    panels = {
        1: {"values": [-60, -40, -20, 0], "u3250": [1097, 1182, 1268, 1354]},
        2: {"values": [60, 40, 20, 0], "u3250": [1522, 1606, 1693, 1777]},
        3: {"values": [-80, -60, -40, -20, 0], "u3250": [1948, 2032, 2116, 2202, 2285]},
    }
    res["load_lines"] = {}
    for pn, P in panels.items():
        lines = []
        for val, u0 in zip(P["values"], P["u3250"]):
            pu = lambda v: u0 + 0.0081 * (v - 3250)
            VV, UU, WW = [], [], []
            for v in range(1790, 3486, 4):
                row = g[v, int(pu(v)) - 8:int(pu(v)) + 9]
                rr = [(int(pu(v)) - 8 + (s + p) / 2, p - s + 1) for s, p in runs(np.where(row)[0])]
                rr = [r for r in rr if r[1] <= 7 and abs(r[0] - pu(v)) <= 5]
                if len(rr) == 1:
                    VV.append(v); UU.append(rr[0][0]); WW.append(rr[0][1])
            a, b, keep, rms = robust_fit(VV, UU)
            VV = np.array(VV)
            lines.append({"value": val, "u_at_v0": a, "slope_du_dv": b, "rms_px": rms, "n_rows": int(keep.sum()),
                          "v_span": [int(VV[keep].min()), int(VV[keep].max())], "width_px_median": float(np.median(WW))})
            print(f"panel {pn} load {val:>4}: u = {a:.2f} + {b:+.5f} v; at v 3495 u {a + b*3495:.1f}, at v 1793 u "
                  f"{a + b*1793:.1f}; rms {rms:.2f} px, ink in {keep.sum()} rows over v {VV[keep].min()}..{VV[keep].max()}, "
                  f"width {np.median(WW)}")
        res["load_lines"][pn] = lines
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
