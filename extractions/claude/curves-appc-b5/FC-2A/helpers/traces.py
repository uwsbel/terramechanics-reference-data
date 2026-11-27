"""Column scan of the two drawn envelope lines of FC-2A.

For every column u, the dark run nearest the rough line position is taken as the line's ink in
that column; its center is the line's center there. Columns where the run is much longer than the
line's own run (a symbol touching the line) or missing (a dash gap) are flagged. A straight line is
fitted to the clean columns of the solid part, and the samples asked for in TASK.md are produced:
left end on the shear-stress axis (x = 0), every 250 psf of normal stress, right end of the ink.
A sample is taken from the measured center of the ink in the columns around it (never from the
fit), and is skipped when it would fall in a dash gap or on a symbol (rule 7).

usage: python traces.py <page.png> <calibration.json> <out_prefix>
"""
import json
import sys

import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
cal = json.load(open(sys.argv[2], encoding="utf-8"))
ax, ay = cal["ax"], cal["ay"]
prefix = sys.argv[3]
X = lambda u, v: ax[0] * u + ax[1] * v + ax[2]
Y = lambda u, v: ay[0] * u + ay[1] * v + ay[2]
la = cal["left_axis"]
axis_u = lambda v: la["u_at_v0"] + la["slope_du_dv"] * v

markers = {   # centers from markers.py (hole centroid / outer extents)
    "s1": (1179.3, 2983.7), "s2": (1400.3, 2769.7), "s3": (1605.7, 2492.4), "s4": (1830.4, 2192.7),
    "s5": (2039.5, 2066.4), "s6": (2259.5, 1854.0), "c1": (1185.4, 3061.6), "c2": (1402.4, 2816.8),
    "c3": (1611.3, 2593.3), "c4": (1819.3, 2403.8), "c5": (2040.6, 2217.7), "c6": (2255.8, 2052.9),
}
lines = {   # rough (u, v) of the solid part's two ends, from the overview
    "upper": ((1020, 3165), (2333, 1654)),
    "lower": ((1033, 3220), (2374, 1818)),
}
MR = 19   # symbols are about 30 px across; columns within MR px of a marker center (in u) are suspect


def runs(col, off):
    idx = np.where(col)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s + off, p + off))
            s = i
        p = i
    out.append((s + off, p + off))
    return out


result = {}
for name, ((u0, v0), (u1, v1)) in lines.items():
    b = (v1 - v0) / (u1 - u0)
    a = v0 - b * u0
    cols = []
    for u in range(int(axis_u(3250)) - 2, 2420):
        vp = a + b * u
        rs = runs(g[int(vp) - 22:int(vp) + 23, u], int(vp) - 22)
        rs = [r for r in rs if abs((r[0] + r[1]) / 2 - vp) < 20]
        if not rs:
            cols.append((u, None, 0, "gap"))
            continue
        r = min(rs, key=lambda r: abs((r[0] + r[1]) / 2 - vp))
        near_marker = any(abs(u - mu) < MR and abs(vp - mv) < 45 for mu, mv in markers.values())
        cols.append((u, (r[0] + r[1]) / 2, r[1] - r[0] + 1, "marker?" if near_marker else "ok"))
    # refit on clean solid columns
    ok = [(u, c, L) for u, c, L, f in cols if f == "ok" and c is not None and u > u0 + 5 and u < u1 - 5]
    Ls = np.array([L for _, _, L in ok])
    Lmed = float(np.median(Ls))
    ok = [(u, c, L) for u, c, L in ok if abs(L - Lmed) <= 3]
    arr = np.array(ok, dtype=float)
    bb, aa = np.polyfit(arr[:, 0], arr[:, 1], 1)
    res = arr[:, 1] - (aa + bb * arr[:, 0])
    t_perp = Lmed / np.sqrt(1 + bb ** 2)
    result[name] = dict(a=aa, b=bb, Lmed=Lmed, t_perp=t_perp, rms=float(np.sqrt((res ** 2).mean())),
                        maxres=float(np.abs(res).max()), cols=cols)
    print(f"{name}: v = {aa:.2f} + {bb:.5f} u; vertical run median {Lmed:.0f} px, perpendicular thickness {t_perp:.1f} px; "
          f"fit rms {result[name]['rms']:.2f} px, max {result[name]['maxres']:.2f} px over {len(arr)} columns")
    # residual profile in 100-px bins (straightness check)
    for lo in range(int(arr[0, 0]) // 100 * 100, 2400, 100):
        m = (arr[:, 0] >= lo) & (arr[:, 0] < lo + 100)
        if m.any():
            print(f"   u {lo}-{lo + 99}: mean residual {res[m].mean():+.2f} px (n {m.sum()})")
    # ink extents: list gaps and long runs
    segs, cur = [], None
    for u, c, L, f in cols:
        has = c is not None
        if has and cur is None:
            cur = [u, u]
        elif has:
            cur[1] = u
        elif cur is not None:
            segs.append(tuple(cur))
            cur = None
    if cur:
        segs.append(tuple(cur))
    print("   ink segments (u ranges):", segs)
    longs = [(u, L) for u, c, L, f in cols if c is not None and L > Lmed + 3]
    if longs:
        groups, gcur = [], [longs[0][0], longs[0][0]]
        for u, L in longs[1:]:
            if u - gcur[1] <= 2:
                gcur[1] = u
            else:
                groups.append(tuple(gcur))
                gcur = [u, u]
        groups.append(tuple(gcur))
        print("   long-run column groups (symbol or axis contact):", groups)
    result[name]["segs"] = segs

json.dump({k: {kk: vv for kk, vv in v.items() if kk != "cols"} for k, v in result.items()},
          open(prefix + "_fits.json", "w"), indent=1, default=float)
# dump the per-column centers for inspection
with open(prefix + "_columns.csv", "w") as f:
    f.write("line,u,v_center,run_len,flag,x,y\n")
    for name, r in result.items():
        for u, c, L, fl in r["cols"]:
            if c is None:
                f.write(f"{name},{u},,0,{fl},,\n")
            else:
                f.write(f"{name},{u},{c},{L},{fl},{X(u, c):.1f},{Y(u, c):.1f}\n")
