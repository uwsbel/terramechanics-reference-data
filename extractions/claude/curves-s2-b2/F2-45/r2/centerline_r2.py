"""Dense center line of the solid trace (lpt95) in drawing order, for sampling and for the x-y check plot.

Near the origin the solid line is shallow on the page (load rises with little penetration), so a row
crosses it in a long run; there the center is taken by columns instead: for each column u from 2150 to
the right frame, the ink run of the column that overlaps the previous column's run (starting from the
row-tracked center at u 2150), center v. Columns where the run is longer than 1.6 times the median (a
dot of the dotted trace touching the line, near u 2240) are flagged. Elsewhere the clean rows of
solid-rows.csv are used. Writes out/F2-45/r2/solid-centerline.csv: u, v, width_px (perpendicular
thickness estimate), src (row|col), clean, x, y (x, y from common.x_of / y_of, for choosing only).
"""
import csv
import numpy as np
from common import INK, VL, HL, vline_u, hline_v, runs, x_of, y_of

rows = [r for r in csv.DictReader(open('out/F2-45/r2/solid-rows.csv'))]
clean = [(int(r['v']), float(r['c']), int(r['w'])) for r in rows if r['clean'] == '1']

# column tracking near the origin
U_SWITCH = 2150
rv = [c for c in clean if abs(c[1] - U_SWITCH) < 3]
v_prev = np.mean([c[0] for c in rv])
prev = (int(v_prev) - 3, int(v_prev) + 3)
col = []
widths = []
for u in range(U_SWITCH, 2275):
    vb = hline_v(HL[0], u) - 7                      # inner edge of the bottom frame
    rr = runs(INK[3400:int(vb) + 1, u], 3400)
    cand = [r for r in rr if r[1] >= prev[0] - 1 and r[0] <= prev[1] + 1]
    if not cand:
        break
    s, e = max(cand, key=lambda r: r[1])           # the lower run if two touch the previous (a dot is above)
    w = e - s + 1
    medw = np.median(widths[-20:]) if len(widths) >= 5 else w
    ok = w <= 1.6 * medw + 1 and abs(u - vline_u(VL[1], (s + e) / 2)) > 5
    col.append((u, (s + e) / 2, w, int(ok), e >= vb - 1))
    if ok:
        widths.append(w)
    prev = (s, e)

pts = []
# drawing order: from the origin end; the column part first (u decreasing), then rows upward (v decreasing)
for u, v, w, ok, at_frame in reversed(col):
    pts.append(dict(u=u, v=v, width_px=w, src='col', clean=ok and not at_frame))
v_cut = min(c[1] for c in col)                     # rows above the column part only
for v, c, w in sorted(clean, key=lambda t: -t[0]):
    if v < v_cut and c < U_SWITCH:
        pts.append(dict(u=c, v=v, width_px=w, src='row', clean=1))
with open('out/F2-45/r2/solid-centerline.csv', 'w', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=['u', 'v', 'width_px', 'src', 'clean', 'x', 'y'])
    wr.writeheader()
    for p in pts:
        p['x'] = round(x_of(p['u'], p['v']), 4)
        p['y'] = round(y_of(p['u'], p['v']), 3)
        wr.writerow(p)
print('column part', len(col), 'first col', col[0], 'last col', col[-1])
print('points', len(pts))
