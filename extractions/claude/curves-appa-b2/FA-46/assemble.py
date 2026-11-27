"""Assemble FA-46 points from the reader's page readings (pixel coordinates read from ASCII dumps and zoomed
crops of p0095.png; see notes.md). Trace samples: x samples (k: 0.05-decade steps from 0.02 mm) are snapped onto
the constant-x line through the read u unless moved to a dash end ('end'); 5% samples are snapped onto the
constant-y line through the read v unless moved."""
import sys, csv, math
from collections import Counter
sys.argv = sys.argv[:1]
from geom import v_for_x, u_for_y, x_at, y_at

LG0 = math.log10(0.02)


def xk(k):
    return 10 ** (LG0 + 0.05 * k)


CLEAN, MERGED, GRIDB, FRAME = 5.5, 7.0, 7.0, 8.0
# x samples: k -> (u, v, bound, flag, note); flag 'x' = snap v to the constant-x line, 'end' = moved to a dash end
XS = {
    "upper": {
        12: (2165.5, 3155.6, MERGED, "x", "strokes A, B, C touch side by side; from left edge"),
        13: (2163.0, 3107.1, MERGED, "x", "from left edge"),
        14: (2163.5, 3055.0, CLEAN, "end", "dash gap 3056-3070 (0.1 mm grid line erased there); moved to dash end"),
        15: (2162.5, 3010.0, MERGED, "x", "from left edge"),
        16: (2162.5, 2961.4, MERGED, "x", "from left edge"),
        17: (2160.5, 2912.9, MERGED, "x", "from left edge"),
        18: (2159.5, 2864.3, MERGED, "x", "from left edge"),
        19: (2159.5, 2820.0, CLEAN, "end", "dash gap 2804-2819; moved to dash end"),
        20: (2158.5, 2767.2, GRIDB, "x", "on 0.2 mm grid line"),
        21: (2157.5, 2719.1, MERGED, "x", "from left edge"),
        22: (2157.5, 2671.0, MERGED, "x", "from left edge"),
        23: (2158.5, 2630.0, CLEAN, "end", "dash gap 2616-2629; moved to dash end"),
        24: (2157.5, 2574.9, MERGED, "x", "from left edge"),
        25: (2156.5, 2526.8, MERGED, "x", "from left edge"),
        26: (2156.5, 2478.7, GRIDB, "x", "on grid line"),
        27: (2156.5, 2426.0, CLEAN, "end", "dash gap 2427-2441; moved to dash end"),
        28: (2154.5, 2390.0, CLEAN, "end", "0.5 mm grid line with a dash gap above it; moved to first visible dash end below"),
        29: (2151.5, 2334.1, MERGED, "x", "three strokes merged; from left edge"),
        30: (2149.5, 2285.5, MERGED, "x", "three strokes merged; from left edge"),
        31: (2141.5, 2237.0, CLEAN, "x", "separate stroke"),
        32: (2134.0, 2192.0, CLEAN, "end", "dash gap 2181-2191; moved to dash end"),
        33: (2114.5, 2140.0, CLEAN, "x", "separate stroke"),
        34: (2090.0, 2091.4, GRIDB, "x", "on 1.0 mm grid line; separate stroke above and below it"),
        35: (2055.5, 2043.1, CLEAN, "x", "separate stroke"),
        36: (2006.0, 1995.5, CLEAN, "x", "separate stroke"),
        37: (1946.5, 1954.5, CLEAN, "end", "crossing in a dash gap; moved to dash end"),
        38: (1853.0, 1898.5, MERGED, "x", "outer (lower) edge of merged band"),
        39: (1741.0, 1852.8, MERGED, "x", "outer edge of merged band"),
        40: (1570.0, 1803.6, GRIDB, "x", "under 2.0 mm grid line; from band edge"),
        41: (1287.0, 1758.0, MERGED, "end", "crossing in dash gap 1271-1286; moved to dash end"),
        42: (916.0, 1708.2, GRIDB, "x", "under a minor grid line; from neighbouring columns"),
        43: (772.5, 1660.0, MERGED, "x", "coarse bend, row cut"),
        44: (740.5, 1611.0, CLEAN, "x", "near a dash end"),
        45: (729.0, 1564.0, FRAME, "end", "runs on the 100% frame; frame erased in dash gap 1552-1563; moved to dash end"),
        46: (720.0, 1512.0, FRAME, "x", "beside the 100% frame, on 4.0 mm grid line"),
        47: (717.0, 1462.0, FRAME, "x", "dash drawn just outside the 100% frame line"),
    },
    "average": {
        12: (2174.3, 3155.6, MERGED, "x", "middle stroke, A and C touching both sides"),
        13: (2174.0, 3107.1, MERGED, "x", "middle stroke"),
        14: (2173.8, 3058.5, CLEAN, "x", "on 0.1 mm grid line; stroke visible alone"),
        15: (2172.4, 3010.0, CLEAN, "x", ""),
        16: (2171.8, 2961.4, MERGED, "x", "middle stroke"),
        17: (2170.8, 2912.9, MERGED, "x", "middle stroke"),
        18: (2170.0, 2864.3, MERGED, "x", "middle stroke"),
        19: (2170.0, 2815.7, CLEAN, "x", ""),
        20: (2168.9, 2767.2, GRIDB, "x", "on 0.2 mm grid line"),
        21: (2168.5, 2719.1, MERGED, "x", "middle stroke"),
        22: (2168.0, 2671.0, MERGED, "x", "middle stroke"),
        23: (2167.0, 2623.0, CLEAN, "x", ""),
        24: (2166.2, 2574.9, MERGED, "x", "middle stroke"),
        25: (2166.0, 2526.8, MERGED, "x", "middle stroke"),
        26: (2165.8, 2478.7, GRIDB, "x", "on grid line"),
        27: (2165.5, 2430.7, CLEAN, "x", ""),
        28: (2165.0, 2382.6, GRIDB, "x", "on 0.5 mm grid line"),
        29: (2163.0, 2334.1, MERGED, "x", "middle of three merged strokes"),
        30: (2160.5, 2285.5, MERGED, "x", "middle of three merged strokes"),
        31: (2157.0, 2237.0, MERGED, "x", "left half of merged B+C"),
        32: (2149.0, 2188.5, CLEAN, "x", "alone (both dashed curves in gaps)"),
        33: (2133.0, 2140.0, MERGED, "x", "left half of merged B+C"),
        34: (2107.5, 2091.4, GRIDB, "x", "on 1.0 mm grid line"),
        35: (2072.5, 2043.1, MERGED, "x", "left half of merged B+C"),
        36: (2025.0, 1995.5, MERGED, "x", "merged band"),
        37: (1966.0, 1947.6, CLEAN, "x", "three separate strokes here"),
        38: (1880.0, 1898.3, MERGED, "x", "merged band"),
        39: (1779.0, 1852.6, MERGED, "x", "merged band"),
        40: (1615.0, 1803.2, GRIDB, "x", "under 2.0 mm grid line"),
        41: (1370.0, 1755.4, MERGED, "x", "merged band"),
        42: (978.0, 1707.9, GRIDB, "x", "under a minor grid line"),
        43: (789.5, 1660.0, MERGED, "x", "coarse bend, row cut"),
        44: (751.0, 1611.0, CLEAN, "x", ""),
        45: (737.5, 1562.0, MERGED, "x", "beside the 100% frame"),
        46: (731.0, 1512.0, FRAME, "x", "merges into the 100% frame, on 4.0 mm grid line"),
    },
    "lower": {
        12: (2183.8, 3155.6, MERGED, "x", "between B and the 0% frame, merged with the frame"),
        13: (2183.5, 3107.1, MERGED, "x", "merged with the 0% frame"),
        14: (2183.5, 3058.0, MERGED, "end", "dash ends at 3058 (gap 3059-3076); merged with the frame"),
        15: (2182.0, 3012.0, MERGED, "end", "dash gap 2997-3011; moved to dash end"),
        16: (2181.8, 2961.4, MERGED, "x", "merged with the 0% frame"),
        17: (2180.8, 2912.9, MERGED, "x", "merged with the 0% frame"),
        18: (2180.0, 2864.3, MERGED, "x", "merged with the 0% frame"),
        19: (2180.0, 2809.0, MERGED, "end", "dash gap 2810-2824; moved to dash end"),
        20: (2178.9, 2767.2, GRIDB, "x", "on 0.2 mm grid line"),
        21: (2177.5, 2719.1, CLEAN, "x", "right edge visible"),
        22: (2177.5, 2671.0, CLEAN, "x", "right edge visible"),
        23: (2177.5, 2620.0, CLEAN, "end", "dash gap 2621-2635; moved to dash end"),
        24: (2176.5, 2574.9, CLEAN, "x", "right edge visible"),
        25: (2174.5, 2526.8, CLEAN, "x", "right edge visible"),
        26: (2174.5, 2478.7, GRIDB, "x", "on grid line"),
        27: (2174.5, 2430.7, CLEAN, "x", "dash ends at 2431"),
        28: (2173.5, 2396.0, CLEAN, "end", "dash gap 2369-2395 (0.5 mm grid line inside); moved to dash end"),
        29: (2174.5, 2334.1, MERGED, "x", "right edge of merged band"),
        30: (2171.5, 2285.5, MERGED, "x", "right edge of merged band"),
        31: (2167.5, 2237.0, MERGED, "x", "right half of merged B+C"),
        32: (2158.5, 2182.0, MERGED, "end", "dash gap 2183-2194; moved to dash end"),
        33: (2144.0, 2140.0, MERGED, "x", "right half of merged B+C"),
        34: (2119.5, 2091.4, GRIDB, "x", "on 1.0 mm grid line"),
        35: (2085.5, 2043.1, MERGED, "x", "right half of merged B+C"),
        36: (2046.0, 1995.5, MERGED, "x", "merged band"),
        37: (1989.0, 1950.5, MERGED, "end", "crossing in dash gap 1976-1988; moved to dash end"),
        38: (1906.0, 1898.0, MERGED, "x", "upper edge of merged band"),
        39: (1809.0, 1851.0, MERGED, "end", "crossing in dash gap 1810-1823; moved to dash end"),
        40: (1670.0, 1802.9, GRIDB, "x", "under 2.0 mm grid line"),
        41: (1425.0, 1754.7, MERGED, "x", "upper edge of band"),
        42: (1058.0, 1707.5, GRIDB, "x", "under a minor grid line, near a dash end"),
        43: (803.0, 1660.0, MERGED, "x", "coarse bend, row cut"),
        44: (767.5, 1611.0, CLEAN, "x", ""),
        45: (745.5, 1558.0, FRAME, "end", "dash gap 1559-1575; moved to dash end"),
    },
}
# 5% samples: y -> (u, v, bound, flag, note); flag 'y' = snap u to the constant-y line, 'end' = keep as read
YS = {
    "upper": {
        35: (None, 1831.5, CLEAN, "y", "separate stroke below B"),
        40: (1601.0, 1810.0, MERGED, "end", "dash starts at the 40% grid line; partly under 2.0 mm grid line"),
        45: (1520.5, 1792.5, MERGED, "end", "dash gap 1521-1536; moved to dash end"),
        50: (None, 1775.0, MERGED, "y", "on 50% grid line; from bottom edge"),
        55: (None, 1769.0, MERGED, "y", "from bottom edge"),
        60: (None, 1759.0, MERGED, "y", "on 60% grid line"),
        65: (None, 1750.0, MERGED, "y", "from bottom edge"),
        70: (1166.0, 1741.5, MERGED, "end", "dash resumes at the 70% grid line; gap to its left"),
        75: (1098.0, 1734.5, GRIDB, "end", "dash gap 1080-1097 (grid line erased there); moved to dash end"),
        80: (1017.0, 1723.0, MERGED, "end", "dash gap 1019-1038; moved to dash end"),
        85: (None, 1714.5, MERGED, "y", "from bottom edge"),
        90: (None, 1699.5, MERGED, "y", "on 90% grid line"),
        95: (None, 1678.5, MERGED, "y", "coarse bend"),
    },
    "average": {
        30: (None, 1840.6, MERGED, "y", "on 30% grid line"),
        35: (None, 1816.5, CLEAN, "y", "separate stroke"),
        40: (None, 1800.0, GRIDB, "y", "under 2.0 mm grid line"),
        45: (None, 1783.5, MERGED, "y", "merged band"),
        50: (None, 1768.0, MERGED, "y", "merged band"),
        55: (None, 1757.5, MERGED, "y", "merged band"),
        60: (None, 1748.0, MERGED, "y", "merged band"),
        65: (None, 1739.0, GRIDB, "y", "under #8 sieve grid line"),
        70: (None, 1730.5, MERGED, "y", "merged band"),
        75: (None, 1723.0, MERGED, "y", "merged band"),
        80: (None, 1713.0, GRIDB, "y", "under a minor grid line"),
        85: (None, 1704.0, GRIDB, "y", "under a minor grid line"),
        90: (None, 1689.0, MERGED, "y", "merged band"),
        95: (None, 1666.0, MERGED, "y", "coarse bend"),
    },
    "lower": {
        40: (None, 1787.0, MERGED, "y", "top edge of band"),
        45: (None, 1773.0, MERGED, "y", "top edge of band"),
        50: (1456.5, 1759.0, MERGED, "end", "dash gap 1438-1456; dash end at the 50% grid line"),
        55: (1375.5, 1746.5, GRIDB, "end", "dash gap 1376-1391; moved to dash end"),
        60: (None, 1737.0, GRIDB, "y", "inside #8 sieve grid line; dash ends at u 1312"),
        65: (None, 1728.0, MERGED, "y", "top edge of band"),
        70: (None, 1719.5, MERGED, "y", "top edge of band"),
        75: (None, 1712.0, GRIDB, "y", "inside a minor grid line"),
        80: (None, 1702.0, MERGED, "y", "dash starts at the 80% grid line"),
        85: (953.0, 1693.0, MERGED, "end", "dash gap 935-952; moved to dash end"),
        90: (873.0, 1677.5, MERGED, "end", "dash ends at the 90% grid line"),
        95: (None, 1655.0, MERGED, "y", "coarse bend"),
    },
}
FIRST = {"upper": (2166.5, 3186.0, "first point: ink meets the dashed #200 sieve line (0.074 mm)"),
         "average": (2174.5, 3186.0, "first point: ink meets the dashed #200 sieve line"),
         "lower": (2184.0, 3186.0, "first point: ink meets the #200 sieve line; merged with the 0% frame")}
LAST = {"upper": (717.0, 1453.0, "last point: top of the dash drawn just outside the 100% frame, below the #4 sieve line"),
        "average": (730.5, 1501.0, "last point: solid stroke merges into the 100% frame"),
        "lower": (744.0, 1553.0, "last point where this curve can be separated; above it, it cannot be told from B and the frame")}
KNEES = {"upper": [(2134.0, 2192.0, "lower knee"), (772.5, 1660.0, "upper knee")],
         "average": [(2149.0, 2188.5, "lower knee"), (789.5, 1660.0, "upper knee")],
         "lower": [(2158.5, 2182.0, "lower knee"), (803.0, 1660.0, "upper knee")]}

rows = []
for s in ("upper", "average", "lower"):
    pts = []
    fu, fv, fn = FIRST[s]
    pts.append((fu, fv, CLEAN, 5.0, fn))
    xs = {}
    for k, (u, v, b, flag, note) in XS[s].items():
        if flag == "x":
            v = v_for_x(xk(k), u)
        xs[k] = (u, v)
        pts.append((u, v, b, b, f"x={xk(k):.4f} mm" + ("" if flag == "x" else " (moved)") + (f"; {note}" if note else "")))
    ks = sorted(xs)
    yk = {k: y_at(*xs[k]) for k in ks}
    want = set()
    for a, bk in zip(ks, ks[1:]):
        if yk[bk] - yk[a] > 10:
            for y in range(5, 100, 5):
                if yk[a] < y < yk[bk]:
                    want.add(y)
    for y in sorted(want):
        if y not in YS[s]:
            print(f"MISSING 5% reading: {s} y={y}")
            continue
        u, v, b, flag, note = YS[s][y]
        if flag == "y" or u is None:
            u = u_for_y(y, v)
        pts.append((u, v, b, b, f"y={y}%" + ("" if flag == "y" else " (moved)") + (f"; {note}" if note else "")))
    for y in YS[s]:
        if y not in want:
            print(f"note: {s} y={y} read but not required by the rise rule")
    lu, lv, ln = LAST[s]
    pts.append((lu, lv, FRAME, FRAME, ln))
    first, last = pts[0], pts[-1]
    mid = sorted(pts[1:-1], key=lambda p: -p[1])   # drawing order from the fine end: v decreasing (monotonic curve)
    for i, (u, v, bu, bv, note) in enumerate([first] + mid + [last], 1):
        rows.append(dict(figure_id="FA-46", panel=1, series_id=s, point_kind="trace", sequence=i, pixel_u=round(u, 1),
                         pixel_v=round(v, 1), u_bound_px=bu, v_bound_px=bv, symbol="", note=note))
    feats = [(fu, fv, "first point")] + KNEES[s] + [(lu, lv, "last point")]
    for i, (u, v, note) in enumerate(feats, 1):
        b = FRAME if note == "last point" else (5.0 if note == "first point" else MERGED)
        rows.append(dict(figure_id="FA-46", panel=1, series_id=s, point_kind="feature", sequence=i, pixel_u=round(u, 1),
                         pixel_v=round(v, 1), u_bound_px=b, v_bound_px=b, symbol="", note=note))
    print(s, "x-sample percents:", {k: round(yk[k], 1) for k in ks})

with open("points-p1.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
                                      "u_bound_px", "v_bound_px", "symbol", "note"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(Counter((r["series_id"], r["point_kind"]) for r in rows))
