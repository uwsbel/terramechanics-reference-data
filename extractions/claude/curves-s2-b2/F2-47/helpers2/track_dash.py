"""Column tracker for the dashed trace (LPT No. 101) of F2-47, rightward from a seed run.

Usage: python track_dash.py u_start v_start u_end out.csv [--avoid solid.csv ...]
Like track_solid.py, but a dash gap (no run within 7 px of the prediction) is bridged by carrying
the straight-line prediction for up to 25 columns, and a run that overlaps a run of an --avoid
track in the same column (the solid trace) is not taken unless no other run is near; such columns
are flagged 'touch'. Each accepted column is one column of dash ink; columns in gaps are not
written, so every row of the output is on ink.
"""
import csv, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import runs_col, near_vgrid, HL, hline_v

args = sys.argv[1:]
avoid = {}
if '--avoid' in args:
    i = args.index('--avoid')
    for fn in args[i + 1:]:
        for r in csv.DictReader(open(fn)):
            avoid[int(r['u'])] = (int(r['top']), int(r['bot']))
    args = args[:i]
u0, v0, u1, outp = int(args[0]), float(args[1]), int(args[2]), args[3]
acc, lengths, pred, gap = [], [], v0, 0
for u in range(u0, u1 + 1):
    rs = runs_col(u, int(pred - 50), int(pred + 50))
    if any(b - t + 1 > 40 and t - 2 <= pred <= b + 2 for t, b in rs):
        continue
    rs = [(t, b) for t, b in rs if b - t + 1 <= 40]
    best = None
    for t, b in rs:
        d = 0 if t <= pred <= b else min(abs(t - pred), abs(b - pred))
        if d <= 7 and (best is None or d < best[0]):
            best = (d, t, b)
    if best is None:
        gap += 1
        if gap > 25:
            break
        us = np.array([r[0] for r in acc[-10:]]); vs = np.array([r[3] for r in acc[-10:]])
        if len(us) >= 3:
            p = np.polyfit(us, vs, 1); pred = float(np.polyval(p, u + 1))
        continue
    gap = 0
    _, t, b = best
    L = b - t + 1
    med = float(np.median(lengths[-60:])) if lengths else L
    flag = []
    if lengths and L > 1.5 * med:
        flag.append('thick')
    if u in avoid and not (b < avoid[u][0] or t > avoid[u][1]):
        flag.append('touch')
    for H in HL:
        gv = hline_v(H, u)
        if t - 3 <= gv <= b + 3:
            flag.append(f"hgrid{H['y_value']:.0f}")
    if near_vgrid(u, (t + b) / 2):
        flag.append('vgrid')
    acc.append((u, t, b, (t + b) / 2, L, ';'.join(flag)))
    if not flag:
        lengths.append(L)
    us = np.array([r[0] for r in acc[-10:]]); vs = np.array([r[3] for r in acc[-10:]])
    if len(us) >= 3:
        p = np.polyfit(us, vs, 1); pred = float(np.polyval(p, u + 1))
    else:
        pred = (t + b) / 2
with open(outp, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['u', 'top', 'bot', 'center', 'length', 'flag'])
    w.writerows(acc)
print(f"{len(acc)} columns, last u {acc[-1][0]}, median run {np.median(lengths):.1f}, flagged {sum(1 for r in acc if r[5])}")
