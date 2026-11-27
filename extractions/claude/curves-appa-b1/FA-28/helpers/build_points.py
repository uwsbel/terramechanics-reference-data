"""Assemble points-p1.csv of FA-28 from the trace samples (samples.csv, written by trace.py) and the
two ends read by eye on the raw pixel map (see notes.md)."""
import csv
from pathlib import Path

here = Path(__file__).resolve().parent
out = here.parent / "points-p1.csv"
B = 6.0   # half the line thickness: the curve is 11 to 13 px thick across (median 11.6)
FIG, SER = "FA-28", "curve"

first = (773.0, 3224.5, 6.0, 6.0, "left end: the line's ink starts at u 773, 5 px clear of the left frame (frame ink u 759 to 767, Dr 0 at u 763)")
last = (2303.0, 2296.5, 6.0, 6.0, "right end: the line runs into the right frame (frame ink u 2305 to 2312, Dr 1.0 at u 2308); u bound reaches the frame centre")

rows = []
seq = 1
rows.append([FIG, 1, SER, "trace", seq, first[0], first[1], first[2], first[3], "line", first[4]])
with open(here / "samples.csv", newline="") as f:
    for r in csv.DictReader(f):
        seq += 1
        note = f"sample at Dr {float(r['target']):.2f}"
        rows.append([FIG, 1, SER, "trace", seq, round(float(r["u"]), 1), round(float(r["v"]), 1), B, B, "line", note])
seq += 1
rows.append([FIG, 1, SER, "trace", seq, last[0], last[1], last[2], last[3], "line", last[4]])
rows.append([FIG, 1, SER, "feature", 1, first[0], first[1], first[2], first[3], "line", "first point (left end of the line's ink)"])
rows.append([FIG, 1, SER, "feature", 2, last[0], last[1], last[2], last[3], "line",
             "last point (right end, at the right frame); also the maximum of the trace, which rises monotonically; no knee"])
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"])
    w.writerows(rows)
print(f"wrote {out}: {len(rows)} rows")
