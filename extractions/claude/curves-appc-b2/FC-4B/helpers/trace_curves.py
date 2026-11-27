"""Sample the drawn curves of the upper panel (FC-4B, p0127.png) at columns about every 29 px
(5 thousandths of an inch), following each curve from its first marker to the right frame.
At each column the dark runs are listed; the run nearest the prediction (linear extrapolation
from the previous two samples) is taken. Columns within 8 px of a vertical gridline are shifted;
columns within 20 px of one of the series' own markers are shifted away from the marker, so a
symbol is never read as line. Runs that coincide with a horizontal gridline, that are shared
with another series' prediction, or that are unusually thick are flagged in the note.
Writes out/FC-4B/helpers/traces_p1.csv. Run from the FC-4B workspace root."""
import csv, json, sys
import numpy as np
from PIL import Image

sys.path.insert(0, 'out/FC-4B/helpers')
from seeds import P1

im = np.array(Image.open('packet/p0127.png').convert('L'))
dark = im < 128
cal = json.load(open('out/FC-4B/cal-p1/calibration.json'))
vlines = [(l['u_at_v0'], l['slope_du_dv']) for l in cal['vertical_lines']]
hlines = [(l['v_at_u0'], l['slope_dv_du']) for l in cal['horizontal_lines']]


def u_of_vline(l, v):
    return l[0] + l[1] * v


def v_of_hline(l, u):
    return l[0] + l[1] * u


# markers refined by NCC (fallback to seeds) for the column-shift rule and the start points
mk = {}
for r in csv.DictReader(open('out/FC-4B/helpers/markers_refined.csv')):
    if r['panel'] == '1':
        mk.setdefault(r['series_id'], []).append((float(r['ncc_u']), float(r['ncc_v'])))

V0, V1 = 1205, 2655  # inside the frame


def runs_at(u, halfwidth=1):
    col = dark[V0:V1, u - halfwidth:u + halfwidth + 1].min(axis=1)  # dark in all columns u-h..u+h
    out = []
    v = 0
    n = len(col)
    while v < n:
        if col[v]:
            s = v
            while v < n and col[v]:
                v += 1
            out.append(((s + v - 1) / 2 + V0, v - s))
        else:
            v += 1
    return out


# starting (u, v) per series: the first marker (curves begin there)
start = {sid: min(pts) for sid, pts in mk.items()}
U_END = 2250
order = ['n4695', 'n3815', 'n2934', 'n1761', 'n734']
columns = {}
for sid in order:
    u0 = int(round(start[sid][0])) + 22  # first sample just right of the first marker
    cols = []
    u = u0
    while u < U_END - 6:
        uu = u
        # keep away from vertical gridlines
        for l in vlines:
            gu = u_of_vline(l, 1900)
            if abs(uu - gu) < 9:
                uu = int(gu + 9) if uu >= gu else int(gu - 9)
        # keep away from this series' markers
        for (mu, mv) in mk[sid]:
            if abs(uu - mu) < 20:
                uu = int(mu + 20) if uu >= mu else int(mu - 20)
        cols.append(uu)
        u += 29
    columns[sid] = cols

samples = {sid: [] for sid in order}
notes = {sid: [] for sid in order}
prev = {sid: [] for sid in order}
# marker guide: the series' markers in u order (the off-curve plus of n4695 at u=938 is left out,
# the curve was drawn above it); v interpolated linearly between neighbours, held flat outside
guide = {}
for sid in order:
    pts = sorted(p for p in mk[sid] if not (sid == 'n4695' and abs(p[0] - 938) < 5))
    guide[sid] = (np.array([p[0] for p in pts]), np.array([p[1] for p in pts]))


def guide_v(sid, c):
    gu, gv = guide[sid]
    return float(np.interp(c, gu, gv))


all_cols = sorted({(c, sid) for sid in order for c in columns[sid]})
for c, sid in all_cols:
    rs = runs_at(c)
    p = prev[sid]
    g = guide_v(sid, c)
    if len(p) >= 2:
        (u1, v1), (u2, v2) = p[-2], p[-1]
        pred = v2 + (v2 - v1) * (c - u2) / max(u2 - u1, 1)
        tol_g = 45
    elif len(p) == 1:
        pred = p[-1][1]
        tol_g = 45
    else:
        pred = g
        tol_g = 60
    # the n4695 curve is strongly concave between its first marker (u 848) and the marker at
    # u 1197, so a straight-line marker guide is up to 80 px off there; continuity does the work
    if sid == 'n4695' and c < 1200:
        tol_g = 130
    cands = []
    for (vc, th) in rs:
        if th < 4 or th > 60:
            continue
        # a thin run sitting on a horizontal gridline is the gridline, not a curve
        if th < 10 and any(abs(vc - v_of_hline(l, c)) < 5 for l in hlines):
            continue
        if abs(vc - g) > tol_g:
            continue
        cands.append((abs(vc - pred), vc, th))
    if not cands:
        notes[sid].append((c, f'no run within {tol_g} px of marker guide (gap in drawn line?)'))
        continue
    cands.sort()
    d, vc, th = cands[0]
    # a steep start (n4695, n3815) moves 60 px in v between the first columns, so the
    # continuity test is loose until two samples exist
    if d > (35 if len(p) >= 2 else 90):
        notes[sid].append((c, f'nearest run {d:.0f} px from extrapolation; skipped'))
        continue
    note = []
    for l in hlines:
        if abs(vc - v_of_hline(l, c)) < 8:
            note.append('on horizontal gridline, run merged with it')
    if th > 18:
        note.append(f'thick run {th} px (overlap or merge)')
    for o in order:
        if o == sid:
            continue
        po = prev[o]
        if len(po) >= 1 and abs(po[-1][1] - vc) < 20 and abs(po[-1][0] - c) < 60:
            note.append(f'close to {o} trace')
    samples[sid].append((c, vc, th, '; '.join(note)))
    prev[sid].append((c, vc))

with open('out/FC-4B/helpers/traces_p1.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['series_id', 'sequence', 'pixel_u', 'pixel_v', 'thickness', 'note'])
    for sid in order:
        for i, (c, vc, th, note) in enumerate(samples[sid], 1):
            w.writerow([sid, i, c, vc, th, note])
for sid in order:
    print(sid, len(samples[sid]), 'samples; skipped:', notes[sid])
    print('   ', [(c, round(v), th) for c, v, th, n in samples[sid]])
