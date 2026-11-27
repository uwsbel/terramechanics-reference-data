"""Draft trace samples for F2-34: for each series and each penetration sample, find the dark run on
that row nearest a hand-made guide polyline (from the row scans and crops), report center, width
and the thickness normal to the line. Prints a table for review; the reviewed points go to
points-p1.csv by hand (helpers/build_points.py)."""
import sys, json, math
import numpy as np
from PIL import Image
img = np.array(Image.open('packet/p0090.png').convert('L'))
cal = json.load(open('out/F2-34/cal-p1/calibration.json'))
ax, ay = cal['ax'], cal['ay']
vl, hl = cal['vertical_lines'], cal['horizontal_lines']
DARK = 160
U0, U1 = 1250, 2262

def v_of_x(x, u):
    return (x - ax[0]*u - ax[2]) / ax[1]
def x_of(u, v): return ax[0]*u + ax[1]*v + ax[2]
def y_of(u, v): return ay[0]*u + ay[1]*v + ay[2]

def runs(v):
    row = img[v, U0:U1] < DARK
    out = []; i = 0
    while i < len(row):
        if row[i]:
            j = i
            while j < len(row) and row[j]: j += 1
            out.append((U0+i, U0+j-1)); i = j
        else: i += 1
    return out

def near_hgrid(u, v):
    for L in hl:
        vg = L['v_at_u0'] + L['slope_dv_du']*u
        if abs(v - vg) <= 7: return L['x_value']
    return None
def on_vgrid(a, b, v):
    for L in vl:
        ug = L['u_at_v0'] + L['slope_du_dv']*v
        if a-1 <= ug <= b+1: return L['y_value']
    return None

def guide_u(poly, v):
    # poly: list of (u, v) with v decreasing along the trace; linear interpolation in v
    pts = sorted(poly, key=lambda p: p[1])
    for (u1, v1), (u2, v2) in zip(pts, pts[1:]):
        if v1 <= v <= v2:
            t = (v - v1)/(v2 - v1) if v2 != v1 else 0
            return u1 + t*(u2-u1)
    return None

def pick(poly, v, tol=14):
    ug = guide_u(poly, v)
    if ug is None: return None
    best = None
    for a, b in runs(v):
        c = (a+b)/2
        d = min(abs(c-ug), abs(a-ug), abs(b-ug))
        if d <= tol and (best is None or d < best[0]): best = (d, a, b)
    return best

def sample(poly, v):
    """center u at row v; if the row sits on a horizontal grid line, interpolate between v-9 and v+9"""
    g = near_hgrid(guide_u(poly, v), v)
    if g is not None:
        r1, r2 = pick(poly, v-9), pick(poly, v+9)
        if r1 and r2:
            a = (r1[1]+r2[1])/2; b = (r1[2]+r2[2])/2
            return a, b, 'hgrid%g' % g
        return None
    r = pick(poly, v)
    if r: return r[1], r[2], ''
    return None

def thickness(u, v, a, b):
    # run height along the column at the run center, clipped to 60 px
    c = int(round((a+b)/2)); col = img[:, c] < DARK
    i = v
    while i > v-60 and col[i-1]: i -= 1
    j = v
    while j < v+60 and col[j+1]: j += 1
    return j - i + 1

series = json.load(open(sys.argv[1]))
print('series,x_target,v,u_center,run_a,run_b,w_row,h_col,t_normal,flag,x_aff,y_aff')
for sid, spec in series.items():
    poly = spec['poly']
    xs = spec['xs']
    for x in xs:
        ug = guide_u(poly, v_of_x(x, 1800))
        if ug is None: print(sid, x, 'no guide'); continue
        v = int(round(v_of_x(x, ug)))
        s = sample(poly, v)
        if s is None: print('%s,%g,%d,NONE' % (sid, x, v)); continue
        a, b, flag = s
        u = (a+b)/2; w = b-a+1
        h = thickness(u, v, a, b)
        # local slope of the guide
        u1, u2 = guide_u(poly, v-10), guide_u(poly, v+10)
        s_ = (u2-u1)/20 if (u1 is not None and u2 is not None) else 0
        t = w/math.sqrt(1+s_*s_)
        vg = on_vgrid(a, b, v)
        if vg is not None: flag += ' vgrid%g' % vg
        print('%s,%g,%d,%.1f,%g,%g,%d,%d,%.1f,%s,%.3f,%.1f' % (sid, x, v, u, a, b, w, h, t, flag.strip(), x_of(u, v), y_of(u, v)))
