"""Assemble points-p1.csv and points-p2.csv for FC-4B from the refined markers
(markers_refined.csv, corrected by the template-center offsets), the traced curves
(traces_p1.csv) and the feature points (first marker, peak of the drawn line by a dense
column scan, last point of the drawn line). Run from the FC-4B workspace root."""
import csv, json
import numpy as np
from PIL import Image

FIG = 'FC-4B'
COLS = ['figure_id', 'panel', 'series_id', 'point_kind', 'sequence', 'pixel_u', 'pixel_v',
        'u_bound_px', 'v_bound_px', 'symbol', 'note']
# true-center minus eye-center of the template instance (template_centers.py)
OFF = {'triangle-up': (-0.5, -2.0), 'square': (-1.0, 2.5), 'triangle-down': (0.5, 0.5),
       'plus': (0.5, 1.0), 'circle': (-0.5, 0.0), 'small-circle': (0.0, 0.0)}
# markers where the NCC fit is not trusted (low score, frame or cluster): eye value kept
EYE_OVERRIDE = {(2, 'n2934', 806, 3272): (806, 3272)}

im = np.array(Image.open('packet/p0127.png').convert('L'))
dark = im < 128
V0, V1 = 1205, 2655


def runs_at(u, halfwidth=1):
    col = dark[V0:V1, u - halfwidth:u + halfwidth + 1].min(axis=1)
    out, v, n = [], 0, len(col)
    while v < n:
        if col[v]:
            s = v
            while v < n and col[v]:
                v += 1
            out.append(((s + v - 1) / 2 + V0, v - s))
        else:
            v += 1
    return out


markers = {1: [], 2: []}
for r in csv.DictReader(open('out/FC-4B/helpers/markers_refined.csv')):
    panel = int(r['panel'])
    sym = r['symbol']
    key = 'small-circle' if (sym == 'circle' and panel == 2) else sym
    su, sv = int(r['seed_u']), int(r['seed_v'])
    k = (panel, r['series_id'], su, sv)
    if k in EYE_OVERRIDE:
        u, v = EYE_OVERRIDE[k]
        note = (r['note'] + '; ' if r['note'] else '') + 'NCC fit rejected (frame interference), eye reading kept'
        b = 5
    else:
        u = float(r['ncc_u']) + OFF[key][0]
        v = float(r['ncc_v']) + OFF[key][1]
        note = r['note']
        score = float(r['score'])
        n = note.lower()
        if 'frame' in n or 'attached' in n or 'overlap' in n or 'below' in n or 'coincides' in n:
            b = 4
        elif 'gridline' in n or 'touching' in n:
            b = 3
        else:
            b = 2
        if score < 0.5:
            b = max(b, 4)
            note = (note + '; ' if note else '') + f'low template score {score:.2f}'
        if abs(u - su) > 3 or abs(v - sv) > 4:
            note = (note + '; ' if note else '') + f'template fit moved {u-su:+.1f},{v-sv:+.1f} px from eye reading'
    markers[panel].append((r['series_id'], sym, u, v, b, note))

order = ['n4695', 'n3815', 'n2934', 'n1761', 'n734']
traces = {sid: [] for sid in order}
for r in csv.DictReader(open('out/FC-4B/helpers/traces_p1.csv')):
    traces[r['series_id']].append((int(r['pixel_u']), float(r['pixel_v']), int(r['thickness']), r['note']))

rows1 = []
for sid in order:
    ms = sorted([m for m in markers[1] if m[0] == sid], key=lambda m: m[2])
    tu = [t[0] for t in traces[sid]]
    tv = [t[1] for t in traces[sid]]
    for i, (s, sym, u, v, b, note) in enumerate(ms, 1):
        # a marker more than 15 px (about 50 psf) from the drawn line is flagged: the author's
        # curve was not drawn through it
        if tu[0] <= u <= tu[-1]:
            dv = v - float(np.interp(u, tu, tv))
            if abs(dv) > 15 and 'off the drawn curve' not in note:
                note = (note + '; ' if note else '') + f'marker off the drawn curve ({dv:+.0f} px in v, line passes {"above" if dv > 0 else "below"} it)'
        rows1.append([FIG, 1, sid, 'marker', i, round(u, 1), round(v, 1), b, b, sym, note])
for sid in order:
    for i, (u, v, th, note) in enumerate(traces[sid], 1):
        vb = max(3, round(th / 2))
        if th > 18 and 'gridline' not in note:
            note = (note + '; ' if note else '') + 'steep segment, vertical run longer than the line is thick'
        rows1.append([FIG, 1, sid, 'trace', i, u, round(v, 1), 1, vb, '', note])

# features
mk1 = {sid: sorted([m for m in markers[1] if m[0] == sid], key=lambda m: m[2]) for sid in order}
for sid in order:
    tr = traces[sid]
    first = mk1[sid][0]
    feats = [(first[2], first[3], 4, 4, 'first point: the drawn line starts under the first marker')]
    # peak: dense scan around the trace minimum in v, skipping columns within 16 px of a marker
    i_min = int(np.argmin([t[1] for t in tr]))
    uc = tr[i_min][0]
    best = None
    for u in range(uc - 45, uc + 46, 2):
        if any(abs(u - m[2]) < 16 for m in mk1[sid]):
            continue
        rs = [r for r in runs_at(u) if 4 <= r[1] <= 40 and abs(r[0] - tr[i_min][1]) < 30]
        if not rs:
            continue
        vc, th = min(rs, key=lambda r: abs(r[0] - tr[i_min][1]))
        if best is None or vc < best[1]:
            best = (u, vc, th)
    pk_note = 'peak of the drawn line (minimum v by dense column scan)'
    vs = [t[1] for t in tr]
    flat = sum(1 for v in vs if v - min(vs) < 6)
    if flat >= 6:
        pk_note += '; plateau, the maximum is not sharp (several samples within 6 px of it)'
    if sid == 'n4695':
        pk_note += '; peak lies at the marker near u 2100, read between markers'
    feats.append((best[0], best[1], 12 if flat >= 6 else 4, max(3, round(best[2] / 2)), pk_note))
    # last point
    if sid == 'n4695':
        last = mk1[sid][-1]
        feats.append((last[2], last[3], 4, 4, 'last point: the drawn line ends under the last marker, which touches the right frame'))
    else:
        # the line may stop a few px short of the marker on the frame: walk left from u 2244
        rs = []
        for u in (2244, 2241, 2238, 2235, 2232):
            rs = [r for r in runs_at(u) if 4 <= r[1] <= 40 and abs(r[0] - tr[-1][1]) < 30]
            if rs:
                break
        if rs:
            vc, th = min(rs, key=lambda r: abs(r[0] - tr[-1][1]))
            feats.append((u, vc, 2, max(3, round(th / 2)), 'last point: drawn line just before it meets the right frame (x = 250), where the last marker sits on the frame'))
        else:
            feats.append((tr[-1][0], tr[-1][1], 1, 6, 'last point: last readable trace sample before the frame'))
    for i, (u, v, ub, vb, note) in enumerate(feats, 1):
        rows1.append([FIG, 1, sid, 'feature', i, round(u, 1), round(v, 1), ub, vb, '', note])

with open('out/FC-4B/points-p1.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(COLS)
    w.writerows(rows1)

rows2 = []
for sid in order:
    ms = sorted([m for m in markers[2] if m[0] == sid], key=lambda m: m[2])
    for i, (s, sym, u, v, b, note) in enumerate(ms, 1):
        rows2.append([FIG, 2, sid, 'marker', i, round(u, 1), round(v, 1), b, b, sym, note])
with open('out/FC-4B/points-p2.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(COLS)
    w.writerows(rows2)
print('p1 rows', len(rows1), 'p2 rows', len(rows2))
from collections import Counter
print(Counter((r[2], r[3]) for r in rows1))
print(Counter((r[2], r[3]) for r in rows2))
