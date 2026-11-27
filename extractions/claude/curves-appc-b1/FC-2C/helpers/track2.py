"""Fine-step tracker for the drawn curves of FC-2C panel 1.

Walks each curve from its first marker in steps of `step` px in u, picking at each column the
dark run nearest to a linear prediction (slope from the last accepted points). Dash gaps are
bridged by carrying the prediction forward (nothing is recorded in a gap). Then the trace is
sampled at x = 3, 8, 13, ... thousandths (columns away from vertical gridlines): the nearest
tracked ink column within `snap` px is used, with its actual u. The table is reviewed by eye
before anything goes into the points file.
"""
import json, sys, csv
import numpy as np
from PIL import Image

IMG = "packet/p0122.png"
CAL = "out/FC-2C/cal-p1/calibration.json"
DARK = 128

im = np.array(Image.open(IMG).convert("L"))
cal = json.load(open(CAL))
ax, ay = cal["ax"], cal["ay"]
A = np.array([[ax[0], ax[1]], [ay[0], ay[1]]])
b = np.array([ax[2], ay[2]])
Ainv = np.linalg.inv(A)

def px_to_val(u, v):
    return A @ np.array([u, v]) + b

def val_to_px(x, y):
    return Ainv @ (np.array([x, y]) - b)

def runs(u, v0, v1, half=1):
    col = im[v0:v1, u - half:u + half + 1].min(axis=1) < DARK
    out, start = [], None
    for i, d in enumerate(col):
        if d and start is None:
            start = i
        if not d and start is not None:
            out.append((v0 + (start + i - 1) / 2.0, i - start)); start = None
    if start is not None:
        out.append((v0 + (start + len(col) - 1) / 2.0, len(col) - start))
    return out

def grid_v(u):
    return [l["v_at_u0"] + l["slope_dv_du"] * u for l in cal["horizontal_lines"]]

def track(seeds, end_u, step=3, tol=7, maxgap=40, nslope=4):
    pts = [tuple(p) + (0, "seed") for p in seeds]   # (u, v, thickness, tag)
    u = int(seeds[-1][0]) + step
    last_ink_u = seeds[-1][0]
    while u <= end_u:
        recent = pts[-nslope:]
        if len(recent) >= 2:
            us = np.array([p[0] for p in recent]); vs = np.array([p[1] for p in recent])
            slope = np.polyfit(us, vs, 1)[0]
        else:
            slope = 0.0
        u2, v2 = pts[-1][0], pts[-1][1]
        pred = v2 + slope * (u - u2)
        rs = runs(u, int(pred) - 40, int(pred) + 40)
        cands = sorted([(abs(c - pred), c, t) for c, t in rs if abs(c - pred) <= tol and t <= 34])
        if cands:
            d, c, t = cands[0]
            tag = ""
            if t > 10: tag += "thick"
            if min(abs(c - g) for g in grid_v(u)) < 5: tag += "/grid"
            pts.append((u, c, t, tag))
            last_ink_u = u
        else:
            if u - last_ink_u > maxgap:
                break
        u += step
    return pts

def sample(pts, xs, snap=8):
    ink = [p for p in pts if p[3] != "seed"]
    out = []
    for x in xs:
        u0 = val_to_px(x, 3000)[0]
        best = min(ink, key=lambda p: abs(p[0] - u0), default=None)
        if best is None or abs(best[0] - u0) > snap:
            out.append((x, u0, None)); continue
        out.append((x, u0, best))
    return out

SERIES = {
    "n4400": ([(813, 1814), (816, 1808)], 1700),
    "n3660": ([(721, 2071), (724, 2064)], 1650),
    "n2995": ([(753, 2069), (756, 2063)], 1600),
    "n2200": ([(737, 2432), (740, 2427)], 1490),
    "n1468": ([(703, 2685), (704, 2678)], 1200),
    "n734":  ([(722, 2641), (725, 2633)], 1110),
}

if __name__ == "__main__":
    which = sys.argv[1:] or list(SERIES)
    xs = list(range(3, 250, 5))
    for name in which:
        seeds, end_u = SERIES[name]
        pts = track(seeds, end_u)
        print("=" * 20, name, f"tracked {len(pts)} pts, last u={pts[-1][0]}")
        for p in pts:
            if p[3] and p[3] != "seed":
                print(f"   u={p[0]} v={p[1]:.1f} t={p[2]} {p[3]}")
        print("  samples:")
        for x, u0, best in sample(pts, xs):
            if best is None:
                print(f"   x={x:4d} u0={u0:.0f}  -- no ink within 8 px")
            else:
                print(f"   x={x:4d} u0={u0:.0f}  u={best[0]} v={best[1]:.1f} t={best[2]} {best[3]}")
        with open(f"out/FC-2C/helpers/track-{name}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(["u", "v", "thickness", "tag"]); w.writerows(pts)
