"""Marker inventory for FC-3C (both panels), assembled from the zoom-3 tile reading and the
template search (find_markers.py search), then checked marker by marker on contact sheets.
Writes markers-p1.csv and markers-p2.csv (points.csv columns, marker rows only).
Edits after the eye check are made here, so the file is the record of what was changed."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
        "u_bound_px", "v_bound_px", "symbol", "note"]

# (u, v, u_bound, v_bound, note)
P1 = {
 ("n4695", "plus"): [
  (859.0, 1662.0, 2, 3, "first point; sits on the 4000 gridline, curve starts here"),
  (971.9, 1397.6, 2, 2, ""),
  (1086.3, 1292.1, 2, 2, "8 px left of the x=50 gridline"),
  (1196.8, 1236.6, 2, 2, ""),
  (1308.0, 1214.0, 3, 3, "merged with the thick dash of the curve; arms barely visible"),
  (1431.0, 1214.0, 2, 2, ""),
  (1549.6, 1231.7, 2, 2, ""),
  (1660.6, 1262.2, 2, 2, ""),
  (1774.5, 1304.5, 2, 2, ""),
  (1950.9, 1390.4, 2, 3, "just below the 5000 gridline, 20 px left of the x=200 gridline"),
  (2092.0, 1405.5, 2, 2, "template instance"),
  (2266.2, 1446.0, 3, 2, "on the x=250 gridline; last point"),
 ],
 ("n3815", "circle"): [
  (859.3, 1897.0, 2, 2, "first point, curve starts here"),
  (975.0, 1626.5, 2, 2, ""),
  (1088.6, 1534.2, 2, 2, "touches the x=50 gridline"),
  (1200.4, 1500.2, 2, 2, ""),
  (1311.5, 1461.0, 2, 2, ""),
  (1427.0, 1445.5, 2, 2, ""),
  (1542.8, 1457.0, 2, 2, ""),
  (1664.9, 1496.9, 2, 2, ""),
  (1781.0, 1527.5, 2, 2, ""),
  (1957.0, 1590.0, 2, 2, "template instance"),
  (2103.5, 1608.0, 2, 2, ""),
  (2258.1, 1659.1, 3, 3, "on the crossing of the x=250 and 4000 gridlines; last point"),
 ],
 ("n2934", "triangle-down"): [
  (862.3, 2073.3, 2, 2, "first point, curve starts here"),
  (977.8, 1867.0, 2, 2, ""),
  (1085.6, 1833.0, 2, 2, "left edge on the x=50 gridline"),
  (1207.0, 1830.2, 2, 2, ""),
  (1321.2, 1829.0, 2, 2, ""),
  (1439.3, 1833.3, 2, 2, ""),
  (1552.4, 1846.8, 2, 2, ""),
  (1677.0, 1881.0, 2, 2, "on the x=150 gridline"),
  (1787.3, 1911.3, 2, 2, ""),
  (1959.5, 1956.0, 2, 2, "near the 3000 gridline, left of the x=200 gridline"),
  (2104.4, 1983.4, 2, 2, ""),
  (2251.3, 1999.7, 2, 2, "last point; 15 px left of the x=250 gridline"),
 ],
 ("n1761", "square"): [
  (873.5, 2322.0, 2, 2, "first point, curve starts here"),
  (981.5, 2168.0, 2, 2, ""),
  (1092.0, 2123.5, 2, 2, "right edge on the x=50 gridline"),
  (1206.5, 2123.5, 2, 2, ""),
  (1319.2, 2121.5, 2, 2, ""),
  (1439.0, 2129.5, 2, 2, ""),
  (1668.0, 2141.5, 2, 2, "template instance; no square between x=110 and x=150"),
  (1787.3, 2158.7, 2, 2, ""),
  (1957.0, 2185.0, 2, 2, "left of the x=200 gridline"),
  (2083.1, 2211.9, 2, 2, ""),
  (2266.0, 2248.0, 3, 3, "on the crossing of the x=250 and 2000 gridlines; last point"),
 ],
 ("n734", "triangle-up"): [
  (874.7, 2536.7, 2, 2, "first point; base touches the 1000 gridline"),
  (984.0, 2455.5, 2, 2, ""),
  (1102.5, 2448.5, 2, 2, "on the x=50 gridline"),
  (1215.0, 2468.0, 2, 2, ""),
  (1327.5, 2491.5, 2, 2, ""),
  (1447.5, 2507.0, 2, 2, ""),
  (1566.6, 2529.8, 2, 2, ""),
  (1687.0, 2546.7, 2, 2, "on the crossing of the x=150 and 1000 gridlines"),
  (1802.5, 2555.0, 2, 2, ""),
  (1972.1, 2569.1, 2, 2, "on the x=200 gridline"),
  (2093.5, 2585.5, 2, 2, ""),
  (2258.2, 2587.4, 2, 2, "last point; 11 px left of the x=250 gridline"),
 ],
}

P2 = {
 ("n4695", "plus"): [
  (828.0, 3354.5, 3, 2, "on the left frame line (x=0); lowest of the x=0 stack"),
  (941.0, 3323.0, 2, 3, "overlaps the circle above it (shared stroke)"),
  (1058.9, 3312.1, 2, 3, "overlaps the circle above it"),
  (1177.2, 3286.5, 2, 3, "overlaps the circle above it; just below the 0 gridline"),
  (1289.6, 3274.1, 2, 3, "horizontal arm lies on the 0 gridline; center from the vertical arm"),
  (1409.2, 3253.9, 3, 3, "on the x=100 gridline; overlaps the circle above it"),
  (1523.0, 3240.7, 2, 3, "overlaps the circle above it"),
  (1640.5, 3225.5, 2, 3, "overlaps the circle above it"),
  (1754.7, 3209.6, 2, 3, "overlaps the circle above it"),
  (1872.4, 3196.4, 2, 3, "overlaps the circle above it"),
  (1989.6, 3185.6, 3, 3, "on the x=200 gridline; overlaps the circle above it"),
  (2105.5, 3179.5, 2, 3, "overlaps the triangle-down above it"),
  (2275.7, 3160.7, 3, 2, "on the x=250 gridline; last point"),
 ],
 ("n3815", "circle"): [
  (825.6, 3325.8, 3, 2, "on the left frame line (x=0); touches the triangle-up above and the plus below"),
  (888.3, 3312.3, 2, 2, "clean; the circle series has a point at x=10 that the others do not"),
  (940.5, 3305.5, 2, 3, "overlaps the plus below it"),
  (1058.5, 3287.5, 2, 3, "overlaps the plus below it; touches the square above"),
  (1175.0, 3266.5, 2, 3, "between square above and plus below, touching both; on the 0 gridline"),
  (1289.0, 3251.5, 2, 2, ""),
  (1407.0, 3238.0, 3, 3, "on the x=100 gridline; overlaps the plus below"),
  (1521.0, 3223.5, 2, 3, "overlaps the plus below it"),
  (1639.5, 3205.5, 2, 3, "overlaps the plus below it"),
  (1754.7, 3187.7, 2, 3, "overlaps the plus below it"),
  (1871.2, 3173.4, 2, 3, "overlaps the plus below it"),
  (1989.5, 3158.0, 3, 3, "on the x=200 gridline; overlaps the plus below"),
  (2133.6, 3146.8, 2, 2, "touches the triangle-down to its left; extra point at x=225"),
  (2254.0, 3148.2, 2, 2, "touches the triangle-down to its right; extra point at x=245; last point"),
 ],
 ("n2934", "triangle-down"): [
  (854.4, 3328.0, 2, 2, "touches the square above it; first point at x=5, not at x=0"),
  (1004.6, 3310.2, 2, 2, ""),
  (1119.2, 3287.8, 3, 3, "on the crossing of the x=50 and 0 gridlines"),
  (1233.0, 3263.5, 2, 2, ""),
  (1349.2, 3241.7, 2, 2, ""),
  (1470.5, 3224.0, 2, 2, ""),
  (1584.4, 3212.7, 2, 2, ""),
  (1699.2, 3197.4, 3, 2, "on the x=150 gridline"),
  (1814.5, 3179.5, 2, 2, "template instance"),
  (1929.5, 3166.0, 2, 2, ""),
  (2107.2, 3151.8, 2, 3, "overlaps the plus below it; touches the circle to its right"),
  (2277.3, 3135.8, 3, 2, "on the x=250 gridline; last point"),
 ],
 ("n1761", "square"): [
  (859.0, 3300.0, 2, 2, "touches the triangle-down below it; first point at x=5, not at x=0"),
  (942.0, 3280.0, 2, 3, "on the 0 gridline; touches the circle below"),
  (1059.8, 3259.4, 2, 2, "touches the circle below"),
  (1175.0, 3238.5, 2, 2, "touches the circle below"),
  (1291.5, 3209.5, 2, 2, ""),
  (1405.8, 3178.4, 3, 2, "on the x=100 gridline"),
  (1525.5, 3160.5, 2, 2, ""),
  (1636.5, 3137.5, 2, 2, ""),
  (1755.0, 3115.5, 2, 2, ""),
  (1865.2, 3089.6, 2, 2, ""),
  (1989.8, 3069.8, 3, 2, "on the x=200 gridline"),
  (2106.6, 3058.0, 2, 2, ""),
  (2276.2, 3049.4, 3, 2, "on the x=250 gridline; last point"),
 ],
 ("n734", "triangle-up"): [
  (827.0, 3298.5, 3, 2, "on the left frame line (x=0); touches the circle below it"),
  (1006.5, 3274.0, 2, 3, "sits on the 0 gridline"),
  (1118.5, 3237.5, 3, 2, "on the x=50 gridline"),
  (1237.0, 3210.0, 2, 2, ""),
  (1353.3, 3193.7, 2, 2, ""),
  (1468.0, 3160.0, 2, 2, ""),
  (1584.0, 3136.5, 2, 2, ""),
  (1701.5, 3120.5, 3, 2, "on the x=150 gridline"),
  (1815.5, 3098.0, 2, 2, "template instance"),
  (1928.5, 3091.0, 2, 2, ""),
  (2107.5, 3084.5, 2, 2, ""),
  (2277.7, 3082.3, 3, 2, "on the x=250 gridline; last point"),
 ],
}


def write(panel, D, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for (sid, sym), pts in D.items():
            for i, (u, v, bu, bv, note) in enumerate(pts, 1):
                w.writerow(["FC-3C", panel, sid, "marker", i, "%.1f" % u, "%.1f" % v, bu, bv, sym, note])


if __name__ == "__main__":
    write(1, P1, os.path.join(HERE, "markers-p1.csv"))
    write(2, P2, os.path.join(HERE, "markers-p2.csv"))
    print("p1", sum(len(v) for v in P1.values()), "p2", sum(len(v) for v in P2.values()))
