"""Dense guide from a pass-1 track: running median of the inked v over +-half columns, written
for every column between the first and last inked column (interpolated across gaps).
python smooth.py tracks/n4695.csv guides/n4695.csv [--half 15] [--skip-flags symbol,vgrid,hgrid]"""
import argparse, csv
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("track"); ap.add_argument("out")
ap.add_argument("--half", type=int, default=15)
ap.add_argument("--skip-flags", default="vgrid,hgrid")
a = ap.parse_args()
skip = set(a.skip_flags.split(","))
pts = [(int(r["u"]), float(r["v"])) for r in csv.DictReader(open(a.track, encoding="utf-8"))
       if r["v"] != "" and not (set(r["flags"].split("|")) & skip)]
u = np.array([p[0] for p in pts]); v = np.array([p[1] for p in pts])
out = []
for uu in range(u.min(), u.max() + 1):
    m = np.abs(u - uu) <= a.half
    if m.sum() >= 3:
        out.append((uu, float(np.median(v[m]))))
uo = np.array([o[0] for o in out]); vo = np.array([o[1] for o in out])
with open(a.out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["u", "v"])
    for uu in range(u.min(), u.max() + 1):
        w.writerow([uu, round(float(np.interp(uu, uo, vo)), 1)])
print("wrote", a.out)
