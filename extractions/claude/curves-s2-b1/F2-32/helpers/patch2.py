"""Second patch of track.py: in the stretch where the LPT 52 dots run beside the LPT 53 solid line
(v 2222 to 3115) a dot is accepted only where it is a run of its own, separated from the solid
line's run; a row where the dot is merged into the solid line is not an observation of the dot."""
p = 'out/F2-32/helpers/track.py'
s = open(p, encoding='utf-8').read()

s = s.replace('''def nearest_ink_row(pts, v, maxd=14):''', '''def track_dots(guide, v_start, v_end, tol, max_w=9):
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


def nearest_ink_row(pts, v, maxd=14):''')

s = s.replace("T['lpt52'] = track(g_52, 2222, 3475, 6, max_w=9)",
              "T['lpt52'] = track_dots(g_52, 2222, 3115, 6)\nT['lpt52'].update(track(g_52, 3116, 3475, 6, max_w=9))")

# the first-dot row at the top (2218-2226) is clipped by the load-50 grid column; keep the end
# rows as hand-read features/trace rows (already in the script).
open(p, 'w', encoding='utf-8').write(s)
print('patched2:', 'def track_dots' in s)
