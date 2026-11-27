import csv, sys
sys.path.insert(0, "out/FC-3B")
from markers_p1 import M
from markers_p2 import M2
cols = ["figure_id","panel","series_id","point_kind","sequence","pixel_u","pixel_v","u_bound_px","v_bound_px","symbol","note"]
def marker_rows(panel, MM):
    rows = []
    for sid, (sym, pts) in MM.items():
        for i, (u, v, b, note) in enumerate(pts, 1):
            rows.append(["FC-3B", panel, sid, "marker", i, u, v, b, b, sym, note])
    return rows
p1 = marker_rows(1, M)
with open("out/FC-3B/work/traces-p1-raw.csv", newline="") as f:
    p1 += [[r[c] for c in cols] for r in csv.DictReader(f)]
order = {"marker": 0, "trace": 1, "feature": 2}
p1.sort(key=lambda r: (list(M).index(r[2]), order[r[3]], int(r[4])))
with open("out/FC-3B/points-p1.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(p1)
p2 = marker_rows(2, M2)
with open("out/FC-3B/points-p2.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(p2)
print(len(p1), len(p2))
