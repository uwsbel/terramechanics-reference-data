"""Reader's helper: assemble points-p1.csv for FC-17 from the circle fits and the trace samples."""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIG = "FC-17"
COLS = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
        "u_bound_px", "v_bound_px", "symbol", "note"]
rows = []

# Circles: centres from circles.py (ring fitted on rays, rms 0.35 to 0.64 px), left to right.
circles = [
    (1132.0, 2178.4, 3.0, 3.0, "circle",
     "single; the solid (mean) curve runs over the top of the ring and merges with it (u 1115 to 1147), "
     "centre fitted on the free part of the ring; bound widened"),
    (1337.6, 2146.9, 2.5, 2.5, "circle",
     "single; the x = 0.3 grid line runs through the right part of the ring"),
    (1364.6, 1940.9, 3.0, 3.0, "circle",
     "pair 1 left; the joining line leaves its right side; the x = 0.3 grid line touches its left side and the "
     "upper dashed curve passes behind its top (a dash ends at the grid line, the next starts at the ring's upper right); bound widened"),
    (1472.9, 2168.0, 2.0, 2.0, "circle",
     "single; sits in a gap of the lower dashed curve (one dash ends at u 1449, the next starts at the x = 0.4 grid "
     "line, u 1503); the ring does not touch the curve"),
    (1676.9, 1935.1, 2.0, 2.0, "circle",
     "pair 1 right; the joining line enters its left side"),
    (2644.9, 1671.1, 2.0, 2.0, "circle-dot",
     "outside the plot frame, 64 px right of the right frame line (about x 1.14 and y 49.7, beyond the labelled lines; the frame is at "
     "about x 1.10); ring heavier than the data circles and a dot at its centre; no joining line; whether it is a data "
     "point plotted beyond the frame or a mark that is not data cannot be told from the page; flagged for review"),
]
for i, (u, v, bu, bv, sym, note) in enumerate(circles, 1):
    rows.append([FIG, 1, "data", "marker", i, u, v, bu, bv, sym, note])

ends = {
    "upper": ("first point: the ink starts at the right edge of the x = 0 grid line (columns 875 to 879 are the "
              "grid line); any part under the line cannot be seen",
              "last point: the dash meets the inner edge of the right frame line (u 2571); nothing shows beyond the "
              "frame; also the maximum of the trace"),
    "mean": ("first point: the ink starts 11 px left of the x = 0 grid line",
             "last point: the line meets the inner edge of the right frame line (u 2574); nothing shows beyond the "
             "frame; also the maximum of the trace"),
    "lower": ("first point: the ink starts 12 px left of the x = 0 grid line",
              "last point: the last dash runs through the right frame line (u 2576 to 2585) and ends 8 px beyond it; "
              "also the maximum of the trace"),
}
widen = {("mean", 10): (5.5, "the x = 0.4 grid line and the 45 grid line both cross the curve here; centre from "
                              "the curve's free edges on either side; bound widened")}
override_first = {"upper": (880, 2073.0, 3.0, 4.5)}   # read from the binary columns: rows 2069 to 2077 at u 880

for s in ("upper", "mean", "lower"):
    with (HERE / f"samp_{s}.csv").open(encoding="utf-8") as f:
        samp = [line.rstrip("\n").split(",", 4) for line in f if line.strip()]
    samp = [(float(a), float(b), float(c), float(d), e) for a, b, c, d, e in samp]
    if s in override_first:
        u, v, bu, bv = override_first[s]
        samp[0] = (u, v, bu, bv, samp[0][4])
    for i, (u, v, bu, bv, note) in enumerate(samp, 1):
        if (s, i) in widen:
            bv = widen[(s, i)][0]
            note += "; " + widen[(s, i)][1]
        if i == 1:
            note = ends[s][0]
        elif i == len(samp):
            note = ends[s][1]
        rows.append([FIG, 1, s, "trace", i, u, v, bu, bv, "", note])
    (u0, v0, bu0, bv0, _), (u1, v1, bu1, bv1, _) = samp[0], samp[-1]
    rows.append([FIG, 1, s, "feature", 1, u0, v0, bu0, bv0, "", ends[s][0]])
    rows.append([FIG, 1, s, "feature", 2, u1, v1, bu1, bv1, "", ends[s][1]])

with (HERE / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(COLS)
    w.writerows(rows)
print(f"wrote {len(rows)} rows")
