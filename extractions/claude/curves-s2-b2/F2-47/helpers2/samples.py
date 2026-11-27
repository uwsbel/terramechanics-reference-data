"""Trace samples every 0.25 in and the measured features of both F2-47 traces (helper).

Reads work/solid-cl.csv and work/dash-cl.csv (centerlines.py). For each target penetration the
column of that penetration is found at the trace's row (piecewise between the drawn x lines, each
with its own tilt) and the nearest clean column of the trace is taken: for the solid a column with
no flag (no grid line, letter or other line in its run), for the dashed line a column with no flag
at least 3 columns inside its dash, so every sample is on the line's own ink. The center of the run
is the sample. Bounds (rule 7): half the line thickness measured across the line at that column
(run length times cos of the local angle, median over +-3 columns); the dashed line's bound is
widened along the line by half the gap between its dashes (mean of the gaps on either side of the
dash), projected on u and v. Samples within 3 px (edge to edge) of the other trace are noted and
widened by 2 px. Prints one line per sample for review; writes work/auto-samples.csv.
"""
import csv, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import ROOT, x_of, y_of, u_of

W = ROOT + 'out/F2-47/work/'
def load(fn):
    D = {}
    for r in csv.DictReader(open(W + fn)):
        D[int(r['u'])] = dict(top=int(r['top']), bot=int(r['bot']), c=float(r['center']), L=int(r['length']), seg=r['seg'], flag=r['flag'])
    return D
S, Dd = load('solid-cl.csv'), load('dash-cl.csv')
segs = {}
for u, r in Dd.items():
    a = segs.setdefault(r['seg'], [u, u]); a[0] = min(a[0], u); a[1] = max(a[1], u)
order = sorted(segs, key=lambda s: segs[s][0])
gap_of = {}
for s1, s2 in zip(order, order[1:]):
    b1, a2 = segs[s1][1], segs[s2][0]
    g = float(np.hypot(a2 - b1, Dd[a2]['c'] - Dd[b1]['c']))
    gap_of.setdefault(s1, []).append(g); gap_of.setdefault(s2, []).append(g)

def slope(D, u, seg):
    us = [w for w in range(u - 6, u + 7) if w in D and D[w]['seg'] == seg and not any(k in D[w]['flag'] for k in ('vgrid', 'hgrid', 'thick', 'arrow'))]
    if len(us) < 4: us = [w for w in range(u - 6, u + 7) if w in D and D[w]['seg'] == seg]
    return float(np.polyfit(us, [D[w]['c'] for w in us], 1)[0])

def thick(D, u, seg, s):
    Ls = [D[w]['L'] for w in range(u - 3, u + 4) if w in D and D[w]['seg'] == seg and not D[w]['flag']]
    if not Ls: Ls = [D[u]['L']]
    return float(np.median(Ls)) / np.sqrt(1 + s * s)

OK_FLAGS = {'', 'extra-ink', 'arrow-near', 'extra-ink;arrow-near'}   # the run taken is the line's own
def clean(D, u, dashed):
    r = D.get(u)
    if r is None or r['flag'] not in OK_FLAGS or r['L'] < 7: return False
    # no grid line, merged letter or other line within 3 columns
    if any(w in D and D[w]['flag'] not in OK_FLAGS for w in range(u - 3, u + 4)): return False
    if any(w not in D for w in range(u - 3, u + 4)) and not dashed: return False
    if dashed:
        a, b = segs[r['seg']]
        if u < a + 4 or u > b - 4: return False
    return True

def bounds(D, u, dashed):
    seg = D[u]['seg']; s = slope(D, u, seg); t = thick(D, u, seg, s)
    th = np.arctan(abs(s)); h = t / 2
    if dashed:
        g = float(np.mean(gap_of.get(seg, [17.8]))) / 2
        bu = h * np.sin(th) + g * np.cos(th); bv = h * np.cos(th) + g * np.sin(th)
    else:
        bu = bv = h; g = 0
    return s, t, g, bu, bv

def other_dist(D2, u, v):
    best = 1e9
    for w in range(u - 25, u + 26):
        if w in D2:
            r = D2[w]
            d = np.hypot(w - u, max(0, r['top'] - v, v - r['bot']))
            best = min(best, d)
    return best

rows = []
for name, D, D2, dashed, x0, x1 in (('lpt91', S, Dd, False, 0.5, 6.75), ('lpt101', Dd, S, True, 0.5, 6.0)):
    us = sorted(D)
    for x in np.arange(x0, x1 + 1e-9, 0.25):
        # column of x at the trace's row (iterate: row from the trace near that column)
        v = 3000.0
        for _ in range(4):
            ut = u_of(x, v)
            near = min(us, key=lambda w: abs(w - ut)); v = D[near]['c']
        cands = [w for w in us if clean(D, w, dashed)]
        u = min(cands, key=lambda w: abs(w - ut))
        r = D[u]
        s, t, g, bu, bv = bounds(D, u, dashed)
        # distance from this trace's run to the other trace's ink (edge to edge, in px)
        dd = other_dist(D2, u, r['c']) - t / 2
        note = ''
        other = 'LPT No. 101 (dashed)' if name == 'lpt91' else 'LPT No. 91 (solid)'
        if dd < 3:
            note = f'touches {other} here: bound widened 2 px'; bu += 2; bv += 2
        elif dd < 8:
            note = f'{other} ink {dd:.0f} px away'
        if 'extra-ink' in r['flag']:
            note = (note + '; ' if note else '') + 'a stray mark beside the line in this column, not used'
        if 'arrow-near' in r['flag']:
            note = (note + '; ' if note else '') + 'arrowhead of the LPT No. 101 label just above, not used'
        rows.append(dict(series=name, x_target=round(x, 2), u=u, v=r['c'], dx=round(x_of(u, r['c']) - x, 4),
                         bu=round(bu, 1), bv=round(bv, 1), seg=r['seg'], slope=round(s, 2), t=round(t, 1), g=round(g, 1),
                         y=round(y_of(u, r['c']), 1), d_other=round(dd, 1), note=note))
with open(W + 'auto-samples.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r['series'], r['x_target'], 'u', r['u'], 'v', r['v'], 'dx', r['dx'], 'y', r['y'], 'b', r['bu'], r['bv'], r['seg'], 's', r['slope'], 't', r['t'], 'g', r['g'], 'dother', r['d_other'], r['note'])
