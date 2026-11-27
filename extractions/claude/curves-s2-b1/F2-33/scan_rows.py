import sys, numpy as np
from PIL import Image
im = np.array(Image.open('packet/p0089.png').convert('L'))
dark = im < 128
VGRID = [363, 761, 1149, 1533, 1922, 2309]
def runs_row(v, u0, u1):
    row = dark[v, u0:u1]
    out = []; i = 0; n = len(row)
    while i < n:
        if row[i]:
            j = i
            while j < n and row[j]: j += 1
            out.append((u0 + (i + j - 1) / 2.0, j - i)); i = j
        else: i += 1
    return out
def runs_col(u, v0, v1):
    col = dark[v0:v1, u]
    out = []; i = 0; n = len(col)
    while i < n:
        if col[i]:
            j = i
            while j < n and col[j]: j += 1
            out.append((v0 + (i + j - 1) / 2.0, j - i)); i = j
        else: i += 1
    return out
mode = sys.argv[1]
a, b, step = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
lo, hi = int(sys.argv[5]), int(sys.argv[6])
for p in range(a, b + 1, step):
    rr = runs_row(p, lo, hi) if mode == 'row' else runs_col(p, lo, hi)
    rr = [(c, w) for c, w in rr if 2 <= w <= 24 and not (mode == 'row' and any(abs(c - g) < 9 for g in VGRID))]
    print(p, ' '.join(f'{c:.1f}/{w}' for c, w in rr))
