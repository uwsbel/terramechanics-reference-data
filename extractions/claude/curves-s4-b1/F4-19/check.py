"""Self-check of the samples: on ink, and centered on the ink across the line (original image)."""
import sys, json
sys.path.insert(0,'out/F4-19'); sys.path.insert(0,'tools')
import numpy as np
import trace_tools as T
gray = T.load_gray(); DARK = gray < T.DARK
ink, BM = T.load_clean()
S = json.load(open('out/F4-19/samples.json'))
G = json.load(open('out/F4-19/guides.json'))
def runs_along(p, n, half=10):
    return T.profile_runs(DARK, p, n, half)
bad = 0
for key, rows in S.items():
    for i, r in enumerate(rows):
        p = np.array([r['u'], r['v']])
        u, v = int(round(p[0])), int(round(p[1]))
        on = DARK[v, u]
        near = DARK[v-2:v+3, u-2:u+3].any()
        # local direction from neighbours
        a = rows[max(0, i-1)]; b = rows[min(len(rows)-1, i+1)]
        d = np.array([b['u']-a['u'], b['v']-a['v']], float); nd = np.hypot(*d)
        d = d/nd if nd > 0 else np.array([1.0, 0.0])
        n = np.array([-d[1], d[0]])
        rr = T.nearest_run(runs_along(p, n), 0.0, 0.5)
        off = None; w = None
        if rr:
            off = 0.5*(rr[0]+rr[1]); w = rr[1]-rr[0]+0.5
        flag = (not near) or (off is not None and abs(off) > 2.0 and w < 16)
        if flag or not on:
            bad += 1
            print(f"{key:9s} {r['kind']} {r['target']:>6g} ({r['u']:.1f},{r['v']:.1f}) on={on} near={near} off={off} w={w} | {r['note'][:80]}")
print('flagged', bad)
