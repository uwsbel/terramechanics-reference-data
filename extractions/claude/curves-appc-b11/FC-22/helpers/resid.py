import sys, json
import numpy as np
res = json.load(open(sys.argv[1]))
for name, rows in res.items():
    rows = [r for r in rows if (r[3] - r[2]) < 14 and not r[4] and not r[5]]
    A = np.array([[r[0], r[1]] for r in rows])
    p = np.polyfit(A[:, 0], A[:, 1], 1)
    by = {}
    for r in rows:
        d = abs(r[1] - np.polyval(p, r[0]))
        if d < 12 and (r[0] not in by or d < by[r[0]][0]):
            by[r[0]] = (d, r)
    U = np.array(sorted(by)); V = np.array([by[u][1][1] for u in U])
    p = np.polyfit(U, V, 1); p2 = np.polyfit(U, V, 2)
    print(name, "linear", p, "rms", np.sqrt(np.mean((V - np.polyval(p, U))**2)), "quad", p2, "rms", np.sqrt(np.mean((V - np.polyval(p2, U))**2)))
    line = []
    for b in range(840, 2440, 40):
        m = (U >= b) & (U < b + 40)
        if m.sum() > 3:
            line.append(f"{b}:{np.mean(V[m] - np.polyval(p, U[m])):+.1f}")
    print("   ", " ".join(line))
