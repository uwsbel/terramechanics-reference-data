"""Track B (the solid curve) through the column region using strokes that are separately visible,
then the spacings to C (above) and A (below). Initial prediction: band3 model M(u)."""
import json, csv
import numpy as np
from common import g, grid_at, runs_col
b3 = {int(k): v for k, v in json.load(open("band3.json")).items()}
U0, U1 = 790, 2075
def loess(pu, pv, span, at, deg=2):
    pu, pv = np.asarray(pu, float), np.asarray(pv, float)
    out = []
    for u in at:
        d = np.abs(pu - u) / span
        w = np.where(d < 1, (1 - d ** 3) ** 3, 0)
        if (w > 0).sum() < deg + 3: out.append(np.nan); continue
        X = np.vstack([(pu - u) ** k for k in range(deg + 1)]).T
        sw = np.sqrt(w)
        p, *_ = np.linalg.lstsq(X * sw[:, None], pv * sw, rcond=None)
        out.append(p[0])
    return np.array(out)
us_all = np.arange(U0, U1 + 1)
pred = np.array([b3[u]["M"] if u in b3 else np.nan for u in us_all])
ok = ~np.isnan(pred); pred = np.interp(us_all, us_all[ok], pred[ok])
def strokes(u, center):
    lo, hi = int(center) - 35, int(center) + 35
    if g[lo:hi + 1, u].mean() > 0.75: return None
    rr = runs_col(u, lo, hi)
    res = []
    for a, b in rr:
        if b - a < 3: continue
        gg = [grid_at(v, u) for v in range(a, b + 1)]
        if all(gg): continue
        res.append((a, b, any(gg)))
    return res
for it in range(4):
    obsB, obsSC, obsSA = [], [], []
    for i, u in enumerate(us_all):
        st = strokes(u, pred[i])
        if not st: continue
        clean = [(a, b) for a, b, gtouch in st if not gtouch]
        hs = [b - a + 1 for a, b in clean]
        # strokes of a single-line height (8..17 px)
        singles = [(a, b) for (a, b), h in zip(clean, hs) if 8 <= h <= 17]
        if not singles: continue
        cs = [0.5 * (a + b) for a, b in singles]
        j = int(np.argmin([abs(c - pred[i]) for c in cs]))
        if abs(cs[j] - pred[i]) <= 6:
            obsB.append((u, cs[j]))
            for k, c in enumerate(cs):
                if k == j: continue
                d = c - cs[j]
                if -20 <= d <= -8: obsSC.append((u, -d))
                if 8 <= d <= 22: obsSA.append((u, d))
    bu = [a for a, b in obsB]; bv = [b for a, b in obsB]
    newpred = loess(bu, bv, 45, us_all)
    ok = ~np.isnan(newpred)
    newpred = np.interp(us_all, us_all[ok], newpred[ok])
    # robust: drop obs far from fit and refit
    fit_at = dict(zip(us_all, newpred))
    keep = [(a, b) for a, b in obsB if abs(b - fit_at[a]) <= 3.5]
    newpred = loess([a for a, b in keep], [b for a, b in keep], 45, us_all)
    ok = ~np.isnan(newpred)
    pred = np.interp(us_all, us_all[ok], newpred[ok])
    print("iter", it, "B obs", len(obsB), "kept", len(keep), "SC", len(obsSC), "SA", len(obsSA))
sc = loess([a for a, b in obsSC], [b for a, b in obsSC], 120, us_all, deg=1)
sa = loess([a for a, b in obsSA], [b for a, b in obsSA], 120, us_all, deg=1)
sc = np.interp(us_all, us_all[~np.isnan(sc)], sc[~np.isnan(sc)])
sa = np.interp(us_all, us_all[~np.isnan(sa)], sa[~np.isnan(sa)])
out = {}
marks = []
for i, u in enumerate(us_all):
    out[int(u)] = dict(B=float(pred[i]), C=float(pred[i] - sc[i]), A=float(pred[i] + sa[i]), sc=float(sc[i]), sa=float(sa[i]))
    if u % 3 == 0:
        marks += [dict(u=u, v=round(pred[i] - sc[i], 1), s="C"), dict(u=u, v=round(pred[i], 1), s="B"), dict(u=u, v=round(pred[i] + sa[i], 1), s="A")]
json.dump(out, open("btrack.json", "w"))
json.dump(dict(B=obsB, SC=obsSC, SA=obsSA), open("btrack_obs.json", "w"))
with open("btrack_marks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["u", "v", "s"]); w.writeheader(); w.writerows(marks)
for u in range(U0, U1 + 1, 25):
    o = out[u]; print(u, f"C={o['C']:.1f} B={o['B']:.1f} A={o['A']:.1f} sc={o['sc']:.1f} sa={o['sa']:.1f}")
