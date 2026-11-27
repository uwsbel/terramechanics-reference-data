"""Assemble points-p1.csv of FA-40: the two edges of the hatched band, read on the y = 45 and y = 40
grid lines, which are the band's edges. Samples from samples-top.txt and samples-bottom.txt (trace.py
--line), ends read on the raw pixel map (see notes.md)."""
import csv
from pathlib import Path

here = Path(__file__).resolve().parent
FIG = "FA-40"
B = 4.0   # half the line thickness: the 45 and 40 lines are 7 to 9 px thick (median 8)
ends = {
    "band-top": ((794.0, 2039.0, 7.0, B, "left end: the y = 45 line runs into the left frame (frame ink u 783 to 793, centre about 787); first column clear of the frame; u bound reaches the frame centre"),
                 (2334.0, 2025.0, 6.0, B, "right end: the y = 45 line runs into the right frame (frame ink u 2335 to 2345, centre about 2340); last column clear of the frame; u bound reaches the frame centre")),
    "band-bottom": ((798.0, 2424.0, 6.0, B, "left end: the y = 40 line runs into the left frame (frame ink u 788 to 797, centre about 792); first column clear of the frame; u bound reaches the frame centre"),
                    (2339.0, 2412.0, 5.0, B, "right end: the y = 40 line runs into the right frame (frame ink u 2340 to 2349, centre about 2344); last column clear of the frame; u bound reaches the frame centre")),
}
files = {"band-top": "samples-top.txt", "band-bottom": "samples-bottom.txt"}
rows = []
for ser in ("band-top", "band-bottom"):
    first, last = ends[ser]
    edge = "upper edge of the hatched band, drawn on the y = 45 grid line" if ser == "band-top" else "lower edge of the hatched band, drawn on the y = 40 grid line"
    seq = 1
    rows.append([FIG, 1, ser, "trace", seq, *first[:4], "line", first[4]])
    lines = (here / files[ser]).read_text().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith("target,"))
    for r in csv.DictReader(lines[i0:]):
        seq += 1
        rows.append([FIG, 1, ser, "trace", seq, round(float(r["u"]), 1), round(float(r["v"]), 1), B, B, "line",
                     f"sample at Dr {float(r['target']):.2f}; {edge}"])
    seq += 1
    rows.append([FIG, 1, ser, "trace", seq, *last[:4], "line", last[4]])
    rows.append([FIG, 1, ser, "feature", 1, *first[:4], "line", "first point (left end, at the left frame)"])
    rows.append([FIG, 1, ser, "feature", 2, *last[:4], "line", "last point (right end, at the right frame); the edge is a straight horizontal line: no peak other than its constant value, no knee"])
out = here.parent / "points-p1.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"])
    w.writerows(rows)
print(f"wrote {out}: {len(rows)} rows")
