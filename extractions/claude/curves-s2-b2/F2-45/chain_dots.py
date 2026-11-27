"""Chain the dot cores of the dotted trace (lpt79) in drawing order, from the dot nearest the origin.
Reads out/F2-45/work/cores.csv (from trace_f245.py); writes out/F2-45/work/dots.csv with each dot's
center (core centroid), its ink extent (bounding box of the original ink connected to the core, grid
band pixels left out) and the spacing to the previous dot."""
import csv, json
import numpy as np
from PIL import Image

INK = np.array(Image.open('packet/p0106.png').convert('L')) < 128
cal = json.load(open('out/F2-45/cal-p1/calibration.json'))
VL = cal['vertical_lines']; HL = cal['horizontal_lines']
cores = [r for r in csv.DictReader(open('out/F2-45/work/cores.csv'))]
P = np.array([[float(r['cu']), float(r['cv'])] for r in cores])
N = np.array([int(r['n_core']) for r in cores])

def ongrid(u, v, half=4):
    for L in VL[1:-1]:
        if abs(u - (L['u_at_v0'] + L['slope_du_dv'] * v)) <= half: return True
    for L in HL[1:-1]:
        if abs(v - (L['v_at_u0'] + L['slope_dv_du'] * u)) <= half: return True
    return False

def ink_extent(cu, cv, r=8):
    """Ink pixels within r of the core centroid, excluding grid band pixels farther than 5 px from it."""
    us, vs = [], []
    for dv in range(-r, r + 1):
        for du in range(-r, r + 1):
            u, v = int(round(cu)) + du, int(round(cv)) + dv
            if du * du + dv * dv > r * r or not INK[v, u]: continue
            if ongrid(u, v) and du * du + dv * dv > 25: continue
            us.append(u); vs.append(v)
    us, vs = np.array(us), np.array(vs)
    return us.min(), us.max(), vs.min(), vs.max(), len(us), us.mean(), vs.mean()

start = np.argmin(np.hypot(P[:, 0] - 2229.9, P[:, 1] - 3559.2))
chain = [start]
d = np.array([-0.55, -0.83])       # initial direction: up and to the left
used = {start}
while True:
    p = P[chain[-1]]
    best = None
    for i in range(len(P)):
        if i in used or N[i] < 1: continue
        q = P[i] - p
        dist = np.hypot(*q)
        if not (8 <= dist <= 30): continue
        cosang = q @ d / dist
        if cosang < np.cos(np.radians(30)): continue
        score = abs(dist - 17) + 20 * (1 - cosang)
        if best is None or score < best[0]: best = (score, i)
    if best is None: break
    i = best[1]
    q = P[i] - p
    d = 0.6 * d + 0.4 * q / np.hypot(*q); d /= np.hypot(*d)
    chain.append(i); used.add(i)

with open('out/F2-45/work/dots.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['k', 'u', 'v', 'n_core', 'ink_umin', 'ink_umax', 'ink_vmin', 'ink_vmax', 'n_ink', 'ink_u', 'ink_v', 'spacing', 'on_grid'])
    prev = None
    for k, i in enumerate(chain, 1):
        u, v = P[i]
        e = ink_extent(u, v)
        sp = '' if prev is None else round(float(np.hypot(*(P[i] - prev))), 2)
        w.writerow([k, round(u, 2), round(v, 2), N[i], *e[:5], round(e[5], 2), round(e[6], 2), sp, int(ongrid(u, v, 7))])
        prev = P[i]
print('dots chained:', len(chain), 'first', P[chain[0]], 'last', P[chain[-1]])
