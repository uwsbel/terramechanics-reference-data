"""Write points-p1.csv for Fig. 2-42 (F2-42) from the reading specs below.

Each sample is read on the page image (packet/p0102.png, binary at 300 dpi) by one of these methods:
  ("pt", u, v)                 a pixel read by eye on zoomed crops or a dot centroid (blobs.py)
  ("row", v, guess)            center of the ink run nearest `guess` along row v
  ("row_left", v, guess, h)    left edge of that run + h (a line whose right side runs into another line)
  ("row_right", v, guess, h)   right edge of that run - h (a line whose left side runs into another line)
  ("col", u, guess)            center of the ink run nearest `guess` along column u
The script checks that every trace sample has ink within 2 px and prints each value for review.
"""
import csv
from pathlib import Path
from inklib import G, row_center, col_center, row_runs, nearest

HERE = Path(__file__).resolve().parent
FIG, PANEL = "F2-42", 1

# Bounds (px), from the measured line widths and gaps (notes.md):
#   B solid, about 10 px wide -> 5
#   D dashes about 9 px wide, gaps 10 to 15 px -> 6 (half the gap along the line)
#   C dashes about 9 to 12 px wide, gaps about 12 px -> 6
#   A dots about 9 to 10 px across, gaps about 7 to 8 px -> 5
B5, D6, C6, A5 = (5, 5), (6, 6), (6, 6), (5, 5)
W7, W8 = (7, 7), (8, 8)

SPECS = {
    # ---------------- lpt25: D, dashed line (dashes about 45 to 50 px, gaps 10 to 15 px) ----------------
    "lpt25": ("dashed", [
        ("feature", ("pt", 848, 3229), W8, "first: lowest ink of D that can be told apart; its dashes run along the right edge of the left frame and merge into the frame at about 75 lb, so below this D is hidden in the frame line or not drawn"),
        ("trace", ("row_right", 3210, 850, 4.5), D6, "about 100 lb; dash along the right edge of the left frame, its left half merged with the frame (center = right edge - 4.5 px)"),
        ("trace", ("row_left", 3054, 856, 4.5), W7, "about 200 lb; runs together with B on its right (center = left edge + 4.5 px)"),
        ("trace", ("row_left", 2898, 860, 4.5), W7, "about 300 lb; runs together with B on its right (center = left edge + 4.5 px)"),
        ("trace", ("row", 2743, 873), D6, "about 400 lb (row 12 px below the 400 lb line)"),
        ("trace", ("row_left", 2582, 892, 4.5), W7, "about 500 lb; runs together with B on its right (center = left edge + 4.5 px)"),
        ("trace", ("row", 2431, 913), D6, "about 600 lb (row 10 px below the 600 lb line)"),
        ("trace", ("row", 2394, 918), D6, "x 0.25 in"),
        ("trace", ("row", 2268, 937), D6, "about 700 lb"),
        ("trace", ("row_left", 2120, 965, 4.5), W7, "about 800 lb (row 10 px below the 800 lb line); runs together with B on its right (center = left edge + 4.5 px)"),
        ("trace", ("row", 2020, 995), W7, "x 0.5 in; D and B coincide here (D crosses B from its left to its right between about 2060 and 1950 px), one run 12 px wide"),
        ("trace", ("row", 1954, 1014), W7, "about 900 lb; D and B coincide (one run 11 px wide)"),
        ("feature", ("row", 1864, 1068), W8, "knee: the steep rise bends into the gentle middle part; corner of the two tangents at about (1044, 1845)"),
        ("trace", ("row", 1857, 1073), D6, "x 0.75 in"),
        ("trace", ("col", 1157, 1788), D6, "x 1.0 in (column 7 px right of the 1 in line, x about 1.02)"),
        ("trace", ("col", 1228, 1752), D6, "x 1.25 in"),
        ("trace", ("col", 1308, 1708), D6, "x 1.5 in (start of a dash, x about 1.51)"),
        ("trace", ("pt", 1382, 1647), W7, "x 1.75 in; D crosses B here (D below B at u 1360, above it at u 1390); center taken 5 px below the top edge of the merged run"),
        ("trace", ("row", 1548, 1469), D6, "x 2.0 in (row clear of the 2 in line, x about 2.03)"),
        ("trace", ("row", 1459, 1535), D6, "x 2.25 in"),
        ("feature", ("row", 1340, 1612), D6, "last: D meets the top edge of the frame (about 1300 lb) at x about 2.51 in"),
    ]),
    # ---------------- lpt23: B, solid line ----------------
    "lpt23": ("solid", [
        ("feature", ("pt", 857, 3124), W8, "first: lowest ink of the solid line B, at about 146 lb, x about 0.05 in; rows 3128 to 3142 hold no ink between u 849 (the frame and its edge) and u 861, so a solid line does not continue below here outside the frame; where B starts is uncertain"),
        ("trace", ("row_right", 3054, 863, 4.5), W7, "about 200 lb; runs together with D on its left (center = right edge - 4.5 px)"),
        ("trace", ("row", 2880, 874), B5, "about 300 lb; B alone in this row (D, A and C in gaps)"),
        ("trace", ("row", 2740, 886), B5, "about 400 lb (row 9 px below the 400 lb line)"),
        ("trace", ("row", 2569, 907), B5, "about 500 lb"),
        ("trace", ("row", 2481, 919), B5, "x 0.25 in"),
        ("trace", ("row", 2431, 928), B5, "about 600 lb (row 10 px below the 600 lb line)"),
        ("trace", ("row", 2268, 950), B5, "about 700 lb"),
        ("trace", ("row", 2132, 972), B5, "about 800 lb (row 22 px below the 800 lb line, in a gap of D)"),
        ("trace", ("row", 2020, 995), W7, "x 0.5 in; B and D coincide here (one run 12 px wide)"),
        ("trace", ("row", 1954, 1014), W7, "about 900 lb; B and D coincide (one run 11 px wide)"),
        ("trace", ("row", 1810, 1056), B5, "about 1000 lb (row 8 px below the 1000 lb line)"),
        ("trace", ("row", 1771, 1073), B5, "x 0.75 in"),
        ("feature", ("pt", 1134, 1704), W8, "knee: the steep rise bends into the plateau; the circled B touches the line here"),
        ("trace", ("col", 1157, 1685), B5, "x 1.0 in (column 7 px right of the 1 in line, x about 1.02)"),
        ("trace", ("col", 1228, 1666), B5, "x 1.25 in; plateau"),
        ("trace", ("col", 1305, 1666), B5, "x 1.5 in; plateau"),
        ("feature", ("col", 1355, 1666), D6, "knee: end of the plateau, B starts to rise again; a dash of D touches B from below at u 1360 to 1390"),
        ("trace", ("pt", 1382, 1657), W7, "x 1.75 in; B and D cross here (merged run 1642 to 1663); center from B on either side"),
        ("trace", ("col", 1466, 1615), B5, "x 2.0 in (column clear of the 2 in line, x about 2.02)"),
        ("feature", ("pt", 1495, 1596), B5, "last: end of the solid line (also its highest load)"),
    ]),
    # ---------------- lpt22: A, dotted line ----------------
    "lpt22": ("dotted", [
        ("feature", ("pt", 847, 3324), W8, "first: the dots run down along the left frame; the last separate dot is at (850, 3304); below it the dots merge with the frame near the origin"),
        ("trace", ("pt", 853.1, 3269.2), A5, "about 50 lb; isolated dot (centroid), between the frame and C"),
        ("trace", ("pt", 859, 3199), W7, "about 100 lb; dot merged with C on its right (center = left edge + 4.5 px)"),
        ("trace", ("pt", 871.5, 3048), W7, "about 200 lb; dot merged with B on its left and C on its right (center = right edge of the merged run - 4.5 px)"),
        ("trace", ("pt", 883.5, 2889), A5, "about 300 lb; dot between B and C"),
        ("trace", ("pt", 895.5, 2749), A5, "about 400 lb; dot against B on its left (center = right edge - 4.5 px)"),
        ("trace", ("pt", 917, 2578), A5, "about 500 lb and x 0.25 in; dot against B on its left"),
        ("trace", ("pt", 937.5, 2440), A5, "about 600 lb; dot between B and C"),
        ("trace", ("pt", 964.8, 2268.0), A5, "about 700 lb; isolated dot (centroid)"),
        ("trace", ("pt", 994.8, 2150.9), A5, "x 0.5 in; isolated dot (centroid)"),
        ("trace", ("pt", 1000.5, 2134.6), A5, "about 800 lb; isolated dot (centroid); above it A runs on top of C (about 2125 to 2040 px) and comes out on C's right"),
        ("trace", ("pt", 1080.4, 2024.0), A5, "x 0.75 in (dot at x about 0.78; the dot at x 0.73 is merged with the end of a dash of C)"),
        ("feature", ("pt", 1138.6, 1990.6), A5, "peak, first maximum: highest dot (centroid)"),
        ("trace", ("pt", 1155, 1997.5), W7, "x 1.0 in; dot partly merged with the 1 in line"),
        ("trace", ("pt", 1231.1, 2032.9), A5, "x 1.25 in; dot (centroid)"),
        ("feature", ("pt", 1264.7, 2042.3), A5, "knee, minimum: lowest dot after the peak (centroid)"),
        ("trace", ("pt", 1302.8, 2008.4), A5, "x 1.5 in; dot (centroid); A has crossed C between u 1280 and 1300 (one dot hidden under C)"),
        ("trace", ("pt", 1382.9, 1896.2), A5, "x 1.75 in; dot (centroid)"),
        ("trace", ("pt", 1449, 1791.5), A5, "x 2.0 in (dot at x about 1.96; the next dots touch the 1000 lb and 2 in lines)"),
        ("trace", ("pt", 1539.8, 1644.1), A5, "x 2.25 in; dot (centroid)"),
        ("feature", ("pt", 1613, 1525), W7, "last: last dot of A, merged into the lower end of a dash of C as a bulge on its left; the dot before it (1604, 1541) is isolated; above it no dot shows beside C, so A ends here or runs on hidden under C"),
    ]),
    # ---------------- lpt24: C, dashed line (dashes about 110 px, gaps about 12 px) ----------------
    "lpt24": ("dashed", [
        ("feature", ("pt", 859, 3349), C6, "first: C's ink runs into the bottom frame line (0 lb, drawn 12 px thick) at x about 0.05 in; v taken 3 px inside the frame's top edge, the bound reaches its center line"),
        ("trace", ("row", 3192, 871), C6, "about 100 lb"),
        ("trace", ("row", 3053, 883), C6, "about 200 lb (row 12 px below the 200 lb line)"),
        ("trace", ("row", 2896, 895), C6, "about 300 lb (first rows of a dash; the gap is at 2878 to 2890)"),
        ("trace", ("row", 2740, 910), C6, "about 400 lb (row 9 px below the 400 lb line)"),
        ("trace", ("row", 2667, 919), C6, "x 0.25 in"),
        ("trace", ("row", 2575, 930), C6, "about 500 lb"),
        ("trace", ("row", 2431, 951), C6, "about 600 lb (row 10 px below the 600 lb line)"),
        ("trace", ("row", 2272, 977), C6, "about 700 lb"),
        ("trace", ("row", 2192, 996), C6, "x 0.5 in"),
        ("trace", ("row", 2132, 1018), C6, "about 800 lb (row 22 px below the 800 lb line); above it A runs on top of C up to about 2040 px"),
        ("trace", ("row", 2004, 1072), C6, "x 0.75 in"),
        ("feature", ("col", 1116, 1950), C6, "peak, first maximum: top of the line (run 1944 to 1955)"),
        ("trace", ("col", 1156, 1958), C6, "x 1.0 in (column 6 px right of the 1 in line, x about 1.02)"),
        ("trace", ("col", 1228, 1991), C6, "x 1.25 in"),
        ("trace", ("col", 1305, 2024), C6, "x 1.5 in"),
        ("feature", ("col", 1313, 2024), C6, "knee, minimum: bottom of the trough (flat from u 1306 to 1324); A crosses C just before it"),
        ("trace", ("row", 1965, 1382), C6, "x 1.75 in"),
        ("trace", ("row", 1793, 1471), C6, "x 2.0 in (row clear of the 1000 lb line, x about 2.03; C passes 6 px from the grid crossing)"),
        ("trace", ("row", 1682, 1535), C6, "x 2.25 in"),
        ("trace", ("row", 1537, 1618), C6, "x 2.5 in (lower end of a dash, x about 2.52; C is in a gap at x 2.5)"),
        ("trace", ("row", 1417, 1687), C6, "x 2.75 in"),
        ("feature", ("row", 1340, 1735), C6, "last: C meets the top edge of the frame (about 1300 lb) at x about 2.92 in"),
    ]),
}


def read(method):
    m = method[0]
    if m == "pt":
        return float(method[1]), float(method[2]), None
    if m == "row":
        v, guess = method[1], method[2]
        c, w, r = row_center(v, guess, 12)
        return c, float(v), w
    if m in ("row_left", "row_right"):
        v, guess, h = method[1], method[2], method[3]
        r = nearest(row_runs(v, int(guess - 14), int(guess + 14)), guess)
        u = r[0] + h if m == "row_left" else r[1] - h
        return float(u), float(v), r[1] - r[0] + 1
    if m == "col":
        u, guess = method[1], method[2]
        c, w, r = col_center(u, guess, 12)
        return float(u), c, w
    raise ValueError(m)


def ink_near(u, v, d=2):
    u, v = int(round(u)), int(round(v))
    return bool(G[v - d:v + d + 1, u - d:u + d + 1].any())


rows = []
for sid, (style, specs) in SPECS.items():
    for i, (kind, method, (bu, bv), note) in enumerate(specs, start=1):
        u, v, w = read(method)
        ok = ink_near(u, v)
        print(f"{sid} {i:2d} {kind:7s} u={u:7.1f} v={v:7.1f} run_w={w} ink={'yes' if ok else 'NO'}  {note[:70]}")
        if kind == "trace" and not ok:
            raise SystemExit(f"no ink near trace sample {sid} {i}")
        rows.append({"figure_id": FIG, "panel": PANEL, "series_id": sid, "point_kind": kind, "sequence": i,
                     "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv,
                     "symbol": style, "note": note})

cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with (HERE / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"wrote {HERE / 'points-p1.csv'}: {len(rows)} rows")
