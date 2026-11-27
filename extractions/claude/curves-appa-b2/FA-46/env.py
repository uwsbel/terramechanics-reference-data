"""Column-based envelope analysis of the merged band (u 790..2070).
Per column: T, Bt (band top/bottom excluding grid-row ink), flags when adjacent to grid ink or vertical grid line.
Envelope fits: C top edge (T) and A bottom edge (Bt) by robust local quadratic fits; a column where the edge is
retracted by more than RET px from the fit is a dash gap of that curve."""
import csv, json, sys
import numpy as np
from common import g, grid_at, vc, runs_col
U0, U1 = 790, 2075
RET = 5.0
cols = {}
for u in range(U0 - 40, U1 + 41):
    c = int(round(vc(u))); lo, hi = c - 42, c + 42
    seg = g[lo:hi + 1, u]
    if seg.mean() > 0.75:
        continue   # vertical grid line column
    rr = runs_col(u, lo, hi)
    band = [(a, b) for a, b in rr if b - a >= 2 and not all(grid_at(v, u) for v in range(a, b + 1))]
    if not band:
        continue
    # keep the cluster of runs around the centre: drop runs separated from the main cluster by > 10 px
    cl = [band[0]]
    best = []
    for r in band[1:]:
        if r[0] - cl[-1][1] <= 10: cl.append(r)
        else:
            best.append(cl); cl = [r]
    best.append(cl)
    cl = max(best, key=lambda cc: sum(b - a + 1 for a, b in cc))
    T, Bt = cl[0][0], cl[-1][1]
    # edge touching grid ink (the band run merges into a grid line) is unreliable
    Tg = grid_at(T, u) or grid_at(T - 1, u)
    Bg = grid_at(Bt, u) or grid_at(Bt + 1, u)
    cols[u] = dict(T=T, Bt=Bt, Tg=Tg, Bg=Bg, runs=cl)
def robust_fit(us, vs, center, side):
    # quadratic in (u-center); side=-1 for top envelope (smaller v is outer), +1 for bottom
    us, vs = np.array(us, float), np.array(vs, float)
    keep = np.ones(len(us), bool)
    for _ in range(6):
        if keep.sum() < 6: break
        p = np.polyfit(us[keep] - center, vs[keep], 2)
        res = (vs - np.polyval(p, us - center)) * side   # positive = outward
        # retracted (inward) points beyond RET are gaps
        newkeep = res > -RET
        if (newkeep == keep).all(): break
        keep = newkeep
    return p
out = {}
for u in range(U0, U1 + 1):
    if u not in cols: continue
    win = [w for w in range(u - 30, u + 31) if w in cols]
    tu = [w for w in win if not cols[w]["Tg"]]
    bu = [w for w in win if not cols[w]["Bg"]]
    pT = robust_fit(tu, [cols[w]["T"] for w in tu], u, -1) if len(tu) >= 8 else None
    pB = robust_fit(bu, [cols[w]["Bt"] for w in bu], u, +1) if len(bu) >= 8 else None
    c = cols[u]
    Tf = float(np.polyval(pT, 0)) if pT is not None else None
    Bf = float(np.polyval(pB, 0)) if pB is not None else None
    slopeT = float(pT[1]) if pT is not None else None
    Cp = None if (Tf is None or c["Tg"]) else bool(c["T"] <= Tf + RET)
    Ap = None if (Bf is None or c["Bg"]) else bool(c["Bt"] >= Bf - RET)
    out[u] = dict(T=c["T"], Bt=c["Bt"], Tg=c["Tg"], Bg=c["Bg"], Tf=Tf, Bf=Bf, slope=slopeT, Cp=Cp, Ap=Ap,
                  runs=" ".join(f"{a}-{b}" for a, b in c["runs"]))
json.dump(out, open("env.json", "w"))
for u in range(U0, U1 + 1, 5):
    if u in out:
        o = out[u]
        print(u, o["T"], o["Bt"], "Tg" if o["Tg"] else "  ", "Bg" if o["Bg"] else "  ",
              f"Tf={o['Tf']:.1f}" if o["Tf"] is not None else "Tf=-", f"Bf={o['Bf']:.1f}" if o["Bf"] is not None else "Bf=-",
              "C" if o["Cp"] else ("c" if o["Cp"] is False else "?"), "A" if o["Ap"] else ("a" if o["Ap"] is False else "?"), o["runs"])
