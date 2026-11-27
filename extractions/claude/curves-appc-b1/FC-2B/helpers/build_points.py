"""Builds points-p1.csv and points-p2.csv for FC-2B from the reader's by-eye marker readings
(hard-coded below, read from zoomed crops) plus trace samples of the drawn upper-panel curves.

Trace sampling: at columns every ~25 px (about 4.3 thousandths), avoiding vertical gridlines and
marker centres, the dark run (min over u-1..u+1, as tools/plot_grid.py scan does) nearest the
value interpolated between the series' neighbouring markers is taken as the drawn line; a column
with no run within tolerance (a gap in the dashed line) is moved in 5 px steps up to 20 px.
A run thicker than 16 px is a merge (two curves, a curve and a gridline, or a marker) and gets a
wider bound and a note. Bound in v is half the run thickness. Features (first, peak, last) come
from a dense 2 px scan of the same line.
"""
import csv
import numpy as np
from PIL import Image

IMG = "packet/p0121.png"
FIG = "FC-2B"
img = np.array(Image.open(IMG).convert("L")) < 128

# ---- upper panel markers: (u, v, ub, vb, note) ----
P1 = {
 "n4400": ("asterisk", [
  (823,2492,4,4,"first point; overlaps the first x of n3660 and both curves; centre read at zoom 6"),
  (816,2312,2,2,""),(930,2079,2,2,""),(990,2004,2,2,""),(1106,1893,2,2,""),(1167,1839,2,2,""),
  (1225,1792,2,2,""),(1282,1758,2,2,""),(1334,1730,3,2,"on the x=100 gridline"),(1452,1670,2,3,"on the 4000 gridline"),
  (1517,1643,2,2,""),(1575,1619,2,2,""),(1690,1581,2,2,""),(1798,1552,2,2,""),(1973,1514,2,2,""),
  (2221,1501,8,3,"symbol at/just beyond the right frame (x about 252); doubles as legend key; may be the x=250 reading"),
 ]),
 "n3660": ("x", [
  (823,2497,6,6,"first x inferred under the first asterisk of n4400; not separable from it"),
  (855,2326,2,2,""),(932,2220,2,2,""),(1053,2093,4,3,"left half hidden by the x=50 gridline"),(1107,2037,2,2,""),
  (1168,1999,2,2,""),(1230,1957,2,3,"on the 3000 gridline"),(1400,1871,2,2,""),(1463,1844,2,2,""),(1575,1798,2,2,""),
  (1685,1764,2,2,""),(1800,1729,2,2,""),(1915,1699,3,2,"on the x=200 gridline"),(2090,1678,2,2,""),
  (2208,1690,6,3,"symbol on the right frame (x about 250); doubles as legend key"),
 ]),
 "n2995": ("square", [
  (825,2520,2,2,"first point; just below the n4400/n3660 first markers"),(883,2403,2,2,""),(943,2320,2,2,""),
  (995,2249,3,3,"on the 2000 gridline"),(1053,2197,3,2,"on the x=50 gridline"),(1110,2148,2,2,""),(1167,2115,2,2,""),
  (1225,2078,2,2,""),(1284,2052,2,2,""),(1343,2023,3,2,"on the x=100 gridline"),(1402,2000,2,2,""),
  (1513,1957,2,3,"on the 3000 gridline"),(1688,1898,2,2,""),(1917,1860,3,2,"on the x=200 gridline"),(2042,1858,2,2,""),
  (2150,1860,2,2,""),(2226,1864,8,3,"symbol beyond the right frame (x about 253); doubles as legend key"),
 ]),
 "n2200": ("triangle-up", [
  (817,2592,2,3,"first point; centre = bounding-box centre (apex and base midpoint), as for all triangles"),(883,2507,2,3,""),(942,2447,2,3,""),
  (1002,2392,2,3,""),(1109,2309,2,3,""),(1167,2279,2,3,""),(1227,2237,2,3,""),(1283,2210,2,3,""),(1395,2160,2,3,""),
  (1460,2150,2,3,""),(1510,2132,2,3,""),(1567,2097,2,3,""),(1632,2087,3,3,"on the x=150 gridline"),(1688,2071,2,3,""),
  (1865,2045,2,3,""),(2040,2045,2,3,""),(2210,2060,6,4,"symbol on the right frame (x about 250); doubles as legend key"),
 ]),
 "n1468": ("circle", [
  (820,2712,2,2,"first point; open circle"),(883,2631,2,2,""),(942,2562,2,2,""),(1000,2520,2,2,""),(1112,2462,2,2,""),
  (1170,2443,2,2,""),(1225,2422,2,2,""),(1287,2395,2,2,""),(1357,2368,3,2,"touches the x=100 gridline"),(1398,2352,2,2,""),
  (1460,2327,2,2,""),(1512,2308,2,2,""),(1687,2282,2,2,""),(1742,2283,2,2,""),(1807,2292,2,2,""),
  (1865,2305,2,2,"last marker; the drawn line ends here"),
 ]),
 "n734": ("circle", [
  (817,2750,3,3,"filled dot; all n734 markers are filled dots on a solid line"),(868,2723,3,3,"filled dot"),(938,2691,3,3,"filled dot"),
  (997,2671,3,3,"filled dot"),(1051,2655,3,3,"filled dot; on the x=50 gridline"),(1112,2638,3,3,"filled dot"),(1171,2617,3,3,"filled dot"),
  (1224,2599,3,3,"filled dot"),(1282,2588,3,3,"filled dot"),(1340,2572,3,3,"filled dot; on the x=100 gridline"),(1397,2561,3,3,"filled dot"),
  (1453,2555,3,4,"filled dot; merged with the 1000 gridline"),(1518,2552,3,4,"filled dot; merged with the 1000 gridline"),
  (1571,2552,3,4,"filled dot; merged with the 1000 gridline"),(1681,2548,3,4,"filled dot; merged with the 1000 gridline"),
  (1742,2530,4,4,"filled dot; small bump above the line, less distinct than the others"),(1806,2527,3,3,"filled dot"),
  (1860,2527,3,3,"filled dot"),(1918,2524,3,3,"filled dot; on the x=200 gridline"),(1975,2529,3,3,"filled dot"),
  (2032,2529,3,3,"filled dot"),(2096,2525,3,3,"filled dot"),(2159,2526,3,3,"filled dot"),
  (2218,2526,6,3,"filled dot on the right frame (x about 251); doubles as legend key"),
 ]),
}
VGRID = [755, 1047, 1337, 1627, 1918, 2211]   # approximate u of vertical gridlines/frame, upper panel
HGRID = [1086, 1377, 1668, 1962, 2254, 2543, 2834]


def runs(u, v0, v1, halfwidth=1):
    col = img[v0:v1, u - halfwidth:u + halfwidth + 1].all(axis=1)
    out, start = [], None
    for i, d in enumerate(col):
        if d and start is None:
            start = i
        if not d and start is not None:
            out.append((v0 + (start + i - 1) / 2, i - start))
            start = None
    if start is not None:
        out.append((v0 + (start + len(col) - 1) / 2, len(col) - start))
    return out


def interp_v(markers, u):
    us = [m[0] for m in markers]
    vs = [m[1] for m in markers]
    return float(np.interp(u, us, vs))


def near_any(u, lst, d):
    return any(abs(u - x) <= d for x in lst)


def bare_gridline(c, t):
    """A thin run (<= 8 px) centred on a horizontal gridline is the gridline itself, not the
    curve (the drawn curves are 9 to 11 px thick); such a run is never a trace sample."""
    return near_any(c, HGRID, 3) and t <= 8


def chord_slope(markers, u):
    us = [m[0] for m in markers]
    vs = [m[1] for m in markers]
    for i in range(len(us) - 1):
        if us[i] <= u <= us[i + 1] and us[i + 1] != us[i]:
            return (vs[i + 1] - vs[i]) / (us[i + 1] - us[i])
    return 0.0


def tol_at(markers, u):
    # the drawn curve bows away from the marker-to-marker chord where it is steep
    return 14 + 10 * abs(chord_slope(markers, u))


def trace_series(markers, u_start, u_end, step=20):
    mus = [m[0] for m in markers]
    samples = []
    u = u_start
    while u <= u_end:
        found = None
        for shift in (0, 3, -3, 6, -6, 9, -9, 12, -12, 15):
            uu = u + shift
            if uu < u_start or uu > u_end or near_any(uu, VGRID, 7) or near_any(uu, mus, 11):
                continue
            pv = interp_v(markers, uu)
            tol = tol_at(markers, uu)
            cands = [(abs(c - pv), c, t, uu) for c, t in runs(uu, int(pv) - 60, int(pv) + 60) if abs(c - pv) <= tol and t <= 30 and not bare_gridline(c, t)]
            if cands:
                found = min(cands)
                break
        if found:
            d, c, t, uu = found
            note = ""
            vb = max(2, t / 2)
            if t > 16:
                note = "thick run: curve merged with a gridline or another curve"
                vb = t / 2
            elif near_any(c, HGRID, 6):
                note = "on a horizontal gridline"
                vb = max(vb, 4)
            samples.append((uu, c, 1, vb, note))
        u += step
    return samples


def row_runs(v, u0, u1, halfwidth=1):
    row = img[v - halfwidth:v + halfwidth + 1, u0:u1].all(axis=0)
    out, start = [], None
    for i, d in enumerate(row):
        if d and start is None:
            start = i
        if not d and start is not None:
            out.append((u0 + (start + i - 1) / 2, i - start))
            start = None
    if start is not None:
        out.append((u0 + (start + len(row) - 1) / 2, len(row) - start))
    return out


def row_trace(markers, v_top, v_bottom, step=25, tol=12):
    """Samples a near-vertical segment by rows: for each v, the horizontal dark run nearest the
    chord between the two markers bracketing that v."""
    (u0, v0), (u1, v1) = markers
    out = []
    for v in range(v_bottom, v_top - 1, -step):
        pu = u0 + (u1 - u0) * (v - v0) / (v1 - v0)
        cands = [(abs(c - pu), c, t) for c, t in row_runs(v, int(pu) - 40, int(pu) + 40) if abs(c - pu) <= tol and t <= 20]
        if cands:
            d, c, t = min(cands)
            out.append((c, v, max(2, t / 2), 1, "row sample on the near-vertical start of the curve; u bound is half the run width"))
    return out


def dense_line(markers, u_start, u_end):
    pts = []
    mus = [m[0] for m in markers]
    for uu in range(u_start, u_end + 1, 2):
        if near_any(uu, VGRID, 7) or near_any(uu, mus, 11):
            continue
        pv = interp_v(markers, uu)
        tol = tol_at(markers, uu)
        cands = [(abs(c - pv), c, t) for c, t in runs(uu, int(pv) - 60, int(pv) + 60) if abs(c - pv) <= tol and t <= 16 and not bare_gridline(c, t)]
        if cands:
            b = min(cands)
            pts.append((uu, b[1], b[2]))
    return pts


rows = []


def add(panel, sid, kind, seq, u, v, ub, vb, sym, note):
    rows.append([FIG, panel, sid, kind, seq, u, v, ub, vb, sym, note])


TRACE_RANGE = {"n4400": (812, 2208), "n3660": (818, 2208), "n2995": (818, 2208), "n2200": (812, 2208),
               "n1468": (812, 1868), "n734": (812, 2208)}
ROWSEG = {"n4400": ((0, 1), 2330, 2470), "n3660": ((0, 1), 2350, 2475)}
FIRST = {"n4400": (812, 2525, "drawn line starts below the first marker cluster, near 1150 psf"),
         "n3660": (818, 2520, "drawn line starts in the first marker cluster, shared ink with n4400"),
         "n2995": (820, 2535, "drawn line starts at the first square"),
         "n2200": (814, 2600, "drawn line starts at the first triangle"),
         "n1468": (816, 2715, "drawn line starts at the first circle"),
         "n734": (812, 2753, "solid line starts at the first dot")}
for sid, (sym, mk) in P1.items():
    for i, (u, v, ub, vb, note) in enumerate(mk, 1):
        add(1, sid, "marker", i, u, v, ub, vb, sym, note)
    u0, u1 = TRACE_RANGE[sid]
    tr = []
    if sid in ROWSEG:
        (ma, mb), vtop, vbot = ROWSEG[sid]
        tr += row_trace((mk[ma][:2], mk[mb][:2]), vtop, vbot)
    tr += trace_series(mk, u0 + 10, u1)
    for i, (u, v, ub, vb, note) in enumerate(tr, 1):
        add(1, sid, "trace", i, u, v, ub, vb, "", note)
    dl = dense_line(mk, u0, u1)
    fu, fv, fnote = FIRST[sid]
    add(1, sid, "feature", 1, fu, fv, 4, 5, "", "first point of the drawn line; " + fnote)
    pk = min(dl, key=lambda p: p[1])
    plat = [p for p in dl if p[1] <= pk[1] + 3]
    add(1, sid, "feature", 2, pk[0], pk[1], max(4, (plat[-1][0] - plat[0][0]) / 2), max(3, pk[2] / 2), "",
        f"peak of the drawn line (plateau within 3 px from u={plat[0][0]} to u={plat[-1][0]}); u bound is half the plateau width")
    last = dl[-1]
    add(1, sid, "feature", 3, last[0], last[1], 4, max(3, last[2] / 2), "",
        "last sampled point of the drawn line" + (" (line ends at the last circle)" if sid == "n1468" else " (line runs to the right frame)"))

HDR = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with open("out/FC-2B/points-p1.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(HDR)
    w.writerows(rows)
print("p1 rows", len(rows))

# ---- lower panel markers ----
STACK = ("stack of symbols merged at this displacement; identity assigned by vertical order "
         "(dot, circle, triangle, square, x, asterisk from the top), shape not resolvable")
P2 = [
 (817, {"n1468": (3277, 4, "only symbol in this column (ring shape); blob wider than one ring, a second symbol (dot of n734?) may be merged at its right")}),
 (871, {"n734": (3276, 6, STACK), "n1468": (3285, 6, STACK), "n2200": (3295, 5, STACK), "n2995": (3305, 5, STACK), "n4400": (3316, 5, STACK + "; lowest symbol has asterisk-like legs; x not found")}),
 (930, {"n734": (3279, 6, STACK), "n1468": (3288, 6, STACK), "n2200": (3297, 5, STACK), "n2995": (3305, 5, STACK), "n4400": (3317, 5, STACK + "; x not found")}),
 (985, {"n734": (3281, 6, STACK), "n1468": (3290, 6, STACK), "n2200": (3302, 5, STACK), "n2995": (3311, 5, STACK), "n4400": (3321, 5, STACK + "; x not found")}),
 (1042, {"n734": (3281, 6, STACK + "; on the x=50 gridline"), "n1468": (3289, 6, STACK), "n2200": (3302, 5, STACK), "n2995": (3312, 5, STACK), "n4400": (3321, 5, STACK + "; x not found")}),
 (1104, {"n734": (3283, 6, STACK), "n1468": (3291, 6, STACK), "n2200": (3306, 5, STACK), "n2995": (3316, 5, STACK), "n4400": (3325, 5, STACK + "; x not found")}),
 (1162, {"n734": (3280, 6, STACK), "n1468": (3290, 6, STACK), "n2200": (3303, 5, STACK), "n2995": (3313, 5, STACK), "n4400": (3326, 5, STACK + "; x not found")}),
 (1220, {"n734": (3275, 5, STACK), "n1468": (3287, 5, STACK + "; hole visible"), "n2200": (3305, 5, STACK), "n2995": (3316, 5, STACK), "n3660": (3326, 6, STACK), "n4400": (3340, 5, STACK)}),
 (1276, {"n734": (3276, 5, STACK), "n1468": (3287, 5, STACK), "n2200": (3300, 6, STACK), "n2995": (3316, 5, STACK), "n3660": (3326, 6, STACK), "n4400": (3341, 5, STACK)}),
 (1334, {"n734": (3264, 5, "filled blob above the zero line, merged with it and with the x=100 gridline"), "n1468": (3278, 6, STACK), "n2200": (3287, 6, STACK), "n2995": (3306, 6, STACK), "n3660": (3327, 6, STACK), "n4400": (3339, 5, STACK)}),
 (1390, {"n734": (3261, 4, "filled dot straddling the zero line"), "n1468": (3278, 4, "ring with hole, below the zero line"), "n2200": (3298, 5, "triangle, apex at 3289"), "n2995": (3315, 5, "square with hole"), "n3660": (3325, 6, "not seen separately; merged between square and asterisk"), "n4400": (3337, 4, "asterisk at the bottom of the stack")}),
 (1450, {"n1468": (3275, 4, "ring just below the zero line; dot of n734 not found (under the ring or on the zero line)"), "n2200": (3295, 5, "triangle, apex at 3286"), "n2995": (3312, 5, "square with hole"), "n3660": (3325, 6, "not seen separately; merged between square and asterisk"), "n4400": (3335, 4, "asterisk")}),
 (1507, {"n734": (3255, 4, "filled dot above the zero line"), "n1468": (3269, 5, "on the zero line, merged with it"), "n2200": (3291, 5, "triangle, apex at 3282"), "n2995": (3309, 5, "square with hole"), "n3660": (3321, 6, "not seen separately; merged between square and asterisk"), "n4400": (3335, 4, "asterisk")}),
 (1566, {"n2200": (3288, 5, "triangle, apex at 3277; dot and circle of this column not found (zero line looks clean)"), "n2995": (3308, 5, "square with hole"), "n3660": (3321, 6, "not seen separately; merged between square and asterisk"), "n4400": (3334, 4, "asterisk")}),
 (1626, {"n734": (3241, 3, "filled dot; on the x=150 gridline"), "n1468": (3263, 5, "ring merged with the zero line and the x=150 gridline"), "n2200": (3285, 5, "triangle"), "n2995": (3297, 5, "square"), "n3660": (3309, 5, "x"), "n4400": (3333, 4, "asterisk")}),
 (1684, {"n1468": (3259, 4, "ring resting on the zero line; dot of n734 not found"), "n2200": (3283, 4, "triangle, apex at 3272"), "n2995": (3304, 5, "square"), "n3660": (3320, 6, "x, merged with the square above and the asterisk below"), "n4400": (3337, 4, "asterisk")}),
 (1740, {"n734": (3230, 3, "filled dot, clean"), "n1468": (3256, 3, "ring, clean"), "n2200": (3284, 4, "triangle, apex at 3274"), "n2995": (3303, 5, "square"), "n3660": (3319, 5, "x"), "n4400": (3339, 4, "asterisk")}),
 (1801, {"n1468": (3251, 3, "ring, clean; dot of n734 not found in this column"), "n2200": (3283, 4, "triangle, apex at 3272"), "n2995": (3302, 5, "square"), "n3660": (3319, 5, "x"), "n4400": (3337, 4, "asterisk")}),
 (1858, {"n734": (3213, 3, "filled dot, clean"), "n1468": (3241, 3, "ring, clean"), "n2200": (3283, 4, "triangle, apex at 3272"), "n2995": (3297, 5, "square"), "n3660": (3312, 5, "x"), "n4400": (3337, 4, "asterisk")}),
 (1912, {"n1468": (3234, 3, "ring on the x=200 gridline; dot of n734 not found"), "n2200": (3268, 6, "triangle merged with the zero line and the x=200 gridline, apex at 3257"), "n2995": (3291, 5, "square with hole"), "n3660": (3310, 5, "x"), "n4400": (3336, 4, "asterisk")}),
 (1975, {"n2200": (3260, 4, "triangle sitting on the zero line, apex 3251; dot and circle of this column not found"), "n2995": (3287, 3, "square, clean"), "n3660": (3307, 3, "x, clean"), "n4400": (3333, 3, "asterisk, clean")}),
 (2032, {"n734": (3200, 3, "filled dot, clean"), "n2200": (3259, 4, "triangle sitting on the zero line, apex 3249; circle not found"), "n2995": (3287, 3, "square, clean"), "n3660": (3305, 3, "x, clean"), "n4400": (3330, 3, "asterisk")}),
 (2091, {"n2200": (3258, 4, "triangle sitting on the zero line, apex 3247; dot and circle not found"), "n2995": (3281, 3, "square, clean"), "n3660": (3304, 3, "x, clean"), "n4400": (3327, 3, "asterisk")}),
 (2147, {"n734": (3188, 3, "filled dot, clean"), "n2200": (3257, 4, "triangle sitting on the zero line, apex 3246; circle not found"), "n2995": (3284, 3, "square, clean"), "n3660": (3305, 3, "x, clean"), "n4400": (3328, 3, "asterisk")}),
 (2205, {"n2200": (3256, 4, "triangle at the right frame, apex 3243; dot and circle not found"), "n2995": (3282, 4, "square overlapping the right frame"), "n3660": (3302, 4, "x overlapping the right frame"), "n4400": (3327, 4, "asterisk overlapping the right frame")}),
]
UOVR = {(1740, "n1468"): 1744, (1858, "n1468"): 1856, (1858, "n2995"): 1860, (1858, "n3660"): 1861, (1858, "n4400"): 1861,
        (2032, "n2995"): 2034, (2032, "n3660"): 2034, (2032, "n4400"): 2036, (2091, "n3660"): 2093, (2091, "n4400"): 2093,
        (2147, "n734"): 2149, (2205, "n2995"): 2203, (2205, "n4400"): 2206, (1334, "n734"): 1331, (1390, "n734"): 1389,
        (1507, "n734"): 1505, (1507, "n1468"): 1505, (1740, "n734"): 1738, (1912, "n1468"): 1913, (1626, "n2200"): 1625,
        (1626, "n2995"): 1625, (1626, "n4400"): 1625}
SYM = {"n4400": "asterisk", "n3660": "x", "n2995": "square", "n2200": "triangle-up", "n1468": "circle", "n734": "circle"}
rows2 = []
seq = {s: 0 for s in SYM}
for u, d in P2:
    for sid in ["n734", "n1468", "n2200", "n2995", "n3660", "n4400"]:
        if sid not in d:
            continue
        v, vb, note = d[sid]
        uu = UOVR.get((u, sid), u)
        seq[sid] += 1
        if sid == "n734":
            note = "filled dot; " + note
        ub = 3 if vb <= 3 else 4
        if u == 2205:
            ub = 5
        rows2.append([FIG, 2, sid, "marker", seq[sid], uu, v, ub, vb, SYM[sid], note])
with open("out/FC-2B/points-p2.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(HDR)
    w.writerows(rows2)
print("p2 rows", len(rows2))
