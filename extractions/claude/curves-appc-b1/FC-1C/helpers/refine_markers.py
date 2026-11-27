"""Refine rough marker centers read by eye from zoomed crops.

Input CSV: panel, series_id, symbol, u, v, note   (u, v rough, +-6 px)
Output CSV: the points-p<n>.csv columns, with the refined center.

Centrally symmetric symbols (x, asterisk, square, plus, circle): the center is the point
that maximizes the 180-degree self-overlap of the ink in a window (radius R). A straight
line through the marker is itself centrally symmetric about every point on it, so it does
not pull the estimate along the line; the symbol's own ink decides.
Triangles: u from mirror symmetry about a vertical axis; v from the ink extent (top to
bottom) in the columns |u - cu| <= 2, i.e. the bounding-box center of the symbol.
Everything is checked afterwards by eye on the overlay; this only sharpens a by-eye read.
"""
import sys, csv
import numpy as np
from PIL import Image

img = np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
ink = (img < 128).astype(float)
H, W = ink.shape
R = 13       # window radius
S = 7        # search radius around the rough center

def win(cu, cv, r):
    return ink[cv - r:cv + r + 1, cu - r:cu + r + 1]

def central_score(cu, cv):
    w = win(cu, cv, R)
    return float(np.minimum(w, w[::-1, ::-1]).sum())

def mirror_u_score(cu, cv):
    w = win(cu, cv, R)
    return float(np.minimum(w, w[:, ::-1]).sum())

def refine_central(u0, v0):
    best = None
    for du in range(-S, S + 1):
        for dv in range(-S, S + 1):
            s = central_score(u0 + du, v0 + dv)
            # tie-break toward the rough center
            key = (s, -(du * du + dv * dv))
            if best is None or key > best[0]:
                best = (key, u0 + du, v0 + dv)
    return best[1], best[2], best[0][0]

def refine_triangle(u0, v0, symbol):
    # u: mirror symmetry, averaged over a few candidate v
    best = None
    for du in range(-S, S + 1):
        s = sum(mirror_u_score(u0 + du, v0 + dv) for dv in (-3, 0, 3))
        key = (s, -du * du)
        if best is None or key > best[0]:
            best = (key, u0 + du)
    cu = best[1]
    # v: center of the ink extent (first to last ink row) in the columns cu-1..cu+1 within
    # v0 +- 15: the bounding-box center of the triangle (base edge to apex). A straight
    # line through the symbol lies inside that extent unless it is steep. If the band is
    # nearly all ink (a vertical gridline runs through it) the rough v is kept.
    col = ink[v0 - 15:v0 + 16, cu - 1:cu + 2].max(axis=1)
    rows = np.where(col > 0)[0]
    if len(rows) == 0 or len(rows) > 27:
        return cu, v0, -1.0
    cv = v0 - 15 + (rows.min() + rows.max()) / 2.0
    return cu, cv, float(rows.max() - rows.min() + 1)

rows_in = list(csv.DictReader(open(sys.argv[2], newline='')))
out = csv.writer(open(sys.argv[3], 'w', newline=''))
out.writerow(['figure_id', 'panel', 'series_id', 'point_kind', 'sequence', 'pixel_u', 'pixel_v',
              'u_bound_px', 'v_bound_px', 'symbol', 'note', 'rough_u', 'rough_v', 'score'])
seq = {}
for r in rows_in:
    u0, v0 = int(r['u']), int(r['v'])
    sym = r['symbol']
    if sym in ('triangle-up', 'triangle-down'):
        cu, cv, sc = refine_triangle(u0, v0, sym)
    else:
        cu, cv, sc = refine_central(u0, v0)
    key = (r['panel'], r['series_id'])
    seq[key] = seq.get(key, 0) + 1
    bound = r.get('bound', '') or '2'
    out.writerow([r.get('figure_id', 'FC-1C'), r['panel'], r['series_id'], 'marker', seq[key],
                  int(round(cu)), int(round(cv)), bound, bound, sym, r.get('note', ''), u0, v0, sc])
