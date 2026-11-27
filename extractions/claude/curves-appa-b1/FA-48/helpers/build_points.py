"""Assemble points-p1.csv of FA-48 from samples2.txt (trace.py --open 7 --tol 2) and the two ends read
on the raw pixel map; the Dr 0.85 sample, on a thin joint of the drawn line, is read on the raw mask
(see notes.md)."""
import csv
from pathlib import Path

here = Path(__file__).resolve().parent
FIG, SER = "FA-48", "curve"
B = 6.0   # half the line thickness: the curve is 11 to 12.7 px thick across
first = (802.0, 2539.5, 7.0, B, "left end: the curve runs into the left frame (frame ink u 791 to 799, centre about 795); first column clear of the frame; u bound reaches the frame centre")
last = (2332.0, 1570.0, 6.0, B, "right end: the curve runs into the right frame (frame ink u 2334 to 2342, centre about 2338) above the y = 50 line; last column clear of the frame; u bound reaches the frame centre")
override = {0.85: (2102.6, 1667.0, B, B, "sample at Dr 0.85; the drawn line is thin here (6 px), a joint between two strokes with the lower part of the line missing from u 2093 to 2118; centre of the ink taken; the strokes on either side extrapolate to v 1670 to 1671.5, inside the bound")}
rows = []
seq = 1
rows.append([FIG, 1, SER, "trace", seq, *first[:4], "line", first[4]])
L = (here / "samples2.txt").read_text().splitlines()
i0 = next(i for i, l in enumerate(L) if l.startswith("target,"))
for r in csv.DictReader(L[i0:]):
    seq += 1
    t = round(float(r["target"]), 2)
    if t in override:
        u, v, bu, bv, note = override[t]
    else:
        u, v, bu, bv = round(float(r["u"]), 1), round(float(r["v"]), 1), B, B
        note = f"sample at Dr {t:.2f}" + ("; above the y = 50 line, the highest labelled line: extrapolated" if t >= 0.92 else "")
    rows.append([FIG, 1, SER, "trace", seq, u, v, bu, bv, "line", note])
seq += 1
rows.append([FIG, 1, SER, "trace", seq, *last[:4], "line", last[4]])
rows.append([FIG, 1, SER, "feature", 1, *first[:4], "line", "first point (left end, at the left frame)"])
rows.append([FIG, 1, SER, "feature", 2, *last[:4], "line", "last point (right end, at the right frame); also the maximum of the trace, which rises monotonically; no knee"])
out = here.parent / "points-p1.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"])
    w.writerows(rows)
print(f"wrote {out}: {len(rows)} rows")
