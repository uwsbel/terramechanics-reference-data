"""Column tracker for one drawn trace on the page image (F2-47 reading helper).

Usage: python out/F2-47/helpers/track.py <calibration.json> <image> <u_start> <v_start> <u_end>
                                          [--step 1] [--tol 8] [--maxgap 40] [--out track.csv]

Starting from the ink run that contains (u_start, v_start), steps one column at a time to the
right and in each column keeps the dark run (threshold 128) whose center is closest to the
center predicted from the last accepted columns (linear extrapolation over the last 6). A run
longer than 40 px is a vertical grid line or the frame: the column is skipped. A column with no
run within `tol` px of the prediction is a gap (a dash gap, or a dropout of the line): the
prediction is carried on, and the tracker gives up after `maxgap` consecutive empty columns.
Each accepted column is written with its run top, bottom, center and length, and a flag when the
run is longer than 1.6 times the median length so far (another line, a letter or a grid line
touching the trace: such columns are reviewed by eye before they are used).
Pixel coordinates are those of the unrotated page (u right, v down).
"""
import argparse, csv, json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('cal'); ap.add_argument('image')
ap.add_argument('u_start', type=int); ap.add_argument('v_start', type=float)
ap.add_argument('u_end', type=int)
ap.add_argument('--tol', type=float, default=8)
ap.add_argument('--maxgap', type=int, default=40)
ap.add_argument('--out', default=None)
a = ap.parse_args()

img = np.array(Image.open(a.image).convert('L')) < 128
cal = json.load(open(a.cal))
hl = sorted(cal['horizontal_lines'], key=lambda L: L['y_value'])

def runs(u, v0, v1):
    col = img[v0:v1, u]
    out = []; i = 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]: j += 1
            out.append((v0 + i, v0 + j - 1)); i = j
        else:
            i += 1
    return out

def grid_tag(u, a_, b_):
    for L in hl:
        gv = L['v_at_u0'] + L['slope_dv_du'] * u
        if a_ - 3 <= gv <= b_ + 3:
            return f"grid{L['y_value']:.0f}"
    return ''

acc = []   # (u, top, bot, center, length, flag)
pred = a.v_start
gap = 0
lengths = []
step = 1 if a.u_end >= a.u_start else -1
for u in range(a.u_start, a.u_end + step, step):
    rs = [(t, b) for t, b in runs(u, int(pred - 60), int(pred + 60))]
    if any(b - t + 1 > 40 and t <= pred <= b for t, b in rs):
        continue   # vertical grid line or frame
    rs = [(t, b) for t, b in rs if b - t + 1 <= 40]
    best = None
    for t, b in rs:
        c = (t + b) / 2
        d = 0 if t <= pred <= b else min(abs(t - pred), abs(b - pred))
        if d <= a.tol and (best is None or d < best[0]):
            best = (d, t, b)
    if best is None:
        gap += 1
        if gap > a.maxgap:
            break
        if len(acc) >= 2:
            us = np.array([r[0] for r in acc[-6:]]); vs = np.array([r[3] for r in acc[-6:]])
            p = np.polyfit(us, vs, 1) if len(us) > 1 else (0, vs[-1])
            pred = float(np.polyval(p, u + step))
        continue
    gap = 0
    _, t, b = best
    L = b - t + 1
    med = float(np.median(lengths)) if lengths else L
    flag = []
    if lengths and L > 1.6 * med: flag.append('thick')
    g = grid_tag(u, t, b)
    if g: flag.append(g)
    acc.append((u, t, b, (t + b) / 2, L, ';'.join(flag)))
    if not flag: lengths.append(L)
    us = np.array([r[0] for r in acc[-6:]]); vs = np.array([r[3] for r in acc[-6:]])
    if len(us) >= 2:
        p = np.polyfit(us, vs, 1)
        pred = float(np.polyval(p, u + step))
    else:
        pred = (t + b) / 2

if a.out:
    with open(a.out, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['u', 'top', 'bot', 'center', 'length', 'flag'])
        for r in acc: w.writerow(r)
print(f"{len(acc)} columns accepted, last u = {acc[-1][0] if acc else None}, median run {np.median(lengths) if lengths else 0}")
