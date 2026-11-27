"""Centrelines of A, B, C in the column-cut region from the envelopes (env2.json).
C = Tf + wv/2, A = Bf - wv/2, B = Tf + f (Bf - Tf) with f from columns where B's own edge is visible.
wv = WPERP * sqrt(1 + slope^2) (vertical extent of one stroke). Writes centers_col.json and marks csv."""
import json, csv
import numpy as np
WPERP = 11.0
e = {int(k): v for k, v in json.load(open("env2.json")).items()}
us = np.array(sorted(e), float)
Tf = np.array([e[int(u)]["Tf"] for u in us]); Bf = np.array([e[int(u)]["Bf"] for u in us])
mid = 0.5 * (Tf + Bf)
slope = np.gradient(mid, us)
# smooth slope
k = 15
slope_s = np.array([np.median(slope[max(0, i - k):i + k + 1]) for i in range(len(us))])
wv = WPERP * np.sqrt(1 + slope_s ** 2)
fs, fu, how = [], [], []
for i, u in enumerate(us.astype(int)):
    o = e[u]
    runs = [tuple(map(int, r.split("-"))) for r in o["runs"].split()]
    B = None
    if len(runs) == 3 and all(b - a >= 6 for a, b in runs):
        B = 0.5 * (runs[1][0] + runs[1][1]); h = "3runs"
    elif o["Cp"] is False and not o["Tg"]:
        B = o["T"] + wv[i] / 2 - 0.5; h = "Cgap"
    elif o["Ap"] is False and not o["Bg"]:
        B = o["Bt"] - wv[i] / 2 + 0.5; h = "Agap"
    if B is not None and Bf[i] - Tf[i] > 15:
        f = (B - Tf[i]) / (Bf[i] - Tf[i])
        if 0.2 < f < 0.8:
            fs.append(f); fu.append(u); how.append(h)
fs, fu = np.array(fs), np.array(fu, float)
fsm = np.array([np.median(fs[np.abs(fu - u) <= 60]) if (np.abs(fu - u) <= 60).sum() >= 5 else np.nan for u in us])
# fill nans by interpolation
ok = ~np.isnan(fsm)
fsm = np.interp(us, us[ok], fsm[ok])
out = {}
marks = []
for i, u in enumerate(us.astype(int)):
    C = Tf[i] + wv[i] / 2 - 0.5
    A = Bf[i] - wv[i] / 2 + 0.5
    B = Tf[i] + fsm[i] * (Bf[i] - Tf[i])
    out[int(u)] = dict(C=float(C), B=float(B), A=float(A), wv=float(wv[i]), f=float(fsm[i]), Cp=e[u]["Cp"], Ap=e[u]["Ap"],
                       Tg=e[u]["Tg"], Bg=e[u]["Bg"], Tf=float(Tf[i]), Bf=float(Bf[i]), runs=e[u]["runs"])
    if u % 3 == 0:
        for s, v in (("C", C), ("B", B), ("A", A)):
            marks.append(dict(u=u, v=round(v, 1), s=s))
json.dump(out, open("centers_col.json", "w"))
with open("centers_marks.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["u", "v", "s"]); w.writeheader(); w.writerows(marks)
print("f samples", len(fs), "by", {h: how.count(h) for h in set(how)})
for u in range(800, 2081, 40):
    i = int(np.argmin(np.abs(us - u)))
    print(int(us[i]), f"f={fsm[i]:.2f} wv={wv[i]:.1f} slope={slope_s[i]:.2f}")
