"""Assemble the column centerlines of both F2-47 traces from the page (helper, second Claude reader).

Solid (lpt91): column runs from track_solid.py (work/solidA2.csv u 592..900, work/solidB.csv u
930..2639), flagged columns kept with their flag. The start (u < 592) is read by rows in
samples.py, and the crossing with the dashed line (u 901..929) is left out here.
Dashed (lpt101): the dash components of comps.py (grid lines masked 4 px), one entry per dash with
its ids; per column the run of the component's pixels (top, bottom). Dashes merged with the solid
(D4 at the start, D10 at the crossing, D35 at 6 in) are read from the column runs directly with
the solid's run removed. Writes work/solid-cl.csv and work/dash-cl.csv (u, top, bot, center,
length, seg, flag) and prints the gaps between successive dashes measured along the line.
"""
import csv, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import ROOT, runs_col, near_vgrid, HL, hline_v

W = ROOT + 'out/F2-47/work/'
solid = {}
for fn, lo, hi in (('solidA2.csv', 592, 900), ('solidB.csv', 930, 2639)):
    for r in csv.DictReader(open(W + fn)):
        u = int(r['u'])
        if lo <= u <= hi:
            solid[u] = (int(r['top']), int(r['bot']), r['flag'])

z = np.load(W + 'comps.npz'); lab = z['lab']; bu0, bv0 = int(z['box'][0]), int(z['box'][1])
DASHES = [  # (name, component ids) in drawing order, from comps.txt, each checked on crops
    ('D5', [270]), ('D6', [368]), ('D7', [565]), ('D8', [654, 725]), ('D9', [980]),
    ('D11', [1404]), ('D12', [1749]), ('D13', [1940, 2032]), ('D14', [2374]), ('D15', [2731]),
    ('D16', [3093]), ('D17', [3373]), ('D18', [3731]), ('D19', [4035]), ('D20', [4347]),
    ('D21', [4851]), ('D22', [5153]), ('D23', [5447]), ('D24', [5678, 5803]), ('D25', [6118]),
    ('D26', [6512]), ('D27', [6850]), ('D28', [7114]), ('D29', [7338, 7396]), ('D30', [7607]),
    ('D31', [7813]), ('D32', [7998]), ('D33', [8151]), ('D34', [8306])]
dash = {}
for name, ids in DASHES:
    m = np.isin(lab, ids)
    if name == 'D7':   # the arrowhead of the LPT No. 101 label sits on the dash's left end: dash band only
        m[:2925 - bv0, :] = False
    vv, uu = np.nonzero(m)
    cols = {}
    for u in np.unique(uu):
        col = np.sort(vv[uu == u])
        # runs of this component in the column (a stray mark can join a dash through a corner)
        br = np.flatnonzero(np.diff(col) > 1)
        starts = np.concatenate(([col[0]], col[br + 1])); ends = np.concatenate((col[br], [col[-1]]))
        cols[int(u)] = list(zip(starts, ends))
    # straight line through the single-run columns, then in every column the run nearest it
    single = [(u, (r[0][0] + r[0][1]) / 2) for u, r in cols.items() if len(r) == 1 and r[0][1] - r[0][0] >= 6]
    p = np.polyfit([a for a, _ in single], [b for _, b in single], 1)
    for u, rr in cols.items():
        pv = np.polyval(p, u)
        t, b = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 - pv))
        if abs((t + b) / 2 - pv) > 5 and b - t < 6:
            continue   # a stray mark joined to the dash (under D21), not the dashed line
        fl = 'extra-ink' if len(rr) > 1 else ''
        if name == 'D7' and u + bu0 <= 731:   # arrowhead merged on top of the dash: the dash is its bottom 11 px
            t = b - 10; fl = (fl + ';arrow').strip(';')
        elif name == 'D7' and u + bu0 <= 745:
            fl = (fl + ';arrow-near').strip(';')
        for H in HL:
            if abs(hline_v(H, u + bu0) - (pv + bv0)) <= 9:
                fl = (fl + f";hgrid{H['y_value']:.0f}").strip(';')
        dash[u + bu0] = [int(t) + bv0, int(b) + bv0, name, fl]
# merged dashes, from the column runs: D4 (start), D10 (crossing), D35 (6 in)
for u in range(580, 612):
    rs = [(t, b) for t, b in runs_col(u, 3010, 3080)]
    if not rs: continue
    t, b = rs[0]
    if u in solid and not (b < solid[u][0] or t > solid[u][1]):
        dash[u] = [t, solid[u][0] - 1, 'D4', 'touch']   # dash above the solid's run
    else:
        dash[u] = [t, b, 'D4', '']
for u in range(901, 949):
    rs = [(t, b) for t, b in runs_col(u, 2945, 2985)]
    if u <= 924:
        dash[u] = [rs[0][0], rs[0][1], 'D10', 'cross']
    else:
        t, b = rs[-1]
        dash[u] = [t, b, 'D10', '']
for u in range(2312, 2355):
    rs = [(t, b) for t, b in runs_col(u, 2235, 2290) if b - t < 40]
    if not rs or near_vgrid(u, 2260): continue
    if len(rs) >= 2:
        t, b = rs[-1]; fl = ''
        if u >= 2342:
            fl = 'touch'
    else:   # dash merged with the solid above it: the dash is the bottom 12 px, the solid the top 9 px
        top, b = rs[0]
        t = b - 11; fl = 'touch'
        solid[u] = (top, top + 8, 'touch')
    dash[u] = [t, b, 'D35', fl]
for u in range(2336, 2342):
    solid.pop(u, None)   # the x = 6 grid line
for u in list(dash):
    if near_vgrid(u, (dash[u][0] + dash[u][1]) / 2):
        dash[u][3] = (dash[u][3] + ';vgrid').strip(';')
    for H in HL:
        gv = hline_v(H, u)
        if dash[u][0] - 3 <= gv <= dash[u][1] + 3:
            dash[u][3] = (dash[u][3] + f";hgrid{H['y_value']:.0f}").strip(';')
for fn, D, seg in (('solid-cl.csv', solid, None), ('dash-cl.csv', dash, 1)):
    with open(W + fn, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['u', 'top', 'bot', 'center', 'length', 'seg', 'flag'])
        for u in sorted(D):
            r = D[u]
            if seg is None:
                w.writerow([u, r[0], r[1], (r[0] + r[1]) / 2, r[1] - r[0] + 1, 'S', r[2]])
            else:
                w.writerow([u, r[0], r[1], (r[0] + r[1]) / 2, r[1] - r[0] + 1, r[2], r[3]])
# gaps between successive dashes, along the line (end center to start center)
names = []
for u in sorted(dash):
    if not names or names[-1][0] != dash[u][2]:
        names.append([dash[u][2], u, u])
    names[-1][2] = u
gaps = []
for (n1, a1, b1), (n2, a2, b2) in zip(names, names[1:]):
    c1 = (dash[b1][0] + dash[b1][1]) / 2; c2 = (dash[a2][0] + dash[a2][1]) / 2
    g = float(np.hypot(a2 - b1, c2 - c1))
    gaps.append((n1, n2, b1, a2, round(g, 1)))
for g in gaps: print('gap', g)
print('dashes', [(n, a, b) for n, a, b in names])
