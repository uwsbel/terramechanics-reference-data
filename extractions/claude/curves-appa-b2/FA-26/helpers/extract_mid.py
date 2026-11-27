"""Centre of each curve, column by column, in the flat middle of the band (u 690 to 1860), from columns whose
two band edges are not on a grid line (profile.py cols). Three lines touching: 28 to 36 px; two lines: 19 to
26 px (one dashed curve in a gap). Lower series (L) is the top line, upper series (U) the bottom line,
average (A) the middle (solid, continuous). In a two-line column the missing line is the one whose edge sits
more than half a line inside the trend of the clean three-line columns within 40 to 120 px. Writes
mid_obs.csv: u, curve, v_centre, kind (3 / 2L / 2U meaning which line is missing)."""
import csv
from pathlib import Path
import numpy as np
base = Path(__file__).resolve().parents[1]
seen = {}
for f in sorted((base / "helpers").glob("profile_cols_*.csv")):
    for r in csv.DictReader(f.open(encoding="utf-8")):
        seen[int(r["pos"])] = r
U = [u for u in sorted(seen) if 640 <= u <= 1880]
R = [seen[u] for u in U]
Ua = np.array(U, float)
T = np.array([int(r["lo_edge"]) for r in R], float); B = np.array([int(r["hi_edge"]) for r in R], float)
# an edge on a thin grid row (3 px or less) is taken at the middle of that row (error 1.5 px or less);
# an edge on a thicker grid row makes the column unusable
def thin(tag):
    if not tag:
        return True, None
    a, b = map(int, tag.split("-"))
    return (b - a + 1) <= 3, (a + b + 1) / 2
okT, okB = [], []
for i, r in enumerate(R):
    o, m = thin(r["lo_on_grid"]); okT.append(o)
    if m is not None and o: T[i] = m
    o, m = thin(r["hi_on_grid"]); okB.append(o)
    if m is not None and o: B[i] = m
H = B - T + 1
clean = np.array(okT) & np.array(okB)
three = clean & (H >= 28) & (H <= 36)
two = clean & (H >= 19) & (H <= 26)
def pred(mask, y, u):
    for hh in (40, 80, 120):
        m = mask & (np.abs(Ua - u) <= hh)
        if m.sum() >= 4 and np.ptp(Ua[m]) > 6:
            return float(np.polyval(np.polyfit(Ua[m], y[m], 1), u))
    return None
out = []
for i, u in enumerate(U):
    if not (three[i] or two[i]):
        continue
    # local vertical line thickness from clean two-line columns (half their height), else 10.75
    m2 = two & (np.abs(Ua - u) <= 100)
    h = float(np.median(H[m2]) / 2) if m2.sum() >= 3 else 10.75
    if three[i]:
        out += [(u, "lower", T[i] + h / 2, "3"), (u, "average", (T[i] + B[i]) / 2, "3"), (u, "upper", B[i] - h / 2, "3")]
        continue
    tp, bp = pred(three, T, u), pred(three, B, u)
    if tp is None or bp is None:
        continue
    lmiss, umiss = (T[i] - tp) > h / 2, (bp - B[i]) > h / 2
    if lmiss and not umiss:
        out += [(u, "average", T[i] + h / 2, "2L"), (u, "upper", B[i] - h / 2, "2L")]
    elif umiss and not lmiss:
        out += [(u, "lower", T[i] + h / 2, "2U"), (u, "average", B[i] - h / 2, "2U")]
with (base / "helpers" / "mid_obs.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["u", "curve", "v", "kind"])
    for o in out:
        w.writerow([o[0], o[1], round(o[2], 2), o[3]])
# presence segments of the dashed curves, from clean columns
for cv, missk in (("lower", "2L"), ("upper", "2U")):
    st = []
    for i, u in enumerate(U):
        k = "3" if three[i] else None
        if two[i]:
            ks = [o[3] for o in out if o[0] == u]
            k = ks[0] if ks else None
        if k is None:
            continue
        pres = k != missk
        if st and st[-1][0] == pres:
            st[-1][2] = u
        else:
            st.append([pres, u, u])
    print(cv, " ".join(f"{'ink' if p else 'GAP'}[{a}-{b}]" for p, a, b in st))
