"""Write out/F2-34/points-p1.csv from the reviewed pixel readings (see notes.md)."""
import csv
F = 'F2-34'
rows = []
def add(sid, kind, u, v, ub, vb, note=''):
    rows.append([F, 1, sid, kind, 0, u, v, ub, vb, '', note])

# lpt87 (A), trace samples every 0.25 in from the origin
A = [
 (0.00, 2221, 3654, 6, 4, 'first ink at the origin corner on the load axis; sample at 0 in is the first point'),
 (0.25, 2037, 3587, 5, 5, 'at the knee; fit line 13 px to the left'),
 (0.50, 2029, 3522, 4, 4, ''),
 (0.75, 2026, 3457, 4, 4, ''),
 (1.00, 2018.5, 3391, 4, 4, 'on the 1 in grid line; center interpolated from 9 px above and below'),
 (1.25, 2003.5, 3326, 4, 4, ''),
 (1.50, 1982, 3261, 5, 5, ''),
 (1.75, 1955, 3195, 5, 5, 'on the 200 lb grid line'),
 (2.00, 1922.5, 3130, 4, 4, 'on the 2 in grid line; interpolated'),
 (2.25, 1884.5, 3065, 6, 5, 'crossing: A and the fit line coincide between v 3010 and 3075; merged run'),
 (2.50, 1855.5, 3000, 3, 4, ''),
 (2.75, 1823, 2935, 5, 5, ''),
 (3.00, 1786, 2869, 5, 5, 'on the 3 in grid line; interpolated'),
 (3.25, 1752, 2804, 5, 5, ''),
 (3.50, 1718.5, 2739, 4, 4, ''),
 (3.75, 1683.5, 2674, 7, 6, 'on the 400 lb grid line; run merged with the grid line'),
 (4.00, 1650, 2609, 5, 5, 'on the 4 in grid line; interpolated'),
 (4.25, 1614, 2543, 5, 5, ''),
 (4.50, 1578, 2478, 5, 5, ''),
 (4.75, 1541, 2413, 5, 5, ''),
 (5.00, 1504, 2348, 5, 5, 'on the 5 in grid line; interpolated'),
 (5.25, 1466, 2283, 5, 5, ''),
 (5.50, 1427, 2217, 5, 5, 'on the 600 lb grid line'),
 (5.75, 1390, 2152, 6, 5, ''),
 (6.00, 1351.5, 2087, 5, 5, 'on the 6 in grid line; interpolated'),
 (6.25, 1310, 2022, 5, 5, ''),
]
for x, u, v, ub, vb, n in A:
    add('lpt87', 'trace', u, v, ub, vb, ('sample at %.2f in; ' % x + n).rstrip('; '))
add('lpt87', 'feature', 2221, 3654, 6, 4, 'first')
add('lpt87', 'feature', 2039, 3589, 5, 5, 'knee: shallow start along the load axis turns steep at about 140 lb')
add('lpt87', 'feature', 1995, 3300, 8, 40, 'knee: gradual bend from the near-vertical stretch (1.0 in) to the steady slope (1.8 in); location approximate')
add('lpt87', 'feature', 1291, 1991, 5, 5, 'peak: maximum load is at the end of the trace (same point as last)')
add('lpt87', 'feature', 1291, 1991, 5, 5, 'last')

# fit (thick straight line), both ends and every drawn penetration line it crosses
Fp = [
 (2041, 3651, 4, 3, 'lower end of the ink where it meets the load axis line (axis ink v 3654 to 3659)'),
 (1974.5, 3391, 4, 4, 'at the 1 in grid line; interpolated'),
 (1903.8, 3130, 4, 4, 'at the 2 in grid line; interpolated'),
 (1828, 2869, 4, 4, 'at the 3 in grid line; interpolated'),
 (1758, 2608, 5, 4, 'at the 4 in grid line; interpolated; B hidden under the fit here'),
 (1686, 2347, 5, 4, 'at the 5 in grid line; on the 400 lb grid line'),
 (1609.8, 2086, 4, 4, 'at the 6 in grid line; interpolated'),
 (1534, 1825, 4, 4, 'at the 7 in grid line (unlabelled); interpolated'),
 (1529.5, 1811, 4, 4, 'upper end of the ink'),
]
for u, v, ub, vb, n in Fp:
    add('fit', 'trace', u, v, ub, vb, n)
add('fit', 'feature', 2042.5, 3657, 4, 3, 'intercept')
add('fit', 'feature', 1668, 1695, 22, 302, 'label: Slope = A gamma Nq = 54 lbs./in.')

# lpt88 (B), trace samples every 0.25 in from 2 in
B = [
 (2.00, 2210, 3125, 8, 3, 'ink starts on the load axis at the 2 in grid line and runs along that grid line to u 2100, showing above it only in short stretches; sample at 2 in is the first point'),
 (2.25, 1899, 3065, 5, 4, 'shallow stretch; joins the fit line just above (v 3060)'),
 (2.50, 1867.5, 3000, 5, 4, 'merged with the fit line (B runs along its right side from v 3060 to 2950)'),
 (2.75, 1858, 2934, 3, 3, '2 px right of the fit line'),
 (3.00, 1848.2, 2869, 3, 3, 'on the 3 in grid line; interpolated'),
 (3.25, 1831.5, 2804, 3, 3, ''),
 (3.50, 1808.5, 2738, 2.5, 2.5, ''),
 (3.75, 1784.5, 2673, 2.5, 2.5, ''),
 (4.00, 1758, 2608, 5, 4, 'hidden under the fit line (merged from v 2620 to 2456)'),
 (4.25, 1739, 2543, 5, 4, 'hidden under the fit line'),
 (4.50, 1718, 2477, 6, 4, 'merged with the fit line; B on the left side of the merged run'),
 (4.75, 1692, 2412, 4, 3, 'on the 400 lb grid line, 13 px left of the fit line'),
 (5.00, 1667.8, 2347, 2.5, 2.5, 'on the 5 in grid line; interpolated'),
 (5.25, 1644.5, 2282, 3, 3, ''),
 (5.50, 1617.5, 2216, 3, 3, ''),
 (5.75, 1591, 2151, 3, 3, ''),
 (6.00, 1568, 2086, 3, 3, 'on the 6 in grid line; interpolated'),
 (6.25, 1544.5, 2021, 2.5, 2.5, ''),
 (6.50, 1520.5, 1955, 2.5, 2.5, ''),
 (6.75, 1490.5, 1890, 2.5, 2.5, ''),
 (7.00, 1461.5, 1825, 2.5, 2.5, 'on the 7 in grid line (unlabelled); interpolated'),
 (7.25, 1439.5, 1760, 2.5, 2.5, ''),
 (7.50, 1414.5, 1694, 3, 3, ''),
 (7.75, 1387, 1629, 3.5, 3, ''),
 (8.00, 1359.2, 1564, 2.5, 2.5, 'on the 8 in grid line (unlabelled); interpolated'),
]
for x, u, v, ub, vb, n in B:
    add('lpt88', 'trace', u, v, ub, vb, ('sample at %.2f in; ' % x + n).rstrip('; '))
add('lpt88', 'feature', 2210, 3125, 8, 3, 'first')
add('lpt88', 'feature', 1888, 3060, 10, 8, 'knee: B turns from its shallow start to run along the fit line; the bend spreads from u 2100 to 1890')
add('lpt88', 'feature', 1347, 1528, 3, 3, 'peak: maximum load is at the end of the trace (same point as last)')
add('lpt88', 'feature', 1347, 1528, 3, 3, 'last')

# sequence numbers per series and kind, in drawing order
seq = {}
for r in rows:
    k = (r[2], r[3]); seq[k] = seq.get(k, 0) + 1; r[4] = seq[k]
with open('out/F2-34/points-p1.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['figure_id','panel','series_id','point_kind','sequence','pixel_u','pixel_v','u_bound_px','v_bound_px','symbol','note'])
    w.writerows(rows)
print(len(rows), 'rows')
