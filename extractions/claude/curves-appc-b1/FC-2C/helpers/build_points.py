"""Assemble points-p1.csv and points-p2.csv for FC-2C from the by-eye readings (markers, features,
by-eye trace overrides) and the ridge-follower samples (helpers/follow-*.csv, reviewed on the
overlay). Every number here was read from a zoomed crop or taken from the follower output and
checked on the overlay; see notes.md for the ambiguities."""
import csv

COLS = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
        "u_bound_px", "v_bound_px", "symbol", "note"]
FIG = "FC-2C"
rows1, rows2 = [], []


def add(rows, panel, series, kind, pts, symbol=""):
    for i, p in enumerate(pts, 1):
        u, v, bu, bv = p[0], p[1], p[2], p[3]
        note = p[4] if len(p) > 4 else ""
        rows.append([FIG, panel, series, kind, i, u, v, bu, bv, symbol, note])


# ---------------- panel 1 markers ----------------
add(rows1, 1, "n4400", "marker", [
    (813, 1814, 2, 2), (878, 1693, 2, 2), (931, 1621, 2, 2), (990, 1544, 2, 2), (1052, 1484, 2, 2),
    (1113, 1428, 2, 2), (1167, 1397, 2, 2), (1216, 1366, 3, 3, "just below the 5000 psf gridline"),
    (1285, 1338, 3, 3, "touches the x=100 gridline"), (1344, 1319, 2, 2), (1401, 1303, 2, 2),
    (1457, 1295, 2, 2), (1512, 1289, 2, 2), (1571, 1290, 3, 3, "on the x=150 gridline"),
    (1627, 1297, 2, 2), (1689, 1320, 2, 2, "last asterisk; drawn line ends here")], "asterisk")
add(rows1, 1, "n3660", "marker", [
    (721, 2071, 2, 2, "first x; sits just left of the first square"), (757, 1987, 2, 2), (816, 1878, 2, 2),
    (875, 1797, 2, 2), (937, 1722, 2, 2), (987, 1678, 3, 3, "on the x=50 gridline"), (1042, 1634, 2, 2),
    (1102, 1601, 2, 2), (1163, 1573, 2, 2), (1220, 1557, 2, 2), (1282, 1539, 3, 3, "on the x=100 gridline"),
    (1345, 1524, 2, 2), (1397, 1514, 3, 3, "overlaps the dashed line"), (1459, 1505, 2, 2), (1515, 1504, 2, 2),
    (1586, 1503, 2, 2), (1637, 1506, 2, 2, "last x; drawn line ends here")], "x")
add(rows1, 1, "n2995", "marker", [
    (753, 2069, 2, 2, "short dash printed under the square at v 2086"), (787, 2000, 2, 2),
    (821, 1938, 3, 3, "on the 3000 psf gridline"), (877, 1874, 2, 2, "square open at the top, line passes through"),
    (988, 1763, 3, 3, "on the x=50 gridline"), (1052, 1724, 2, 2), (1102, 1698, 2, 2), (1162, 1674, 2, 2),
    (1222, 1661, 2, 2, "short dash printed under the square at v 1679"), (1283, 1631, 3, 3, "touches the x=100 gridline"),
    (1461, 1628, 2, 2), (1570, 1640, 3, 3, "on the x=150 gridline; lower edge on the 4000 psf gridline; last square")], "square")
add(rows1, 1, "n2200", "marker", [
    (736, 2432, 2, 2, "first triangle; line begins here"), (790, 2346, 2, 2), (821, 2303, 2, 2),
    (874, 2212, 3, 3, "base sits on the 2000 psf gridline"), (934, 2139, 2, 2),
    (965, 2116, 6, 6, "UNCERTAIN: only a horizontal base (u 951-979, v 2124) is distinct; left edge merged with the drawn line, right edge with the x=50 gridline; may not be a marker"),
    (1052, 2040, 2, 2), (1167, 1988, 2, 2), (1225, 1961, 2, 2),
    (1287, 1950, 4, 4, "on the x=100 gridline and overlapping the 3000 psf gridline"),
    (1344, 1947, 3, 3, "just under the 3000 psf gridline"), (1401, 1928, 3, 3, "base on the 3000 psf gridline, apex above")], "triangle-up")
add(rows1, 1, "n1468", "marker", [
    (705, 2685, 3, 3, "left side merged with the left frame line"), (714, 2560, 2, 2), (751, 2453, 2, 2),
    (816, 2354, 2, 2), (901, 2284, 2, 2), (983, 2247, 3, 3, "on the x=50 gridline"),
    (1048, 2224, 3, 3, "on the 2000 psf gridline"), (1162, 2222, 3, 3, "on the 2000 psf gridline; last circle")], "circle")
add(rows1, 1, "n734", "marker", [
    (723, 2647, 2, 2, "filled circle"), (759, 2521, 3, 3, "filled circle on the 1000 psf gridline"),
    (814, 2456, 2, 2, "filled circle"), (928, 2417, 2, 2, "filled circle"), (1041, 2427, 2, 2, "filled circle; last")], "circle")


# ---------------- panel 1 traces ----------------
def fs(u, v, L, note=""):
    """follower sample: u_bound 2, v_bound = half the measured run length (min 2)"""
    return (u, v, 2, max(2, round(L / 2)), note)


add(rows1, 1, "n4400", "trace", [
    fs(824.4, 1786.1, 8), fs(853.8, 1733.5, 10), fs(883.5, 1691.1, 6), fs(913.0, 1640.2, 9), fs(943.6, 1600.7, 10),
    fs(971.7, 1561.4, 7), fs(1001.5, 1539.0, 1), fs(1029.4, 1500.8, 12), fs(1054.1, 1473.3, 2, "near asterisk at 1052"),
    fs(1089.2, 1449.1, 14), fs(1114.0, 1420.1, 5), fs(1148.2, 1408.4, 11), fs(1176.8, 1389.8, 5),
    (1205, 1370, 2, 5, "by eye; dash merged with the asterisk at 1216"),
    (1234, 1356, 2, 4, "by eye; dash merged with the 5000 psf gridline"),
    fs(1261.5, 1349.2, 12), fs(1292.8, 1336.2, 4), fs(1322.9, 1325.1, 12), fs(1348.8, 1320.7, 10), fs(1380.9, 1305.9, 12),
    fs(1407.8, 1308.9, 9), fs(1437.7, 1295.1, 11), fs(1466.4, 1287.9, 4), fs(1494.0, 1288.8, 11),
    (1530, 1289, 3, 4, "by eye; nearest dash ink, column 1526 falls on the asterisk at 1512"),
    fs(1550.7, 1287.9, 9), (1590, 1291, 3, 4, "by eye; nearest dash ink, column 1584 falls on the asterisk at 1571"),
    fs(1615.0, 1292.1, 6), fs(1644.2, 1303.7, 11), fs(1670.5, 1314.3, 5, "dash ends at 1672")])
add(rows1, 1, "n3660", "trace", [
    fs(738.1, 2027.5, 11, "steep section"), fs(767.3, 1963.9, 10, "steep"), fs(796.9, 1910.2, 10, "steep"), fs(827.3, 1860.4, 9),
    fs(854.4, 1820.6, 11), fs(884.1, 1782.5, 1), fs(911.9, 1748.1, 13), fs(943.3, 1715.9, 5), fs(969.4, 1689.7, 12),
    fs(999.6, 1666.3, 11), (1026, 1649, 3, 4, "by eye; end of a dash, the 4000 psf gridline passes at v 1650"),
    fs(1058.5, 1624.8, 8), fs(1088.8, 1604.8, 7), fs(1118.5, 1591.0, 11), fs(1144.3, 1579.2, 11), fs(1170.3, 1563.4, 3),
    fs(1205.6, 1557.1, 8), fs(1237.6, 1550.2, 8), fs(1264.3, 1540.7, 11), fs(1292.0, 1530.0, 2), fs(1319.7, 1529.4, 13),
    fs(1350.8, 1529.7, 7), fs(1379.1, 1518.0, 11), fs(1411.1, 1514.6, 2), fs(1439.1, 1510.3, 9), fs(1465.3, 1512.2, 6),
    fs(1498.1, 1504.3, 2), fs(1521.9, 1509.3, 7), fs(1556.1, 1501.9, 10),
    (1586.5, 1500.2, 2, 5, "inside the x marker at 1586"), fs(1612.3, 1503.4, 11, "dash ends at 1622")])
add(rows1, 1, "n2995", "trace", [
    fs(767.1, 2037.7, 9, "steep"), fs(797.1, 1979.6, 10, "steep"), fs(829.1, 1928.0, 5), fs(854.5, 1890.6, 9), fs(885.0, 1861.5, 5),
    fs(911.3, 1826.0, 10), fs(941.5, 1799.4, 10), fs(969.8, 1777.1, 11), fs(1000.2, 1762.6, 2), fs(1030.2, 1733.2, 10),
    fs(1059.3, 1727.7, 13, "run includes the square at 1052"), fs(1089.6, 1702.3, 11), fs(1115.9, 1689.9, 14, "run includes the square at 1102"),
    fs(1147.0, 1681.3, 4), fs(1180.0, 1666.1, 4), fs(1205.4, 1662.7, 9), fs(1230.3, 1657.9, 12), fs(1262.9, 1647.4, 12),
    fs(1291.1, 1641.7, 11), fs(1319.7, 1637.6, 12), fs(1351.4, 1631.3, 10), fs(1379.7, 1630.1, 14), fs(1408.4, 1625.7, 11),
    fs(1436.5, 1625.7, 12), (1466, 1625, 2, 5, "by eye; inside the square at 1461"), fs(1496.3, 1628.1, 12),
    (1524, 1632, 2, 4, "by eye"), (1550, 1636, 3, 4, "by eye; end of the last dash before the square at 1570")])
add(rows1, 1, "n2200", "trace", [
    (741.3, 2421.1, 2, 5, "inside the first triangle; steep"), fs(767.1, 2371.0, 10, "steep"), fs(795.8, 2324.0, 9), fs(825.0, 2279.2, 10),
    fs(854.3, 2235.7, 10), (886, 2197, 2, 4, "by eye; start of the dash after the 2000 psf gridline crossing"),
    (913, 2173, 2, 3, "by eye"), (943.4, 2138.3, 2, 5, "inside the triangle at 934"), fs(970.9, 2104.2, 9), fs(1000.0, 2081.8, 11),
    fs(1031.2, 2056.4, 10), (1055, 2040, 2, 5, "by eye; inside the triangle at 1052"), fs(1089.3, 2017.4, 10), fs(1117.4, 2001.3, 11),
    fs(1142.5, 1988.7, 8), (1175, 1980, 2, 7, "inside the triangle at 1167; line position uncertain"),
    (1205, 1961, 2, 3, "by eye"), (1240, 1949, 3, 4, "by eye; nearest dash ink, column 1234 falls on the triangle at 1225; dash below the 3000 psf gridline"),
    (1263, 1950, 2, 4, "by eye; dash below the 3000 psf gridline"), (1292, 1937, 2, 5, "by eye; line crosses and merges with the 3000 psf gridline"),
    (1321, 1933, 2, 4, "by eye; merged with gridline"), (1351, 1930, 2, 4, "by eye; just above the 3000 psf gridline"),
    (1376, 1930, 3, 4, "by eye; nearest dash ink before the triangle at 1401"), (1409, 1930, 2, 5, "by eye; inside the triangle at 1401"),
    (1438, 1930, 2, 4, "by eye"), (1467, 1931, 2, 4, "by eye; dash ends at about 1470")])
add(rows1, 1, "n1468", "trace", [
    (708.8, 2675.9, 2, 6, "near-vertical section just above the first circle"), fs(737.5, 2481.4, 9, "steep"), fs(767.9, 2415.6, 9, "steep"),
    fs(797.0, 2372.1, 10), fs(828.4, 2339.8, 10), fs(855.2, 2315.6, 10), fs(883.4, 2292.9, 1), fs(910.9, 2282.0, 9),
    fs(941.5, 2262.5, 12), fs(973.5, 2255.3, 4), (1000, 2238, 2, 4, "by eye; thick dash under the 2000 psf gridline"),
    (1030, 2228, 2, 4, "by eye; dash merged with the 2000 psf gridline"),
    (1072, 2219, 3, 4, "by eye; nearest ink, start of the thick dash above the gridline (column 1059 is a gap after the circle at 1048)"),
    (1088, 2219, 2, 3, "by eye; thick dash 3 to 6 px above the 2000 psf gridline"), (1117, 2219, 2, 3, "by eye"),
    (1146, 2219, 2, 3, "by eye; dash ends at about 1147")])
add(rows1, 1, "n734", "trace", [
    fs(737.6, 2570.5, 9, "steep"), (767.3, 2508.3, 2, 6, "run includes the filled circle at 759 and the 1000 psf gridline"),
    fs(797.7, 2470.7, 11), fs(827.0, 2447.5, 6), fs(854.9, 2431.5, 11), fs(885.6, 2421.9, 12), fs(913.7, 2417.8, 3),
    fs(942.2, 2416.9, 6), fs(970.3, 2416.1, 12), fs(999.3, 2419.7, 12), fs(1031.7, 2423.1, 8, "near the filled circle at 1041"),
    fs(1059.2, 2431.4, 9), fs(1086.7, 2438.5, 10, "end of the drawn line")])

# ---------------- panel 1 features ----------------
add(rows1, 1, "n4400", "feature", [
    (813, 1814, 5, 5, "first point: drawn line begins at the first asterisk"),
    (1541, 1289, 4, 4, "peak: plateau from about u 1500 to 1600 at v 1289, flat within the line thickness"),
    (1689, 1320, 5, 5, "last point: drawn line ends at the last asterisk (dash ends at 1672)")])
add(rows1, 1, "n3660", "feature", [
    (721, 2071, 5, 5, "first point: line begins at the first x"),
    (1580, 1502, 4, 4, "peak: plateau from about u 1540 to 1620 at v 1502"),
    (1637, 1506, 5, 5, "last point: line ends at the last x (dash ends at 1622)")])
add(rows1, 1, "n2995", "feature", [
    (753, 2069, 5, 5, "first point: line begins at the first square"),
    (1450, 1625, 5, 5, "peak: plateau from about u 1400 to 1500 at v 1625; line passes through the square at 1461"),
    (1570, 1640, 5, 5, "last point: line ends at the last square")])
add(rows1, 1, "n2200", "feature", [
    (736, 2432, 5, 5, "first point: line begins at the first triangle"),
    (1420, 1929, 4, 4, "peak: plateau from about u 1350 to 1470 at v 1930, just above the 3000 psf gridline"),
    (1470, 1931, 4, 4, "last point: dash ends on the 3000 psf gridline")])
add(rows1, 1, "n1468", "feature", [
    (705, 2685, 5, 5, "first point: first circle, on the left frame line"),
    (1108, 2219, 4, 4, "peak: plateau from about u 1070 to 1147, thick dash 3 to 6 px above the 2000 psf gridline"),
    (1162, 2222, 5, 5, "last point: line ends at the last circle on the 2000 psf gridline")])
add(rows1, 1, "n734", "feature", [
    (723, 2647, 5, 5, "first point: line begins at the first filled circle"),
    (955, 2416, 4, 4, "peak: plateau from about u 913 to 985 at v 2416"),
    (1087, 2439, 3, 3, "last point: end of the drawn line, past the filled circle at 1041")])

# ---------------- panel 2 markers ----------------
add(rows2, 2, "n2995", "marker", [
    (708, 3227, 3, 3, "flat top, rectangular hole; square or circle; merged with the filled circle at 722"),
    (739, 3217, 3, 3, "flat top, rectangular hole; merged with the filled circle at 750"),
    (922, 3202.5, 3, 3, "tail at lower right"),
    (984, 3201, 4, 4, "stack of four symbols on the x=50 gridline; round hole, square or circle"),
    (1041.5, 3195.5, 2, 2), (1101, 3209, 3, 3, "stack of three merged symbols (v 3182 to 3240)"),
    (1159, 3180, 3, 3, "merged with the triangle below"), (1217.5, 3166.5, 2, 2),
    (1277, 3161, 3, 3, "on the x=100 gridline"),
    (1450, 3172, 4, 4, "square or circle; merged with the symbols above and below")], "square")
add(rows2, 2, "n734", "marker", [
    (722, 3230, 3, 3, "filled blob 13 px; filled circle or x; merged with the square at 708"),
    (750, 3223, 3, 3, "filled blob; merged with the square at 739"), (804, 3210, 2, 2),
    (862, 3198.5, 2, 2, "small spikes top and bottom"),
    (980, 3178, 4, 4, "dark blob at the top of the stack on the x=50 gridline; filled circle inferred"),
    (1043, 3148.5, 2, 2)], "circle")
add(rows2, 2, "n1468", "marker", [
    (892.5, 3199.5, 2, 2), (982, 3188, 4, 4, "stack on the x=50 gridline"), (1040.5, 3174.5, 2, 2),
    (1101, 3192, 3, 3, "top of a stack of three"), (1152.5, 3158, 2, 2), (1218, 3193, 3, 3, "x merged below"),
    (1277, 3186, 4, 4, "on the x=100 gridline; merged stack"),
    (1334, 3178, 3, 3, "round; could be a small triangle"), (1334, 3190, 3, 3, "circle or square"),
    (1393, 3180, 4, 4, "circle or square; merged"), (1450, 3159, 3, 3, "circle or square")], "circle")
add(rows2, 2, "n2200", "marker", [
    (805, 3229, 3, 3, "base near the zero gridline"), (862.5, 3222, 2, 2), (924, 3222, 3, 3, "merged with the square above"),
    (985, 3224, 3, 3, "stack on the x=50 gridline"), (1041, 3219, 2, 2), (1102, 3228, 3, 3, "base on the zero gridline; stack of three"),
    (1161, 3200, 3, 3, "merged with the square above"), (1393, 3167, 3, 3, "pointed top; triangle or square")], "triangle-up")
add(rows2, 2, "n3660", "marker", [
    (1219, 3208, 4, 4, "upper arms merged into the circle above; x or triangle"),
    (1277, 3201, 5, 5, "on the x=100 gridline; x or a second open symbol; merged stack"),
    (1334, 3203, 4, 4, "lower half visible; upper half merged"), (1392, 3193, 4, 4, "merged above"),
    (1451, 3183, 4, 4, "merged above"), (1511.5, 3174, 2, 2), (1568, 3166, 3, 3, "on the x=150 gridline"),
    (1624.5, 3168, 2, 2)], "x")
add(rows2, 2, "n4400", "marker", [
    (1160, 3225.5, 2, 2), (1220, 3228.5, 2, 2, "touches the zero gridline"), (1277, 3230, 3, 3, "on the x=100 gridline"),
    (1335.5, 3219, 2, 2), (1395, 3213, 2, 2), (1450.5, 3204, 2, 2), (1510.5, 3201, 2, 2),
    (1565, 3197, 3, 3, "on the x=150 gridline"), (1624.5, 3192, 2, 2), (1684.5, 3183.5, 2, 2)], "asterisk")

for path, rows in (("out/FC-2C/points-p1.csv", rows1), ("out/FC-2C/points-p2.csv", rows2)):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        w.writerows(rows)
    print(path, len(rows), "rows")
