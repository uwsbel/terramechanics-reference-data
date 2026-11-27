"""Classify each column of the band profile (profile.py cols) as three lines (3), or two lines with the top
dashed curve (lower series, L) or the bottom dashed curve (upper series, U) in a gap; centre of each
curve in that column. Two lines are 21 to 24 px high, three lines 30 to 34 (lines touching, about 10.5 px
each). In a two-line column the missing line is the one whose edge has moved inward by more than half a
line from the trend of the three-line columns around it (both edges are tested; a column where they
disagree is marked '?'). Writes cols_classified.csv."""
import csv, sys
from pathlib import Path
import numpy as np
base = Path(__file__).resolve().parents[1]
seen = {}
for f in sorted((base / "helpers").glob("profile_cols_*.csv")):
    for r in csv.DictReader(f.open(encoding="utf-8")):
        seen[int(r["pos"])] = r
u0, u1 = int(sys.argv[1]), int(sys.argv[2])
U = [u for u in sorted(seen) if u0 <= u <= u1]
R = [seen[u] for u in U]
Ua = np.array(U, float)
T = np.array([int(r["lo_edge"]) for r in R], float); B = np.array([int(r["hi_edge"]) for r in R], float)
H = B - T + 1
Tg = np.array([bool(r["lo_on_grid"]) for r in R]); Bg = np.array([bool(r["hi_on_grid"]) for r in R])
three = (H >= 28) & (H <= 38)
two = (H >= 19) & (H <= 26)
def pred(mask, y, u, half=40):
    for hh in (half, 2 * half, 3 * half):
        m = mask & (np.abs(Ua - u) <= hh)
        if m.sum() >= 4 and np.ptp(Ua[m]) > 6:
            return float(np.polyval(np.polyfit(Ua[m], y[m], 1), u))
    return None
rows = []
for i, u in enumerate(U):
    h2 = np.median(H[two & ~Tg & ~Bg & (np.abs(Ua - u) <= 80)]) / 2 if (two & ~Tg & ~Bg & (np.abs(Ua - u) <= 80)).sum() >= 3 else 10.75
    cls = "3" if three[i] else ("2" if two[i] else "?")
    tp = pred(three & ~Tg, T, u); bp = pred(three & ~Bg, B, u)
    miss = ""
    if cls == "2" and tp is not None and bp is not None:
        lmiss = (T[i] - tp) > 0.5 * h2
        umiss = (bp - B[i]) > 0.5 * h2
        miss = "L" if lmiss and not umiss else ("U" if umiss and not lmiss else "?")
    L = A = Uc = ""
    if cls == "3":
        L, A, Uc = T[i] + h2 / 2, (T[i] + B[i]) / 2, B[i] - h2 / 2
    elif cls == "2" and miss == "L":
        A, Uc = T[i] + h2 / 2, B[i] - h2 / 2
    elif cls == "2" and miss == "U":
        L, A = T[i] + h2 / 2, B[i] - h2 / 2
    rows.append({"u": u, "T": int(T[i]), "B": int(B[i]), "H": int(H[i]), "cls": cls + ("-" + miss if miss else ""),
                 "Tg": int(Tg[i]), "Bg": int(Bg[i]), "h": round(h2, 2), "Tpred": "" if tp is None else round(tp, 1),
                 "Bpred": "" if bp is None else round(bp, 1),
                 "L": "" if L == "" else round(L, 1), "A": "" if A == "" else round(A, 1), "U": "" if Uc == "" else round(Uc, 1)})
with (base / "helpers" / f"cols_classified_{u0}_{u1}.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
# segments
seg = []
for r in rows:
    k = r["cls"]
    if seg and seg[-1][0] == k and r["u"] - seg[-1][2] <= 8:
        seg[-1][2] = r["u"]; seg[-1][3] += 1
    else:
        seg.append([k, r["u"], r["u"], 1])
print(" ".join(f"[{a}-{b} {k} n{n}]" for k, a, b, n in seg))
