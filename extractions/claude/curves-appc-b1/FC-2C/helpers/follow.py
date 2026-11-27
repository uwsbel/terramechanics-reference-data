"""Ridge follower for the drawn curves of FC-2C panel 1 (and the lower panel if needed).

Starting at a seed point with a seed direction, the follower advances `step` px along the current
direction and re-centres on the ink by scanning the perpendicular line through the advanced point
(dark run nearest to it, within `radius` px). Dash gaps are bridged by continuing in the same
direction for up to `maxgap` px without recording. A perpendicular run longer than `maxrun` px is a
gridline or a marker crossing; the position is recorded but flagged. Output: a polyline of ink
centres with the local run thickness, plus samples at the requested x values (nearest tracked
point in u). Every sample is then reviewed on the overlay by eye.
"""
import json, sys, csv, math
import numpy as np
from PIL import Image

IMG = "packet/p0122.png"
DARK = 128
im = np.array(Image.open(IMG).convert("L"))
H, W = im.shape

def load_cal(path):
    cal = json.load(open(path))
    ax, ay = cal["ax"], cal["ay"]
    A = np.array([[ax[0], ax[1]], [ay[0], ay[1]]]); b = np.array([ax[2], ay[2]])
    return cal, A, b, np.linalg.inv(A)

def dark(u, v):
    ui, vi = int(round(u)), int(round(v))
    if 0 <= ui < W and 0 <= vi < H:
        return im[vi, ui] < DARK
    return False

def perp_runs(p, n, radius):
    """dark runs along the line p + s*n, s in [-radius, radius]; returns list of (s_center, length)."""
    out, start = [], None
    ss = np.arange(-radius, radius + 1, 1.0)
    for i, s in enumerate(ss):
        d = dark(p[0] + s * n[0], p[1] + s * n[1])
        if d and start is None: start = i
        if not d and start is not None:
            out.append(((ss[start] + ss[i - 1]) / 2, i - start)); start = None
    if start is not None:
        out.append(((ss[start] + ss[-1]) / 2, len(ss) - start))
    return out

def follow(seed, direction, step=4.0, radius=10, maxgap=45, maxrun=30, smooth=0.6, stop_u=None, max_steps=2000, maxturn_deg=180, maxlen=99):
    p = np.array(seed, float); d = np.array(direction, float); d /= np.linalg.norm(d)
    pts = [(p[0], p[1], 0, "seed")]
    gap = 0.0
    for _ in range(max_steps):
        q = p + step * d
        n = np.array([-d[1], d[0]])
        rs = perp_runs(q, n, radius)
        if not rs:
            gap += step
            if gap > maxgap: break
            p = q
            continue
        rs_ok = [r for r in rs if r[1] <= maxlen] or rs
        s, L = min(rs_ok, key=lambda r: abs(r[0]))
        if L > maxrun:
            # crossing a gridline or a marker: keep the predicted position, flag it
            newp = q; tag = "cross"
        else:
            newp = q + s * n; tag = "thick" if L > 11 else ""
        nd = newp - p; nn = np.linalg.norm(nd)
        if nn > 0:
            nd /= nn
            if len(pts) > 4 and math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(nd, d)))))) > maxturn_deg:
                # too sharp a turn: a marker or a gridline pulled the centre; treat as a gap
                gap += step
                if gap > maxgap: break
                p = q
                continue
            d = smooth * d + (1 - smooth) * nd; d /= np.linalg.norm(d)
        p = newp; gap = 0.0
        pts.append((p[0], p[1], L, tag))
        if stop_u is not None and p[0] > stop_u: break
    return pts

def sample_at(pts, Ainv, b, xs, snap=6.0):
    ink = [p for p in pts if p[3] in ("", "thick")]
    out = []
    for x in xs:
        u0 = (Ainv @ (np.array([x, 3000.0]) - b))[0]
        best = min(ink, key=lambda p: abs(p[0] - u0), default=None)
        out.append((x, u0, best if best is not None and abs(best[0] - u0) <= snap else None))
    return out

if __name__ == "__main__":
    cal, A, b, Ainv = load_cal("out/FC-2C/cal-p1/calibration.json")
    SERIES = {
        "n4400": [((813, 1814), (0.45, -1.0), 1700)],
        "n3660": [((721, 2071), (0.35, -1.0), 1650)],
        "n2995": [((753, 2069), (0.35, -1.0), 1600)],
        "n2200": [((737, 2432), (0.45, -1.0), 868), ((934, 2139), (0.75, -0.65), 1490)],
        "n1468": [((703, 2685), (0.08, -1.0), 975), ((1048, 2224), (1.0, -0.05), 1200)],
        "n734":  [((722, 2641), (0.25, -1.0), 1110)],
    }
    which = sys.argv[1:] or list(SERIES)
    xs = list(range(3, 250, 5))
    allrows = []
    for name in which:
        pts = []
        for seed, d0, stop_u in SERIES[name]:
            pts += follow(seed, d0, stop_u=stop_u)
        seed, d0, _ = SERIES[name][0]
        back = follow(seed, (-d0[0], -d0[1]), maxgap=8, max_steps=10)
        print("=" * 20, name, f"{len(pts)} pts, last ({pts[-1][0]:.0f},{pts[-1][1]:.0f}); backward from seed: {len(back)-1} steps, last ({back[-1][0]:.0f},{back[-1][1]:.0f})")
        vmin = min(pts[1:], key=lambda p: p[1]) if len(pts) > 1 else None
        print(f"   topmost ink point (peak): ({vmin[0]:.0f},{vmin[1]:.0f})")
        for x, u0, bst in sample_at(pts, Ainv, b, xs):
            if bst is None:
                print(f"   x={x:4d} u0={u0:.0f}  -- none")
            else:
                print(f"   x={x:4d} u0={u0:.0f}  u={bst[0]:.1f} v={bst[1]:.1f} L={bst[2]} {bst[3]}")
                allrows.append(["FC-2C", 1, name, "trace", x, f"{bst[0]:.1f}", f"{bst[1]:.1f}", 2, max(2, bst[2] // 2), "", bst[3]])
        with open(f"out/FC-2C/helpers/follow-{name}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(["u", "v", "runlen", "tag"])
            for p in pts: w.writerow([f"{p[0]:.1f}", f"{p[1]:.1f}", p[2], p[3]])

    with open("out/FC-2C/helpers/samples-auto.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"])
        w.writerows(allrows)
