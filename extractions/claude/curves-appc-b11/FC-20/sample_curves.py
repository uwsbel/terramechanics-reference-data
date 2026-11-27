"""Trace samples of the FC-20 curves at every 0.05 of Dr, from the column traces (reader's helper).

Inputs: trace-<curve>.csv written by trace_curves.py (centre of the curve's ink in every column),
cal-p1/ (the grid lines, via tools/calibrate_axes.py piecewise_maps), and the stretches of ink of
each curve as read on the zoomed crops (DASHES below). Steps:
1. Line thickness: median over clean columns of run length / sqrt(1 + slope^2).
2. Usable columns: clean ink; a column whose run touches a horizontal grid line keeps the curve's
   free edge and puts the centre half a (vertical) line width from it, on the side the curve lies;
   columns merged with a circle, specks (run < 4 px) and columns outside the stretches are dropped.
3. A sample at Dr = d is where the x map along the usable columns crosses d, interpolated between
   two usable columns at most 18 px apart (bridging a vertical grid line, whose ink hides the
   curve's over ~15 px). If d falls in a gap between stretches, the sample moves to the nearest
   stretch end, on its ink (the centre of the last usable column of that stretch).
Prints one line per sample; writes samples-<curve>.csv (dr_target, u, v, how).
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
import calibrate_axes as ca  # noqa: E402

cal, X, Y = ca.piecewise_maps(str(HERE / "cal-p1"))
HL = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]

# stretches of ink read on the crops (first and last column of each dash), page u
DASHES = {
    "mean": [(812, 2322)],
    "upper": [(800, 971), (1004, 1100), (1128, 1241), (1278, 1395), (1440, 1485), (1491, 1500),
              (1506, 1524), (1527, 1545), (1581, 1659), (1683, 1799), (1827, 1908), (1952, 2062),
              (2119, 2261), (2284, 2336)],
    "lower": [(804, 976), (1029, 1189), (1217, 1351), (1377, 1482), (1504, 1602), (1615, 1752),
              (1777, 1944), (1987, 2139), (2173, 2341)],
}


def xval(u, v):
    return X.value(u, v)[0]


def load(name):
    rows = list(csv.DictReader((HERE / f"trace-{name}.csv").open(encoding="utf-8")))
    return [(int(r["u"]), float(r["v"]) if r["v"] else None, int(r["run"]) if r["run"] else 0, r["status"]) for r in rows]


def thickness(rows):
    clean = [(u, v, r) for u, v, r, s in rows if s == "ink" and r >= 4]
    U = np.array([c[0] for c in clean], float)
    V = np.array([c[1] for c in clean], float)
    R = np.array([c[2] for c in clean], float)
    T = []
    for i in range(len(U)):
        m = np.abs(U - U[i]) <= 10
        if m.sum() >= 6:
            k = np.polyfit(U[m], V[m], 1)[0]
            T.append(R[i] / np.sqrt(1 + k * k))
    return float(np.median(T)), float(np.percentile(T, 10)), float(np.percentile(T, 90))


def usable(name, rows, T):
    dash = DASHES[name]
    clean = {u: v for u, v, r, s in rows if s == "ink" and r >= 4}
    out = {}
    for u, v, r, s in rows:
        if v is None or not any(a <= u <= b for a, b in dash) or r < 4 and s != "ink":
            continue
        if s == "ink":
            out[u] = (v, "ink")
        elif s == "hgrid":
            # neighbours' line to tell the side and the local slope
            nb = [(uu, clean[uu]) for uu in range(u - 40, u + 41) if uu in clean]
            if len(nb) < 6:
                continue
            k, c = np.polyfit([p[0] for p in nb], [p[1] for p in nb], 1)
            pred = k * u + c
            vh = min((a + b * u for a, b in HL), key=lambda x: abs(x - pred))
            tv = T * np.sqrt(1 + k * k)
            half = r / 2
            top, bot = v - half + 0.5, v + half - 0.5
            cen = top + (tv - 1) / 2 if pred < vh else bot - (tv - 1) / 2
            out[u] = (cen, f"hgrid free edge (run {r}, pred {pred:.1f})")
    return out


def sample(name, extra_targets=()):
    rows = load(name)
    T, t10, t90 = thickness(rows)
    use = usable(name, rows, T)
    us = sorted(use)
    pts = [(u, use[u][0], xval(u, use[u][0])) for u in us]
    first, last = pts[0], pts[-1]
    print(f"{name}: thickness median {T:.1f} px (10th {t10:.1f}, 90th {t90:.1f}); usable columns {len(us)}; "
          f"ink from u {first[0]} (Dr {first[2]:.4f}) to u {last[0]} (Dr {last[2]:.4f})")
    targets = [d for d in np.round(np.arange(0, 1.0001, 0.05), 2) if first[2] < d < last[2]]
    res = []
    for d in targets:
        hit = None
        for (u0, v0, x0), (u1, v1, x1) in zip(pts, pts[1:]):
            if (x0 - d) * (x1 - d) <= 0 and u1 - u0 <= 18:
                f = 0 if x1 == x0 else (d - x0) / (x1 - x0)
                hit = (u0 + f * (u1 - u0), v0 + f * (v1 - v0), f"interp {u0}-{u1}" + (" " + use[u0][1] if use[u0][1] != "ink" else "") + (" " + use[u1][1] if use[u1][1] != "ink" else ""))
                break
        if hit is None:
            # in a gap: nearest stretch end (by Dr)
            ends = []
            for a, b in DASHES[name]:
                ua = min((u for u in us if a <= u <= b), default=None)
                ub = max((u for u in us if a <= u <= b), default=None)
                for e in (ua, ub):
                    if e is not None:
                        ends.append((abs(xval(e, use[e][0]) - d), e))
            _, e = min(ends)
            hit = (float(e), use[e][0], f"gap: moved to dash end u {e} (Dr {xval(e, use[e][0]):.4f})")
        res.append((d, *hit))
        print(f"   Dr {d:.2f}: u {hit[0]:.1f} v {hit[1]:.1f}  {hit[2]}")
    with (HERE / f"samples-{name}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["dr_target", "u", "v", "how"])
        for r in res:
            w.writerow([r[0], round(r[1], 1), round(r[2], 1), r[3]])
    return T


for n in ("mean", "upper", "lower"):
    sample(n)
