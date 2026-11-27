"""Refine eye-read marker seeds by normalized cross-correlation with templates cut from
clean instances on the same page (synthetic ring for the small lower-panel circle).
Search window +-8 px. Prints seed, refined center, NCC score and shift.
Run from the FC-4B workspace root."""
import sys, csv
import numpy as np
from PIL import Image
sys.path.insert(0, 'out/FC-4B/helpers')
from seeds import P1, P2

im = np.array(Image.open('packet/p0127.png').convert('L')).astype(float)
dark = (im < 128).astype(float)


def patch(u, v, h):
    return dark[int(v) - h:int(v) + h + 1, int(u) - h:int(u) + h + 1]


# templates cut from clean instances: (center u, v, half size)
T = {
    'triangle-up': patch(1502, 3097, 19), 'square': patch(1503, 3247, 19),
    'triangle-down': patch(924, 3296, 19), 'plus': patch(1442, 3331, 19), 'circle': patch(1782, 1651, 19),
}
yy, xx = np.mgrid[-12:13, -12:13]
r = np.hypot(xx, yy)
T['small-circle'] = ((r <= 9.5) & (r >= 3.5)).astype(float)


def ncc(a, b):
    a = a - a.mean()
    b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return (a * b).sum() / d if d > 0 else 0.0


def refine(u, v, sym, panel, R=8):
    key = 'small-circle' if (sym == 'circle' and panel == 2) else sym
    t = T[key]
    h = t.shape[0] // 2
    best = (-2, u, v)
    for dv in range(-R, R + 1):
        for du in range(-R, R + 1):
            s = ncc(t, patch(u + du, v + dv, h))
            if s > best[0]:
                best = (s, u + du, v + dv)
    return best


rows = []
for panel, seeds in ((1, P1), (2, P2)):
    for sid, sym, u, v, note in seeds:
        s, ru, rv = refine(u, v, sym, panel)
        rows.append((panel, sid, sym, u, v, ru, rv, round(s, 3), note))
        print(f"p{panel} {sid:6s} {sym:14s} seed=({u},{v}) ncc=({ru},{rv}) score={s:.2f} shift=({ru-u:+d},{rv-v:+d}) {note}")
with open('out/FC-4B/helpers/markers_refined.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['panel', 'series_id', 'symbol', 'seed_u', 'seed_v', 'ncc_u', 'ncc_v', 'score', 'note'])
    w.writerows(rows)
