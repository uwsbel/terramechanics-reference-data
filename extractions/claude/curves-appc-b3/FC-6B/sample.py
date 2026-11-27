"""Pick trace samples from a dense track (track.py).

Every column with line ink gets an estimate of the line center:
  clean  : the run's center (no grid line, no symbol in the column);
  hgrid  : the run merges with a horizontal grid line; the line center is taken from the run's
           free edge (top + tl/2 or bottom - tl/2, tl = the line's own vertical thickness from the
           clean columns nearby), the edge being chosen by the guide; when the run is no thicker
           than the line itself, its center. These carry a wider bound and a note.
Columns within --vgrid-excl of a vertical grid line or inside a symbol box are never sampled.
Consecutive estimated columns form dashes; a sample goes 3 px inside each end of every dash and
interior samples no more than --step px apart, preferring clean columns within +-6 px.
Columns whose run is thinner than --min-rel-thick of the local median (a scan dropout, a tapered
dash end) are not clean. v is the mean over the column and its two neighbours; v_bound is half the largest run thickness
of the three for a clean sample, tl/2 + 2 for a grid-merged one.

python sample.py tracks/n4695.csv guides/n4695.csv --u-min 721 --u-max 2075 [--step 26]
"""
import argparse
import csv

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("track")
ap.add_argument("guide")
ap.add_argument("--u-min", type=int, default=0)
ap.add_argument("--u-max", type=int, default=99999)
ap.add_argument("--step", type=int, default=26)
ap.add_argument("--max-thick", type=int, default=45)
ap.add_argument("--min-len", type=int, default=8)
ap.add_argument("--jump", type=float, default=4)
ap.add_argument("--min-rel-thick", type=float, default=0.7)
a = ap.parse_args()

rows = {int(r["u"]): r for r in csv.DictReader(open(a.track, encoding="utf-8"))}
gd = {int(r["u"]): float(r["v"]) for r in csv.DictReader(open(a.guide, encoding="utf-8"))}


def flags(u):
    return set(rows[u]["flags"].split("|")) if u in rows else {"none"}


clean = {}
for u, r in rows.items():
    if a.u_min <= u <= a.u_max and r["v"] != "" and not (flags(u) & {"vgrid", "hgrid", "symbol", "none"}):
        t = int(r["thick"])
        if 5 <= t <= a.max_thick:
            clean[u] = (float(r["v"]), t)


# drop partial runs (a scan dropout leaves only part of the line's width, or a tapered dash end):
# a clean column must be at least --min-rel-thick of the median thickness within +-40 columns
_med = {u: float(np.median([clean[x][1] for x in clean if abs(x - u) <= 40])) for u in clean}
clean = {u: c for u, c in clean.items() if c[1] >= a.min_rel_thick * _med[u]}


def tl_near(u):
    ts = [clean[x][1] for x in clean if abs(x - u) <= 40]
    return float(np.median(ts)) if ts else 13.0


est = {}   # u -> (v, half_bound, kind)
for u, r in rows.items():
    if not (a.u_min <= u <= a.u_max) or r["v"] == "":
        continue
    fl = flags(u)
    if u in clean:
        est[u] = (clean[u][0], clean[u][1] / 2, "clean")
    elif "hgrid" in fl and not (fl & {"vgrid", "symbol"}):
        top, bot = float(r["top"]), float(r["bot"])
        tl = tl_near(u)
        if bot - top + 1 <= tl + 1:
            v = (top + bot) / 2
        else:
            c_top, c_bot = top + tl / 2, bot - tl / 2
            g = gd.get(u, (c_top + c_bot) / 2)
            v = c_top if abs(c_top - g) <= abs(c_bot - g) else c_bot
        est[u] = (v, tl / 2 + 2, "hgrid")

cols = sorted(est)
dashes, cur = [], []
for u in cols:
    if cur and (u != cur[-1] + 1 or abs(est[u][0] - est[cur[-1]][0]) > a.jump):
        dashes.append(cur)
        cur = []
    cur.append(u)
if cur:
    dashes.append(cur)
dashes = [d for d in dashes if len(d) >= a.min_len]

print("u,v,v_bound,kind,dash")
for k, d in enumerate(dashes):
    lo, hi = d[0] + 3, d[-1] - 3
    n = max(1, -(-(hi - lo) // a.step))
    targets = sorted(set([lo + round(i * (hi - lo) / n) for i in range(n + 1)])) if hi - lo >= 10 else [(lo + hi) // 2]
    used = []
    for t in targets:
        u = t
        if est[t][2] != "clean":
            for dd in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6):
                x = t + dd
                if x in d and lo <= x <= hi and est[x][2] == "clean":
                    u = x
                    break
        if u in used:
            continue
        used.append(u)
        nb = [x for x in (u - 1, u, u + 1) if x in d]
        vs = [est[x][0] for x in nb]
        bs = [est[x][1] for x in nb]
        print(f"{u},{sum(vs) / len(vs):.1f},{max(bs):.1f},{est[u][2]},{k}")
