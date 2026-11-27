"""Print dark runs (< 128) of page columns: cols.py v0 v1 u_from u_to [step] (F2-47 helper)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import runs_col, x_of, y_of
v0, v1, ua, ub = map(int, sys.argv[1:5]); st = int(sys.argv[5]) if len(sys.argv) > 5 else 1
for u in range(ua, ub + 1, st):
    rs = runs_col(u, v0, v1)
    print(u, ' '.join(f"{a}-{b}({b-a+1};y{y_of(u, (a+b)/2):.0f})" for a, b in rs))
