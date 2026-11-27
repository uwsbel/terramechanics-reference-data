"""Column runs: colsum.py u0 u1 step v0 v1 ; runs tagged g (all grid rows) or * (touching grid rows)"""
import sys
from common import g, grid_at, runs_col
u0, u1, s, v0, v1 = map(int, sys.argv[1:6])
for u in range(u0, u1 + 1, s):
    if g[v0:v1 + 1, u].mean() > 0.75:
        print(f"{u}: (vertical grid line)"); continue
    txt = []
    for a, b in runs_col(u, v0, v1):
        gg = [grid_at(v, u) for v in range(a, b + 1)]
        txt.append(f"{a}-{b}" + ("g" if all(gg) else ("*" if any(gg) else "")))
    print(f"{u}: " + " ".join(txt))
