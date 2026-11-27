import csv, json
import numpy as np
from pathlib import Path
HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "edges.csv")))
us, cs = [], []
for r in rows:
    if r["T"] and r["Tg"] == "0" and r["Bg"] == "0":
        us.append(int(r["u"])); cs.append(0.5 * (int(r["T"]) + int(r["Bt"])))
us, cs = np.array(us), np.array(cs)
# running median over +-20 columns, then sample every 10 px
knots = []
for u in range(740, 2131, 10):
    m = (us >= u - 20) & (us <= u + 20)
    if m.sum() >= 5:
        knots.append((u, float(np.median(cs[m]))))
json.dump(knots, open(HERE / "center_knots.json", "w"))
print(len(knots)); print(knots[::5])
