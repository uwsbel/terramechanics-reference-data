"""Print horizontal dark runs of page rows: rows.py u0 u1 v_from v_to [step] (F2-47 helper)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import runs_row, x_of, y_of
u0, u1, va, vb = map(int, sys.argv[1:5]); st = int(sys.argv[5]) if len(sys.argv) > 5 else 1
for v in range(va, vb - 1 if vb < va else vb + 1, -st if vb < va else st):
    rs = runs_row(v, u0, u1)
    print(v, f"y~{y_of(u0, v):6.1f}", ' '.join(f"{a}-{b}({b-a+1};x{x_of((a+b)/2, v):.3f})" for a, b in rs))
