"""Reader helper for Figure 2-33 (page p0089.png): builds the centerline of each drawn line from
the ink, samples the recorded traces every 0.25 in of penetration, and writes points-p1.csv.
Pixel coordinates are those of the unrotated page (u right, v down)."""
import json, csv
import numpy as np
from PIL import Image

IMG = 'packet/p0089.png'
CAL = 'out/F2-33/cal-p1/calibration.json'
OUT = 'out/F2-33/points-p1.csv'
FIG = 'F2-33'

im = np.array(Image.open(IMG).convert('L'))
dark = im < 128
cal = json.load(open(CAL))
ax, ay = cal['ax'], cal['ay']
HL = {int(h['x_value']): h for h in cal['horizontal_lines']}   # penetration lines
VL = {int(v['y_value']): v for v in cal['vertical_lines']}     # load lines

def pen(u, v): return ax[0]*u + ax[1]*v + ax[2]
def load(u, v): return ay[0]*u + ay[1]*v + ay[2]
def grid_v(p, u): h = HL[p]; return h['v_at_u0'] + h['slope_dv_du']*u
PENS = sorted(HL)
def pen_pw(u, v):
    """penetration interpolated between the two detected grid lines around v (at this u);
    beyond the last line, extrapolated with the spacing of the last interval"""
    vs = [grid_v(p, u) for p in PENS]
    for k in range(len(PENS)-1):
        if vs[k] >= v >= vs[k+1]:
            return PENS[k] + (vs[k]-v)/(vs[k]-vs[k+1])
    if v > vs[0]: return PENS[0] - (v-vs[0])/(vs[0]-vs[1])
    return PENS[-1] + (vs[-1]-v)/(vs[-2]-vs[-1])

# ---------- run finders ----------
def row_runs(v, u0, u1, wmin=1, wmax=10**6):
    row = dark[int(round(v)), u0:u1]; out = []; i = 0; n = len(row)
    while i < n:
        if row[i]:
            j = i
            while j < n and row[j]: j += 1
            w = j - i
            if wmin <= w <= wmax: out.append((u0 + (i + j - 1)/2.0, w))
            i = j
        else: i += 1
    return out
def col_runs(u, v0, v1, wmin=1, wmax=10**6):
    col = dark[v0:v1, int(round(u))]; out = []; i = 0; n = len(col)
    while i < n:
        if col[i]:
            j = i
            while j < n and col[j]: j += 1
            w = j - i
            if wmin <= w <= wmax: out.append((v0 + (i + j - 1)/2.0, w))
            i = j
        else: i += 1
    return out
def run_through(line, c):
    """width of the dark run that contains index c along a 1-D boolean line; None if not dark"""
    c = int(round(c))
    if not line[c]: return None
    i = c
    while i > 0 and line[i-1]: i -= 1
    j = c
    while j < len(line)-1 and line[j+1]: j += 1
    return j - i + 1
def widths_through(u, v):
    rw = run_through(dark[int(round(v)), :], u)
    cw = run_through(dark[:, int(round(u))], v)
    return rw, cw

# ---------- trackers ----------
def track_rows(u_start, v_start, v_end, step, wmin, wmax, maxdev=10, u_lo=340, u_hi=2320):
    """follow a line by rows from v_start to v_end (step may be negative); returns [(u, v, w)]
    with w the row-run width"""
    pts = [(u_start, v_start, None)]
    pred_slope = 0.0
    v = v_start + step
    last_u, last_v = u_start, v_start
    while (step < 0 and v >= v_end) or (step > 0 and v <= v_end):
        pred = last_u + pred_slope*(v - last_v)
        cands = [(abs(c - pred), c, w) for c, w in row_runs(v, u_lo, u_hi, wmin, wmax)]
        cands = [c for c in cands if c[0] <= maxdev]
        if cands:
            d, c, w = min(cands)
            if abs(v - last_v) > 0: pred_slope = 0.5*pred_slope + 0.5*(c - last_u)/(v - last_v)
            pts.append((c, v, w)); last_u, last_v = c, v
        v += step
    return pts
def track_cols(v_start, u_start, u_end, step, wmin, wmax, maxdev=8, v_lo=1750, v_hi=3618):
    pts = [(u_start, v_start, None)]
    pred_slope = 0.0
    u = u_start + step
    last_u, last_v = u_start, v_start
    while (step < 0 and u >= u_end) or (step > 0 and u <= u_end):
        pred = last_v + pred_slope*(u - last_u)
        cands = [(abs(c - pred), c, w) for c, w in col_runs(u, v_lo, v_hi, wmin, wmax)]
        cands = [c for c in cands if c[0] <= maxdev]
        if cands:
            d, c, w = min(cands)
            if abs(u - last_u) > 0: pred_slope = 0.5*pred_slope + 0.5*(c - last_v)/(u - last_u)
            pts.append((u, c, w)); last_u, last_v = u, c
        u += step
    return pts

# ---------- straight lines ----------
def fit_line(rows, prior, wmin, wmax, exclude, tol=15):
    """least-squares u = a + b v through the row-run centres of a thick straight line, taking in
    each row the run nearest the prior line (a function of v) within tol px; rows where the run
    is merged with something else (width outside wmin..wmax) or listed in exclude are left out"""
    us, vs, ws = [], [], []
    for v in rows:
        if any(a <= v <= b for a, b in exclude): continue
        up = prior(v)
        rr = [(abs(c-up), c, w) for c, w in row_runs(v, int(up)-60, int(up)+60, wmin, wmax)]
        rr = [r for r in rr if r[0] <= tol]
        if rr:
            d, c, w = min(rr); us.append(c); vs.append(v); ws.append(w)
    vs = np.array(vs, float); us = np.array(us, float)
    A = np.vstack([np.ones_like(vs), vs]).T
    (a, b), res, *_ = np.linalg.lstsq(A, us, rcond=None)
    r = us - (a + b*vs)
    return a, b, float(np.sqrt(np.mean(r**2))), len(vs), float(np.median(ws))

def line_top(a, b, v_from, v_to, wmin, wmax, tol=8):
    """highest row (smallest v) that still holds the line's run: the top of its ink"""
    last = None
    for v in range(v_from, v_to, -1):
        u = a + b*v
        rr = [c for c, w in row_runs(v, int(u)-40, int(u)+40, wmin, wmax) if abs(c-u) <= tol]
        if rr: last = v
        elif last is not None and v < last - 3: break
    return last

# ================= lpt74 (thin, A) =================
# near-horizontal start: columns from u=2250 down to 1690; first ink merged with the load-0 axis line
l74a = [(2290, 3611.0, None), (2270, 3610.5, None), (2260, 3610.5, None)]
l74a += track_cols(3605.5, 2250, 1690, -5, 3, 12, maxdev=8, v_lo=3440, v_hi=3611)
# kink region, where the trace runs along the right edge of the fit line (manual, from 2 px row scans)
l74b = [(1680, 3495, 6), (1672, 3490, 6), (1660, 3480, 6), (1650, 3470, 6), (1647, 3460, 6),
        (1649.5, 3454, 6), (1650.5, 3448, 10), (1655, 3442, 8)]
# steep part: rows from 3440 up to the end at 2238
# lpt74 gap under the label: no ink between v=2921 and v=2981 (checked by 2 px row scans),
# so the steep part is tracked in two pieces and nothing is interpolated across the gap
GAP74 = (2921, 2981)
l74c = track_rows(1656.5, 3440, 3002, -2, 3, 24, maxdev=8)
# crossing of the pen 2 grid line (2 px row scans; the grid line rows 2994 to 2996 are merged)
l74c += [(1572.5, 3000, 6), (1568, 2995, 6), (1564, 2990, 9), (1562.5, 2988, 6), (1560.5, 2984, 6), (1559.5, 2982, 6)]
l74c += track_rows(1520.5, 2920, 2338, -2, 3, 24, maxdev=8)
# step at constant penetration near v 2330 (2 px row scans: 2336 u 1028, 2328 u 992..1004, 2324 u 994.5)
l74c += [(1028, 2336, 7), (1016, 2332, 24), (1000, 2328, 12), (994.5, 2324, 6)]
l74c += track_rows(992.5, 2320, 2238, -2, 3, 24, maxdev=8)
l74 = l74a + l74b + l74c
l74 = [(u, v, w) for (u, v, w) in l74 if 2238 <= v]
l74.append((935.0, 2237.5, 5))

for (u, v, w) in l74:
    pass
# ================= lpt75 (thick, B) =================
l75a = [(2303.0, 2991.0, None)]
l75a += track_cols(2991.0, 2298, 1060, -5, 8, 20, maxdev=8, v_lo=2560, v_hi=3000)
# merged with the fit line (v 2612..2730): centre of the merged run
l75b = []
for v in range(2728, 2612, -4):
    if 2686 <= v <= 2698: continue
    rr = row_runs(v, 930, 1070, 12, 40)
    if rr: l75b.append((rr[0][0], v, rr[0][1]))
l75c = track_rows(965.5, 2608, 2238, -2, 6, 18, maxdev=10)
l75 = l75a + l75b + l75c
l75.append((910.5, 2236.0, 6))

# ================= straight lines =================
# priors from the 10 px row scans (fit: 781 at v 2400, 1747.5 at 3600; bce: 1572.5 at 2200, 2088.5 at 3600)
fit_a, fit_b, fit_rms, fit_n, fit_w = fit_line(range(2110, 3600, 3), lambda v: 781 + (v-2400)*0.8054, 10, 17,
                                               exclude=[(2140, 2200), (2600, 2740), (3440, 3500)])
bce_a, bce_b, bce_rms, bce_n, bce_w = fit_line(range(2010, 3600, 3), lambda v: 1572.5 + (v-2200)*0.3686, 9, 17,
                                               exclude=[(2810, 2870)])
fit_top, fit_top_u = 2096, 544.5   # rows 2096 (u 544.5, w 12) is the highest with ink; 2092 none
bce_top, bce_top_u = 1994, 1499.0  # row 1994 (u 1499, w 9) highest with ink; 1990 none
for name, a, b, rows_ in (('fit', fit_a, fit_b, range(2100, 3600, 100)), ('bce', bce_a, bce_b, range(2000, 3600, 100))):
    print(name, 'residual bands (ink centre minus line) :')
    for v0 in rows_:
        r = []
        for v in range(v0, v0+100, 2):
            up = a + b*v
            rr = [c for c, w in row_runs(v, int(up)-40, int(up)+40, 8, 18) if abs(c-up) <= 15]
            if len(rr) == 1: r.append(rr[0]-up)
        print('   v %d..%d: n=%d mean %.1f' % (v0, v0+100, len(r), (np.mean(r) if r else float('nan'))))
print('fit: u = %.2f + %.4f v, rms %.2f px, n=%d, median width %.0f, top ink row %s (line gives u %.1f, ink %.1f)' % (fit_a, fit_b, fit_rms, fit_n, fit_w, fit_top, fit_a+fit_b*fit_top, fit_top_u))
print('bce: u = %.2f + %.4f v, rms %.2f px, n=%d, median width %.0f, top ink row %s (line gives u %.1f, ink %.1f)' % (bce_a, bce_b, bce_rms, bce_n, bce_w, bce_top, bce_a+bce_b*bce_top, bce_top_u))

# ---------- sampling ----------
def sample_at_pen(line, target):
    """walk the polyline in drawing order; return (u, v) where pen crosses target (first crossing)"""
    for (u0, v0, _), (u1, v1, _) in zip(line[:-1], line[1:]):
        p0, p1 = pen_pw(u0, v0), pen_pw(u1, v1)
        if (p0 - target)*(p1 - target) <= 0 and p0 != p1:
            t = (target - p0)/(p1 - p0)
            return u0 + t*(u1 - u0), v0 + t*(v1 - v0)
    return None

rows = []
def add(series, kind, seq, u, v, ub, vb, note=''):
    rows.append(dict(figure_id=FIG, panel=1, series_id=series, point_kind=kind, sequence=seq,
                     pixel_u=round(u, 1), pixel_v=round(v, 1), u_bound_px=round(ub, 1),
                     v_bound_px=round(vb, 1), symbol='', note=note))

def bounds_for(u, v, line, cap=40, min_b=2.0):
    """half the row-run and column-run widths through the point; a run merged with a grid line
    or another line (wider than cap), or a point just off the ink, takes the line's typical width"""
    rw, cw = widths_through(u, v)
    note = []
    typ = [w for (_, _, w) in line if w]
    typ_w = float(np.median(typ)) if typ else 6.0
    if rw is None or rw > cap:
        note.append('row run %s, u bound from the line width nearby' % ('off ink' if rw is None else 'merged (%d px)' % rw)); rw = typ_w
    if cw is None or cw > cap:
        note.append('column run %s, v bound from the line width nearby' % ('off ink' if cw is None else 'merged (%d px)' % cw)); cw = typ_w
    return max(min_b, rw/2.0), max(min_b, cw/2.0), '; '.join(note)

NOTES = {
 'lpt74': [(3455, 3496, 'inside the fit line ink (trace runs along its right edge); u uncertain within the thick line'),
           (3305, 3320, 'on the pen 1 grid line'),
           (2990, 3000, 'on the pen 2 grid line; trace ink continuous through it'),
           (2918, 2924, 'last ink before the gap under the label LPT No. 75, Gp = 105 (no ink v 2921 to 2981)'),
           (2686, 2698, 'on the pen 3 grid line'),
           (2380, 2390, 'on the pen 4 grid line; trace at a shallow angle here (step)')],
 'lpt75': [(2985, 2996, 'first ink at the right frame line (load 0), drawn on the pen 2 grid line'),
           (2915, 2930, 'thick line at a shallow angle: row run long, u bound is half of it'),
           (2612, 2730, 'runs together with the fit line (pen 2.9 to 3.27): merged run centre, bound half the merged width'),
           (2686, 2698, 'on the pen 3 grid line'),
           (2380, 2390, 'on the pen 4 grid line')],
}

def write_trace(series, line, targets, first_note, last_pt, last_note, features):
    seq = 1
    u0, v0, _ = line[0]
    ub, vb = features[0][2], features[0][3]
    add(series, 'trace', seq, u0, v0, ub, vb, 'first ink; ' + first_note); seq += 1
    for t in targets:
        s = sample_at_pen(line, t)
        if s is None: print('  no sample for', series, t); continue
        u, v = s
        if series == 'lpt74' and GAP74[0] < v < GAP74[1]:
            print('  sample inside the gap, skipped:', series, t, round(v, 1)); continue
        ub, vb, bn = bounds_for(u, v, line)
        note = 'pen %.2f' % t
        extra = [n for (lo, hi, n) in NOTES.get(series, []) if lo <= v <= hi]
        if extra: note += '; ' + '; '.join(extra)
        if bn: note += '; ' + bn
        add(series, 'trace', seq, u, v, ub, vb, note); seq += 1
    u1, v1 = last_pt
    ub, vb, bn = bounds_for(u1, v1, line)
    add(series, 'trace', seq, u1, v1, ub, vb, 'last ink; ' + last_note); seq += 1
    for (u, v, ub, vb, note) in features:
        add(series, 'feature', seq, u, v, ub, vb, note); seq += 1

targets74 = [0.25*k for k in range(1, 18)]   # 0.25 .. 4.25
write_trace('lpt74', l74, targets74,
            'thin recorded trace A, LPT No. 74; ink starts merged with the load-0 axis line near the frame corner; u uncertain by about 10 px',
            (935.0, 2237.5), 'thin line ends 25 px right of the thick line end (lpt75); maximum load of the trace is here',
            [(2290, 3611, 10, 3, 'first'),
             (1648, 3456, 6, 8, 'knee: first load peak (about 850 lb at pen 0.53); trace touches the fit line here, centre partly hidden in its ink'),
             (1753, 3305, 3, 8, 'knee: local load minimum after the first peak (about 720 lb at pen 1.0), rightmost point of the hump'),
             (1241, 2535, 10, 3, 'knee: small step at constant penetration (recorder wiggle), about 25 lb'),
             (1104, 2394, 10, 3, 'knee: step at constant penetration on the pen 4 grid line (about 30 lb)'),
             (992.5, 2318, 3, 6, 'knee: short vertical run (constant load) before the last rise'),
             (935.0, 2237.5, 3, 3, 'peak: maximum load of the trace (its last point)'),
             (935.0, 2237.5, 3, 3, 'last')])
targets75 = [2.25 + 0.25*k for k in range(0, 9)]   # 2.25 .. 4.25
write_trace('lpt75', l75, targets75,
            'thick recorded trace B, LPT No. 75, started two inches below the surface; ink starts at the right frame line (load 0) on the pen 2 grid line',
            (910.5, 2236.0), 'rounded end of the thick line; maximum load of the trace is here',
            [(2303, 2991, 5, 6, 'first'),
             (1046, 2725, 10, 8, 'knee: joins the fit line (runs together with it up to v 2612)'),
             (960, 2613, 8, 8, 'knee: leaves the fit line to the right; local load maximum (about 1740 lb at pen 3.27)'),
             (1018.5, 2494, 5, 10, 'knee: local load minimum of the hook (about 1670 lb at pen 3.65), rightmost point'),
             (910.5, 2236.0, 6, 3, 'peak: maximum load of the trace (its last point)'),
             (910.5, 2236.0, 6, 3, 'last')])

# straight lines: both ends, crossings of the labelled penetration lines, intercept, label
def local_u(a, b, v, half_window=24, wmin=8, wmax=18):
    """ink centre of a thick straight line at row v from a straight fit through the clean rows
    within half_window of v (rows where the run is merged with a grid line are left out)"""
    us, vs = [], []
    for vv in range(int(v)-half_window, int(v)+half_window+1):
        if vv >= dark.shape[0]: continue
        up = a + b*vv
        rr = [c for c, w in row_runs(vv, int(up)-40, int(up)+40, wmin, wmax) if abs(c-up) <= 15]
        if len(rr) == 1: us.append(rr[0]); vs.append(vv)
    if len(vs) < 6: return a + b*v, 0, 99.0
    A = np.vstack([np.ones(len(vs)), np.array(vs, float)]).T
    (la, lb), *_ = np.linalg.lstsq(A, np.array(us, float), rcond=None)
    r = np.array(us) - (la + lb*np.array(vs))
    return la + lb*v, len(vs), float(np.sqrt(np.mean(r**2)))

def write_line(series, a, b, rms, width, top_v, top_u, label_uv, label_bounds, label_txt, pens):
    seq = 1
    half = width/2.0   # half the measured thickness of the line (median row-run width)
    v0 = 3615.0
    for it in range(5):
        v0 = grid_v(0, a + b*v0)
    u0, n0, r0 = local_u(a, b, v0)
    print('  %s lower end: local u %.1f (n=%d, rms %.1f) vs global %.1f' % (series, u0, n0, r0, a + b*v0))
    add(series, 'trace', seq, u0, v0, half, 4, 'lower end of the ink, at the load axis (pen 0 line); thick straight line, half width %.0f px' % half); seq += 1
    for p in pens:
        v = 3000.0
        for it in range(5):
            v = grid_v(p, a + b*v)
        u, n, r = local_u(a, b, v)
        print('  %s pen %d: local u %.1f (n=%d, rms %.1f) vs global %.1f' % (series, p, u, n, r, a + b*v))
        if n >= 20:
            add(series, 'trace', seq, u, v, half, 4, 'crossing of the pen %d grid line (ink centre from the rows around the grid line)' % p)
        else:
            add(series, 'trace', seq, a + b*v, v, 10, 4, 'crossing of the pen %d grid line, inside the stretch where lpt75 runs together with the fit line (v 2612 to 2730): from the least-squares line through the whole ink (rms %.1f px), bound widened to half the merged width' % (p, rms))
        seq += 1
    add(series, 'trace', seq, top_u, top_v, half, 4, 'upper end of the ink (highest row with ink)'); seq += 1
    add(series, 'feature', seq, u0, v0, half, 4, 'intercept: meets the load axis (penetration 0)'); seq += 1
    add(series, 'feature', seq, label_uv[0], label_uv[1], label_bounds[0], label_bounds[1], 'label: ' + label_txt + ' (centre of the printed text block; bounds are its half extents)'); seq += 1

write_line('fit', fit_a, fit_b, fit_rms, fit_w, fit_top, fit_top_u, (635, 1638), (37, 398), 'Slope = AγNq = 316 lbs./in.', [1, 2, 3, 4])
write_line('bce', bce_a, bce_b, bce_rms, bce_w, bce_top, bce_top_u, (1865, 2280), (20, 510), 'Bearing Capacity Equation, φ = 49.5°', [1, 2, 3, 4, 5])

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note'])
    w.writeheader(); w.writerows(rows)
print('wrote', OUT, len(rows), 'rows')
# centerlines, for the overlay check only
with open('out/F2-33/centerlines.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['series_id','pixel_u','pixel_v','u_bound_px','v_bound_px','point_kind'])
    for s, L in (('lpt74', l74), ('lpt75', l75)):
        for (u, v, wd) in L: w.writerow([s, u, v, 1, 1, 'trace'])
