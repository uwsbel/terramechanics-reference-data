"""Dotted trace (lpt79) of Figure 2-45: dots as connected components of the ink with the grid line
bands (+-3 px around each fitted interior line), the frame and the solid trace (its tracked run in
each row, widened by 3 px) removed; kept when the component is dot sized (area 12 to 260 px, box at
most 20 px). Fragments of one dot split by a grid band are merged when their centers are within 9 px.
Dots are chained in drawing order from the dot nearest the origin, each next dot within 8 to 40 px
and within 30 degrees of the running direction, preferring a spacing near 17 px.
Writes out/F2-45/work/dots.csv."""
import csv, json
import numpy as np
from PIL import Image

INK = np.array(Image.open('packet/p0106.png').convert('L')) < 128
cal = json.load(open('out/F2-45/cal-p1/calibration.json'))
VL = cal['vertical_lines']; HL = cal['horizontal_lines']
VLi = [L for L in VL if 0 < L['y_value'] < 300]
HLi = [L for L in HL if 0 < L['x_value'] < 7]
v0, v1, u0, u1 = 1470, 3590, 392, 2272
sub = INK[v0:v1, u0:u1].copy()
vv = np.arange(v0, v1)[:, None]; uu = np.arange(u0, u1)[None, :]
gridmask = np.zeros_like(sub)
for L in VLi:
    gridmask |= np.abs(uu - (L['u_at_v0'] + L['slope_du_dv'] * vv)) <= 3
for L in HLi:
    gridmask |= np.abs(vv - (L['v_at_u0'] + L['slope_dv_du'] * uu)) <= 3
m = sub & ~gridmask
for r in csv.DictReader(open('out/F2-45/work/solid-rows.csv')):
    if r['s'] == '': continue
    v = int(r['v']) - v0
    if 0 <= v < m.shape[0]:
        m[v, max(int(r['s']) - 3 - u0, 0):max(int(r['e']) + 4 - u0, 0)] = False

def label(mask):
    lab = np.zeros(mask.shape, int); comps = []
    for a0, b0 in zip(*np.nonzero(mask)):
        if lab[a0, b0]: continue
        n = len(comps) + 1; st = [(a0, b0)]; lab[a0, b0] = n; pix = []
        while st:
            a, b = st.pop(); pix.append((a, b))
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    x, y = a + da, b + db
                    if 0 <= x < mask.shape[0] and 0 <= y < mask.shape[1] and mask[x, y] and not lab[x, y]:
                        lab[x, y] = n; st.append((x, y))
        comps.append(np.array(pix))
    return comps

def erode_disk(mask, r):
    out = mask.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                out &= np.roll(np.roll(mask, dy, axis=0), dx, axis=1)
    return out

# touching dots are separated by an erosion of radius 2 (their necks are thin); each core's dot is the
# ink of the masked image within 8 px that is nearer to this core than to any other core
# seeds: cores of an erosion of radius 3 (separates touching dots), plus the cores of an erosion of
# radius 2 that hold no radius-3 core (the small dots, 6 to 8 px across, vanish at radius 3)
e3 = erode_disk(m, 3)
c3 = label(e3)
c2 = [c for c in label(erode_disk(m, 2)) if not e3[c[:, 0], c[:, 1]].any()]
cores = c3 + c2
C = np.array([[c[:, 1].mean(), c[:, 0].mean()] for c in cores])          # local (u, v)
merged = []
for k, c in enumerate(cores):
    cu, cv = C[k]
    a0, a1 = int(cv) - 9, int(cv) + 10; b0, b1 = int(cu) - 9, int(cu) + 10
    a0, b0 = max(a0, 0), max(b0, 0)
    vs, us = np.nonzero(m[a0:a1, b0:b1]); vs = vs + a0; us = us + b0
    keep = np.hypot(us - cu, vs - cv) <= 8
    vs, us = vs[keep], us[keep]
    if len(vs) == 0: continue
    near = np.nonzero(np.hypot(C[:, 0] - cu, C[:, 1] - cv) <= 18)[0]
    dd = np.stack([np.hypot(us - C[j, 0], vs - C[j, 1]) for j in near])
    own = near[np.argmin(dd, axis=0)] == k
    vs, us = vs[own], us[own]
    hgt, wid = np.ptp(vs) + 1, np.ptp(us) + 1
    if hgt > 20 or wid > 20 or len(vs) < 4: continue
    merged.append(dict(n=len(vs), n_core=len(c), u=us.mean() + u0, v=vs.mean() + v0, umin=us.min() + u0, umax=us.max() + u0,
                       vmin=vs.min() + v0, vmax=vs.max() + v0, frags=1))
P = np.array([[b['u'], b['v']] for b in merged])

start = int(np.argmin(np.hypot(P[:, 0] - 2229.9, P[:, 1] - 3559.2)))
chain = [start]; used = {start}
d = np.array([-0.55, -0.83])
while True:
    p = P[chain[-1]]; best = None
    for i in range(len(P)):
        if i in used: continue
        q = P[i] - p; dist = float(np.hypot(*q))
        if not (8 <= dist <= 40): continue
        cosang = float(q @ d / dist)
        if cosang < np.cos(np.radians(30)): continue
        score = abs(dist - 17) + 20 * (1 - cosang) + (0 if merged[i]['n'] >= 12 else 6)
        if best is None or score < best[0]: best = (score, i)
    if best is None: break
    i = best[1]; q = P[i] - p
    d = 0.6 * d + 0.4 * q / np.hypot(*q); d /= np.hypot(*d)
    chain.append(i); used.add(i)

def near_grid(u, v, half):
    for L in VLi:
        if abs(u - (L['u_at_v0'] + L['slope_du_dv'] * v)) <= half: return True
    for L in HLi:
        if abs(v - (L['v_at_u0'] + L['slope_dv_du'] * u)) <= half: return True
    return False

with open('out/F2-45/work/dots.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['k', 'u', 'v', 'n', 'umin', 'umax', 'vmin', 'vmax', 'frags', 'spacing', 'near_grid'])
    prev = None
    for k, i in enumerate(chain, 1):
        b = merged[i]
        sp = '' if prev is None else round(float(np.hypot(b['u'] - prev[0], b['v'] - prev[1])), 2)
        w.writerow([k, round(b['u'], 2), round(b['v'], 2), b['n'], b['umin'], b['umax'], b['vmin'], b['vmax'],
                    b['frags'], sp, int(near_grid(b['u'], b['v'], 10))])
        prev = (b['u'], b['v'])
print('cores', len(cores), 'dots', len(merged), 'chained', len(chain), 'first', P[chain[0]], 'last', P[chain[-1]])
