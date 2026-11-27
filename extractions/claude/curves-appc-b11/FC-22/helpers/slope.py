import sys, json
import numpy as np
res = json.load(open(sys.argv[1]))
for name, rows in res.items():
    rows = [r for r in rows if (r[3] - r[2]) < 14 and not r[4] and not r[5]]
    A = np.array([[r[0], r[1]] for r in rows]); p = np.polyfit(A[:, 0], A[:, 1], 1)
    by = {}
    for r in rows:
        d = abs(r[1] - np.polyval(p, r[0]))
        if d < 14 and (r[0] not in by or d < by[r[0]][0]):
            by[r[0]] = (d, r)
    U = np.array(sorted(by)); V = np.array([by[u][1][1] for u in U])
    out = []
    for b in range(850, 2420, 60):
        m = (U >= b) & (U < b + 60)
        if m.sum() > 20:
            q = np.polyfit(U[m], V[m], 1); r = V[m] - np.polyval(q, U[m])
            out.append(f"{b}:{q[0]:.3f}({np.sqrt(np.mean(r**2)):.1f},{m.sum()})")
    print(name); print("   ", " ".join(out))
