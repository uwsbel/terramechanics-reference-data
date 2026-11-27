"""Reader helper for Figure 2-32 (page p0088.png, printed sideways: penetration up, load left).

Follows each drawn line row by row along a hand-set guide polyline (read from zoomed crops),
takes the dark run nearest to the guide in every row, and writes the trace samples (one every
0.25 in of penetration, on ink) and the features. Grid lines are masked so a run is the curve's
own ink; a sample that would fall on a grid line is moved to the nearest ink row off the line.
Pixel coordinates are those of the unrotated page (u right, v down).

Run from the F2-32 workspace: python out/F2-32/helpers/track.py
"""
import csv, json, math
import numpy as np
from PIL import Image

IMG = 'packet/p0088.png'
CAL = 'out/F2-32/cal-p1/calibration.json'
OUT = 'out/F2-32/points-p1.csv'
FIG = 'F2-32'

im = np.array(Image.open(IMG).convert('L'))
dark = im < 128
cal = json.load(open(CAL))
ax, ay = cal['ax'], cal['ay']

# grid lines as located (plot_grid.py lines, right strip for the horizontal ones)
HROWS = [1416.0, 1618.5, 1827.5, 2034.5, 2239.5, 2446.0, 2653.5, 2861.0, 3066.5, 3274.5, 3476.5, 3689.0]
VCOLS = [541.0, 749.5, 958.0, 1167.0, 1369.0, 1575.0, 1782.0, 1988.5]
GRID_HALF = 6
mask = np.ones_like(dark)
for r in HROWS:
    mask[int(r) - GRID_HALF:int(r) + GRID_HALF + 1, :] = 0
for c in VCOLS:
    mask[:, int(c) - 5:int(c) + 6] = 0
ink = dark & mask.astype(bool)
colmask = np.zeros(dark.shape[1], bool)
for c in VCOLS:
    colmask[int(c) - 5:int(c) + 6] = True


def clipped(a, b):
    """True when the run touches a masked vertical grid column (the line crosses a load grid line)."""
    return colmask[max(a - 1, 0)] or colmask[min(b + 1, len(colmask) - 1)]


def is_grid_row(v):
    return any(abs(v - r) <= GRID_HALF for r in HROWS)


def runs_in_row(v, u0=530, u1=2000):
    row = ink[v, u0:u1]
    out = []
    inrun = False
    for i, d in enumerate(row):
        if d and not inrun:
            s = i; inrun = True
        elif not d and inrun:
            out.append((s + u0, i - 1 + u0)); inrun = False
    if inrun:
        out.append((s + u0, u1 - 1))
    return out


def pen_of(u, v):
    return ax[0] * u + ax[1] * v + ax[2]


def load_of(u, v):
    return ay[0] * u + ay[1] * v + ay[2]


def v_of_pen(pen, u):
    return (pen - ax[0] * u - ax[2]) / ax[1]


class Guide:
    def __init__(self, pts):  # list of (v, u), v increasing
        self.pts = sorted(pts)

    def u(self, v):
        p = self.pts
        if v <= p[0][0]:
            (v0, u0), (v1, u1) = p[0], p[1]
        elif v >= p[-1][0]:
            (v0, u0), (v1, u1) = p[-2], p[-1]
        else:
            for i in range(len(p) - 1):
                if p[i][0] <= v <= p[i + 1][0]:
                    (v0, u0), (v1, u1) = p[i], p[i + 1]
                    break
        return u0 + (u1 - u0) * (v - v0) / (v1 - v0) if v1 != v0 else u0


def track(guide, v_start, v_end, tol, max_w=None):
    """Row by row from v_start to v_end: the run nearest the guide within tol px, or None.
    Runs clipped by a vertical grid column are left out; with max_w, wider runs (merged with a
    neighbouring line) are left out too, so that only a lone run of this line is accepted."""
    pts = {}
    for v in range(v_start, v_end + 1):
        if is_grid_row(v):
            continue
        ug = guide.u(v)
        best = None
        for a, b in runs_in_row(v):
            if clipped(a, b):
                continue
            if max_w is not None and b - a + 1 > max_w:
                continue
            c = 0.5 * (a + b)
            d = 0 if a <= ug <= b else min(abs(ug - a), abs(ug - b))
            if d <= tol and (best is None or abs(c - ug) < abs(best[0] - ug)):
                best = (c, a, b)
        if best is not None:
            pts[v] = best
    return pts


def track_dots(guide, v_start, v_end, tol, max_w=9):
    """Like track(), for the dotted line where it runs just left of the solid line: a row counts
    only when the dot is a run of its own (width <= max_w, not clipped) with the solid line's run
    starting 2 to 20 px to its right."""
    pts = {}
    for v in range(v_start, v_end + 1):
        if is_grid_row(v):
            continue
        ug = guide.u(v)
        rr = runs_in_row(v)
        best = None
        for i, (a, b) in enumerate(rr):
            if clipped(a, b) or b - a + 1 > max_w:
                continue
            right = [r for r in rr if 2 <= r[0] - b <= 20]
            if not right:
                continue
            c = 0.5 * (a + b)
            d = 0 if a <= ug <= b else min(abs(ug - a), abs(ug - b))
            if d <= tol and (best is None or abs(c - ug) < abs(best[0] - ug)):
                best = (c, a, b)
        if best is not None:
            pts[v] = best
    return pts


def nearest_ink_row(pts, v, maxd=14):
    for d in range(0, maxd + 1):
        for vv in (v - d, v + d):
            if vv in pts:
                return vv
    return None


rows = []
seq = {}


def add(series, kind, u, v, ub, vb, note=''):
    seq[series] = seq.get(series, 0) + 1
    rows.append(dict(figure_id=FIG, panel=1, series_id=series, point_kind=kind, sequence=seq[series],
                     pixel_u=round(u, 1), pixel_v=round(v, 1), u_bound_px=round(ub, 1), v_bound_px=round(vb, 1),
                     symbol='', note=note))


def slope_at(pts, v, h=12):
    vs = [vv for vv in range(v - h, v + h + 1) if vv in pts]
    if len(vs) < 4:
        return 0.65
    us = [pts[vv][0] for vv in vs]
    return abs(np.polyfit(vs, us, 1)[0])


def bounds_from_run(pts, v):
    c, a, b = pts[v]
    w = b - a + 1
    s = slope_at(pts, v)
    t = w / math.sqrt(1 + s * s)  # thickness normal to the line
    return max(1.0, w / 2.0), max(1.0, t / 2.0), w


def thickness(pts, v):
    c, a, b = pts[v]
    w = b - a + 1
    s = slope_at(pts, v)
    return w / math.sqrt(1 + s * s)


def near_vcol(u, d=16):
    return any(abs(u - c) <= d for c in VCOLS)


def sample_trace(series, pts, pens, expected_t, overlap_note, dash_note):
    """Trace samples at the given penetrations; each on ink, moved off grid rows and dash gaps."""
    for pen in pens:
        ug = np.mean([p[0] for p in pts.values()])
        v = int(round(v_of_pen(pen, ug)))
        # refine v with the tracked u at that v
        for _ in range(3):
            uu = pts[nearest_ink_row(pts, v, 40)][0]
            v = int(round(v_of_pen(pen, uu)))
        vv = nearest_ink_row(pts, v, 24)
        if vv is None:
            print('WARNING', series, pen, 'no ink within 24 rows of', v)
            continue
        notes = []
        # a tapered dash end (run much thinner than the line): move to a full-width row nearby
        if thickness(pts, vv) < 0.5 * expected_t:
            for d in range(1, 10):
                cands = [x for x in (vv - d, vv + d) if x in pts and thickness(pts, x) >= 0.7 * expected_t]
                if cands:
                    notes.append(f'row {vv} is a tapered dash end; moved {cands[0] - vv:+d} px to the full-width ink')
                    vv = cands[0]
                    break
        ub, vb, w = bounds_from_run(pts, vv)
        t = thickness(pts, vv)
        if vv != v:
            if is_grid_row(v):
                notes.insert(0, f'nominal pen {pen:.2f} is on the pen {int(round(pen))} grid line; sampled at nearest ink row off it ({vv - v:+d} px)')
            elif near_vcol(pts[vv][0]) or near_vcol(ug):
                notes.insert(0, f'nominal pen {pen:.2f} falls where the line crosses a load grid line; sampled at the nearest row clear of it ({vv - v:+d} px)')
            else:
                notes.insert(0, f'{dash_note} at nominal pen {pen:.2f}; sampled at nearest ink row ({vv - v:+d} px)')
        if t > expected_t * 1.5:
            notes.append(overlap_note)
            vb = max(vb, ub)
        add(series, 'trace', pts[vv][0], vv, ub, vb, '; '.join(notes))


# ---------------------------------------------------------------- guides (v, u) from the crops
# thin straight fit line: top end (761,1925) to the load axis at (1893,3683); ink is thin solid
# 1925-2150, thin dashed 2165-2222 and 3408-3500, coincident with the LPT 52 dots 2222-3390,
# thin solid 3516-3683.
g_fit = Guide([(1924, 761), (2148, 904.5), (2222, 951.5), (2250, 971), (2300, 1007), (2500, 1125),
               (2700, 1260.5), (2900, 1390), (3100, 1516.5), (3204, 1589.5), (3300, 1644),
               (3340, 1670), (3380, 1696), (3412, 1724.5), (3444, 1743), (3484, 1769.5), (3604, 1844.5),
               (3620, 1855), (3652, 1875.5), (3676, 1890.5), (3683, 1894)])
# LPT 93, thick dashed: starts on the load axis at pen 0 (dash blob u 1951-1985), rises steeply in
# load to a knee near (1885,3650), then straight up-left to its top end (914,2270).
g_93 = Guide([(3683, 1968), (3664, 1920), (3652, 1886), (3644, 1879), (3628, 1861), (3604, 1833.5),
              (3572, 1809), (3548, 1791), (3524, 1772), (3484, 1743.5), (3444, 1713), (3404, 1680),
              (3364, 1647), (3324, 1614), (3300, 1595.5), (3236, 1543.5), (3196, 1511), (3148, 1476),
              (3100, 1439), (3052, 1404), (3012, 1378.5), (2972, 1350), (2932, 1323.5), (2892, 1298),
              (2852, 1270.5), (2804, 1242), (2756, 1212.5), (2708, 1183), (2660, 1153), (2612, 1125),
              (2564, 1094), (2516, 1064), (2468, 1035), (2420, 1005), (2372, 975.5), (2324, 946),
              (2300, 931), (2270, 914)])
# LPT 53, thick solid: starts on the pen-2 grid line at the load axis, leaves the grid line near
# u 1900, bends up-left and runs straight (right of the dots) to its top end (981.5,2216).
g_53 = Guide([(3266, 1900), (3262, 1880), (3254, 1840), (3246, 1800), (3240, 1770), (3236, 1755),
              (3228, 1736), (3220, 1713), (3212, 1694), (3204, 1678), (3196, 1660), (3188, 1645),
              (3180, 1634), (3172, 1620), (3164, 1608), (3156, 1599), (3148, 1587), (3132, 1567),
              (3124, 1561), (3116, 1553), (3108, 1546), (3100, 1537), (3092, 1530), (3084, 1524),
              (3076, 1516), (3000, 1461), (2900, 1396.5), (2800, 1338), (2700, 1274), (2600, 1203),
              (2500, 1131), (2412, 1074), (2300, 1020.5), (2260, 1001), (2246, 995), (2232, 987.5),
              (2226, 984.5), (2216, 981.5)])
# LPT 52, dotted: first dot (1973.5,3475) on the pen-1 grid line at the load axis; dots rise
# steeply in load, bend near pen 1.3 and join the straight line (on which the thin fit line lies)
# near (1700,3370); top end at the first dot (965.5,2222).
g_52 = Guide([(3475, 1973.5), (3473, 1959.5), (3469, 1945.5), (3465, 1931.5), (3462, 1917), (3460, 1903),
              (3458, 1890), (3452, 1862), (3444, 1840), (3436, 1815), (3428, 1795), (3420, 1776),
              (3412, 1760), (3404, 1741), (3396, 1734), (3388, 1721), (3380, 1708), (3372, 1702),
              (3364, 1696), (3356, 1687.5), (3340, 1678.5), (3324, 1660.5), (3300, 1646), (3204, 1589.5),
              (3100, 1516.5), (3000, 1453), (2900, 1388), (2800, 1326), (2700, 1260.5), (2600, 1196),
              (2500, 1124), (2412, 1070), (2300, 1006), (2258, 986), (2248, 979.5), (2232, 972.5), (2222, 965.5)])

T = {}
T['fit'] = track(g_fit, 1924, 3683, 5)
T['lpt93'] = track(g_93, 2270, 3683, 7)
T['lpt53'] = track(g_53, 2216, 3267, 7)
T['lpt52'] = track_dots(g_52, 2222, 3115, 6)
T['lpt52'].update(track(g_52, 3116, 3475, 6, max_w=9))

for k, pts in T.items():
    vs = sorted(pts)
    print(k, 'tracked rows', len(vs), 'from', vs[0], 'to', vs[-1])

# ---------------------------------------------------------------- LPT 93
pts = T['lpt93']
add('lpt93', 'feature', 1968, 3683, 17, 5,
    'first: trace starts on the load axis at pen 0; first dash is a blob lying on the frame line, u 1951 to 1985 (interval)')
add('lpt93', 'trace', 1968, 3683, 17, 5, 'ink start: first dash lying on the frame line at pen 0, u 1951 to 1985 (interval)')
add('lpt93', 'feature', 1903, 3655, 10, 4,
    'knee: upper-left end of the first (shallow) dash, where the initial rise (load 0 to about 5 lb within 0.17 in) turns into the straight part; the next dash starts at (1886,3652) across a gap, the thin fit line passes through the same spot')
pens = np.arange(0.25, 7.0, 0.25)
sample_trace('lpt93', pts, pens, 8, 'runs together with the thin fit line here (merged ink), bound widened',
             'dash gap')
add('lpt93', 'trace', 914, 2270, 4, 4, 'ink end: top end of the dashed line')
add('lpt93', 'feature', 914, 2270, 4, 4, 'last: top end of the dashed line ink; also the peak (load increases to the end)')
add('lpt93', 'feature', 914, 2270, 4, 4, 'peak: maximum load is at the last point')

# ---------------------------------------------------------------- LPT 53
pts = T['lpt53']
add('lpt53', 'feature', 1940, 3271, 45, 5,
    'first: trace starts on the pen 2 grid line at load 0 (test started 2 in below the surface); its ink coincides with the grid line between u 1895 and 1985, start given as an interval')
add('lpt53', 'trace', 1940, 3271, 45, 5, 'ink start: on the pen 2 grid line at load 0, coincident with the grid line between u 1895 and 1985 (interval)')
add('lpt53', 'feature', 1900, 3266, 6, 5,
    'knee: the trace leaves the pen 2 grid line here (slope changes from along the line to about 5 px per px); after it the curve bends smoothly up to the straight part by about pen 3.5, with no sharp kink')
pens = np.arange(2.25, 7.25, 0.25)
sample_trace('lpt53', pts, pens, 7, 'runs together with the LPT 52 dots (merged ink), bound widened', 'gap in ink')
add('lpt53', 'trace', 981.5, 2216, 4, 4, 'ink end: top end of the solid line')
add('lpt53', 'feature', 981.5, 2216, 4, 4, 'last: top end of the solid line ink; also the peak')
add('lpt53', 'feature', 981.5, 2216, 4, 4, 'peak: maximum load is at the last point')

# ---------------------------------------------------------------- LPT 52
pts = T['lpt52']
add('lpt52', 'feature', 1973.5, 3475, 4, 4,
    'first: first dot, on the pen 1 grid line next to the load axis (test started 1 in below the surface); a 7 px gap separates it from the frame')
add('lpt52', 'trace', 1973.5, 3475, 4, 4, 'ink start: first dot, on the pen 1 grid line next to the load axis')
add('lpt52', 'feature', 1850, 3447, 6, 5,
    'knee (gentle): the initial rise (load 0 to about 7 lb within 0.15 in) bends gradually here from about 4.8 to 2.7 px per px; the sharper knee is the join with the straight part, recorded separately')
add('lpt52', 'feature', 1703, 3377, 6, 5,
    'knee: the climbing start joins the straight part (slope changes from about 1.8 to 0.65 px per px); from here up the dots lie on the straight line the thin fit line is drawn on')
pens = np.arange(1.25, 7.25, 0.25)
sample_trace('lpt52', pts, pens, 6, 'dot merged with the thin fit line or the LPT 53 solid line, bound widened', 'between dots (dots about 12 px apart; the LPT 53 solid line runs just right of them)')
add('lpt52', 'trace', 965.5, 2222, 3, 4, 'ink end: top end of the dotted line (last dot)')
add('lpt52', 'feature', 965.5, 2222, 3, 4, 'last: top end of the dotted line (first dot); also the peak')
add('lpt52', 'feature', 965.5, 2222, 3, 4, 'peak: maximum load is at the last point')

# ---------------------------------------------------------------- fit line
pts = T['fit']
add('fit', 'trace', 761, 1925, 2, 2, 'upper end of the thin line ink')
for pen in [8, 7, 6, 5, 4, 3, 2, 1]:
    r = HROWS[11 - pen]
    v = int(round(r))
    above = nearest_ink_row(pts, v - GRID_HALF - 1, 40)
    below = nearest_ink_row(pts, v + GRID_HALF + 1, 40)
    if above > v - GRID_HALF - 1:
        above = max(x for x in pts if x < v - GRID_HALF - 1)
    if below < v + GRID_HALF + 1:
        below = min(x for x in pts if x > v + GRID_HALF + 1)
    ua, ub_ = pts[above][0], pts[below][0]
    u = ua + (ub_ - ua) * (r - above) / (below - above)
    hw = max(bounds_from_run(pts, above)[0], bounds_from_run(pts, below)[0])
    note = f'crossing of the pen {pen} grid line, interpolated between the ink {v - above} px above and {below - v} px below'
    if 2 <= pen <= 7:
        note += '; here the fit line coincides with the LPT 52 dotted trace (its straight part) and has no separate ink'
        hw = max(hw, 5)
    add('fit', 'trace', u, r, hw, 3, note)
add('fit', 'trace', 1893, 3683, 4, 3, 'lower end of the thin line ink, on the load axis (frame)')
add('fit', 'feature', 1893, 3683, 4, 3, 'intercept: the line meets the load axis (pen 0) here; the page prints Intercept = 4.7 lbs.')
# label center: text block "Slope = 6.5 lbs./in. = A gamma N_q", ink u 838-884, v 1349-1949 (leader below)
add('fit', 'feature', 861, 1649, 23, 300, 'label: Slope = 6.5 lbs./in. = A gamma Nq (the gamma is a Greek letter, Nq has q as a subscript; printed rotated, reading upward; center of the text block, leader arrow from its lower end to the line at (862,2042))')

# a dot sampled on one row: its center is known to no better than the dot radius (about 3 px)
for r in rows:
    if r['series_id'] == 'lpt52' and r['point_kind'] == 'trace':
        r['u_bound_px'] = max(r['u_bound_px'], 3.0)
        r['v_bound_px'] = max(r['v_bound_px'], 3.0)

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['figure_id', 'panel', 'series_id', 'point_kind', 'sequence', 'pixel_u', 'pixel_v',
                                      'u_bound_px', 'v_bound_px', 'symbol', 'note'])
    w.writeheader()
    for r in rows:
        w.writerow(r)
print('wrote', OUT, len(rows), 'rows')
from collections import Counter
print(Counter((r['series_id'], r['point_kind']) for r in rows))

# diagnostics: tracked runs every 8 rows, for checking
with open('out/F2-32/helpers/track-diagnostic.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['series', 'v', 'u_center', 'run_a', 'run_b', 'width'])
    for k, pts in T.items():
        for v in sorted(pts):
            if v % 4 == 0:
                c, a, b = pts[v]
                w.writerow([k, v, c, a, b, b - a + 1])
