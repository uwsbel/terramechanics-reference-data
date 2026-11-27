import numpy as np
from PIL import Image
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
D = g < 160
# approximate lines (u, v) endpoints
L = {"dr95": ((922, 3006), (2380, 1050)), "dr0": ((922, 3448), (2376, 2087))}
for sid, ((u0, v0), (u1, v1)) in L.items():
    s = (v1 - v0) / (u1 - u0)
    print("==", sid, "slope dv/du %.4f" % s)
    cols = []
    for u in range(int(u0) - 2, int(u1) + 6):
        vp = v0 + s * (u - u0)
        lo, hi = int(vp - 14), int(vp + 15)
        idx = np.where(D[lo:hi, u])[0]
        if len(idx):
            # largest contiguous run nearest vp
            runs = []
            for i in idx:
                if runs and i - runs[-1][-1] <= 1: runs[-1].append(i)
                else: runs.append([i])
            r = min(runs, key=lambda r: abs(np.mean(r) + lo - vp))
            cols.append((u, np.mean(r) + lo, len(r), np.mean(r)+lo-vp))
        else:
            cols.append((u, None, 0, None))
    # print ink segments along u
    seg = None
    for u, c, w, dv in cols:
        if c is not None and seg is None: seg = [u, u, [w], [dv]]
        elif c is not None: seg[1] = u; seg[2].append(w); seg[3].append(dv)
        elif seg is not None:
            print("  ink u %d..%d (len %d), vertical width median %d, offset from guess %.1f..%.1f" % (seg[0], seg[1], seg[1]-seg[0]+1, np.median(seg[2]), min(seg[3]), max(seg[3]))); seg = None
    if seg: print("  ink u %d..%d (len %d), vertical width median %d, offset %.1f..%.1f" % (seg[0], seg[1], seg[1]-seg[0]+1, np.median(seg[2]), min(seg[3]), max(seg[3])))
