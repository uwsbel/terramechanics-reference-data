"""Sample the drawn upper-panel curves (trace points) and read their features.

For each series: the markers (already read) are interpolated piecewise-linearly in u to
predict where the curve is at a column; the dark run nearest that prediction (combining
columns u-1..u+1 by min, like plot_grid.py scan with halfwidth 1) is the curve. Columns are
chosen every 5 thousandths (x = 2.5 + 5k, never on a vertical gridline) and moved 15 px
off any marker of the same series so a hollow symbol does not split the run. Pure
horizontal gridline runs (thin, at a gridline v) are skipped; a run that overlaps a
gridline and is thicker than the line alone is kept with a note and a wider bound.
Bound = half the run thickness (min 3 px). Features: first point (line starts at the first
marker), peak (minimum v of the drawn line, found on a 1 px column sweep), last point.
"""
import csv, json, sys, math
import numpy as np
from PIL import Image

img, markers_csv, cal_json, out_csv = sys.argv[1:5]
ink = (np.asarray(Image.open(img).convert('L')) < 128)
cal = json.load(open(cal_json))
ax, ay = cal['ax'], cal['ay']
grid_v = [(h['v_at_u0'], h['slope_dv_du']) for h in cal['horizontal_lines']]

def u_of_x(x, v):
    # invert x = ax0 u + ax1 v + ax2
    return (x - ax[1] * v - ax[2]) / ax[0]

def runs_at(u, v0, v1):
    col = ink[v0:v1, u - 1:u + 2].min(axis=1)
    out, start = [], None
    for i, d in enumerate(col):
        if d and start is None: start = i
        if (not d) and start is not None:
            out.append((v0 + start, v0 + i - 1)); start = None
    if start is not None: out.append((v0 + start, v0 + len(col) - 1))
    return [((a + b) / 2.0, b - a + 1, a, b) for a, b in out]

def gridline_near(v, u):
    for v0, s in grid_v:
        gv = v0 + s * u
        if abs(v - gv) <= 4: return gv
    return None

def pick(u, vpred, tol=30):
    cands = []
    for c, t, a, b in runs_at(u, int(vpred - tol - 10), int(vpred + tol + 10)):
        g = gridline_near(c, u)
        if g is not None and t <= 7:
            continue            # a bare gridline
        if t < 5:
            continue            # a thin remnant at the end of a dash, not the 9 px line
        if abs(c - vpred) <= tol:
            cands.append((abs(c - vpred), c, t, a, b))
    cands.sort()
    return cands

markers = {}
for r in csv.DictReader(open(markers_csv, newline='')):
    if r['point_kind'] != 'marker' or r['panel'] != '1': continue
    markers.setdefault(r['series_id'], []).append((int(r['pixel_u']), int(r['pixel_v'])))
for s in markers: markers[s].sort()

# where each drawn line ends: 'marker' = at the last marker, or a column near the frame
ends = {'n3520': 'marker', 'n2935': 'marker', 'n2345': 'marker', 'n1760': 'marker',
        'n1172': 2080, 'n587': 2080, 'n294': 'marker'}
order = ['n3520', 'n2935', 'n2345', 'n1760', 'n1172', 'n587', 'n294']

def predict(s, u):
    m = markers[s]
    us = [a for a, b in m]; vs = [b for a, b in m]
    return float(np.interp(u, us, vs))

rows = []
feat = []
for s in order:
    m = markers[s]
    u_first = m[0][0]
    u_last = m[-1][0] if ends[s] == 'marker' else ends[s]
    seq = 0
    # --- trace samples
    k = 0
    while True:
        x = 2.5 + 5 * k; k += 1
        if x > 260: break
        u = int(round(u_of_x(x, predict(s, 1500))))
        u = int(round(u_of_x(x, predict(s, u))))
        if u < u_first + 8 or u > u_last - 8: continue
        note = ''
        for mu, mv in m:
            if abs(u - mu) <= 19:        # symbols are 20 to 26 px wide
                u2 = mu + 20 if u >= mu else mu - 20
                if u_first + 8 <= u2 <= u_last - 8:
                    u = u2; note = 'column moved off a marker'
                break
        vp = predict(s, u)
        c = pick(u, vp)
        if not c:
            # the curves are dashed, with a gap of about 15 to 20 px on each side of a marker:
            # step the column away from the nearest marker until ink is found
            mu = min(m, key=lambda p: abs(p[0] - u))[0]
            sgn = 1 if u >= mu else -1
            for step in range(3, 31, 3):
                u2 = u + sgn * step
                if not (u_first + 8 <= u2 <= u_last - 8): break
                c = pick(u2, predict(s, u2))
                if c:
                    u = u2; note += ('; ' if note else '') + 'column moved %d px off a gap in the dashed line' % (sgn * step)
                    break
        if not c:
            rows.append([s, 'trace', 0, u, int(round(vp)), 0, 0, 'NO-INK ' + note]); continue
        d, vc, t, a, b = c[0]
        bound = max(3, int(math.ceil(t / 2.0)))
        slope = abs(predict(s, u + 10) - predict(s, u - 10)) / 20.0
        if len(c) > 1 and c[1][0] - d < 25:
            note += ('; ' if note else '') + 'another run within 25 px (v=%d)' % c[1][1]
        g = gridline_near(vc, u)
        if g is not None:
            note += ('; ' if note else '') + 'merged with the horizontal gridline'
        if t > 14 and slope > 0.6:
            note += ('; ' if note else '') + 'steep segment: the vertical cut of the line is %d px, bound is half of it' % t
        elif t > 14:
            note += ('; ' if note else '') + 'thick run (%d px): ink shared with another line or symbol' % t
        seq += 1
        rows.append([s, 'trace', seq, u, vc, 1, bound, note])
    # --- features: first point
    feat.append([s, 'feature', 1, m[0][0], m[0][1], 3, 3, 'first point: the line starts at the first marker'])
    # peak: sweep columns at 1 px
    best = None
    sweep = []
    for u in range(u_first + 5, u_last - 5):
        if min(abs(u - mu) for mu, mv in m) <= 19: continue   # not through a symbol
        vp = predict(s, u)
        c = pick(u, vp, tol=25)
        if not c: continue
        d, vc, t, a, b = c[0]
        if t > 16: continue      # through a symbol or a merged region, skip for the peak
        sweep.append((u, vc, t))
    vmin = min(v for u, v, t in sweep)
    flat = [u for u, v, t in sweep if v <= vmin + 1.0]
    u_pk = int(round(np.mean(flat)))
    t_pk = [t for u, v, t in sweep if u == u_pk]
    t_pk = t_pk[0] if t_pk else 10
    ub = max(3, int(math.ceil((max(flat) - min(flat)) / 2.0)))
    feat.append([s, 'feature', 2, u_pk, vmin, ub, max(3, int(math.ceil(t_pk / 2.0))),
                 'peak of the drawn line; flat top from u=%d to %d (v within 1 px of the minimum)' % (min(flat), max(flat))])
    # last point
    if ends[s] == 'marker':
        feat.append([s, 'feature', 3, m[-1][0], m[-1][1], 3, 3, 'last point: the line ends at the last marker'])
    else:
        u = ends[s]
        c = pick(u, predict(s, u))
        d, vc, t, a, b = c[0]
        feat.append([s, 'feature', 3, u, vc, 4, max(3, int(math.ceil(t / 2.0))),
                     'last point: the line runs on to the right frame line (x = 250); read at u=%d' % u])

w = csv.writer(open(out_csv, 'w', newline=''))
w.writerow(['figure_id', 'panel', 'series_id', 'point_kind', 'sequence', 'pixel_u', 'pixel_v',
            'u_bound_px', 'v_bound_px', 'symbol', 'note'])
for s, kind, seq, u, v, bu, bv, note in rows + feat:
    w.writerow(['FC-1C', 1, s, kind, seq, int(u), int(round(v)), bu, bv, '', note])
