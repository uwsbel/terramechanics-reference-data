"""Ink along the curve through each trace sample: fraction of inked pixels on the segment +-8 px along
the local curve direction (from the neighbouring samples), and the extent of ink on each side before
the first white run of 3 px; pixels on long horizontal grid runs count as unknown. Flags samples whose
ink on the segment is broken next to them (possible dash gap)."""
import csv
import numpy as np
import fa22lib as L
INK = L.page() < 128
HL = np.load(L.OUT / "helpers" / "hline.npy")
rows = list(csv.DictReader(open(L.OUT / "points-p1.csv", encoding="utf-8")))
for s in ("upper", "lower", "average"):
    tr = sorted([r for r in rows if r["series_id"] == s and r["point_kind"] == "trace"], key=lambda r: int(r["sequence"]))
    P = [(float(r["pixel_u"]), float(r["pixel_v"])) for r in tr]
    for i, r in enumerate(tr):
        a, b = P[max(i - 1, 0)], P[min(i + 1, len(P) - 1)]
        d = np.array([b[0] - a[0], b[1] - a[1]]); n = np.hypot(*d)
        if n == 0: continue
        d /= n
        u, v = P[i]
        stat = []
        for t in range(-8, 9):
            x, y = int(round(u + t * d[0])), int(round(v + t * d[1]))
            # widen across the line by +-2 px
            ex = [-d[1], d[0]]
            vals = []
            for k in (-2, -1, 0, 1, 2):
                xx, yy = int(round(x + k * ex[0])), int(round(y + k * ex[1]))
                vals.append(2 if HL[yy, xx] else int(INK[yy, xx]))
            stat.append("?" if all(q == 2 for q in vals) else ("#" if any(q == 1 for q in vals) else "."))
        sseg = "".join(stat)
        centre = sseg[6:11]
        if "." in centre and "merge" not in r["note"]:
            print(f"{s:8s} {r['sequence']:>3s} ({u:.1f},{v:.1f}) {sseg}  {r['note'][:70]}")
