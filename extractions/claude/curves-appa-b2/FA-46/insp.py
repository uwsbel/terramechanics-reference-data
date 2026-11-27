"""ASCII inspection window: '#' ink, '+' ink on a known horizontal grid row, '.' paper.
Model centres from centers_col.json overlaid every 4th column as C/B/A (lowercase where on paper).
Usage: insp.py u0 u1 v0 v1 [nomodel]"""
import sys, json
from common import g, grid_at
u0, u1, v0, v1 = map(int, sys.argv[1:5])
model = {}
if len(sys.argv) <= 5:
    try:
        m = json.load(open("centers_col.json"))
        for u in range(u0, u1 + 1):
            if u % 4 == 0 and str(u) in m:
                for s in "CBA":
                    model[(u, int(round(m[str(u)][s])))] = s
    except FileNotFoundError:
        pass
print("      " + "".join("|" if u % 10 == 0 else " " for u in range(u0, u1 + 1)))
for v in range(v0, v1 + 1):
    line = []
    for u in range(u0, u1 + 1):
        ch = ("+" if grid_at(v, u) else "#") if g[v, u] else "."
        if (u, v) in model:
            s = model[(u, v)]
            ch = s if g[v, u] else s.lower()
        line.append(ch)
    print(f"{v:5d} " + "".join(line))
print(f"u from {u0}; '|' at multiples of 10")
