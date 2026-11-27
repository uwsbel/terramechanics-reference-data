"""Marker readings for FC-6B (both panels), as read and checked on the contact sheets
(sheets/chk-*.png for squares, circles and pluses from match.py; sheets/tri-*.png for the
triangles, whose centers come from trigeom.py and the eye check). Writes markers.csv in the
points-file columns. Bounds: 2 px for a clean marker; triangles carry 3 px in v because the
plotting convention (centroid, used here, versus bounding-box center, H/6 = 5 px toward the
apex) is not known; wider where a symbol sits on a grid line, on the frame or under a line.
"""
import csv

FIG = "FC-6B"
TRI_V = 3
N = None  # placeholder for "no note"

# (panel, series, symbol, u, v, ub, vb, note)
M = [
    # ---- upper panel, n4695, triangle-up
    (1, "n4695", "triangle-up", 706.0, 1783.2, 2, 4, "first marker; apex hidden under the short stroke that joins it to the n3815 square above; v from the base"),
    (1, "n4695", "triangle-up", 824.8, 1526.2, 3, 4, "apex on the 2000 gridline; the shared n4695/n3815 line touches the left side; v from the base"),
    (1, "n4695", "triangle-up", 931.7, 1403.5, 2, TRI_V, "curve line enters the left base corner; u from the two sides"),
    (1, "n4695", "triangle-up", 1047.5, 1296.5, 2, TRI_V, N),
    (1, "n4695", "triangle-up", 1159.0, 1214.5, 2, 4, "3000 gridline crosses the lower part of the triangle"),
    (1, "n4695", "triangle-up", 1334.8, 1092.5, 2, TRI_V, N),
    (1, "n4695", "triangle-up", 1453.3, 1028.5, 2, TRI_V, N),
    (1, "n4695", "triangle-up", 1567.0, 984.5, 2, TRI_V, N),
    (1, "n4695", "triangle-up", 1800.5, 900.5, 2, TRI_V, "right base corner close to the 200 gridline; no n4695 marker near x = 180 where the other series have one"),
    (1, "n4695", "triangle-up", 1919.5, 867.0, 2, 4, "the curve line runs into the base from the left; v from apex and base"),
    (1, "n4695", "triangle-up", 2089.0, 863.5, 3, TRI_V, "last marker; line touches the left side, right corner close to the 250 gridline"),
    # ---- upper panel, n3815, square
    (1, "n3815", "square", 703.9, 1739.1, 2, 2, "first marker; the shared line leaves its upper-right corner and a short stroke joins its bottom to the n4695 triangle below"),
    (1, "n3815", "square", 824.5, 1566.0, 3, 2, "the shared n4695/n3815 line runs along its left side"),
    (1, "n3815", "square", 936.9, 1459.6, 2, 2, N),
    (1, "n3815", "square", 1050.8, 1387.9, 2, 2, N),
    (1, "n3815", "square", 1162.2, 1354.3, 2, 2, N),
    (1, "n3815", "square", 1339.1, 1242.5, 2, 2, N),
    (1, "n3815", "square", 1461.3, 1168.9, 2, 2, N),
    (1, "n3815", "square", 1570.4, 1133.1, 2, 2, N),
    (1, "n3815", "square", 1685.5, 1093.0, 2, 2, N),
    (1, "n3815", "square", 1804.3, 1049.0, 3, 2, "right side on the 200 gridline"),
    (1, "n3815", "square", 1922.9, 1014.2, 2, 2, N),
    (1, "n3815", "square", 2090.4, 1000.8, 3, 2, "last marker; right side on the 250 gridline"),
    # ---- upper panel, n2934, triangle-down
    (1, "n2934", "triangle-down", 708.9, 1838.5, 2, TRI_V, "first marker; the line starts at its upper-right corner"),
    (1, "n2934", "triangle-down", 821.8, 1727.5, 2, TRI_V, N),
    (1, "n2934", "triangle-down", 940.0, 1677.5, 3, 4, "the curve line runs along its top edge; right corner close to the 50 gridline; u from the apex"),
    (1, "n2934", "triangle-down", 1051.3, 1595.5, 2, TRI_V, N),
    (1, "n2934", "triangle-down", 1167.5, 1529.5, 2, TRI_V, "top edge just below the 2000 gridline"),
    (1, "n2934", "triangle-down", 1340.8, 1451.5, 2, TRI_V, N),
    (1, "n2934", "triangle-down", 1458.7, 1398.8, 2, TRI_V, N),
    (1, "n2934", "triangle-down", 1577.0, 1361.2, 2, TRI_V, N),
    (1, "n2934", "triangle-down", 1688.3, 1326.8, 2, TRI_V, N),
    (1, "n2934", "triangle-down", 1806.8, 1289.5, 3, TRI_V, "right corner touches the 200 gridline and the line"),
    (1, "n2934", "triangle-down", 1923.8, 1265.5, 2, TRI_V, N),
    (1, "n2934", "triangle-down", 2095.0, 1233.5, 3, 4, "last marker; right corner merged with the 250 gridline, top edge close to the 3000 gridline; u from the apex"),
    # ---- upper panel, n1761, circle
    (1, "n1761", "circle", 708.6, 1933.7, 2, 2, "first marker"),
    (1, "n1761", "circle", 825.0, 1866.0, 2, 2, N),
    (1, "n1761", "circle", 942.7, 1812.6, 2, 3, "top of the circle on the 1000 gridline"),
    (1, "n1761", "circle", 1052.5, 1776.2, 2, 2, N),
    (1, "n1761", "circle", 1165.0, 1741.2, 2, 2, N),
    (1, "n1761", "circle", 1342.5, 1700.1, 2, 2, N),
    (1, "n1761", "circle", 1457.0, 1672.5, 2, 2, N),
    (1, "n1761", "circle", 1575.8, 1656.1, 2, 2, N),
    (1, "n1761", "circle", 1684.1, 1637.0, 2, 2, N),
    (1, "n1761", "circle", 1807.4, 1630.7, 3, 2, "right side touches the 200 gridline"),
    (1, "n1761", "circle", 1920.7, 1627.7, 2, 2, N),
    (1, "n1761", "circle", 2088.0, 1623.1, 2, 2, "last marker"),
    # ---- upper panel, n734, plus
    (1, "n734", "plus", 712.2, 1979.8, 2, 2, "first marker"),
    (1, "n734", "plus", 822.3, 1976.7, 2, 2, N),
    (1, "n734", "plus", 939.1, 1976.2, 2, 2, "right arm close to the 50 gridline"),
    (1, "n734", "plus", 1054.3, 1976.5, 2, 2, N),
    (1, "n734", "plus", 1168.3, 1984.8, 2, 2, "left arm touches the end of a line dash; sits below the drawn line"),
    (1, "n734", "plus", 1336.9, 1986.9, 2, 2, "sits below the drawn line"),
    (1, "n734", "plus", 1460.0, 1982.1, 2, 2, N),
    (1, "n734", "plus", 1575.9, 1988.4, 2, 2, "sits below the drawn line"),
    (1, "n734", "plus", 1695.7, 1986.1, 2, 2, N),
    (1, "n734", "plus", 1818.8, 1997.2, 3, 2, "vertical bar hidden in the 200 gridline; u from the horizontal bar"),
    (1, "n734", "plus", 1925.1, 1996.6, 2, 2, N),
    (1, "n734", "plus", 2101.2, 2001.2, 2, 2, "last marker; right arm touches the 250 gridline"),
    # ---- lower panel, n734, plus
    (2, "n734", "plus", 643.8, 2600.7, 3, 2, "on the left frame; vertical bar hidden in the frame line"),
    (2, "n734", "plus", 724.6, 2602.1, 2, 2, N),
    (2, "n734", "plus", 838.8, 2604.7, 2, 2, N),
    (2, "n734", "plus", 959.1, 2604.4, 3, 2, "on the 50 gridline"),
    (2, "n734", "plus", 1066.3, 2609.6, 2, 2, N),
    (2, "n734", "plus", 1183.3, 2611.3, 2, 2, N),
    (2, "n734", "plus", 1306.3, 2607.0, 2, 2, N),
    (2, "n734", "plus", 1413.3, 2608.0, 2, 2, N),
    (2, "n734", "plus", 1530.6, 2610.4, 3, 2, "on the 150 gridline"),
    (2, "n734", "plus", 1650.2, 2609.3, 2, 2, N),
    (2, "n734", "plus", 1763.3, 2609.9, 2, 2, "a short stray dash to its right (u 1773 to 1810) is not a drawn line"),
    (2, "n734", "plus", 1935.3, 2608.4, 2, 2, N),
    (2, "n734", "plus", 2115.0, 2608.6, 3, 2, "on the 250 gridline"),
    # ---- lower panel, n1761, circle
    (2, "n1761", "circle", 648.5, 2903.0, 3, 2, "on the left frame"),
    (2, "n1761", "circle", 729.5, 2915.2, 2, 2, N),
    (2, "n1761", "circle", 847.4, 2928.2, 2, 2, N),
    (2, "n1761", "circle", 960.0, 2932.6, 3, 2, "on the 50 gridline"),
    (2, "n1761", "circle", 1069.9, 2935.7, 2, 2, N),
    (2, "n1761", "circle", 1192.6, 2939.2, 2, 2, N),
    (2, "n1761", "circle", 1304.3, 2939.1, 2, 2, N),
    (2, "n1761", "circle", 1423.3, 2934.6, 2, 2, N),
    (2, "n1761", "circle", 1531.7, 2933.8, 3, 2, "on the 150 gridline"),
    (2, "n1761", "circle", 1644.7, 2925.0, 2, 2, N),
    (2, "n1761", "circle", 1764.5, 2912.9, 2, 2, N),
    (2, "n1761", "circle", 1941.0, 2903.2, 2, 2, N),
    (2, "n1761", "circle", 2116.6, 2895.2, 3, 2, "on the 250 gridline"),
    # ---- lower panel, n2934, triangle-down
    (2, "n2934", "triangle-down", 649.5, 3112.5, 3, 4, "on the left frame; apex hidden in the frame line"),
    (2, "n2934", "triangle-down", 714.5, 3125.5, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 830.8, 3139.5, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 950.5, 3147.8, 3, TRI_V, "right corner on the 50 gridline; u from the apex"),
    (2, "n2934", "triangle-down", 1064.7, 3147.8, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 1184.7, 3151.5, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 1297.8, 3154.5, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 1410.3, 3150.8, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 1531.3, 3149.2, 3, 4, "on the 150 gridline; apex hidden in the gridline"),
    (2, "n2934", "triangle-down", 1644.7, 3146.2, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 1760.3, 3144.8, 2, TRI_V, "outline broken on the right side (scan)"),
    (2, "n2934", "triangle-down", 1935.0, 3135.8, 2, TRI_V, N),
    (2, "n2934", "triangle-down", 2118.8, 3121.5, 3, 4, "on the 250 gridline; apex hidden in the gridline"),
    # ---- lower panel, n4695, triangle-up
    (2, "n4695", "triangle-up", 649.8, 3178.2, 3, 4, "on the left frame"),
    (2, "n4695", "triangle-up", 709.7, 3185.5, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 826.3, 3207.5, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 946.5, 3206.8, 3, TRI_V, "right base corner on the 50 gridline; u from the apex"),
    (2, "n4695", "triangle-up", 1059.3, 3219.0, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 1173.2, 3218.5, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 1293.7, 3217.2, 2, 4, "outline thicker than the others (H about 33 px); v averaged from apex and base"),
    (2, "n4695", "triangle-up", 1405.3, 3219.5, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 1526.3, 3214.2, 3, TRI_V, "on the 150 gridline"),
    (2, "n4695", "triangle-up", 1633.7, 3213.5, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 1753.5, 3215.5, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 1925.5, 3203.5, 2, TRI_V, N),
    (2, "n4695", "triangle-up", 2120.0, 3196.0, 3, 4, "on the 250 gridline"),
]


def main():
    seq = {}
    rows = []
    for p, s, sym, u, v, ub, vb, note in M:
        k = (p, s)
        seq[k] = seq.get(k, 0) + 1
        rows.append(dict(figure_id=FIG, panel=p, series_id=s, point_kind="marker", sequence=seq[k],
                         pixel_u=u, pixel_v=v, u_bound_px=ub, v_bound_px=vb, symbol=sym, note=note or ""))
    with open("markers.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("markers per panel/series:", {f"p{k[0]}-{k[1]}": n for k, n in seq.items()})


if __name__ == "__main__":
    main()
