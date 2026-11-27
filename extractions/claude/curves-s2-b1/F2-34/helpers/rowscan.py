"""List dark runs across u on chosen rows v of the page image (inside a u range).
Usage: rowscan.py image v0 v1 step u0 u1 [dark]
Grid-line columns (vertical lines of the calibration) are marked with 'G' when a run is narrow and near one."""
import sys, json
import numpy as np
from PIL import Image
img = np.array(Image.open(sys.argv[1]).convert('L'))
v0, v1, step, u0, u1 = [int(x) for x in sys.argv[2:7]]
dark = int(sys.argv[7]) if len(sys.argv) > 7 else 160
cal = json.load(open('out/F2-34/cal-p1/calibration.json'))
vl = cal['vertical_lines']
for v in range(v0, v1 + 1, step):
    row = img[v, u0:u1] < dark
    runs = []
    i = 0
    while i < len(row):
        if row[i]:
            j = i
            while j < len(row) and row[j]:
                j += 1
            runs.append((u0 + i, u0 + j - 1))
            i = j
        else:
            i += 1
    out = []
    for a, b in runs:
        c = (a + b) / 2
        w = b - a + 1
        tag = ''
        for L in vl:
            ug = L['u_at_v0'] + L['slope_du_dv'] * v
            if abs(c - ug) < 6 and w <= 9:
                tag = 'G%d' % L['y_value']
        out.append('%s[%d-%d c%.1f w%d]' % (tag, a, b, c, w))
    print(v, ' '.join(out))
