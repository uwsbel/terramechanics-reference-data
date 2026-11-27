"""Claude reader helper (FA-18): assemble points-p1.csv from the readings below.

Every number in READINGS was read on the page (row runs, iso-percent runs, zoomed crops; see notes.md).
Pixel positions only: the values are computed afterwards by tools/calibrate_axes.py piecewise.

Conventions (page as scanned): grain size increases up the page (smaller v), percent finer increases
to the left (smaller u). At a fixed grain size the upper curve is the leftmost and the lower curve the
rightmost; at a fixed percent the upper curve is the lowest on the page (largest v) and the lower curve
the highest. The solid average lies between them.
"""
import csv, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import geom  # noqa: E402

WS = HERE.parents[3]
OUT = WS / "out/FA-18/points-p1.csv"
F0 = [l for l in geom.cal["vertical_lines"] if l["y_value"] == 0][0]
F100 = [l for l in geom.cal["vertical_lines"] if l["y_value"] == 100][0]


def f0(v):
    """u of the centre of the 0 percent frame line at row v"""
    return F0["u_at_v0"] + F0["slope_du_dv"] * v


def iso_p_u(p, v):
    c, k = geom.iso_p(p)
    return c + k * v


def g_k(k):
    return 0.02 * 10 ** (0.05 * k)


SER = ("upper", "average", "lower")
MERGED_LOW = "three curves run together along the 0 percent frame (touching, no white between); position from the band edges and the dash gaps (upper = leftmost, lower = next to the frame); bound widened"

# ---- low band, k = 12 .. 33: (v_sample, offset from the 0 percent frame centre, note) per series ----
# offsets in px (negative = left of the frame centre). A v different from the sample's row means the
# sample sat in a dash gap and moved to the nearest dash end (rule 7), or under a grid line it is read
# on the nearest visible ink.
LOW = {
    12: {"v": 3133.5, "upper": (3133.5, -15.5, "under a horizontal grid line (rows 3129-3133); read across it"),
         "average": (3133.5, -6.5, "solid next to the frame; interpolated from its edges at the double gaps of v 3056 and 3116"),
         "lower": (3133.5, -4.5, "lower dashed curve lies on the edge of the 0 percent frame line; hardly separable from it")},
    13: {"v": 3085.0, "upper": (3085.0, -18.0, ""), "average": (3085.0, -8.8, ""), "lower": (3085.0, -5.8, "lower dashed curve overlaps the frame line")},
    14: {"v": 3036.5, "upper": (3036.5, -20.5, "on the 0.1 mm grid line; read across it"),
         "average": (3036.5, -10.6, "on the 0.1 mm grid line; read across it"),
         "lower": (3036.5, -6.2, "on the 0.1 mm grid line; read across it; overlaps the frame line")},
    15: {"v": 2988.1, "upper": (2985.5, -20.5, "sample in a dash gap (v 2987-2999): moved to the nearest dash end"),
         "average": (2988.1, -12.0, "solid edges seen in the double gap at v 2990-2995"),
         "lower": (2988.1, -6.5, "")},
    16: {"v": 2939.6, "upper": (2940.0, -20.5, "first rows of a dash"),
         "average": (2939.6, -14.0, "solid edges seen in the double gap at v 2932-2938"),
         "lower": (2929.0, -7.5, "sample in a dash gap (v 2930-2944): moved to the nearest visible dash end")},
    17: {"v": 2891.2, "upper": (2891.2, -25.5, "upper's left edge coincides with the 2 percent minor line"),
         "average": (2891.2, -15.0, ""), "lower": (2891.2, -7.6, "")},
    18: {"v": 2842.8, "upper": (2842.8, -25.0, "upper's left edge coincides with the 2 percent minor line"),
         "average": (2842.8, -15.5, ""), "lower": (2842.8, -8.0, "")},
    19: {"v": 2794.3, "upper": (2794.0, -26.5, "dash ends under the #80 sieve line just below"),
         "average": (2794.3, -16.1, ""), "lower": (2794.3, -8.1, "")},
    20: {"v": 2745.9, "upper": (2754.0, -25.5, "sample on the 0.2 mm line and in a dash gap (v 2738-2752): moved to the nearest dash end"),
         "average": (2745.9, -17.5, "on the 0.2 mm grid line; solid edges visible in the double gap"),
         "lower": (2743.0, -8.5, "sample in a dash gap (v 2744-2758): moved to the nearest dash end")},
    21: {"v": 2697.8, "upper": (2697.8, -27.5, ""), "average": (2697.8, -17.9, ""), "lower": (2697.8, -8.9, "first rows of a dash")},
    22: {"v": 2649.7, "upper": (2649.7, -27.5, ""), "average": (2649.7, -18.1, ""), "lower": (2649.7, -8.9, "")},
    23: {"v": 2601.6, "upper": (2601.6, -29.5, ""), "average": (2601.6, -18.6, ""), "lower": (2601.6, -8.9, "")},
    24: {"v": 2553.5, "upper": (2550.5, -31.5, "sample in a dash gap (v 2552-2566): moved to the dash end"),
         "average": (2553.5, -19.5, ""), "lower": (2553.5, -9.5, "")},
    25: {"v": 2505.4, "upper": (2506.0, -30.0, "first rows of a dash"),
         "average": (2505.4, -20.3, "solid edges seen in the double gap at v 2498-2503"),
         "lower": (2514.0, -9.5, "sample in a dash gap (v 2496-2510): moved to the nearest dash end")},
    26: {"v": 2457.3, "upper": (2457.3, -31.5, "under a horizontal grid line; read across it"),
         "average": (2457.3, -20.7, "under a horizontal grid line; read across it"),
         "lower": (2457.3, -9.9, "under a horizontal grid line; read across it")},
    27: {"v": 2409.2, "upper": (2409.2, -31.5, ""), "average": (2409.2, -21.7, ""), "lower": (2409.2, -10.3, "")},
    28: {"v": 2361.0, "upper": (2357.0, -33.5, "sample under the 0.5 mm grid line where the dash ends: read on the nearest visible ink"),
         "average": (2361.0, -22.8, "on the 0.5 mm grid line; read across it"),
         "lower": (2361.0, -10.8, "on the 0.5 mm grid line; read across it")},
    29: {"v": 2312.6, "upper": (2303.5, -35.0, "sample in a dash gap (v 2305-2321): moved to the nearest dash end"),
         "average": (2312.6, -23.5, "solid edges seen in the double gap at v 2313-2318"),
         "lower": (2311.0, -11.5, "sample in a dash gap (v 2312-2321): moved to the dash end")},
    30: {"v": 2264.2, "upper": (2264.2, -34.5, ""), "average": (2264.2, -24.5, ""),
         "lower": (2265.0, -13.5, "sample in a dash gap (v 2250-2264): moved to the dash end; lower is clear of the frame here")},
    31: {"v": 2215.7, "upper": (2215.7, -35.5, ""), "average": (2215.7, -24.9, ""), "lower": (2215.7, -13.9, "lower clear of the frame (white between)")},
    32: {"v": 2167.3, "upper": (2167.3, -38.0, ""), "average": (2167.3, -26.7, ""), "lower": (2167.3, -14.9, "lower clear of the frame (white between)")},
    33: {"v": 2118.8, "upper": (2118.8, -43.5, "end of a dash"), "average": (2118.8, -29.6, ""), "lower": (2118.8, -17.0, "lower clear of the frame (white between)")},
}

# ---- k = 34 .. 39: the three curves are distinct strands (pixel u, v read directly) ----
SEP = {
    34: {"upper": (2015.0, 2079.0, 4.5, "sample on the 1.0 mm line and in a dash gap: moved to the nearest dash end"),
         "average": (2031.0, 2070.4, 5.5, "on the 1.0 mm grid line; read across it (average and lower touch here)"),
         "lower": (2043.8, 2070.4, 5.5, "on the 1.0 mm grid line; read across it (average and lower touch here)")},
    35: {"upper": (1999.3, 2022.6, 4.5, ""), "average": (2019.8, 2022.2, 4.5, ""), "lower": (2036.6, 2021.9, 4.5, "")},
    36: {"upper": (1971.5, 1974.5, 4.5, "right edge under the 6 percent minor line"), "average": (1996.5, 1974.0, 4.5, ""), "lower": (2017.0, 1973.8, 4.5, "")},
    37: {"upper": (1929.7, 1926.6, 5.5, "under the 1.4 mm minor line; read across it"),
         "average": (1953.2, 1926.0, 5.5, "under the 1.4 mm minor line; read across it"),
         "lower": (1976.6, 1925.5, 5.5, "under the 1.4 mm minor line; read across it")},
    38: {"upper": (1880.5, 1880.5, 5.5, "right edge under the 12 percent line"), "average": (1897.0, 1879.0, 4.5, ""),
         "lower": (1920.0, 1876.5, 5.5, "left edge under the 10 percent line")},
    39: {"upper": (1786.0, 1833.4, 5.0, ""), "average": (1816.0, 1831.5, 5.0, "right edge under the 16 percent line"),
         "lower": (1845.0, 1830.4, 5.0, "right edge under the 14 percent line")},
}
# strand centres on the iso-percent line p = 19.5 (runs 1790-1801, 1808-1816, 1820-1831)
P195 = {"lower": 1795.5, "average": 1812.0, "upper": 1825.5}

# ---- steep part: band edges along iso-percent lines (top T = lower curve's top edge, bottom B = upper
# curve's bottom edge), knots through edges that are visible (not in a dash gap, not under a grid line);
# between knots the edge is interpolated (under the 2.5 mm line and the #8 sieve line, p 62 to 76) ----
T_KN = [(20.5, 1772), (22.0, 1774), (23.5, 1769), (24.5, 1765), (26.5, 1757), (27.5, 1754), (28.5, 1751), (30.5, 1745),
        (32.5, 1741), (35.5, 1735), (38.5, 1727), (43.5, 1718), (46.5, 1711), (51.0, 1711.5), (53.5, 1708), (57.5, 1706),
        (61.5, 1705), (76.5, 1697), (81.5, 1696), (84.5, 1693), (86.0, 1691), (89.0, 1687.5), (91.0, 1682), (92.5, 1676),
        (93.5, 1670), (95.0, 1661)]
B_KN = [(20.5, 1819), (21.5, 1819), (22.5, 1814), (23.5, 1810), (25.5, 1801), (26.5, 1797), (31.5, 1777), (33.5, 1771),
        (35.0, 1767.5), (36.5, 1767), (38.5, 1761), (39.5, 1759), (41.5, 1756), (43.0, 1752.5), (46.0, 1750), (48.0, 1745),
        (51.0, 1740.5), (54.5, 1737), (60.0, 1736), (76.5, 1725), (80.5, 1725), (81.5, 1723), (84.0, 1716.5), (85.5, 1714),
        (86.5, 1711), (90.5, 1702), (91.5, 1696), (92.5, 1695), (93.5, 1686), (94.5, 1681), (95.5, 1678)]
HALF_T = 4.5   # half the line thickness (curves about 9 px thick where they are separate)


def steep_v(series, p):
    T = float(np.interp(p, *zip(*T_KN)))
    B = float(np.interp(p, *zip(*B_KN)))
    return {"lower": T + HALF_T, "upper": B - HALF_T, "average": 0.5 * (T + B)}[series]


# dash gaps of the upper (bottom edge) and the lower (top edge) found by comparing the edges on the iso-percent
# lines at p and p +- 0.5 with the envelope (a visible edge 7 px or more inside it): the sample moves to the
# nearest visible dash end (rule 7)
MOVE = {("upper", 40.0): 39.5, ("upper", 45.0): 45.5, ("upper", 50.0): 50.5, ("upper", 65.0): 64.5, ("upper", 70.0): 69.5,
        ("lower", 25.0): 24.5, ("lower", 30.0): 30.5, ("lower", 50.0): 50.5, ("lower", 80.0): 80.5}
KMOVE = {("upper", 42): 86.5}


def steep_hidden(p):
    return 61.5 < p < 76.5 or 28.0 < p < 31.0 or 39.0 < p < 43.5


# ---- coarse end: the three curves are one line (band no wider than one or two line widths) ----
COARSE = [  # (k or None, u, v, u_bound, v_bound, note)
    (43, 655.0, 1659.4, 6.0, 4.5, "three curves merged into one line (run 15 px at about 45 degrees); same point for all three"),
    (44, 619.0, 1610.9, 6.0, 4.5, "three curves merged into one line, clear of the frame; same point for all three"),
    (45, 606.0, 1561.5, 10.0, 4.5, "three curves merged with each other and along the 100 percent frame (ink 590-614); same point for all three"),
    (46, 604.5, 1512.0, 9.0, 4.5, "on the 4.0 mm grid line; three curves merged along the 100 percent frame (ink 590-611); same point for all three"),
]
LAST = (602.0, 1466.0, 5.0, 5.0, "last visible curve ink, beside the 100 percent frame; the line continues hidden in the frame line up to the dot at v 1442; three curves merged; same point for all three")
FIRST = {
    "upper": (f0(3162.0) - 15.5, 3162.0, 5.0, 5.0, "fine end of the last dash: ink visible to v 3160, then hidden under the #200 sieve line (v 3161-3168), nothing below"),
    "average": (f0(3175.0) - 6.5, 3175.0, 4.0, 4.0, "fine end: ink beside the frame at v 3170-3176, taken as the solid (it could be the lower dashed curve ending)"),
    "lower": (f0(3172.0) - 4.5, 3172.0, 5.0, 8.0, "fine end: the lower dashed curve merges into the 0 percent frame line; its end is not separable from the frame"),
}
MARKER = (592.0, 1442.0, 3.0, 3.0, "filled dot centred on the 100 percent frame at the #4 sieve line (about 4.7 mm), where the three curves end; one symbol filed under average only")


def polyline(series):
    pts = []   # (u, v)
    pts.append(FIRST[series][:2])
    for k in sorted(LOW):
        v, off, _ = LOW[k][series]
        pts.append((f0(v) + off, v))
    for k in sorted(SEP):
        u, v, _, _ = SEP[k][series]
        pts.append((u, v))
    v = P195[series]
    pts.append((iso_p_u(19.5, v), v))
    for p in np.arange(21.5, 95.01, 0.5):
        v = steep_v(series, p)
        pts.append((iso_p_u(p, v), v))
    for k, u, v, *_ in COARSE:
        pts.append((u, v))
    pts.append(LAST[:2])
    return pts


def cross(pts, side):
    """first crossing of the polyline with a line given by side(u, v) changing sign; returns (u, v)"""
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        s0, s1 = side(u0, v0), side(u1, v1)
        if s0 == 0:
            return u0, v0
        if s0 * s1 < 0:
            t = s0 / (s0 - s1)
            return u0 + t * (u1 - u0), v0 + t * (v1 - v0)
    return None


def pct(u, v):
    return geom.value(u, v)[1]


rows = []
for s in SER:
    seq = 0
    trace = []

    def add(kind, u, v, ub, vb, note, sym=""):
        trace.append((kind, u, v, ub, vb, sym, note))

    u, v, ub, vb, note = FIRST[s]
    add("trace", u, v, ub, vb, "first point; " + note)
    for k in range(12, 34):
        v, off, note = LOW[k][s]
        add("trace", f0(v) + off, v, 5.0, 4.5, f"k={k} g={g_k(k):.4f}; " + MERGED_LOW + ("; " + note if note else ""))
    for k in range(34, 40):
        u, v, ub, note = SEP[k][s]
        add("trace", u, v, ub, 4.5, f"k={k} g={g_k(k):.4f}; three distinct strands" + ("; " + note if note else ""))
    pts = polyline(s)
    steep_pts = [(iso_p_u(p, steep_v(s, p)), steep_v(s, p)) for p in np.arange(21.5, 95.01, 0.25)]
    # the 0.05-decade samples k = 40, 41, 42 on the steep part (from p = 19.5 on)
    seg = [(iso_p_u(19.5, P195[s]), P195[s])] + steep_pts
    ksamp = {}
    for k in (40, 41, 42):
        c, kk = geom.iso_g(g_k(k))
        hit = cross(seg, lambda u, v: v - (c + kk * u))
        ksamp[k] = hit
    pk = {k: pct(*ksamp[k]) for k in ksamp}
    pk[39] = pct(*SEP[39][s][:2])
    pk[43] = pct(*COARSE[0][1:3])
    steep_note = "three curves run together in the steep part (band 20 to 35 px high); upper = bottom edge minus half a line, lower = top edge plus half a line, average = middle of the band; bound widened"
    for k in (40, 41, 42):
        u, v = ksamp[k]
        p = pct(u, v)
        hid = steep_hidden(p) or k == 40
        extra = ""
        if k == 40:
            extra = "; the 2.0 mm crossing is under the 2.0 mm grid line: read across it"
        if (s, k) in KMOVE:   # the crossing falls in a dash gap of this curve: nearest dash end (rule 7)
            pm = KMOVE[(s, k)]
            v = steep_v(s, pm); u = iso_p_u(pm, v)
            extra += f"; the crossing (p {p:.1f}) falls in a dash gap: moved to the nearest dash end at p {pm}"
        add("trace", u, v, 4.5, 7.0 if hid else 6.0, f"k={k} g={g_k(k):.4f}; " + steep_note + extra)
        # extra samples at every 5 percent between this sample and the next where the rise exceeds 10
        nxt = pk[k + 1]
        if nxt - p > 10:
            for m in range(int(math.floor(p / 5)) + 1, int(math.ceil(nxt / 5))):
                q = 5.0 * m
                if q <= p or q >= nxt:
                    continue
                if q <= 95.0:
                    vq = steep_v(s, q) if q >= 21.5 else None
                    if vq is None:
                        continue
                    mv = ""
                    if (s, q) in MOVE:   # in a dash gap of this curve (or on a grid line next to one): rule 7
                        qm = MOVE[(s, q)]
                        vq = steep_v(s, qm)
                        mv = f"; {q:.0f} percent falls in a dash gap (or on a grid line next to one): moved to the nearest visible dash end at p {qm}"
                        q = qm
                    uq = iso_p_u(q, vq)
                    add("trace", uq, vq, 4.5, 7.0 if steep_hidden(q) else 6.0, f"extra sample at {5.0 * m:.0f} percent; " + steep_note + mv)
    # check the rise between k=39 and k=40
    for k, u, v, ub, vb, note in COARSE:
        add("trace", u, v, ub, vb, f"k={k} g={g_k(k):.4f}; " + note)
    u, v, ub, vb, note = LAST
    add("trace", u, v, ub, vb, "last point; " + note)
    for i, (kind, u, v, ub, vb, sym, note) in enumerate(trace, 1):
        rows.append(dict(figure_id="FA-18", panel=1, series_id=s, point_kind=kind, sequence=i, pixel_u=round(u, 1),
                         pixel_v=round(v, 1), u_bound_px=ub, v_bound_px=vb, symbol=sym, note=note))
    # features: first point, knee at the onset of the steep rise (the 2.0 mm crossing), knee where the curve
    # rolls over toward 100 percent (p = 95 on the band), last point (also the peak)
    feats = [
        (FIRST[s][0], FIRST[s][1], FIRST[s][2], FIRST[s][3], "first point (fine end)"),
        (ksamp[40][0], ksamp[40][1], 6.0, 8.0, "knee: onset of the steep rise at about 2.0 mm (slope changes from about 45 degrees to nearly horizontal on the page); under the 2.0 mm grid line"),
        (iso_p_u(95.0, steep_v(s, 95.0)), steep_v(s, 95.0), 6.0, 8.0, "knee: rollover toward 100 percent at about 2.7 mm; three curves merged here"),
        (LAST[0], LAST[1], LAST[2], LAST[3], "last point (coarse end); also the peak (the trace's maximum percent finer, along the 100 percent frame); three curves merged"),
    ]
    for i, (u, v, ub, vb, note) in enumerate(feats, 1):
        rows.append(dict(figure_id="FA-18", panel=1, series_id=s, point_kind="feature", sequence=i, pixel_u=round(u, 1),
                         pixel_v=round(v, 1), u_bound_px=ub, v_bound_px=vb, symbol="", note=note))
    print(s, "percent at k39..43:", {k: round(pk[k], 1) for k in sorted(pk)})

u, v, ub, vb, note = MARKER
rows.append(dict(figure_id="FA-18", panel=1, series_id="average", point_kind="marker", sequence=1, pixel_u=u, pixel_v=v,
                 u_bound_px=ub, v_bound_px=vb, symbol="circle", note=note))
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"wrote {OUT}: {len(rows)} rows")
