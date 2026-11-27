import sys
from PIL import Image
import numpy as np
img = np.array(Image.open(sys.argv[1]).convert('L'))
axis = sys.argv[2]  # 'row' => scan along u at fixed v; 'col' => scan along v at fixed u
pos = [int(x) for x in sys.argv[3].split(',')]
a0, a1 = int(sys.argv[4]), int(sys.argv[5])
dark = int(sys.argv[6]) if len(sys.argv) > 6 else 160
half = int(sys.argv[7]) if len(sys.argv) > 7 else 1
for p in pos:
    if axis == 'row':
        seg = img[p-half:p+half+1, a0:a1].min(axis=0)
    else:
        seg = img[a0:a1, p-half:p+half+1].min(axis=1)
    d = seg < dark
    runs = []
    i = 0
    while i < len(d):
        if d[i]:
            j = i
            while j < len(d) and d[j]:
                j += 1
            runs.append((a0+i, a0+j-1))
            i = j
        else:
            i += 1
    print(p, ' '.join(f'{r[0]}-{r[1]}({(r[0]+r[1])/2:.1f})' for r in runs))
