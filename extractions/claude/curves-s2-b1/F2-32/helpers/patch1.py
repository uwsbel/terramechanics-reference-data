"""One-off patch of track.py (kept for the record of how the reading evolved)."""
p = 'out/F2-32/helpers/track.py'
s = open(p, encoding='utf-8').read()

# 1. clipped runs (touching a masked vertical grid column) are not usable ink
s = s.replace('''ink = dark & mask.astype(bool)
''', '''ink = dark & mask.astype(bool)
colmask = np.zeros(dark.shape[1], bool)
for c in VCOLS:
    colmask[int(c) - 5:int(c) + 6] = True


def clipped(a, b):
    """True when the run touches a masked vertical grid column (the line crosses a load grid line)."""
    return colmask[max(a - 1, 0)] or colmask[min(b + 1, len(colmask) - 1)]
''')
s = s.replace('''def track(guide, v_start, v_end, tol):
    """Row by row from v_start to v_end: the run nearest the guide within tol px, or None."""
    pts = {}
    for v in range(v_start, v_end + 1):
        if is_grid_row(v):
            continue
        ug = guide.u(v)
        best = None
        for a, b in runs_in_row(v):
            c = 0.5 * (a + b)''', '''def track(guide, v_start, v_end, tol, max_w=None):
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
            c = 0.5 * (a + b)''')

# 2. sampler: taper rule, overlap by thickness, notes for vertical grid crossings
old_sampler_start = s.index('def sample_trace(')
old_sampler_end = s.index('# ---------------------------------------------------------------- guides')
s = s[:old_sampler_start] + '''def thickness(pts, v):
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


''' + s[old_sampler_end:]

# 3. tracks: dots accepted only as lone runs
s = s.replace("T['lpt52'] = track(g_52, 2222, 3475, 5)", "T['lpt52'] = track(g_52, 2222, 3475, 6, max_w=9)")

# 4. LPT 93 features and end trace rows
s = s.replace('''add('lpt93', 'feature', 1885, 3650, 6, 5,
    'knee: the shallow initial rise (load 0 to about 5 lb within 0.17 in) turns into the straight part; the thin fit line crosses here')
pens = np.arange(0.25, 7.0, 0.25)
sample_trace('lpt93', pts, pens, 11, 'runs together with the thin fit line here (merged ink), bound widened',
             'dash gap')
add('lpt93', 'feature', 914, 2270, 4, 4, 'last: top end of the dashed line ink; also the peak (load increases to the end)')''', '''add('lpt93', 'trace', 1968, 3683, 17, 5, 'ink start: first dash lying on the frame line at pen 0, u 1951 to 1985 (interval)')
add('lpt93', 'feature', 1903, 3655, 10, 4,
    'knee: upper-left end of the first (shallow) dash, where the initial rise (load 0 to about 5 lb within 0.17 in) turns into the straight part; the next dash starts at (1886,3652) across a gap, the thin fit line passes through the same spot')
pens = np.arange(0.25, 7.0, 0.25)
sample_trace('lpt93', pts, pens, 8, 'runs together with the thin fit line here (merged ink), bound widened',
             'dash gap')
add('lpt93', 'trace', 914, 2270, 4, 4, 'ink end: top end of the dashed line')
add('lpt93', 'feature', 914, 2270, 4, 4, 'last: top end of the dashed line ink; also the peak (load increases to the end)')''')

# 5. LPT 53
s = s.replace('''add('lpt53', 'feature', 1900, 3266, 6, 5,
    'knee: the trace leaves the pen 2 grid line here and bends smoothly up to the straight part by about pen 3; no sharp kink')
pens = np.arange(2.25, 7.25, 0.25)
sample_trace('lpt53', pts, pens, 9, 'runs together with the LPT 52 dots (merged ink), bound widened', 'gap in ink')
add('lpt53', 'feature', 981.5, 2216, 4, 4, 'last: top end of the solid line ink; also the peak')''', '''add('lpt53', 'trace', 1940, 3271, 45, 5, 'ink start: on the pen 2 grid line at load 0, coincident with the grid line between u 1895 and 1985 (interval)')
add('lpt53', 'feature', 1900, 3266, 6, 5,
    'knee: the trace leaves the pen 2 grid line here (slope changes from along the line to about 5 px per px); after it the curve bends smoothly up to the straight part by about pen 3.5, with no sharp kink')
pens = np.arange(2.25, 7.25, 0.25)
sample_trace('lpt53', pts, pens, 7, 'runs together with the LPT 52 dots (merged ink), bound widened', 'gap in ink')
add('lpt53', 'trace', 981.5, 2216, 4, 4, 'ink end: top end of the solid line')
add('lpt53', 'feature', 981.5, 2216, 4, 4, 'last: top end of the solid line ink; also the peak')''')

# 6. LPT 52
s = s.replace('''add('lpt52', 'feature', 1850, 3447, 6, 5,
    'knee: the shallow initial rise (load 0 to about 7 lb within 0.15 in) bends into the climb that joins the straight part near pen 1.55')
pens = np.arange(1.25, 7.25, 0.25)
sample_trace('lpt52', pts, pens, 7, 'dot merged with the thin fit line or the LPT 53 solid line, bound widened', 'between dots')
add('lpt52', 'feature', 965.5, 2222, 3, 4, 'last: top end of the dotted line (first dot); also the peak')''', '''add('lpt52', 'trace', 1973.5, 3475, 4, 4, 'ink start: first dot, on the pen 1 grid line next to the load axis')
add('lpt52', 'feature', 1850, 3447, 6, 5,
    'knee (gentle): the initial rise (load 0 to about 7 lb within 0.15 in) bends gradually here from about 4.8 to 2.7 px per px; the sharper knee is the join with the straight part, recorded separately')
add('lpt52', 'feature', 1703, 3377, 6, 5,
    'knee: the climbing start joins the straight part (slope changes from about 1.8 to 0.65 px per px); from here up the dots lie on the straight line the thin fit line is drawn on')
pens = np.arange(1.25, 7.25, 0.25)
sample_trace('lpt52', pts, pens, 6, 'dot merged with the thin fit line or the LPT 53 solid line, bound widened', 'between dots (dots about 12 px apart; the LPT 53 solid line runs just right of them)')
add('lpt52', 'trace', 965.5, 2222, 3, 4, 'ink end: top end of the dotted line (last dot)')
add('lpt52', 'feature', 965.5, 2222, 3, 4, 'last: top end of the dotted line (first dot); also the peak')''')
open(p, 'w', encoding='utf-8').write(s)
print('patched; sample_trace present:', 'def sample_trace' in s, '; clipped present:', 'def clipped' in s)
