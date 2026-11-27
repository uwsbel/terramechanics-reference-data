import sys, json
import numpy as np
res = json.load(open(sys.argv[1]))
for name, rows in res.items():
    rows = [r for r in rows if (r[3] - r[2]) < 16 and not r[4] and not r[5]]
    # one run per column: keep the one nearest a running linear fit
    A = np.array([[r[0], r[1]] for r in rows])
    p = np.polyfit(A[:, 0], A[:, 1], 1)
    by = {}
    for r in rows:
        d = abs(r[1] - np.polyval(p, r[0]))
        if r[0] not in by or d < by[r[0]][0]:
            by[r[0]] = (d, r)
    us = sorted(by)
    # segments: consecutive columns with gaps <= 1
    segs = []
    s = us[0]; prev = us[0]
    for u in us[1:]:
        if u - prev > 1:
            segs.append((s, prev)); s = u
        prev = u
    segs.append((s, prev))
    print(name, "fit v = %.4f u + %.1f" % tuple(p), "columns", len(us))
    for a, b in segs:
        thick = np.median([by[u][1][3] - by[u][1][2] + 1 for u in range(a, b + 1) if u in by])
        print("   seg u %d..%d  (len %d) v %.1f..%.1f  vthick %.0f" % (a, b, b - a + 1, by[a][1][1], by[b][1][1], thick))
