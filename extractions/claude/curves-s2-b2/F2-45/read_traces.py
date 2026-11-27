"""Helper for the blind reading of Figure 2-45 (page p0106.png, printed sideways).

Tracks the solid trace (lpt95) row by row and the dotted trace (lpt79) dot by dot, in the
unrotated page pixels (u right, v down). Penetration increases up the page (v decreasing), load
increases to the left (u decreasing). Writes diagnostics; the sampling into points-p1.csv is done
by sample_points.py from the tracked polylines written here.
"""
import json, sys, csv
import numpy as np
from PIL import Image

IMG = 'packet/p0106.png'
CAL = 'out/F2-45/cal-p1/calibration.json'

cal = json.load(open(CAL))
ax, ay = cal['ax'], cal['ay']
a = np.array(Image.open(IMG))
ink = a < 128

def xval(u, v):
    return ax[0]*u + ax[1]*v + ax[2]

def yval(u, v):
    return ay[0]*u + ay[1]*v + ay[2]

vlines = cal['vertical_lines']      # load lines: u = u_at_v0 + slope*v
hlines = cal['horizontal_lines']    # penetration lines: v = v_at_u0 + slope*u

def grid_u_at(v):
    return [L['u_at_v0'] + L['slope_du_dv']*v for L in vlines]

def grid_v_at(u):
    return [L['v_at_u0'] + L['slope_dv_du']*u for L in hlines]

# frame (values 0 and 300 for load, 0 and 7 for penetration)
def frame_u(v):
    g = grid_u_at(v)
    return min(g), max(g)

def frame_v(u):
    g = grid_v_at(u)
    return min(g), max(g)

GRID_HALF = 4   # half band width masked around a grid line, px (grid lines are 4 to 6 px thick)

def runs_in_row(v, u0, u1):
    """Ink runs along row v between u0 and u1, with grid columns treated as wildcards: a run may
    continue across a grid band, and its center is taken from the non-grid ink only. Returns a list
    of (u_center, width_nongrid, u_start, u_end, crosses_grid)."""
    row = ink[v, u0:u1]
    gus = grid_u_at(v)
    isgrid = np.zeros_like(row)
    for gu in gus:
        lo, hi = int(round(gu - GRID_HALF)) - u0, int(round(gu + GRID_HALF)) - u0
        lo, hi = max(lo, 0), min(hi, len(row) - 1)
        if hi >= lo:
            isgrid[lo:hi + 1] = True
    out = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] and not isgrid[i]:
            j = i
            # extend while ink, allowing passage through grid columns if ink resumes right after
            while j + 1 < n and (row[j + 1] or isgrid[j + 1]):
                j += 1
            # trim trailing grid-only columns
            while j > i and isgrid[j] and not (row[j] and not isgrid[j]):
                j -= 1
            seg = np.arange(i, j + 1)
            good = seg[(row[i:j + 1]) & (~isgrid[i:j + 1])]
            crosses = bool(isgrid[i:j + 1].any())
            out.append((u0 + good.mean(), len(good), u0 + i, u0 + j, crosses))
            i = j + 1
        else:
            i += 1
    return out

def is_grid_row(v, u):
    for gv in grid_v_at(u):
        if abs(v - gv) <= GRID_HALF:
            return True
    return False

def track_solid(start_u, start_v, v_end, pred_slope=0.87, max_jump=7, step=-1):
    """Follow the solid line from (start_u, start_v) in direction step (-1: upward, v decreasing;
    +1: downward). The line is continuous, so a row without a candidate within max_jump of the
    prediction is left as a gap and the tolerance is NOT widened (the dotted trace runs close by
    and widening made the tracker jump onto it). Returns rows (v, u_center, width, crosses_grid, note)."""
    pts = []
    u_pred = start_u
    v = int(start_v)
    hist = []
    gap = 0
    while (v >= v_end) if step < 0 else (v <= v_end):
        fu0, fu1 = frame_u(v)
        if len(hist) >= 6:
            vs = np.array([h[0] for h in hist[-25:]], float)
            us = np.array([h[1] for h in hist[-25:]], float)
            A = np.vstack([vs, np.ones_like(vs)]).T
            m, c = np.linalg.lstsq(A, us, rcond=None)[0]
            u_pred = m*v + c
        elif hist:
            u_pred = hist[-1][1] + pred_slope*(v - hist[-1][0])
        if is_grid_row(v, u_pred):
            pts.append((v, None, None, False, 'grid-row'))
            v += step
            continue
        rs = runs_in_row(v, int(fu0) + 6, int(fu1) - 6)
        cands = [r for r in rs if 2 <= r[1] <= 40 and abs(r[0] - u_pred) <= max_jump]
        if not cands:
            pts.append((v, None, None, False, 'no-ink'))
            v += step
            continue
        r = min(cands, key=lambda r: abs(r[0] - u_pred))
        pts.append((v, r[0], r[1], r[4], ''))
        hist.append((v, r[0]))
        v += step
    return pts

def components(mask, u0, u1, v0, v1):
    """Simple connected components (8-connectivity) of mask within the box, by flood fill."""
    sub = mask[v0:v1, u0:u1].copy()
    H, W = sub.shape
    seen = np.zeros_like(sub)
    comps = []
    for y in range(H):
        for x in range(W):
            if sub[y, x] and not seen[y, x]:
                stack = [(y, x)]
                seen[y, x] = True
                pix = []
                while stack:
                    cy, cx = stack.pop()
                    pix.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                stack.append((ny, nx))
                ys = np.array([p[0] for p in pix]) + v0
                xs = np.array([p[1] for p in pix]) + u0
                comps.append(dict(n=len(pix), u=xs.mean(), v=ys.mean(), umin=xs.min(), umax=xs.max(),
                                  vmin=ys.min(), vmax=ys.max()))
    return comps

if __name__ == '__main__':
    out = {}
    # ---- solid line: starts at the frame corner (penetration 0, load ~0)
    # find the first row above the bottom frame with the trace
    fu0, fu1 = frame_u(3580)
    fv0, fv1 = frame_v(2270)
    print('frame u at v=3580:', fu0, fu1, ' frame v at u=2270:', fv0, fv1)
    # start where the solid line is clear of the dots (seen on the zoomed crop of the origin:
    # at v = 3500 the solid line is at u ~ 2110 and the dotted trace at u ~ 2195), track upward to the
    # top frame and downward to the bottom frame.
    start_v, start_u = 3500, 2110.5
    rs = runs_in_row(start_v, int(fu0) + 6, int(fu1) - 6)
    print('runs at start row', start_v, rs[-4:])
    up = track_solid(start_u, start_v, int(round(fv0)) + 3, step=-1)
    down = track_solid(start_u, start_v + 1, int(round(fv1)) - 3, step=+1)
    solid = list(reversed(down)) + up
    with open('out/F2-45/track-solid.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['v', 'u', 'width_u', 'crosses_grid', 'note'])
        for p in solid:
            w.writerow([p[0], '' if p[1] is None else round(p[1], 2), p[2] if p[2] is not None else '', int(p[3]), p[4]])
    n_ok = sum(1 for p in solid if p[1] is not None)
    print('solid rows tracked:', n_ok, 'of', len(solid), '; no-ink rows:', sum(1 for p in solid if p[4] == 'no-ink'))

    # ---- dotted line: connected components with the grid bands and the solid trace masked
    mask = ink.copy()
    H, W = mask.shape
    vv = np.arange(H)[:, None]
    uu = np.arange(W)[None, :]
    for L in vlines:
        gu = L['u_at_v0'] + L['slope_du_dv']*vv
        mask &= ~(np.abs(uu - gu) <= GRID_HALF)
    for L in hlines:
        gv = L['v_at_u0'] + L['slope_dv_du']*uu
        mask &= ~(np.abs(vv - gv) <= GRID_HALF)
    # mask the solid trace: a band of +-9 px in u around the tracked center
    for p in solid:
        if p[1] is not None:
            lo, hi = int(p[1] - 9), int(p[1] + 9)
            mask[p[0], lo:hi + 1] = False
    comps = components(mask, int(fu0) + 6, int(fu1) - 6, int(fv0) + 6, int(fv1) - 6)
    comps = [c for c in comps if 12 <= c['n'] <= 400]
    print('components kept:', len(comps))
    with open('out/F2-45/components.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['n', 'u', 'v', 'umin', 'umax', 'vmin', 'vmax'])
        for c in comps:
            w.writerow([c['n'], round(c['u'], 2), round(c['v'], 2), c['umin'], c['umax'], c['vmin'], c['vmax']])
