import numpy as np, json
from PIL import Image
g = np.asarray(Image.open("packet/p0126.png").convert("L")).astype(int)
D = g < 160
L = {"dr95": ((922, 3006), (2380, 1050)), "dr0": ((922, 3448), (2376, 2087))}
# clean column ranges (ink of the line only, away from markers, labels, frame)
clean = {"dr95": {"dash_left": [(928,950),(962,988),(999,1026),(1041,1069),(1080,1107)],
                  "solid": [(1130,1455),(1495,1745),(1797,2070),(2098,2174)],
                  "dash_right": [(2188,2204),(2215,2230),(2245,2261),(2272,2288),(2302,2321),(2331,2350),(2359,2374)]},
         "dr0": {"dash_left": [(928,954),(968,991),(1007,1033),(1050,1080)],
                 "solid": [(1096,1128),(1170,1455),(1474,1745),(1777,2015),(2060,2098),(2108,2270)],
                 "dash_right": [(2313,2339),(2356,2372)]}}
res = {}
for sid, ((u0, v0), (u1, v1)) in L.items():
    s = (v1 - v0) / (u1 - u0)
    pts = {}
    for part, rngs in clean[sid].items():
        P = []
        for a, b in rngs:
            for u in range(a, b + 1):
                vp = v0 + s * (u - u0)
                lo = int(vp - 16)
                idx = np.where(D[lo:int(vp + 17), u])[0]
                runs = []
                for i in idx:
                    if runs and i - runs[-1][-1] <= 1: runs[-1].append(i)
                    else: runs.append([i])
                if not runs: continue
                r = min(runs, key=lambda r: abs(np.mean(r) + lo - vp))
                if len(r) < 8: continue
                P.append((u, r[0] + lo, r[-1] + lo, np.mean(r) + lo, len(r)))
        pts[part] = np.array(P)
    S = pts["solid"]
    b, a = np.polyfit(S[:, 0], S[:, 3], 1)
    r = S[:, 3] - (a + b * S[:, 0])
    print("==", sid, "solid fit v = %.2f + %.5f u ; rms %.2f max %.2f ; median vert width %.1f -> perp thickness %.1f" % (a, b, r.std(), abs(r).max(), np.median(S[:, 4]), np.median(S[:, 4]) / np.hypot(1, b)))
    for part in ("dash_left", "dash_right"):
        Q = pts[part]
        rq = Q[:, 3] - (a + b * Q[:, 0])
        bq, aq = np.polyfit(Q[:, 0], Q[:, 3], 1)
        print("   %s: n=%d mean resid %.2f rms %.2f ; own fit slope %.5f" % (part, len(Q), rq.mean(), rq.std(), bq))
    # residual by solid piece
    for (ua, ub) in clean[sid]["solid"]:
        m = (S[:, 0] >= ua) & (S[:, 0] <= ub)
        print("   solid piece %d-%d mean resid %.2f" % (ua, ub, r[m].mean()))
    # all-ink fit
    A = np.vstack([pts[k] for k in pts])
    b2, a2 = np.polyfit(A[:, 0], A[:, 3], 1)
    print("   all-ink fit v = %.2f + %.5f u" % (a2, b2))
    res[sid] = {"a": a, "b": b, "a_all": a2, "b_all": b2, "pts": {k: v.tolist() for k, v in pts.items()}}
json.dump(res, open("out/FC-4A/linefit.json", "w"))
