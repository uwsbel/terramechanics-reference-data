"""Band model, column region: per column T, Bt (edges not touching grid ink). H3(u) = full three-stroke height
(upper envelope of Bt-T); classification of each column: both dashed strokes present / C missing / A missing;
band centre M(u) from each reliable edge, robustly smoothed. Writes band3.json and band3_marks.csv."""
import json, csv
import numpy as np
from common import g, grid_at, vc, runs_col
U0, U1 = 780, 2080
cols = {}
for u in range(U0 - 80, U1 + 81):
    c = int(round(vc(u))); lo, hi = c - 42, c + 42
    if g[lo:hi + 1, u].mean() > 0.75: continue
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
    Tok = not (grid_at(T, u) or grid_at(T - 1, u)); Bok = not (grid_at(Bt, u) or grid_at(Bt + 1, u))
    cols[u] = dict(T=T, Bt=Bt, Tok=Tok, Bok=Bok, runs=cl)
us = np.array(sorted(cols))
# H3: 85th percentile of Bt-T over +-70 where both edges ok
H = {u: cols[u]["Bt"] - cols[u]["T"] + 1 for u in us if cols[u]["Tok"] and cols[u]["Bok"]}
hu = np.array(sorted(H), float); hv = np.array([H[int(u)] for u in hu])
def H3(u):
    m = np.abs(hu - u) <= 70
    return float(np.percentile(hv[m], 85)) if m.sum() >= 8 else float(np.percentile(hv, 85))
H3u = {int(u): H3(u) for u in us}
# first pass centre from both-ok full-height columns
est = []   # (u, M, kind)
for u in us:
    c = cols[u]; h3 = H3u[int(u)]
    if c["Tok"] and c["Bok"] and (c["Bt"] - c["T"] + 1) >= h3 - 4:
        est.append((u, 0.5 * (c["T"] + c["Bt"]), "full"))
def smooth(points, span=45, iters=4, tol=4.0):
    pu = np.array([p[0] for p in points], float); pm = np.array([p[1] for p in points], float)
    keep = np.ones(len(pu), bool)
    def fit_at(u):
        d = np.abs(pu - u) / span
        w = np.where(d < 1, (1 - d ** 3) ** 3, 0) * keep
        if (w > 0).sum() < 4: return np.nan
        X = np.vstack([np.ones_like(pu), pu - u, (pu - u) ** 2]).T
        sw = np.sqrt(w)
        p, *_ = np.linalg.lstsq(X * sw[:, None], pm * sw, rcond=None)
        return p[0]
    for _ in range(iters):
        f = np.array([fit_at(u) for u in pu])
        keep = np.abs(pm - f) <= tol
    return lambda u: fit_at(u)
M0 = smooth(est)
# second pass: use partial columns too, classified against M0
est2 = list(est)
for u in us:
    c = cols[u]; h3 = H3u[int(u)]; m0 = M0(u)
    if np.isnan(m0): continue
    if c["Tok"] and abs(c["T"] - (m0 - h3 / 2)) <= 4:
        est2.append((u, c["T"] + h3 / 2, "top"))
    if c["Bok"] and abs(c["Bt"] - (m0 + h3 / 2)) <= 4:
        est2.append((u, c["Bt"] - h3 / 2, "bot"))
M = smooth(est2, span=40)
out, marks = {}, []
for u in range(U0, U1 + 1):
    m = M(u)
    if np.isnan(m): continue
    h3 = H3(u)
    c = cols.get(u)
    Cp = Ap = None
    if c is not None:
        if c["Tok"]: Cp = bool(c["T"] <= m - h3 / 2 + 4)
        if c["Bok"]: Ap = bool(c["Bt"] >= m + h3 / 2 - 4)
    out[u] = dict(M=float(m), H3=h3, Cp=Cp, Ap=Ap, T=c["T"] if c else None, Bt=c["Bt"] if c else None,
                  runs=" ".join(f"{a}-{b}" for a, b in c["runs"]) if c else "")
json.dump(out, open("band3.json", "w"))
print("ok", len(out))
for u in range(U0, U1 + 1, 20):
    if u in out: print(u, f"M={out[u]['M']:.1f} H3={out[u]['H3']:.0f}")
