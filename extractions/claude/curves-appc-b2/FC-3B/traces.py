"""Sample the drawn upper-panel curves every 5 thousandths (nominal u = 686.5 + 5.84 x). A column
that falls on a marker of the series or in a dash gap is shifted by up to +-20 px to the nearest
column with ink (the actual column is what is recorded). Runs are assigned to a series by proximity
to the piecewise-linear interpolation of that series' marker centers, which the curves follow.
Also finds the first and last point of each drawn line and its peak (minimum v among the samples).
Writes points rows (trace + feature) as CSV to stdout; skipped stations to stderr."""
import sys, csv
import numpy as np
from PIL import Image
sys.path.insert(0, "out/FC-3B")
from markers_p1 import M
g = np.array(Image.open("packet/p0124.png").convert("L")) < 128
GRID = [(1270.0, 0.0038), (1561.0, 0.0036), (1854.0, 0.0038), (2141.5, 0.0038), (2437.0, 0.0040), (2733.0, 0.0050)]
VGRID = (978, 1271, 1564, 1855, 2143)
RAD = {"circle": 18, "triangle-down": 15, "triangle-up": 16, "square": 14, "plus": 16}
LINE = 10   # typical thickness of a dash, px
def grid_v(u): return [v0 + s*(u-700) for v0, s in GRID]
def runs_at(u, v0=1500, v1=2728, hw=1):
    col = g[v0:v1, u-hw:u+hw+1].min(axis=1)
    idx = np.where(col)[0]
    out = []
    if len(idx) == 0: return out
    s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s + v0, p + v0)); s = i
        p = i
    out.append((s + v0, p + v0))
    return out
def expect(series, u):
    pts = [(m[0], m[1]) for m in M[series][1]]
    return float(np.interp(u, [p[0] for p in pts], [p[1] for p in pts]))
def pick(series, u):
    """Return (v, bound, note) for the series' line at column u, or None."""
    ve = expect(series, u)
    best = None
    for a, b in runs_at(u):
        th = b - a + 1; vc = (a + b) / 2
        if th < 5 or th > 22: continue
        gv = [x for x in grid_v(u) if a - 3 <= x <= b + 3]
        if gv and th <= 8: continue                      # bare gridline
        if abs(vc - ve) > 28: continue
        d = abs(vc - ve)
        if best is None or d < best[0]:
            best = (d, a, b, th, gv)
    if best is None: return None
    d, a, b, th, gv = best
    if gv and th >= 13:
        # curve merged with a horizontal gridline. On a plateau (flat curve) the curve is the part
        # of the run on its own side of the gridline; where the curve is steep it crosses the line
        # and the run center with the full half-thickness bound is used.
        slope = (expect(series, u + 10) - expect(series, u - 10)) / 20
        gname = "%d" % round(5000 - 1000 * GRID.index(next(x for x in GRID if abs(x[0] + x[1]*(u-700) - gv[0]) < 1)))
        if abs(slope) > 0.25: return (a+b)/2, th/2, "curve crosses the %s gridline here; run merged" % gname
        if ve > gv[0] + 3:    return b - LINE/2 + 0.5, 4.0, "run merged with the %s gridline; curve is the lower part of the run" % gname
        elif ve < gv[0] - 3:  return a + LINE/2 - 0.5, 4.0, "run merged with the %s gridline; curve is the upper part of the run" % gname
        else:                 return (a+b)/2, th/2, "curve on the %s gridline; run merged" % gname
    return (a + b) / 2, th / 2, ("thick run %d px (steep line)" % th if th > 14 else "")
w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["figure_id","panel","series_id","point_kind","sequence","pixel_u","pixel_v","u_bound_px","v_bound_px","symbol","note"])
for series, (sym, marks) in M.items():
    rad = RAD[sym]
    def blocked(u):
        return any(abs(u - gu) <= 5 for gu in VGRID) or any(abs(u - m[0]) < rad for m in marks)
    rows = []
    for x in range(10, 250, 5):
        un = int(round(686.5 + 5.84 * x))
        got = None
        for du in [0] + [s*k for k in range(2, 21, 2) for s in (1, -1)]:
            u = un + du
            if blocked(u): continue
            r = pick(series, u)
            if r: got = (u, r, du); break
        if not got:
            print(f"# {series}: no sample near nominal x={x} (u={un}): gap or marker", file=sys.stderr); continue
        u, (v, vb, note), du = got
        if du: note = (f"shifted {du:+d} px from nominal x={x}; " + note).rstrip("; ")
        rows.append((u, v, vb, note))
    seq = 0
    for u, v, vb, note in rows:
        seq += 1
        w.writerow(["FC-3B", 1, series, "trace", seq, u, round(v, 1), 1, round(vb, 1), sym, note])
    # features: first ink column after the first marker, last ink column, peak (min v)
    first = None
    for u in range(int(marks[0][0]) + rad, int(marks[0][0]) + 60):
        r = pick(series, u)
        if r: first = (u, r); break
    last = None
    for u in range(2139, 2000, -1):
        if blocked(u): continue
        r = pick(series, u)
        if r: last = (u, r); break
    # last point for a curve that runs into the 250 gridline: report the last readable column
    peak = min(rows, key=lambda r: r[1])
    fseq = 0
    if first:
        fseq += 1; u, (v, vb, note) = first
        w.writerow(["FC-3B", 1, series, "feature", fseq, u, round(v, 1), 2, round(vb, 1), sym, "first point: left end of the first dash (the line starts at the first marker)" + ("; " + note if note else "")])
    fseq += 1
    w.writerow(["FC-3B", 1, series, "feature", fseq, peak[0], round(peak[1], 1), 3, round(peak[2], 1), sym, "peak: minimum v among the trace samples (flat plateau, location along it uncertain)" + ("; " + peak[3] if peak[3] else "")])
    if last:
        fseq += 1; u, (v, vb, note) = last
        w.writerow(["FC-3B", 1, series, "feature", fseq, u, round(v, 1), 2, round(vb, 1), sym, "last point: end of the last dash" + ("; the last marker follows on the 250 gridline" if series != "n2934" else "; no marker follows, the line ends short of 250") + ("; " + note if note else "")])
    else:
        print(f"# {series}: no last point found", file=sys.stderr)
