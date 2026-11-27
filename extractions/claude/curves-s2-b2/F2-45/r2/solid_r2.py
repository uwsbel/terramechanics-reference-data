"""Solid trace (lpt95, Four-Inch Cylinder, LPT No. 95) of Figure 2-45: center line by rows.

Each row v (constant page row) is crossed by the solid line in one ink run; its center is the line's
center at that row. Tracked from a clean start (v = 3450, u about 2060) upward to the top frame and
downward toward the origin. A run is kept when it overlaps the previous chosen run; a run that is only a
vertical grid line is dropped when another candidate exists; among several, the one nearest the
prediction from the last 20 clean centers. Rows inside a horizontal grid band (+-5 px) are skipped
('hgrid'); runs within 5 px of a vertical grid line are kept but flagged ('vgrid', their center is biased
by the grid ink); runs wider than 1.6 times the local median width are flagged ('wide', text or a dot
touching the line). Only rows flagged clean are used to place samples.
Writes out/F2-45/r2/solid-rows.csv: v, s, e, c, w, clean, note.
"""
import csv
import numpy as np
from common import INK, VL, HL, vline_u, hline_v, runs, near_hgrid

OUT = 'out/F2-45/r2/solid-rows.csv'


def frame_inner_u(v):
    return vline_u(VL[-1], v) + 7, vline_u(VL[0], v) - 7


def grid_only(r, v):
    c, w = (r[0] + r[1]) / 2, r[1] - r[0] + 1
    return w <= 9 and any(abs(c - vline_u(L, v)) <= 4 for L in VL[1:-1])


def touches_vgrid(s, e, v, half=4):
    return any(s - half <= vline_u(L, v) <= e + half for L in VL[1:-1])


def track(v_start, u_start, step, v_stop):
    rows, prev, prev_v, centers, widths = [], None, None, [], []
    v = v_start
    while (v >= v_stop) if step < 0 else (v <= v_stop):
        uref = (prev[0] + prev[1]) / 2 if prev else u_start
        if near_hgrid(uref, v, 5):
            rows.append(dict(v=v, s='', e='', c='', w='', clean=0, note='hgrid'))
            v += step
            continue
        fu0, fu1 = frame_inner_u(v)
        rr = runs(INK[v, int(fu0):int(fu1) + 1], int(fu0))
        if len(centers) >= 6:
            vs = np.array([c[0] for c in centers[-20:]], float)
            us = np.array([c[1] for c in centers[-20:]], float)
            m, k = np.polyfit(vs, us, 1)
            pred = m * v + k
        else:
            pred = uref
        if prev is None:
            cand = [r for r in rr if r[0] - 2 <= u_start <= r[1] + 2]
        else:
            tol = 1 + 2 * (abs(v - prev_v) - 1)
            cand = [r for r in rr if r[1] >= prev[0] - tol and r[0] <= prev[1] + tol]
        if len(cand) > 1:
            ng = [r for r in cand if not grid_only(r, v)]
            cand = ng or cand
        if len(cand) > 1:
            cand = [min(cand, key=lambda r: abs((r[0] + r[1]) / 2 - pred))]
        if not cand:
            rows.append(dict(v=v, s='', e='', c='', w='', clean=0, note='lost'))
            break
        s, e = cand[0]
        w = e - s + 1
        medw = np.median(widths[-30:]) if len(widths) >= 10 else w
        note = ''
        if touches_vgrid(s, e, v):
            note = 'vgrid'
        elif w > 1.6 * medw + 2:
            note = 'wide'
        clean = note == ''
        rows.append(dict(v=v, s=s, e=e, c=(s + e) / 2, w=w, clean=int(clean), note=note))
        if clean:
            centers.append((v, (s + e) / 2))
            widths.append(w)
        prev, prev_v = (s, e), v
        v += step
    return rows


if __name__ == '__main__':
    up = track(3450, 2060, -1, 1462)
    down = track(3451, 2060, +1, 3590)
    solid = list(reversed(down)) + up          # drawing order: from the origin end upward
    with open(OUT, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['v', 's', 'e', 'c', 'w', 'clean', 'note'])
        w.writeheader()
        w.writerows(solid)
    print('rows', len(solid), 'first', solid[0], 'last', solid[-1])
    print({k: sum(1 for r in solid if r['note'] == k) for k in set(r['note'] for r in solid)})
