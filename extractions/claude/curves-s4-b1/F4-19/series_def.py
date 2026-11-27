"""The reader's guide for each trace of Figure 4-19 (Claude, batch curves-s4-b1), in drawing order.

A piece is either an ink-following segment of guides.json ("seg", optionally limited to a range of u or v,
and reversed when it was followed backwards), sampled with snapping to the ink center ("auto"), or a list
of waypoints read by eye from zoomed crops and row/column scans ("pts", mode "manual"), used where the
trace runs together with another trace, a grid line or the frame, so that the ink cannot be split by
machine. A manual piece carries its own bounds (pixels) and the note that explains them.
"""

BUNDLE1 = ("rising branch inside the bundle formed by the left frame and the rising branches of all three runs "
           "(Fig. 4-19 panel 1, first 3 ms); this run's ink cannot be separated there; position read from the "
           "bundle's extent, bound covers its share of the bundle")

SERIES = {
    # ------------------------------------------------------------------ panel 1, force
    (1, "run4"): {"style": "solid", "nominal": 12, "pieces": [
        {"pts": [[741.5, 1987], [743.5, 1970], [744.5, 1955], [744.5, 1940], [746.5, 1925], [747.5, 1910]],
         "ub": 7, "vb": 5, "note": BUNDLE1 + "; center taken 6 px left of the bundle's right edge, which is this run's own edge"},
        {"pts": [[747.5, 1895], [749.5, 1880], [751.5, 1865], [750.0, 1850], [750.0, 1835], [750.5, 1820], [752.5, 1805],
                 [752.5, 1790], [751.5, 1775], [754.5, 1760], [755.5, 1745], [756.0, 1730], [757.0, 1715], [758.0, 1700],
                 [759.0, 1690]],
         "ub": 6, "vb": 5, "note": "rising branch, steep, 3 px right of the frame-and-runs-10-12 bundle (dots of run 10 bridge the gap in places); "
                                     "center from row scans of the ink (half width 5 to 6 px)"},
        {"pts": [[760.0, 1679.5]], "ub": 6, "vb": 6, "note": "apex of the first force peak (top of the stroke at v 1673 plus half the line width)"},
        {"seg": "p1_r4_b_back", "reverse": True, "u": [766, 800]},
        {"seg": "p1_r4_b_fwd", "u": [800, 824]},
        {"pts": [[826, 1759.5], [832, 1767.5], [840, 1777.5], [846, 1783.5]], "ub": 6, "vb": 6,
         "note": "a hole in the ink at 834 to 840 px (v 1772 to 1776) splits the stroke; center from column scans of the full stroke"},
        {"seg": "p1_r4_b_fwd", "u": [848, 930]},
        {"pts": [[935, 1793.5], [945, 1788.5], [955, 1782]], "ub": 6, "vb": 8, "note": "crosses the long-dash trace of run 12; ink merged, bound widened"},
        {"seg": "p1_r4_c", "u": [962, 997]},
        {"pts": [[1005, 1755.5], [1015, 1751.5], [1025, 1747.5]], "ub": 6, "vb": 8, "note": "crosses the dotted trace of run 10; ink merged, bound widened"},
        {"seg": "p1_r4_d", "u": [1030, 1896]},
        {"pts": [[1900, 1906], [1908, 1910], [1916, 1913], [1924, 1918], [1932, 1921], [1940, 1924], [1948, 1927]],
         "ub": 5, "vb": 8, "note": "end of the steep fall, running into the band shared with runs 10 and 12 (all touching); center 6 px above the band's lower edge, bound widened"},
        {"pts": [[1956, 1928.5], [1964, 1929.5], [1980, 1930.5], [2000, 1930.5], [2012, 1929.5], [2020, 1927.5], [2032, 1925], [2048, 1922]],
         "ub": 4, "vb": 6, "note": "lowest of three touching traces (the dots of run 10 lie on it); center from its lower edge and the line width, bound widened"},
        {"pts": [[2064, 1917.5], [2080, 1911], [2096, 1906], [2112, 1902], [2124, 1897], [2136, 1891.5]],
         "ub": 6, "vb": 8, "note": "rises across the touching traces of runs 10 and 12; ink merged, bound widened"},
        {"seg": "p1_r4_tail", "u": [2148, 2312.5]},
    ]},
    (1, "run10"): {"style": "dotted", "nominal": 9, "pieces": [
        {"pts": [[743, 1987], [743, 1950], [743, 1900], [743, 1850], [743, 1800], [744, 1750], [747, 1700], [748, 1650],
                 [749, 1600], [750, 1540], [751, 1490]],
         "ub": 7, "vb": 5, "note": BUNDLE1 + "; dots of this run bridge the gap between the frame-and-run-12 ink and run 4"},
        {"seg": "p1_r10_rise", "v": [1300, 1466]},
        {"pts": [[772.5, 1295.5]], "ub": 9, "vb": 5, "note": "highest dot of the first force peak; the drawn apex lies in the gap to the next dot (790.5, 1312.5), bound widened to half that gap"},
        {"seg": "p1_r10_b", "v": [1305, 1562]},
        {"pts": [[893, 1582], [903, 1601], [912, 1620]], "ub": 7, "vb": 8, "note": "crosses the long-dash trace of run 12; dots merged with the dash, bound widened"},
        {"seg": "p1_r10_c", "u": [920, 998]},
        {"pts": [[1006, 1745], [1013, 1752]], "ub": 7, "vb": 8, "note": "crosses the solid trace of run 4; dot merged with it, bound widened"},
        {"seg": "p1_r10_d", "u": [1018, 1752]},
        {"seg": "p1_r10_e", "u": [1755, 1892]},
        {"pts": [[1905, 1913], [1920, 1915.5], [1940, 1917], [1960, 1917.5], [1990, 1917.5], [2010, 1916.5], [2031, 1914], [2048, 1911.5], [2065, 1908.5]],
         "ub": 5, "vb": 6, "note": "dots between the dash of run 12 above and run 4 below, all three touching; bound widened"},
        {"pts": [[2090, 1908], [2115, 1908], [2142, 1907.5]], "ub": 6, "vb": 8, "note": "tangle with run 12 and the rising run 4 (2068 to 2156 px); identity of the ink not certain, bound widened"},
        {"pts": [[2158, 1908.5], [2174, 1908.5], [2190, 1908.5], [2210, 1908.5], [2228, 1908.5], [2242, 1908.5], [2262, 1908.5],
                 [2278, 1908.5], [2294, 1908.5], [2310, 1908.5]],
         "ub": 5, "vb": 5, "note": "dots sitting on the dash of run 12 (touching); dot center from its top edge and the dot size"},
    ]},
    (1, "run12"): {"style": "long-dash", "nominal": 12, "pieces": [
        {"pts": [[737, 1987], [737, 1900], [737.5, 1800], [737.5, 1700], [738, 1600], [738, 1500], [738.5, 1400], [739, 1300], [739, 1268]],
         "ub": 6, "vb": 5, "note": BUNDLE1 + "; this run touches the frame's right edge (ink 726 to 743 px at 1280 to 1475 px)"},
        {"seg": "p1_r12_a", "v": [590, 1205]},
        {"pts": [[766, 582], [770, 570], [775, 556], [780, 570], [783, 586]], "ub": 6, "vb": 8,
         "note": "apex of the force peak: a short dash (768 to 781, 549 to 576 px) between the rising and falling dashes; center within the bound"},
        {"seg": "p1_r12_b", "v": [615, 1560]},
        {"pts": [[902, 1580], [907, 1600], [911, 1620], [914, 1640]], "ub": 7, "vb": 8, "note": "crosses the dotted trace of run 10; ink merged, bound widened"},
        {"seg": "p1_r12_c", "v": [1650, 1765]},
        {"pts": [[944, 1783], [948, 1797], [952, 1808]], "ub": 7, "vb": 8, "note": "crosses the solid trace of run 4; ink merged, bound widened"},
        {"seg": "p1_r12_d", "u": [954, 1872]},
        {"pts": [[1890, 1915], [1915, 1909], [1930, 1908.5], [1944, 1908.5], [1960, 1907], [1976, 1906.5], [1990, 1905.5], [2000, 1905],
                 [2012, 1904], [2030, 1904], [2048, 1903.5], [2068, 1903]],
         "ub": 5, "vb": 6, "gaps": [[1873, 1911]], "note": "dash lying on the dots of run 10 (touching), with run 4 below (a dash gap from 1873 to about 1911 px); bound widened"},
        {"pts": [[2100, 1906], [2134, 1915.5]], "ub": 6, "vb": 8, "gaps": [[2145, 2155]], "note": "tangle with run 10 and the rising run 4 (2068 to 2156 px); identity of the ink not certain, bound widened"},
        {"pts": [[2160, 1915.5], [2180, 1916.5], [2200, 1918.5], [2220, 1919], [2250, 1919.5], [2270, 1919], [2290, 1918.5], [2305, 1919], [2321, 1919]],
         "ub": 4, "vb": 6, "note": "dash with the dots of run 10 on top (touching); center of the bar measured between dots"},
    ]},
    # ------------------------------------------------------------------ panel 2, displacement
    (2, "run4"): {"style": "solid", "nominal": 12, "pieces": [
        {"pts": [[748, 3270], [756, 3262], [764, 3250], [771, 3238], [778, 3226], [785, 3214], [792, 3202], [798, 3190], [805, 3178],
                 [811, 3166], [818, 3154], [825, 3142], [833, 3130], [841, 3118], [849, 3106]],
         "ub": 11, "vb": 7, "note": "origin to about 8 ms: runs together with runs 10 and 12 in one bundle (dots of run 10 on either side); "
                                    "center of the bundle along a smooth line, bound covers the bundle"},
        {"seg": "p2_r4_back", "reverse": True, "v": [3020, 3100]},
        {"seg": "p2_r4", "u": [902, 1416]},
        {"seg": "p2_r4_b", "u": [1432, 2330]},
    ]},
    (2, "run10"): {"style": "dotted", "nominal": 9, "pieces": [
        {"pts": [[748, 3270], [756, 3262], [764, 3250], [771, 3238], [778, 3226], [785, 3214], [792, 3202], [798, 3190], [805, 3178],
                 [811, 3166], [818, 3154], [825, 3142], [833, 3130], [843, 3117], [856, 3104], [872, 3096]],
         "ub": 11, "vb": 7, "note": "origin to about 8 ms: dots run along the solid trace of run 4 (touching it on either side) in one bundle with run 12; "
                                    "position within the bundle not resolvable, bound covers the bundle"},
        {"seg": "p2_r10", "u": [880, 1712]},
    ]},
    (2, "run12"): {"style": "long-dash", "nominal": 12, "pieces": [
        {"seg": "p2_r12_back", "reverse": True},
        {"seg": "p2_r12", "u": [872, 2345]},
    ]},
}

# features read by eye (pixel, bounds, note); the automatic ones (local extremes on auto stretches) are added in sample.py
FEATURES = {
    (1, "run4"): [
        ("first", 741.5, 1987, 7, 5, "first: ink meets the bottom frame (0 lb) in the corner, merged with the frames and the rising branches of runs 10 and 12"),
        ("peak", 760.0, 1679.5, 6, 6, "peak: first force maximum (apex of the stroke)"),
        ("last", 2312.5, 1870.5, 6, 6, "last: ink ends under the vertical grid line labeled 140 (uniform-grid value 130 ms)"),
    ],
    (1, "run10"): [
        ("first", 743, 1987, 7, 5, "first: in the corner, inside the bundle of the frames and the other two runs; not separable"),
        ("peak", 772.5, 1295.5, 9, 5, "peak: first force maximum, highest dot; the drawn apex is in the gap to the next dot, bound widened"),
        ("last", 2310, 1908.5, 5, 5, "last: last dot, on the dash of run 12, under the grid line labeled 140"),
    ],
    (1, "run12"): [
        ("first", 737, 1987, 6, 5, "first: in the corner, inside the bundle of the frames and the other two runs; not separable"),
        ("peak", 775, 556, 6, 6, "peak: force maximum, apex dash"),
        ("last", 2321, 1919, 4, 6, "last: dash ends 4 px right of the grid line labeled 140, with the last dot of run 10 on it"),
    ],
    (2, "run4"): [
        ("first", 748, 3270, 6, 6, "first: origin, inside the bundle of all three runs and the frames"),
    ],
    (2, "run10"): [
        ("first", 748, 3270, 6, 6, "first: origin, inside the bundle of all three runs and the frames"),
    ],
    (2, "run12"): [],
}
