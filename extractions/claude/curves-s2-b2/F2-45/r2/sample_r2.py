"""Trace samples of Figure 2-45 every 0.25 in of penetration, plus the features read by eye.

Solid trace (lpt95): on the dense center line (solid-centerline.csv, drawing order), the sample at
penetration xt is where the local straight fit of the center line (clean points within 8 px of the
crossing) meets the constant-penetration line xt (piecewise between the drawn lines, each with its own
tilt). Bound: half the perpendicular thickness of the line there (median run width of the fitted points
times the cosine of the line's angle to the run), plus 1 px where the center is interpolated across a
grid line (too few clean points in the window, or on a drawn grid line).

Dotted trace (lpt79): the samples are dot centers (dots.csv): for each xt, the dot nearest in
penetration among the dots not touching a grid line (fitted line within 9 px); a dot touching a grid
line is used only when no clean dot is within 0.06 in, with a note. Bound: the dot's half width across
the line and half the local dot spacing along it, as the half extents in u and v of that ellipse.

Feature rows and the solid trace's first and last trace samples come from features-r2.csv, read by eye
on zoomed crops (pixel coordinates of the page as scanned).
Writes out/F2-45/points-p1.csv.
"""
import csv
import numpy as np
from common import INK, x_of, y_of, v_at_x, HL, VL, hline_v, vline_u, near_hgrid, near_vgrid

FIG = 'F2-45'
OUT = 'out/F2-45/points-p1.csv'
FIELDS = ['figure_id', 'panel', 'series_id', 'point_kind', 'sequence', 'pixel_u', 'pixel_v',
          'u_bound_px', 'v_bound_px', 'symbol', 'note']

feat = [r for r in csv.DictReader(open('out/F2-45/r2/features-r2.csv'))]


def r1(a):
    return round(float(a), 1)


# ------------------------------------------------------------------ solid
C = [r for r in csv.DictReader(open('out/F2-45/r2/solid-centerline.csv'))]
U = np.array([float(r['u']) for r in C])
V = np.array([float(r['v']) for r in C])
W = np.array([float(r['width_px']) for r in C])
OK = np.array([r['clean'] in ('1', 'True') for r in C])
SRC = np.array([r['src'] for r in C])
X = np.array([float(r['x']) for r in C])

sf = [f for f in feat if f['series_id'] == 'lpt95']
first = [f for f in sf if f['role'] == 'first'][0]
last = [f for f in sf if f['role'] == 'last'][0]
x_first = x_of(float(first['u']), float(first['v']))
x_last = x_of(float(last['u']), float(last['v']))

# the page ink less the grid bands (+-4 px around each fitted interior line) and the frame: a sample is
# kept only where the line's own ink, clear of the grid, is within 1 px of it
INKNG = INK.copy()
_vv = np.arange(1400, 3700)[:, None]
_uu = np.arange(300, 2400)[None, :]
_g = np.zeros((_vv.shape[0], _uu.shape[1]), bool)
for L in VL:
    _g |= np.abs(_uu - (L['u_at_v0'] + L['slope_du_dv'] * _vv)) <= (4 if 0 < L['y_value'] < 300 else 8)
for L in HL:
    _g |= np.abs(_vv - (L['v_at_u0'] + L['slope_dv_du'] * _uu)) <= (4 if 0 < L['x_value'] < 7 else 8)
INKNG[1400:3700, 300:2400] &= ~_g


def own_ink_dist(u, v, r=8):
    a0, b0 = int(v) - r, int(u) - r
    vs, us = np.nonzero(INKNG[a0:a0 + 2 * r + 1, b0:b0 + 2 * r + 1])
    return float(np.min(np.hypot(us + b0 - u, vs + a0 - v))) if len(vs) else 99.0


def solid_at(xt):
    """Center of the solid line at penetration xt (first crossing in drawing order)."""
    idx = np.nonzero((X[:-1] <= xt) & (X[1:] > xt))[0]
    if len(idx) == 0:
        return None
    i = idx[0]
    vc, uc = V[i], U[i]
    win = OK & (np.abs(V - vc) <= 8) & (np.abs(U - uc) <= 12)
    interp = False
    if win.sum() < 6:
        win = OK & (np.abs(V - vc) <= 16) & (np.abs(U - uc) <= 24)
        interp = True
    if SRC[i] == 'row':
        b, a = np.polyfit(V[win], U[win], 1)            # u = a + b v
        v = vc
        for _ in range(20):
            u = a + b * v
            v = v_at_x(xt, u)
        u = a + b * v
    else:
        b, a = np.polyfit(U[win], V[win], 1)            # v = a + b u
        u = uc
        for _ in range(20):
            v = v_at_x(xt, u)
            u = (v - a) / b
    s = abs(b)
    thick = np.median(W[win]) / np.sqrt(1 + s * s)
    return u, v, thick, interp


solid = []
for xt0 in np.arange(0.25, 7.0, 0.25):
    if xt0 <= x_first + 0.02 or xt0 >= x_last - 0.02:
        continue
    # where the target falls on a grid line the line's own ink is hidden in the grid ink; the sample is
    # then taken a little to one side (0.025 in, about 8 px), where the line is seen clear of the grid
    for off in (0.0, 0.025, -0.025, 0.04, -0.04):
        r = solid_at(xt0 + off)
        if r and own_ink_dist(r[0], r[1]) <= 1.0:
            break
    else:
        off = 0.0
        r = solid_at(xt0)
    u, v, thick, interp = r
    xt = xt0 + off
    note = []
    bnd = max(thick / 2, 2.0)
    if off:
        what = 'x = %d grid line' % round(xt0) if near_hgrid(*solid_at(xt0)[:2], 5) else 'load grid line it crosses'
        note.append('sampled at %.3f in instead of %.2f in: at %.2f in the line is hidden in the %s'
                    % (xt, xt0, xt0, what))
    if interp:
        note.append('center from a straight fit across a grid crossing')
        bnd += 1
    if own_ink_dist(u, v) > 1.0:
        note.append('the line runs along a grid line here; center from the ink beside the grid line')
        bnd += 1
    solid.append(dict(u=u, v=v, bu=bnd, bv=bnd, note='; '.join(note), xt=xt))

# ------------------------------------------------------------------ dotted
D = [r for r in csv.DictReader(open('out/F2-45/r2/dots.csv'))]
DU = np.array([float(r['u']) for r in D])
DV = np.array([float(r['v']) for r in D])
DX = np.array([x_of(u, v) for u, v in zip(DU, DV)])
NG = np.array([int(r['near_grid']) for r in D])


def dot_bounds(k):
    """Half extents in u, v of the ellipse: half the dot width across the line, half the spacing along."""
    a, b = max(k - 2, 0), min(k + 2, len(D) - 1)
    t = np.array([DU[b] - DU[a], DV[b] - DV[a]])
    sp = np.hypot(*t) / (b - a)
    t /= np.hypot(*t)
    n = np.array([-t[1], t[0]])
    across = 2 * np.sqrt(int(D[k]['n']) / np.pi)        # dot width: diameter of a disk of the dot's area
    if NG[k] or int(D[k]['split']) > 1:                  # part of the dot is under a grid band or a neighbor
        across = max(across, 11.0)
    rh, ha = across / 2, sp / 2
    bu = np.sqrt((ha * t[0]) ** 2 + (rh * n[0]) ** 2)
    bv = np.sqrt((ha * t[1]) ** 2 + (rh * n[1]) ** 2)
    return bu, bv, sp


dotted = []
chosen = [0]
for xt in np.arange(0.25, 7.0, 0.25):
    if xt > DX[-1] + 0.03:
        break
    order = np.argsort(np.abs(DX - xt))
    clean_ = [k for k in order if not NG[k]]
    k = clean_[0]
    note = ''
    if abs(DX[k] - xt) > 0.06:
        k = order[0]
        note = 'dot touches a grid line; its center is from the ink outside the grid band'
    if k in chosen or k == len(D) - 1:
        continue
    if k < chosen[-1]:
        continue
    chosen.append(k)
chosen.append(len(D) - 1)
for k in chosen:
    bu, bv, sp = dot_bounds(k)
    note = f'dot {int(D[k]["k"])} of the chain'
    if NG[k]:
        note += '; dot touches a grid line, center from the ink outside the grid band'
    if k == 0:
        note += '; first distinct dot (an earlier dot may be merged with the solid line near u 2240, v 3573)'
    if k == len(D) - 1:
        note += '; last dot of the line'
    dotted.append(dict(u=DU[k], v=DV[k], bu=bu, bv=bv, note=note))

# ------------------------------------------------------------------ write
rows = []


def add(series, kind, seq, u, v, bu, bv, sym, note):
    rows.append(dict(figure_id=FIG, panel=1, series_id=series, point_kind=kind, sequence=seq,
                     pixel_u=r1(u), pixel_v=r1(v), u_bound_px=r1(bu), v_bound_px=r1(bv), symbol=sym,
                     note=note))


seq = 1
add('lpt95', 'trace', seq, first['u'], first['v'], first['bu'], first['bv'], 'solid',
    'ink start: ' + first['note'])
for s in solid:
    seq += 1
    add('lpt95', 'trace', seq, s['u'], s['v'], s['bu'], s['bv'], 'solid',
        s['note'] if s['note'].startswith('sampled') else
        f'x target {s["xt"]:.2f} in' + ('; ' + s['note'] if s['note'] else ''))
seq += 1
add('lpt95', 'trace', seq, last['u'], last['v'], last['bu'], last['bv'], 'solid', 'ink end: ' + last['note'])
for j, s in enumerate(dotted, 1):
    add('lpt79', 'trace', j, s['u'], s['v'], s['bu'], s['bv'], 'dotted', s['note'])
for series in ('lpt95', 'lpt79'):
    fs = [f for f in feat if f['series_id'] == series]
    for j, f in enumerate(fs, 1):
        if series == 'lpt79':                       # a dot feature takes the dot's own bounds
            k = 0 if f['role'] == 'first' else len(D) - 1
            f['bu'], f['bv'], _ = dot_bounds(k)
        add(series, 'feature', j, f['u'], f['v'], f['bu'], f['bv'],
            'solid' if series == 'lpt95' else 'dotted', f['role'] + ': ' + f['note'])
with open(OUT, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
print('lpt95 trace', 1 + len(solid) + 1, 'lpt79 trace', len(dotted),
      'features', {s: sum(1 for f in feat if f['series_id'] == s) for s in ('lpt95', 'lpt79')})
