"""Assemble points-p1.csv and points-p2.csv for FC-5B from the reader's choices.

Markers: markers_final.py (centers read by eye on zoomed crops, checked by scans).
Traces: the sampling locations below were chosen by the reader on the zoomed crops and the
trace_scan.py listings, away from symbols, gaps and gridlines; this script only measures the
dark run at each chosen location (the run whose center is nearest the reader's expected position)
and writes center and half-thickness. Special cases (merged with a gridline, the n1761/n734
crossing) carry an explicit rule and note.
Run from out/FC-5B/helpers/.
"""
import csv
import json
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, ".")
from markers_final import P1, P2
from trace_scan import expected, expected_u

g = np.asarray(Image.open("../../../packet/p0130.png").convert("L"))
FIG = "FC-5B"


def runs(mask, off):
    idx = np.where(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((int(off + s), int(off + p)))
            s = i
        p = i
    out.append((int(off + s), int(off + p)))
    return out


def col_sample(s, u, exp=None, W=16):
    ve = exp if exp is not None else expected(s, u)
    lo = int(ve - W)
    r = runs(g[lo:lo + 2 * W + 1, u] < 160, lo)
    a, b = min(r, key=lambda t: abs((t[0] + t[1]) / 2 - ve))
    return (a + b) / 2, b - a + 1, (a, b)


def row_sample(s, v, W=16):
    ue = expected_u(s, v)
    lo = int(ue - W)
    r = runs(g[v, lo:lo + 2 * W + 1] < 160, lo)
    a, b = min(r, key=lambda t: abs((t[0] + t[1]) / 2 - ue))
    return (a + b) / 2, b - a + 1, (a, b)


# Sampling plan: ("r", v) row sample on a steep part; ("c", u) column sample; ("cg", u) column
# where the line is merged with the 1000 psf gridline (center = lower edge - 5.5); ("cx", u) the
# crossing of n1761 and n734; ("c2", u) column where n3815 crosses the 2000 psf gridline.
PLAN = {
    "n4695": [("r", 1890), ("r", 1883), ("r", 1877), ("r", 1859), ("r", 1847), ("r", 1835),
              ("c", 815), ("c", 830), ("c", 875), ("c", 890), ("c", 910), ("c", 930), ("c", 945),
              ("c", 1000), ("c", 1020), ("c", 1040), ("c", 1060), ("c", 1110), ("c", 1130), ("c", 1150),
              ("c", 1170), ("c", 1190), ("c", 1200), ("c", 1260), ("c", 1290), ("c", 1340), ("c", 1360),
              ("c", 1380), ("c", 1400), ("c", 1410), ("c", 1460), ("c", 1480), ("c", 1500), ("c", 1520),
              ("c", 1530), ("c", 1585), ("c", 1600), ("c", 1620), ("c", 1640), ("c", 1650), ("c", 1700),
              ("c", 1720), ("c", 1740), ("c", 1760), ("c", 1780), ("c", 1800), ("c", 1820), ("c", 1875),
              ("c", 1890), ("c", 1910), ("c", 1930), ("c", 1940), ("c", 2000), ("c", 2020), ("c", 2040),
              ("c", 2060), ("c", 2080), ("c", 2100), ("c", 2104)],
    "n3815": [("r", 2110), ("r", 2096), ("r", 2084), ("r", 2072), ("r", 2060), ("r", 2048), ("r", 2036),
              ("r", 2024), ("r", 2012), ("r", 2004),
              ("c", 820), ("c", 830), ("c", 838), ("c", 880), ("c", 900), ("c", 920), ("c", 940), ("c", 950),
              ("c", 1000), ("c", 1010), ("c2", 1030), ("c2", 1060), ("c", 1090), ("c", 1100), ("c", 1110),
              ("c", 1120), ("c", 1170), ("c", 1180), ("c", 1190), ("c", 1200), ("c", 1210), ("c", 1260),
              ("c", 1290), ("c", 1350), ("c", 1370), ("c", 1390), ("c", 1410), ("c", 1460), ("c", 1480),
              ("c", 1500), ("c", 1520), ("c", 1530), ("c", 1590), ("c", 1610), ("c", 1630), ("c", 1650),
              ("c", 1670), ("c", 1720), ("c", 1740), ("c", 1760), ("c", 1780), ("c", 1790), ("c", 1846), ("c", 1870),
              ("c", 1880), ("c", 1900), ("c", 1920), ("c", 1930), ("c", 1990), ("c", 2000), ("c", 2020),
              ("c", 2040), ("c", 2060), ("c", 2080), ("c", 2100), ("c", 2112)],
    "n2934": [("r", 2206), ("r", 2200), ("r", 2194), ("r", 2188), ("r", 2182), ("r", 2176), ("r", 2170),
              ("r", 2146), ("r", 2140), ("r", 2134), ("r", 2128), ("r", 2122), ("r", 2116), ("r", 2110),
              ("r", 2104),
              ("c", 820), ("c", 830), ("c", 840), ("c", 880), ("c", 890), ("c", 900), ("c", 920),
              ("c", 940), ("c", 950), ("c", 960), ("c", 970), ("c", 1000), ("c", 1020), ("c", 1040),
              ("c", 1060), ("c", 1070), ("c", 1110), ("c", 1130), ("c", 1150), ("c", 1170), ("c", 1190),
              ("c", 1210), ("c", 1230), ("c", 1240), ("c", 1290), ("c", 1310), ("c", 1330), ("c", 1350),
              ("c", 1370), ("c", 1390), ("c", 1410), ("c", 1460), ("c", 1480), ("c", 1500), ("c", 1520),
              ("c", 1530), ("c", 1590), ("c", 1610), ("c", 1630), ("c", 1650), ("c", 1670), ("c", 1680),
              ("c", 1730), ("c", 1750), ("c", 1770), ("c", 1820), ("c", 1840), ("c", 1870), ("c", 1890),
              ("c", 1910), ("c", 1930), ("c", 1940), ("c", 1990), ("c", 2010), ("c", 2030), ("c", 2050),
              ("c", 2070), ("c", 2090), ("c", 2110), ("c", 2130), ("c", 2136)],
    "n1761": [("c", 730), ("cx", 748), ("c", 766), ("c", 778), ("c", 820), ("c", 832),
              ("c", 880), ("c", 892), ("c", 904), ("c", 916), ("c", 928), ("c", 940),
              ("c", 994), ("c", 1000), ("c", 1018), ("c", 1036), ("c", 1054), ("c", 1072),
              ("c", 1114), ("c", 1132), ("c", 1150), ("c", 1168), ("c", 1186),
              ("c", 1234), ("c", 1250), ("c", 1290), ("c", 1306), ("c", 1346), ("c", 1362), ("c", 1386),
              ("c", 1410),
              ("cg", 1466), ("cg", 1490), ("cg", 1514), ("cg", 1530), ("cg", 1586), ("cg", 1610),
              ("cg", 1634), ("cg", 1650), ("cg", 1706), ("cg", 1730), ("cg", 1754), ("cg", 1770),
              ("cg", 1818), ("cg", 1842), ("cg", 1874), ("cg", 1898), ("cg", 1922), ("cg", 1946),
              ("c", 1994), ("c", 2018), ("c", 2042), ("c", 2066), ("c", 2090), ("c", 2114), ("c", 2138)],
    "n734": [("c", 727), ("cx", 748), ("c", 766), ("c", 776), ("c", 820), ("c", 828), ("c", 836),
             ("c", 884), ("c", 900), ("c", 916), ("c", 932), ("c", 948), ("c", 956),
             ("c", 1004), ("c", 1020), ("c", 1036), ("c", 1052), ("c", 1068),
             ("c", 1116), ("c", 1132), ("c", 1148), ("c", 1164), ("c", 1180),
             ("c", 1228), ("c", 1244), ("c", 1260), ("c", 1292), ("c", 1300),
             ("c", 1356), ("c", 1372), ("c", 1388), ("c", 1404), ("c", 1412),
             ("c", 1468), ("c", 1484), ("c", 1500), ("c", 1516), ("c", 1532),
             ("c", 1588), ("c", 1604), ("c", 1620), ("c", 1636), ("c", 1652),
             ("c", 1700), ("c", 1716), ("c", 1732), ("c", 1748), ("c", 1764),
             ("c", 1820), ("c", 1836), ("c", 1868), ("c", 1884), ("c", 1900), ("c", 1916), ("c", 1932),
             ("c", 1940), ("c", 1988), ("c", 2004), ("c", 2020), ("c", 2036), ("c", 2052), ("c", 2068),
             ("c", 2084), ("c", 2100), ("c", 2116), ("c", 2136)],
}

NOTE = {
    ("n4695", 1890): "first point of the drawn line (lowest ink at u 722-729, v~1892); row sample on the steep start",
    ("n4695", 2104): "last point of the drawn line (ink ends at u~2106, short of the last plus)",
    ("n3815", 2110): "first point of the drawn line, where it leaves the top-right corner of the first triangle-down; row sample",
    ("n3815", 2004): "end of the first drawn segment (ink stops at v~2000, u~782, below the second triangle-down); row sample",
    ("n3815", 1846): "line resumes after the triangle-down at u~1817; a thin stray stroke at v 1820-1822 (u~1815 to 1855) below the line is not part of it",
    ("n3815", 2112): "last point of the drawn line (ink ends at u~2114, before the last triangle-down)",
    ("n2934", 2206): "first point of the drawn line, just above the first circle's outline; row sample",
    ("n2934", 960): "line passes above the circle at u~972 without a gap; sampled on the line, clear of the circle's outline",
    ("n2934", 970): "line passes above the circle at u~972 without a gap; sampled on the line, clear of the circle's outline",
    ("n2934", 2136): "last point of the drawn line, where it meets the last circle (on the 250 gridline)",
    ("n1761", 730): "first point of the drawn line: first column clear of the first square's right edge; run may include the square's top-right corner",
    ("n1761", 2138): "last point of the drawn line, where it meets the last square",
    ("n734", 727): "first point of the drawn line: leaves the right side of the first triangle-up; first column clear of the triangle",
    ("n734", 2136): "last point of the drawn line, where it meets the base of the last triangle-up",
}


def traces(s):
    out = []
    for kind, x in PLAN[s]:
        note = NOTE.get((s, x), "")
        if kind == "r":
            c, w, (a, b) = row_sample(s, x)
            out.append((c, x, round(w / 2, 1), 1, note or "row sample on a steep part (u is the reading, v the chosen row)"))
        elif kind == "c":
            c, w, (a, b) = col_sample(s, x)
            out.append((x, c, 1, round(w / 2, 1), note))
        elif kind == "c2":
            c, w, (a, b) = col_sample(s, x)
            out.append((x, c, 1, 7, f"crosses the 2000 psf gridline here; dark run {a}-{b} includes gridline ink; bound widened"))
        elif kind == "cg":
            c, w, (a, b) = col_sample(s, x)
            out.append((x, b - 5.5, 1, 7, f"merged with the 1000 psf gridline: dark run {a}-{b} is gridline plus line, the line's upper edge is hidden; center = lower edge - 5.5 (half the 11 px line width seen elsewhere)"))
        elif kind == "cx":
            c, w, (a, b) = col_sample(s, x, exp=2250)
            out.append((x, c, 1, round(w / 2, 1), f"the n1761 and n734 lines cross here and share one dark run ({a}-{b}); the same ink is filed under both series"))
    return out


COLS = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
        "u_bound_px", "v_bound_px", "symbol", "note"]


def add(rows, panel, sid, kind, seq, u, v, bu, bv, sym, note):
    rows.append({"figure_id": FIG, "panel": panel, "series_id": sid, "point_kind": kind, "sequence": seq,
                 "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv,
                 "symbol": sym, "note": note})


def main():
    peaks = json.load(open("peaks.json", encoding="utf-8"))
    order = ["n4695", "n3815", "n2934", "n1761", "n734"]
    rows1 = []
    for s in order:
        mk = sorted([m for m in P1 if m[1] == s], key=lambda m: m[3])
        for i, (_, sid, sym, u, v, bu, bv, n) in enumerate(mk, 1):
            add(rows1, 1, sid, "marker", i, u, v, bu, bv, sym, n)
        tr = traces(s)
        for i, (u, v, bu, bv, n) in enumerate(tr, 1):
            add(rows1, 1, s, "trace", i, u, v, bu, bv, "", n)
        f, l, p = tr[0], tr[-1], peaks[s]
        add(rows1, 1, s, "feature", 1, f[0], f[1], f[2], f[3], "", "first point of the drawn line (same location as trace 1)")
        add(rows1, 1, s, "feature", 2, p["u"], p["v"], p["bu"], p["bv"], "", "peak of the drawn line (minimum v of the line center): " + p["note"])
        add(rows1, 1, s, "feature", 3, l[0], l[1], l[2], l[3], "", "last point of the drawn line (same location as the last trace sample)")
    with open("../points-p1.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows1)
    rows2 = []
    for s in order:
        mk = sorted([m for m in P2 if m[1] == s], key=lambda m: m[3])
        for i, (_, sid, sym, u, v, bu, bv, n) in enumerate(mk, 1):
            add(rows2, 2, sid, "marker", i, u, v, bu, bv, sym, n)
    with open("../points-p2.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows2)
    print(len(rows1), "rows p1;", len(rows2), "rows p2")


if __name__ == "__main__":
    main()
