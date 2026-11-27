"""Column-scan tracker for the drawn curves of FC-2C panel 1.

For each series, starting from its first marker, walk the chosen sample columns and pick, at
each column, the dark run whose centre is nearest to a linear prediction from the previous two
accepted points. All runs within a window are printed so the choice can be checked by eye.
Columns that fall in a dash gap are shifted by up to `shift` px to the nearest column with ink
near the prediction. Nothing here is written to the points file automatically; the table is
reviewed first.
"""
import json, sys
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
    out = []
    start = None
    for i, d in enumerate(col):
        if d and start is None:
            start = i
        if not d and start is not None:
            out.append((v0 + (start + i - 1) / 2.0, i - start))
            start = None
    if start is not None:
        out.append((v0 + (start + len(col) - 1) / 2.0, len(col) - start))
    return out

# horizontal gridline v at a given u (for flagging)
def grid_v(u):
    return [l["v_at_u0"] + l["slope_dv_du"] * u for l in cal["horizontal_lines"]]

def track(name, start_pts, x_samples, end_u, tol=14, shift=8, verbose=True):
    """start_pts: list of (u, v) pixel points (markers) used to seed the prediction."""
    pts = list(start_pts)
    out = []
    for x in x_samples:
        u0 = int(round(val_to_px(x, 3000)[0]))
        if u0 > end_u:
            break
        if u0 <= pts[-1][0]:
            continue
        # prediction
        if len(pts) >= 2:
            (u1, v1), (u2, v2) = pts[-2], pts[-1]
            slope = (v2 - v1) / (u2 - u1) if u2 != u1 else 0.0
        else:
            slope = 0.0
            u2, v2 = pts[-1]
        chosen = None
        for du in [0] + [s for k in range(1, shift + 1) for s in (k, -k)]:
            u = u0 + du
            pred = v2 + slope * (u - u2)
            rs = runs(u, int(pred) - 60, int(pred) + 60)
            cands = [(abs(c - pred), c, t) for c, t in rs if abs(c - pred) <= tol and t <= 30]
            if cands:
                cands.sort()
                d, c, t = cands[0]
                gv = min(abs(c - g) for g in grid_v(u))
                chosen = (u, c, t, pred, du, gv, [(round(cc, 1), tt) for cc, tt in rs])
                break
        if chosen is None:
            if verbose:
                print(f"{name} x={x:4d} u={u0}: NO RUN near pred {pred:.1f}; runs {rs}")
            continue
        u, c, t, pred, du, gv, allr = chosen
        pts.append((u, c))
        out.append((x, u, c, t, pred, du, gv, allr))
        if verbose:
            flag = ""
            if t > 12: flag += " THICK"
            if gv < 6: flag += " ON-GRIDLINE"
            if abs(du) > 0: flag += f" shifted{du:+d}"
            print(f"{name} x={x:4d} u={u} v={c:.1f} t={t} pred={pred:.1f}{flag}   runs={allr}")
    return out

if __name__ == "__main__":
    xs = list(range(3, 250, 5))
    series = {
        # name: (seed markers, end u)
        "n4400": ([(813, 1814), (878, 1693)], 1700),
        "n3660": ([(721, 2071), (757, 1987)], 1650),
        "n2995": ([(753, 2069), (787, 2000)], 1580),
        "n2200": ([(737, 2432), (790, 2346)], 1480),
        "n1468": ([(703, 2685), (713, 2560)], 1180),
        "n734":  ([(722, 2641), (759, 2521)], 1100),
    }
    which = sys.argv[1:] or list(series)
    for name in which:
        seeds, end_u = series[name]
        print("=" * 30, name)
        track(name, seeds, xs, end_u)
