"""Dense center line of one panel's trace of Figure 5-25, from chords of the ink.

Along lines of constant time (every 0.0001 s, about 1.7 px) the trace's chord is found in the page
ink with thin horizontal dashes removed (the time lines; vertical opening of 5 px, the trace being 5 to
8 px thick); its midpoint lies on the center line of a locally straight band. Where the trace is steep
(a chord longer than 14 px) chords along lines of constant load (every 0.5 lb) are used instead. A chord
touching a vertical grid line's band, or a chord along a grid line itself, is left out. The run is
tracked from a seed by continuity. Writes centerline-p<n>.json: points (u, v, x, y, chord, kind)."""
import json
import sys
import numpy as np
from trace_tools import Panel, THICK, vline_band

n = int(sys.argv[1])
seed_t, seed_u = float(sys.argv[2]), float(sys.argv[3])
t_lo, t_hi = float(sys.argv[4]), float(sys.argv[5])
out = sys.argv[6]
P = Panel(n)
U0, U1 = P.urange
GRIDY = {1: [0, 20, 40, 60, 80, 100], 2: [0, 20, 40, 60], 3: [0, -20, -40, -60, -80, -100]}[n]


def runs_along(points, band_check=True):
    """points: list of (u, v) along a path; returns runs of THICK ink: (i_a, i_b, touches_band)."""
    on = [THICK[int(round(v)), int(round(u))] for u, v in points]
    band = [vline_band(u, v) for u, v in points] if band_check else [False] * len(points)
    res, s = [], None
    for i, f in enumerate(on + [False]):
        if f and s is None:
            s = i
        if not f and s is not None:
            a, b = s, i - 1
            free = sum(1 for k in range(a, b + 1) if not band[k])
            if free >= 3:
                res.append((a, b, bool(band[a] or band[b] or (b - a + 1) != free)))
            s = None
    return res


def tline(t):
    us = np.arange(U0, U1 + 1, dtype=float)
    va, vb = P.v_at_t(U0, t), P.v_at_t(U1, t)
    return [(u, va + (vb - va) * (u - U0) / (U1 - U0)) for u in us]


# 1. chords along constant time, tracked both ways from the seed
pts = []
ts_up = np.arange(seed_t, t_hi + 1e-9, 0.0001)
ts_dn = np.arange(seed_t - 0.0001, t_lo - 1e-9, -0.0001)
for ts in (ts_up, ts_dn):
    prev = seed_u
    miss = 0
    for t in ts:
        path = tline(t)
        cands = []
        for a, b, amb in runs_along(path):
            um = (path[a][0] + path[b][0]) / 2
            cands.append((abs(um - prev), a, b, amb, um))
        if not cands:
            miss += 1; continue
        d, a, b, amb, um = min(cands)
        if d > 25 + 10 * miss:
            miss += 1; continue
        miss = 0
        prev = um
        vm = (path[a][1] + path[b][1]) / 2
        L = b - a + 1
        if amb:
            pts.append({"kind": "row-amb", "u": um, "v": vm, "chord": L, "t": float(t)}); continue
        pts.append({"kind": "row", "u": um, "v": vm, "chord": L, "t": float(t)})

# 2. chords along constant load where the row chords are long (steep stretches)
steep = [p for p in pts if p["kind"] == "row" and p["chord"] > 14] + [p for p in pts if p["kind"] == "row-amb" and p["chord"] > 14]
row_ok = sorted([p for p in pts if p["kind"] in ("row", "row-amb")], key=lambda p: p["t"])
col = []
if steep:
    # group steep stretches by time
    st = sorted(steep, key=lambda p: p["t"])
    groups, g = [], [st[0]]
    for p in st[1:]:
        if p["t"] - g[-1]["t"] <= 0.0006:
            g.append(p)
        else:
            groups.append(g); g = [p]
    groups.append(g)
    for g in groups:
        # extend each stretch a little in time, take its load range
        t1, t2 = g[0]["t"] - 0.0008, g[-1]["t"] + 0.0008
        near = [p for p in row_ok if t1 <= p["t"] <= t2]
        ys = [P.xy(p["u"], p["v"])[1] for p in near]
        vlo = min(p["v"] for p in near) - 12
        vhi = max(p["v"] for p in near) + 12
        y_lo, y_hi = min(ys), max(ys)
        for y in np.arange(np.ceil(y_lo * 2) / 2, y_hi + 1e-9, 0.5):
            if any(abs(y - gy) < 1.6 for gy in GRIDY):
                continue
            ua, ub = P.u_at_y(vlo, y), P.u_at_y(vhi, y)
            vs = np.arange(int(vlo), int(vhi) + 1, dtype=float)
            path = [(ua + (ub - ua) * (v - vlo) / (vhi - vlo), v) for v in vs]
            rr = runs_along(path, band_check=True)
            if not rr:
                continue
            # the run nearest the row-chord center line at this load
            best = None
            for a, b, amb in rr:
                vm = (path[a][1] + path[b][1]) / 2
                um = (path[a][0] + path[b][0]) / 2
                dmin = min(np.hypot(p["u"] - um, p["v"] - vm) for p in near)
                if best is None or dmin < best[0]:
                    best = (dmin, a, b, amb, um, vm)
            dmin, a, b, amb, um, vm = best
            if dmin > 12 or b - a + 1 > 14:
                continue
            col.append({"kind": "col-amb" if amb else "col", "u": um, "v": vm, "chord": b - a + 1, "y_target": float(y)})
allp = pts + col
for p in allp:
    p["x"], p["y"] = P.xy(p["u"], p["v"])
allp.sort(key=lambda p: p["x"])
json.dump({"panel": n, "points": allp}, open(out, "w", encoding="utf-8"), indent=0)
k = {}
for p in allp:
    k[p["kind"]] = k.get(p["kind"], 0) + 1
print(f"panel {n}: {len(allp)} points {k}; t from {allp[0]['x']:.4f} to {allp[-1]['x']:.4f}")
