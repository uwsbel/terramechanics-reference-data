"""Robust envelopes of the merged band, column-based (u 790..2075): Tf(u) = C's outer (top) edge,
Bf(u) = A's outer (bottom) edge, by LOESS (tricube, local quadratic, span +-SPAN px) with iterative rejection
of retracted points (dash gaps) and outward outliers (stray ink). Writes env2.json and env2_marks.csv."""
import json, csv
import numpy as np
from common import g, grid_at, vc, runs_col
U0, U1, SPAN = 780, 2080, 50
data = {}
for u in range(U0 - SPAN, U1 + SPAN + 1):
    c = int(round(vc(u))); lo, hi = c - 42, c + 42
    seg = g[lo:hi + 1, u]
    if seg.mean() > 0.75: continue
    rr = runs_col(u, lo, hi)
    band = [(a, b) for a, b in rr if b - a >= 2 and not all(grid_at(v, u) for v in range(a, b + 1))]
    if not band: continue
    groups, cl = [], [band[0]]
    for r in band[1:]:
        if r[0] - cl[-1][1] <= 10: cl.append(r)
        else: groups.append(cl); cl = [r]
    groups.append(cl)
    cl = max(groups, key=lambda cc: sum(b - a + 1 for a, b in cc))
    T, Bt = cl[0][0], cl[-1][1]
    Tg = grid_at(T, u) or grid_at(T - 1, u); Bg = grid_at(Bt, u) or grid_at(Bt + 1, u)
    data[u] = dict(T=T, Bt=Bt, Tg=bool(Tg), Bg=bool(Bg), runs=cl)
def loess(us, vs, side, inward_tol=3.0, out_tol=5.0):
    us, vs = np.array(us, float), np.array(vs, float)
    keep = np.ones(len(us), bool)
    fit = np.zeros(len(us))
    for it in range(8):
        for i, u in enumerate(us):
            d = np.abs(us - u) / SPAN
            w = np.where(d < 1, (1 - d ** 3) ** 3, 0) * keep
            if (w > 0).sum() < 5:
                fit[i] = np.nan; continue
            X = np.vstack([np.ones_like(us), us - u, (us - u) ** 2]).T
            Wm = np.sqrt(w)[:, None]
            p, *_ = np.linalg.lstsq(X * Wm, vs * Wm[:, 0], rcond=None)
            fit[i] = p[0]
        res = (vs - fit) * side          # positive = outward
        newkeep = (res > -inward_tol) & (res < out_tol) & ~np.isnan(fit)
        if (newkeep == keep).all(): break
        keep = newkeep
    return fit, keep
uT = [u for u in sorted(data) if not data[u]["Tg"]]
uB = [u for u in sorted(data) if not data[u]["Bg"]]
fT, kT = loess(uT, [data[u]["T"] for u in uT], -1)
fB, kB = loess(uB, [data[u]["Bt"] for u in uB], +1)
allu = np.array(sorted(data), float)
Tf = np.interp(allu, np.array(uT, float)[~np.isnan(fT)], fT[~np.isnan(fT)])
Bf = np.interp(allu, np.array(uB, float)[~np.isnan(fB)], fB[~np.isnan(fB)])
keepT = dict(zip(uT, kT)); keepB = dict(zip(uB, kB))
out = {}
marks = []
for u, tf, bf in zip(allu.astype(int), Tf, Bf):
    d = data[u]
    Cp = None if d["Tg"] else bool(d["T"] <= tf + 4.0)
    Ap = None if d["Bg"] else bool(d["Bt"] >= bf - 4.0)
    out[int(u)] = dict(T=d["T"], Bt=d["Bt"], Tg=d["Tg"], Bg=d["Bg"], Tf=float(tf), Bf=float(bf), Cp=Cp, Ap=Ap,
                       runs=" ".join(f"{a}-{b}" for a, b in d["runs"]))
    if U0 <= u <= U1 and u % 3 == 0:
        h = (bf - tf + 1) / 3
        marks.append(dict(u=u, v=round(tf + h / 2, 1), s="C"))
        marks.append(dict(u=u, v=round((tf + bf) / 2, 1), s="B"))
        marks.append(dict(u=u, v=round(bf - h / 2, 1), s="A"))
json.dump(out, open("env2.json", "w"))
with open("env2_marks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["u", "v", "s"]); w.writeheader(); w.writerows(marks)
print("columns", len(out))
