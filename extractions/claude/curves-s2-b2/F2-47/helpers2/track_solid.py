"""Column tracker for the solid trace (LPT No. 91) of F2-47, rightward from a seed run.

Usage: python track_solid.py u_start v_start u_end out.csv
In each column the dark run nearest the center predicted from the last 8 accepted columns
(straight-line fit) is kept if within 7 px of it; a run longer than 40 px (vertical grid line or
frame) makes the column skipped. Flags: 'thick' (run longer than 1.5 times the running median, i.e.
another line, a letter or a grid line merges with the trace), 'hgrid<value>' (a horizontal grid
line passes within the run), 'vgrid' (a vertical grid line within 6 px).
"""
import csv, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from common import IMG, runs_col, near_vgrid, HL, hline_v

u0, v0, u1, outp = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
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
        if gap > 30:
            break
        continue
    gap = 0
    _, t, b = best
    L = b - t + 1
    med = float(np.median(lengths[-60:])) if lengths else L
    flag = []
    if lengths and L > 1.5 * med:
        flag.append('thick')
    for H in HL:
        gv = hline_v(H, u)
        if t - 3 <= gv <= b + 3:
            flag.append(f"hgrid{H['y_value']:.0f}")
    if near_vgrid(u, (t + b) / 2):
        flag.append('vgrid')
    acc.append((u, t, b, (t + b) / 2, L, ';'.join(flag)))
    if not flag:
        lengths.append(L)
    good = [r for r in acc[-8:]]
    us = np.array([r[0] for r in good]); vs = np.array([r[3] for r in good])
    if len(us) >= 3:
        p = np.polyfit(us, vs, 1); pred = float(np.polyval(p, u + 1))
    else:
        pred = (t + b) / 2
with open(outp, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['u', 'top', 'bot', 'center', 'length', 'flag'])
    w.writerows(acc)
print(f"{len(acc)} columns, last u {acc[-1][0]}, median run {np.median(lengths):.1f}, flagged {sum(1 for r in acc if r[5])}")
