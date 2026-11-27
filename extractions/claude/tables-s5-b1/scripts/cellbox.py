import numpy as np
from PIL import Image
g = np.asarray(Image.open('packet/pages/p0325.png').convert('L'))
cols = {'nasa': (3607, 3923), 'bendix': (3341, 3607), 'vv': (2963, 3341), 'vh': (2617, 2963), 'tau': (2327, 2617),
        'soil': (1821, 2327), 'dr': (1581, 1821), 'gamma': (1257, 1581), 'phi': (977, 1257)}
rows = [(885, 970), (970, 1060), (1060, 1150), (1150, 1235), (1235, 1320), (1320, 1410), (1410, 1500), (1500, 1595)]
for i, (u0, u1) in enumerate(rows, 1):
    out = []
    for k, (v0, v1) in cols.items():
        sub = g[v0 + 15:v1 - 15, u0:u1] < 128   # array index [v, u]
        vs, us = np.where(sub)
        if len(vs) == 0:
            out.append(f"{k}:empty"); continue
        out.append(f"{k}:u{u0+us.min()}-{u0+us.max()},v{v0+15+vs.min()}-{v0+15+vs.max()}")
    print(f"row{i}: " + "  ".join(out))
