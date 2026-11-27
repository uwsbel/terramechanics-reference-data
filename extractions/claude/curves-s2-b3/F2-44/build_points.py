"""Build points-p1.csv for F2-44 (Claude reader, batch curves-s2-b3).

Every sample below was chosen on zoomed crops of p0104.png (out/F2-44/crops/) and is located on
the ink by one of these methods:
  perp  (u, v, ang): profile across the line at (u, v), line at `ang` degrees from horizontal
        (positive rising to the right); the dark run nearest (u, v); its centre is the sample and
        its width the line width w. Bound: half the width across the line; along a dashed line
        half the dash gap (7.5 px), along a solid line half the width; projected on u and v.
  dot   (u, v): centroid of the dot of the dotted trace (a blob of about 10 px); bound 5.5 px.
  rowl  (v, u): in pixel row v, the run nearest u; sample at its left edge plus 4.5 px (the
        shared solid line of the initial rise, overlapped on its right by the dashes of 73).
  rowr  (v, u): as rowl, at the run's right edge minus 4.5 px (73's dashes on the rise).
  rowc  (v, u): in pixel row v, the centre of the run nearest u (24's separate dashes on the rise).
  colt  (u, v): in pixel column u, the run nearest v; its top edge plus 5.5 px (69 above the
        band it forms with 24 and 74).
  colb  (u, v): as colt, bottom edge minus 5.5 px (74 under that band).
  colc  (u, v, ang): in pixel column u, the centre of the run nearest v (where a profile across
        the line would cross a grid line or a neighbouring trace); width = run times cos(ang).
  fix   (u, v): set by hand on the crops, with bounds given explicitly.
Explicit bounds (bu, bv) replace the computed ones where traces run together; the note says why.
"""
import csv
import math
from pathlib import Path

import numpy as np

import perp as P

HERE = Path(__file__).resolve().parent
g = P.g
DARK = 160
DASH_HALF_GAP = 7.5     # dashes of 73 and 24: period about 63 px along the line, dash about 48 px
DOT_BOUND = 5.5         # dots of 74: about 10.5 px across, pitch about 17.5 px (gap about 7 px)


def runs1d(arr, off):
    idx = np.where(arr)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append((s + off, p + off)); s = i
        p = i
    out.append((s + off, p + off))
    return out


def row_run(v, u):
    rs = [r for r in runs1d(g[int(v), int(u) - 30:int(u) + 31] < DARK, int(u) - 30)]
    return min(rs, key=lambda r: 0 if r[0] <= u <= r[1] else min(abs(r[0] - u), abs(r[1] - u)))


def col_run(u, v):
    rs = [r for r in runs1d(g[int(v) - 30:int(v) + 31, int(u)] < DARK, int(v) - 30)]
    return min(rs, key=lambda r: 0 if r[0] <= v <= r[1] else min(abs(r[0] - v), abs(r[1] - v)))


def box(ang, across, along):
    a = math.radians(ang)
    bu = math.hypot(along * math.cos(a), across * math.sin(a))
    bv = math.hypot(along * math.sin(a), across * math.cos(a))
    return bu, bv


def locate(e, style):
    m = e["m"]
    if m == "fix":
        return e["u"], e["v"], e["bu"], e["bv"], ""
    if m == "dot":
        import blobs
        b = blobs.blobs_near(e["u"], e["v"], r=6, win=20)[0]
        assert b["d"] < 6 and b["n"] < 160, (e, b)
        return float(b["cu"]), float(b["cv"]), DOT_BOUND, DOT_BOUND, f"dot {b['n']} px"
    if m == "perp":
        rs = P.perp(e["u"], e["v"], e["ang"])
        r = min(rs, key=lambda r: abs(r["c"]))
        assert abs(r["c"]) < 8, (e, rs)
        w = r["w"]
        along = max(w / 2, DASH_HALF_GAP) if style == "dashed" else w / 2
        bu, bv = box(e["ang"], w / 2, along)
        return r["u"], r["v"], bu, bv, f"w {w:.1f}"
    if m in ("rowl", "rowr", "rowc"):
        a, b = row_run(e["v"], e["u"])
        c = {"rowl": a + 4.0, "rowr": b - 4.0, "rowc": (a + b) / 2}[m]
        if m == "rowc" and "ang" in e:
            # width across = horizontal run times sin(angle)
            w = (b - a + 1) * math.sin(math.radians(e["ang"]))
            along = max(w / 2, DASH_HALF_GAP) if style == "dashed" else w / 2
            bu, bv = box(e["ang"], w / 2, along)
            return c, float(e["v"]), bu, bv, f"row run {a}-{b} w {w:.1f}"
        return c, float(e["v"]), None, None, f"row run {a}-{b}"
    if m in ("colt", "colb"):
        a, b = col_run(e["u"], e["v"])
        c = {"colt": a + 5.0, "colb": b - 5.0}[m]
        return float(e["u"]), c, None, None, f"col run {a}-{b}"
    if m == "colc":
        # centre of the column run; width across = vertical run times cos(angle)
        a, b = col_run(e["u"], e["v"])
        w = (b - a + 1) * math.cos(math.radians(e["ang"]))
        along = max(w / 2, DASH_HALF_GAP) if style == "dashed" else w / 2
        bu, bv = box(e["ang"], w / 2, along)
        return float(e["u"]), (a + b) / 2, bu, bv, f"col run {a}-{b} w {w:.1f}"
    raise ValueError(m)


FIRST_SOLID = dict(m="fix", u=756, v=3118, bu=8, bv=25)
N_FIRST_SOLID = ("all five traces begin together in one blob of ink against the left frame (u 752 to 781, v 3092 to 3145, "
                 "about 140 to 210 lb); the shared solid line runs into the frame at about v 3092 and its end below that "
                 "cannot be told from the frame and the dash pieces; the bound covers v 3093 to 3143")
FIRST_DASH = dict(m="fix", u=771, v=3115, bu=9, bv=16)
N_FIRST_DASH = ("all five traces begin together in one blob of ink against the left frame (u 752 to 781, v 3092 to 3145, "
                "about 140 to 210 lb); the lowest dash piece (u 765 to 778, v 3101 to 3130) belongs to 73 or 24, "
                "which cannot be told apart there; the bound covers that piece")
SHARED = ("drawn on one solid line with {others} on the initial rise (one line about 9 px wide; 73's dashes "
          "overlap its right edge); the traces cannot be told apart here; bound widened")
B200 = dict(m="fix", u=756, v=3099, bu=6, bv=6)
N200 = "the shared solid line meets the left frame here (u 752 to 760 visible); "
DASH200 = dict(m="fix", u=771.5, v=3104, bu=10, bv=8)
N_DASH200 = ("73 and 24 run together against the solid line below about 330 lb; this dash piece "
             "(u 765 to 778, v 3101 to 3125) cannot be attributed to one of them; bound widened")


def solid_rise(others):
    n = SHARED.format(others=others)
    return [
        ("trace", "y=200", B200, N200 + n),
        ("trace", "y=300", dict(m="rowl", v=3022, u=771, bu=6, bv=6), n),
        ("trace", "y=400", dict(m="rowl", v=2944, u=784, bu=6, bv=6), n),
        ("trace", "y=500", dict(m="rowl", v=2872, u=795, bu=6, bv=6), n + "; row moved 5 px above the 500 lb grid line"),
        ("trace", "y=600", dict(m="rowl", v=2789, u=808, bu=6, bv=6), n),
        ("trace", "y=700", dict(m="rowl", v=2711, u=819, bu=6, bv=6), n),
        ("trace", "x=0.25", dict(m="rowl", v=2700, u=821, bu=6, bv=6), n),
    ]


TRACES = {
 "lpt69": ("solid", [
    ("feature", "first", FIRST_SOLID, "first; " + N_FIRST_SOLID),
    ("trace", "start", FIRST_SOLID, "where the ink starts; " + N_FIRST_SOLID),
    *solid_rise("64A and 74"),
    ("trace", "y=800", dict(m="rowl", v=2633, u=830, bu=6, bv=6), "left part of a band about 24 px wide with 64A, 74 and 73's dash on its right; bound widened"),
    ("trace", "y=900", dict(m="rowl", v=2556, u=840, bu=5, bv=5), "the left of the two solid lines side by side (64A on its right)"),
    ("trace", "y=1000", dict(m="perp", u=854, v=2483, ang=78), "row moved off the 1000 lb grid line"),
    ("trace", "y=1100", dict(m="perp", u=875, v=2400, ang=77), ""),
    ("trace", "x=0.5", dict(m="perp", u=894, v=2346, ang=61), ""),
    ("trace", "y=1200", dict(m="perp", u=913, v=2321.5, ang=20), ""),
    ("feature", "peak", dict(m="fix", u=958, v=2308.5, bu=15, bv=5.5), "peak, first maximum; flat top from about u 945 to 970"),
    ("trace", "x=0.75", dict(m="perp", u=971, v=2310.5, ang=-10), ""),
    ("trace", "x=1.0", dict(m="colc", u=1043, v=2376, ang=-50), "column moved 8 px left of the 1 in grid line"),
    ("trace", "x=1.25", dict(m="perp", u=1136, v=2494, ang=-51), "column moved off the 1000 lb grid line"),
    ("trace", "x=1.5", dict(m="perp", u=1205, v=2566.5, ang=-40), "24's dash runs 15 px below"),
    ("feature", "knee-min", dict(m="fix", u=1218, v=2574.5, bu=5.5, bv=5.5), "knee, minimum (kink after the first peak); 24 and 74 join its underside here"),
    ("trace", "x=1.75", dict(m="colt", u=1282, v=2533, bu=6, bv=6), "top of a band about 22 px tall that 69 forms with 24 and 74 on its underside; bound widened"),
    ("trace", "x=2.0", dict(m="colc", u=1364, v=2474.5, ang=45), "crosses the 1000 lb grid line here (the grid line lies inside the trace's run); column moved 6 px right of the 2 in grid line"),
    ("trace", "x=2.25", dict(m="perp", u=1435, v=2399, ang=45), ""),
    ("trace", "x=2.5", dict(m="perp", u=1511, v=2318.5, ang=45), ""),
    ("trace", "x=2.75", dict(m="perp", u=1588, v=2240, ang=45), ""),
    ("trace", "x=3.0", dict(m="colc", u=1659, v=2170, ang=42), "column moved 6 px left of the 3 in grid line"),
    ("feature", "knee-bend1", dict(m="fix", u=1700, v=2136, bu=15, bv=15), "knee (gradual bend: the slope falls from about 45 to about 30 degrees between 3.0 and 3.3 in; location along the line uncertain)"),
    ("trace", "x=3.25", dict(m="perp", u=1741, v=2110, ang=30), ""),
    ("trace", "x=3.5", dict(m="perp", u=1818, v=2077, ang=21), ""),
    ("trace", "x=3.75", dict(m="perp", u=1895, v=2049.5, ang=21), "64A crosses it at about 3.85 in"),
    ("trace", "x=4.0", dict(m="colc", u=1984, v=2015.5, ang=20), "just past the crossing with 64A and 74; column moved off the 4 in grid line and 74's dot"),
    ("trace", "x=4.25", dict(m="perp", u=2049, v=1985.5, ang=30), ""),
    ("feature", "knee-bend2", dict(m="fix", u=2090, v=1954, bu=15, bv=15), "knee (gradual bend upward: the slope rises from about 20 to about 55 degrees between 4.2 and 4.5 in; location along the line uncertain)"),
    ("trace", "x=4.5", dict(m="perp", u=2125, v=1908, ang=55), ""),
    ("trace", "end", dict(m="fix", u=2183, v=1835, bu=5.5, bv=5.5), "where the ink ends"),
    ("feature", "last", dict(m="fix", u=2183, v=1835, bu=5.5, bv=5.5), "last; highest load of the trace"),
 ]),
 "lpt64a": ("solid", [
    ("feature", "first", FIRST_SOLID, "first; " + N_FIRST_SOLID),
    ("trace", "start", FIRST_SOLID, "where the ink starts; " + N_FIRST_SOLID),
    *solid_rise("69 and 74"),
    ("trace", "y=800", dict(m="fix", u=834.5, v=2633, bu=7, bv=6), "64A separates from 69 between about 750 and 950 lb; here within a band about 24 px wide with 69, 74 and 73's dash, about 4 px right of 69; bound widened"),
    ("trace", "y=900", dict(m="rowr", v=2556, u=851, bu=5, bv=5), "the right of the two solid lines side by side (69 on its left)"),
    ("trace", "y=1000", dict(m="perp", u=876, v=2482, ang=66), "row moved off the 1000 lb grid line"),
    ("trace", "x=0.5", dict(m="perp", u=895.5, v=2440, ang=61), ""),
    ("trace", "y=1100", dict(m="perp", u=921, v=2402, ang=45), ""),
    ("feature", "peak", dict(m="fix", u=956, v=2383, bu=15, bv=5.5), "peak, first maximum; flat top from about u 940 to 975"),
    ("trace", "x=0.75", dict(m="perp", u=972, v=2384.5, ang=-5), ""),
    ("trace", "x=1.0", dict(m="colc", u=1044, v=2410, ang=-53), "column moved 7 px left of the 1 in grid line"),
    ("trace", "x=1.25", dict(m="perp", u=1126, v=2547, ang=-61), "just above its crossing with 73 and 24 at about (1135, 2565)"),
    ("trace", "x=1.5", dict(m="perp", u=1206, v=2688, ang=-46), "74 crosses it at about 1.38 in"),
    ("trace", "x=1.75", dict(m="perp", u=1283, v=2734.5, ang=-10), ""),
    ("feature", "knee-min", dict(m="fix", u=1332, v=2741, bu=16, bv=5.5), "knee, minimum after the first peak; flat bottom from about u 1315 to 1345"),
    ("trace", "x=2.0", dict(m="colc", u=1366, v=2728.5, ang=28), "column moved 7 px right of the 2 in grid line"),
    ("trace", "x=2.25", dict(m="perp", u=1437, v=2673.5, ang=44), ""),
    ("trace", "x=2.5", dict(m="perp", u=1514, v=2592, ang=48), ""),
    ("trace", "x=2.75", dict(m="perp", u=1590, v=2501.5, ang=48), ""),
    ("trace", "x=3.0", dict(m="perp", u=1656, v=2422, ang=52), "column moved 10 px left of the 3 in grid line"),
    ("trace", "x=3.25", dict(m="perp", u=1743, v=2305, ang=53), ""),
    ("trace", "x=3.5", dict(m="perp", u=1818, v=2201, ang=55), ""),
    ("trace", "x=3.75", dict(m="colc", u=1895, v=2094.5, ang=54), "74's dots run along its upper side here"),
    ("trace", "x=4.0", dict(m="perp", u=1980, v=1976, ang=56), "just past the crossing with 69 and 74; column moved off the 4 in grid line"),
    ("trace", "x=4.25", dict(m="perp", u=2048, v=1878.5, ang=55), ""),
    ("trace", "end", dict(m="fix", u=2075, v=1838, bu=5.5, bv=5.5), "where the ink ends"),
    ("feature", "last", dict(m="fix", u=2075, v=1838, bu=5.5, bv=5.5), "last; highest load of the trace"),
 ]),
 "lpt74": ("dotted", [
    ("feature", "first", FIRST_SOLID, "first; " + N_FIRST_SOLID),
    ("trace", "start", FIRST_SOLID, "where the ink starts; " + N_FIRST_SOLID),
    *solid_rise("69 and 64A (no dot visible: the dots, if drawn, lie inside that line)"),
    ("trace", "y=800", dict(m="fix", u=834.5, v=2633, bu=8, bv=6), "inside a band about 24 px wide with 69, 64A and 73's dash; 74 leaves it at about (845, 2597); bound widened"),
    ("feature", "peak", dict(m="dot", u=893, v=2587), "peak, first maximum; flat top of dots from about u 877 to 910"),
    ("trace", "x=0.5", dict(m="dot", u=893, v=2587), ""),
    ("trace", "x=0.75", dict(m="dot", u=979, v=2635), ""),
    ("trace", "x=1.0", dict(m="dot", u=1035, v=2675), "dot at 0.95 in (the dot at 1.0 in is on the grid line)"),
    ("feature", "knee-min", dict(m="dot", u=1065, v=2688), "knee, minimum after the first peak (lowest dot)"),
    ("trace", "x=1.25", dict(m="dot", u=1128, v=2663), "74 crosses 64A at about (1171, 2634), 1.38 in"),
    ("trace", "x=1.5", dict(m="dot", u=1199, v=2612), ""),
    ("trace", "x=1.75", dict(m="colb", u=1284, v=2545, bu=6, bv=9), "under 69 together with 24 between about 1.55 and 2.05 in; the dots merge into that band; bottom of the band; bound widened"),
    ("trace", "x=2.0", dict(m="fix", u=1371, v=2493, bu=6, bv=7), "leaves the band under 69 here together with 24, partly merged; bound widened"),
    ("trace", "x=2.25", dict(m="dot", u=1427, v=2455), ""),
    ("trace", "x=2.5", dict(m="dot", u=1513, v=2398), ""),
    ("trace", "x=2.75", dict(m="dot", u=1584, v=2349), ""),
    ("trace", "x=3.0", dict(m="dot", u=1654, v=2297), "the next dot sits on the 3 in grid line"),
    ("trace", "x=3.25", dict(m="dot", u=1748, v=2220), ""),
    ("trace", "x=3.5", dict(m="dot", u=1813, v=2162), ""),
    ("trace", "x=3.67", dict(m="fix", u=1876.5, v=2103, bu=6, bv=6), "dot touching the left side of 64A; 74 then passes under 64A and 69 (dots hidden from about 3.7 to 4.05 in)"),
    ("trace", "x=3.89", dict(m="fix", u=1942.5, v=2045, bu=6, bv=7), "dot partly hidden under the crossing of 64A and 69; only its lower half shows; bound widened"),
    ("trace", "x=4.0", dict(m="dot", u=1990, v=1995), "first clear dot after the crossing (4.06 in)"),
    ("trace", "x=4.25", dict(m="dot", u=2050, v=1931), ""),
    ("trace", "end", dict(m="dot", u=2108, v=1866), "where the ink ends (last dot)"),
    ("feature", "last", dict(m="dot", u=2108, v=1866), "last; highest load of the trace"),
 ]),
 "lpt73": ("dashed", [
    ("feature", "first", FIRST_DASH, "first; " + N_FIRST_DASH),
    ("trace", "start", FIRST_DASH, "where the ink starts; " + N_FIRST_DASH),
    ("trace", "y=200", DASH200, N_DASH200),
    ("trace", "y=300", dict(m="fix", u=781.5, v=3022, bu=6, bv=8), "right half of a run 767 to 786 (solid line plus 73's dash); 24's dash ends just right of it; bound widened"),
    ("trace", "y=400", dict(m="rowr", v=2944, u=792, bu=6, bv=8), "73's dash along the right edge of the solid line (69, 64A, 74); bound widened"),
    ("trace", "y=500", dict(m="rowr", v=2872, u=804, bu=6, bv=8), "73's dash along the right edge of the solid line; row moved 5 px above the 500 lb grid line; bound widened"),
    ("trace", "y=600", dict(m="rowr", v=2795, u=815, bu=6, bv=8), "73's dash along the right edge of the solid line; row moved 6 px off a dash gap; bound widened"),
    ("trace", "x=0.25", dict(m="rowr", v=2775, u=819, bu=6, bv=8), "73's dash along the right edge of the solid line; bound widened"),
    ("trace", "y=700", dict(m="rowr", v=2711, u=830, bu=6, bv=8), "73's dash along the right edge of the solid line; bound widened"),
    ("trace", "y=800", dict(m="rowr", v=2633, u=846, bu=6, bv=8), "right edge of a band about 24 px wide with 69, 64A and 74; bound widened"),
    ("trace", "x=0.5", dict(m="perp", u=888, v=2569.5, ang=0), "on the plateau; 74's dots 18 px below"),
    ("feature", "peak", dict(m="fix", u=911, v=2569, bu=18, bv=5.5), "peak, first maximum; flat top from about u 875 to 926 (a dash gap at 897 to 907)"),
    ("trace", "x=0.75", dict(m="perp", u=974, v=2591.5, ang=-28), "24 crosses it at about (955, 2582), 0.69 in"),
    ("trace", "x=1.0", dict(m="perp", u=1045, v=2629.5, ang=-12), "column moved 6 px left of the 1 in grid line"),
    ("feature", "knee-min", dict(m="fix", u=1060, v=2632.5, bu=8, bv=5.5), "knee, minimum (V-shaped, after the first peak); its bottom at about u 1068 falls in a dash gap; on the last ink before the gap"),
    ("trace", "x=1.25", dict(m="perp", u=1124, v=2578.5, ang=46), "just below its crossing with 64A and 24 at about (1135, 2565); 73 then crosses 69 at about (1168, 2532)"),
    ("trace", "x=1.5", dict(m="rowc", v=2462, u=1209, ang=62), "row 12 px above the 1000 lb grid line; dash bound"),
    ("trace", "x=1.75", dict(m="perp", u=1292, v=2295, ang=63), ""),
    ("trace", "x=2.0", dict(m="perp", u=1355.5, v=2187, ang=57), ""),
    ("trace", "x=2.25", dict(m="perp", u=1432, v=2080.5, ang=51), ""),
    ("trace", "x=2.5", dict(m="perp", u=1509, v=1995, ang=46), ""),
    ("trace", "x=2.75", dict(m="perp", u=1595, v=1915, ang=44), "first ink of the dash after a gap at 2.74 in"),
    ("trace", "end", dict(m="fix", u=1650, v=1862, bu=5.5, bv=5.5), "where the ink ends (end of the last dash, 2.96 in)"),
    ("feature", "last", dict(m="fix", u=1650, v=1862, bu=5.5, bv=5.5), "last; highest load of the trace"),
 ]),
 "lpt24": ("dashed", [
    ("feature", "first", FIRST_DASH, "first; " + N_FIRST_DASH),
    ("trace", "start", FIRST_DASH, "where the ink starts; " + N_FIRST_DASH),
    ("trace", "y=200", DASH200, N_DASH200),
    ("trace", "y=300", dict(m="fix", u=794.5, v=3018, bu=6, bv=7), "end of 24's dash where it joins the bundle (rows 3002 to 3020 run 770 to 799 with the solid line and 73); bound widened"),
    ("trace", "y=400", dict(m="rowc", v=2944, u=808, ang=76), "clear of the bundle, 20 px right of it"),
    ("trace", "x=0.25", dict(m="rowc", v=2888, u=821, ang=75), ""),
    ("trace", "y=500", dict(m="rowc", v=2872, u=825, ang=75), "row moved 5 px above the 500 lb grid line"),
    ("trace", "y=600", dict(m="rowc", v=2800, u=846, ang=72), "row moved 11 px to the first ink after a dash gap"),
    ("trace", "y=700", dict(m="rowc", v=2711, u=877, ang=69), "the arrow of the label LPT No. 24 points at this dash (tip at about (870, 2735))"),
    ("trace", "x=0.5", dict(m="rowc", v=2656, u=902, ang=67), "end of a dash before a gap at 2660 to 2671"),
    ("trace", "y=800", dict(m="rowc", v=2633, u=912, ang=66), ""),
    ("trace", "x=0.75", dict(m="perp", u=980, v=2563.5, ang=35), "first ink after a dash gap; 24 crossed 73 at about (955, 2582)"),
    ("trace", "y=900", dict(m="perp", u=992, v=2554.5, ang=30), ""),
    ("feature", "peak", dict(m="fix", u=1014, v=2545.5, bu=15, bv=5.5), "peak, first maximum; flat top from about u 1010 to 1050 (a dash gap at 1020 to 1034)"),
    ("trace", "x=1.0", dict(m="perp", u=1045, v=2547, ang=0), "column moved 6 px left of the 1 in grid line"),
    ("trace", "x=1.25", dict(m="colc", u=1122, v=2561.5, ang=-13), "just left of its crossing with 64A and 73 at about (1135, 2565)"),
    ("trace", "x=1.5", dict(m="perp", u=1203, v=2582.5, ang=-17), "end of the last dash before 24 joins the underside of 69"),
    ("feature", "knee-min", dict(m="fix", u=1206, v=2584, bu=10, bv=6), "knee, minimum after the first peak: 24 turns up here into the underside of 69; the turn itself is hidden under 69's ink; bound widened"),
    ("trace", "x=1.75", dict(m="fix", u=1282, v=2540, bu=6, bv=10), "inside the band under 69 with 74 (between about 1.55 and 2.05 in); 24 not separable there; bound widened"),
    ("trace", "x=2.0", dict(m="fix", u=1365, v=2488, bu=6, bv=8), "leaves the band under 69 here together with 74, partly merged; bound widened"),
    ("trace", "x=2.25", dict(m="colc", u=1434, v=2437, ang=37), "74's dot sits just below"),
    ("trace", "x=2.5", dict(m="perp", u=1505, v=2376, ang=45), "6 px before the end of a dash"),
    ("trace", "x=2.75", dict(m="perp", u=1588, v=2298, ang=42), ""),
    ("trace", "x=3.0", dict(m="fix", u=1667, v=2221, bu=6, bv=7.5), "the last dash, short, crosses the 3 in grid line; row centre of run 1660 to 1674"),
    ("trace", "end", dict(m="fix", u=1670, v=2214, bu=5.5, bv=5.5), "where the ink ends (upper end of the last dash, 3.01 in)"),
    ("feature", "last", dict(m="fix", u=1670, v=2214, bu=5.5, bv=5.5), "last; highest load of the trace"),
 ]),
}


def main():
    rows = []
    log = []
    for sid, (style, entries) in TRACES.items():
        seq = 0
        for kind, tag, e, note in entries:
            u, v, bu, bv, info = locate(e, style)
            if "bu" in e and e["m"] != "fix":
                bu, bv = e["bu"], e["bv"]
            if bu is None:
                bu, bv = 5.0, 5.0
            seq += 1
            rows.append(dict(figure_id="F2-44", panel=1, series_id=sid, point_kind=kind, sequence=seq,
                             pixel_u=round(u, 1), pixel_v=round(v, 1), u_bound_px=round(bu, 1), v_bound_px=round(bv, 1),
                             symbol="", note=note))
            log.append(f"{sid:7s} {seq:3d} {kind:7s} {tag:11s} ({u:7.1f},{v:7.1f}) b ({bu:4.1f},{bv:4.1f}) {info}")
    with (HERE / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("\n".join(log))
    print(f"wrote {len(rows)} rows")


if __name__ == "__main__":
    main()
