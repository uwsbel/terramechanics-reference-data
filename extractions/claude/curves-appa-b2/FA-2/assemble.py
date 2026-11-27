"""Assemble the FA-2 reading (points-p1.csv) from
  1. samples crossing the tracked stroke centres (build.py) where the three curves are apart
     (grain sizes 10^(0.05 k), k = 7 .. -1, and percent levels 30 .. 65), each checked on overlays,
     with the reader's corrections listed in OVERRIDE;
  2. the reader's readings where the curves run together (top end, shallow stretch u 840..1135, fine
     end along the 0 percent frame), from band edges and the order upper >= average >= lower (merged.py
     rule), listed in MANUAL with widened bounds;
  3. first point, last point and knee features.
Pixel coordinates refer to packet/p0007.png."""
import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as Bd  # noqa: E402
import fa2_tools as T  # noqa: E402

HALF = 5.0   # half the stroke thickness (10 px on this scan)

# ---- 1. tracked samples -------------------------------------------------------------------------
K_TRACKED = {"upper": range(6, -2, -1), "average": range(7, -2, -1), "lower": range(7, -2, -1)}
P_TRACKED = {"upper": [65, 60, 55, 50, 45, 40, 35], "average": [65, 60, 55, 50, 45, 40, 35, 30],
             "lower": [65, 60, 55, 50, 45, 40, 35, 30]}
# corrections after the overlay check: (series, kind, level) -> (u, v, ub, vb, note)
OVERRIDE = {
    ("upper", "k", 6): (1428.0, 1778.4, 5, 6, "sampling line on the 2.0 mm grid line; the upper curve runs along it and is hidden in it from u 1410 to 1450: centre from its exposed edges either side"),
    ("upper", "p", 50): (1423.5, 1777.0, 5, 6, "under the 2.0 mm grid line (hidden from u 1410 to 1450): centre from the exposed stroke either side"),
    ("upper", "p", 60): (1275.7, 1749.0, 5, 5, "stroke crossed by the 60 percent grid line; centre from the clean columns either side"),
    ("average", "p", 60): (1275.5, 1730.5, 5, 6, "on the 60 percent grid line, which hides the stroke here; centre from the clean columns either side"),
    ("lower", "p", 60): (1275.6, 1713.5, 5, 6, "stroke touches the dashed 2.36 mm sieve line above it: centre from its lower edge"),
    ("lower", "p", 55): (1348.5, 1720.5, 5, 5, "dash end (the level falls 1 px into the gap; moved to the dash end, rule 7)"),
    ("lower", "p", 50): (1425.0, 1733.5, 5, 5, "dash end (level in a dash gap, moved to the nearer end, rule 7)"),
    ("lower", "p", 30): (1722.0, 1805.4, 5, 5, "dash end (level in a dash gap, moved to the nearer end, rule 7)"),
    ("lower", "k", 5): (1780.0, 1825.0, 5, 5, "dash end (sample in a dash gap, moved to the nearer end, rule 7)"),
    ("lower", "k", 4): (1896.0, 1873.5, 5, 5, "dash end (sample in a dash gap, moved to the nearer end, rule 7)"),
    ("lower", "k", 0): (2118.5, 2068.5, 5, 5, "sampling line on the 1.0 mm grid line, in a dash gap that the grid line hides; moved to the first visible ink of the next dash below it"),
    ("upper", "k", 4): (1781.0, 1868.0, 5, 5, "dash end (sample in a dash gap, moved to the nearer end, rule 7)"),
}

# ---- 2. merged stretches (reader's readings) ------------------------------------------------------
TOP = "top end: the three curves run together along the 100 percent frame; position from the band edges and the order upper >= average >= lower, bound widened"
SHALLOW = "the three curves run together (u 840..1135); position from the band's top and bottom edges and the order upper >= average >= lower, bound widened"
FINE = "fine end: the three curves run together along the 0 percent frame; position from the band edges and the order upper >= average >= lower, bound widened"
# series -> list of (kind, level, u, v_or_None, ub, vb, note); v None means: on the sampling line of grain k
MANUAL = {
    "upper": [
        ("k", 13, 682.0, None, 7, 4, TOP + "; ink protrudes left of the frame (above 100 percent)"),
        ("k", 12, 690.0, None, 7, 5, TOP + "; on the 4.0 mm grid line"),
        ("k", 11, 691.0, None, 7, 4, TOP + "; the upper curve lies on the frame line here"),
        ("k", 10, 722.0, None, 7, 4, TOP),
        ("k", 9, 768.0, None, 9, 4, TOP),
        ("k", 8, 895.0, None, 5, 6, SHALLOW + "; at the start of a dash of the upper curve; nearly parallel to the sampling line"),
        ("p", 85, 912.7, 1690.0, 5, 8, SHALLOW),
        ("p", 80, 985.5, 1700.0, 5, 8, SHALLOW),
        ("p", 75, 1058.8, 1717.5, 5, 8, SHALLOW + "; lower edge on the dashed 2.36 mm sieve line"),
        ("p", 70, 1132.1, 1725.0, 5, 8, SHALLOW),
        ("k", 7, 1170.0, None, 5, 6, "stroke separating from the band, just before a dash end"),
    ],
    "average": [
        ("k", 13, 686.5, None, 9, 4, TOP + "; hidden between the other two"),
        ("k", 12, 695.0, None, 9, 5, TOP + "; hidden between the other two; on the 4.0 mm grid line"),
        ("k", 11, 708.5, None, 6, 4, "two strokes visible right of the frame (703-714 and 719-728); the average taken as the left one"),
        ("k", 10, 734.5, None, 9, 4, TOP + "; hidden between the other two"),
        ("k", 9, 781.0, None, 11, 4, TOP + "; hidden between the other two"),
        ("p", 90, 839.9, 1665.0, 5, 10, SHALLOW + "; hidden between the other two"),
        ("k", 8, 951.0, None, 5, 10, SHALLOW + "; hidden between the other two"),
        ("p", 85, 912.6, 1681.0, 5, 10, SHALLOW + "; hidden between the other two"),
        ("p", 80, 985.3, 1690.5, 5, 10, SHALLOW + "; hidden between the other two"),
        ("p", 75, 1058.6, 1702.0, 5, 8, SHALLOW),
        ("p", 70, 1131.9, 1709.0, 5, 8, SHALLOW),
    ],
    "lower": [
        ("k", 13, 689.0, None, 7, 4, TOP + "; no ink right of the frame, so the curve is under or left of it"),
        ("k", 12, 701.0, None, 8, 5, TOP + "; on the 4.0 mm grid line"),
        ("k", 11, 723.5, None, 5, 4, "two strokes visible right of the frame (703-714 and 719-728); the lower taken as the right one"),
        ("k", 10, 747.0, None, 7, 4, TOP),
        ("k", 9, 795.0, None, 7, 4, TOP),
        ("p", 90, 839.8, 1654.5, 5, 8, SHALLOW),
        ("p", 85, 912.5, 1672.0, 5, 8, SHALLOW),
        ("p", 80, 985.1, 1681.0, 5, 8, SHALLOW),
        ("k", 8, 1013.0, None, 5, 8, SHALLOW + "; nearly parallel to the sampling line"),
        ("p", 75, 1058.5, 1693.0, 5, 8, SHALLOW + "; upper edge may be hidden in the 2.5 mm grid line"),
        ("p", 70, 1131.6, 1696.0, 5, 8, SHALLOW),
    ],
}
# fine end, k = -2 .. -22: (upper u, average u, lower u) on the sampling line, with bounds; a tuple
# (u, v) is a dash end the sample moved to
FINE_ROWS = {
    -2: ((2110.0, 6), (2120.0, 6), (2134.5, 5)),
    -3: ((2118.0, 6), (2125.0, 7), (2138.5, 6)),
    -4: (((2127.5, 2264.0), 5), (2137.0, 5), (2140.0, 5)),
    -5: ((2126.0, 6), (2132.0, 6), ((2141.5, 2310.0), 5)),
    -6: ((2133.0, 6), (2135.0, 7), (2143.0, 7)),
    -7: ((2134.0, 6), (2139.0, 8), (2144.5, 6)),
    -8: ((2136.0, 6), (2140.0, 7), (2144.0, 6)),
    -9: ((2137.0, 6), (2142.0, 7), (2147.0, 6)),
    -10: ((2138.5, 6), (2138.5, 6), ((2147.0, 2542.0), 5)),
    -11: ((2139.0, 6), (2144.0, 7), (2149.5, 6)),
    -12: ((2143.0, 6), (2146.5, 6), (2150.0, 6)),
    -13: ((2145.0, 6), (2150.0, 8), (2156.0, 8)),
    -14: ((2145.5, 6), (2148.0, 7), (2151.0, 8)),
    -15: ((2147.0, 6), (2149.0, 7), (2151.0, 8)),
    -16: ((2151.0, 6), (2153.5, 7), (2156.0, 7)),
    -17: ((2152.0, 6), (2155.0, 7), (2158.0, 8)),
    -18: ((2155.0, 6), (2157.0, 6), (2159.0, 7)),
    -19: ((2155.5, 6), (2155.5, 6), (2155.5, 6)),
    -20: ((2155.0, 6), (2156.0, 6), (2157.5, 7)),
    -21: ((2158.0, 6), (2158.5, 6), (2159.0, 6)),
    -22: ((2158.5, 6), (2158.5, 6), (2158.5, 6)),
}
FINE_NOTES = {-6: "; on the 0.5 mm grid line", -8: "; next to the 0.4 mm grid line", -14: "; on the 0.2 mm grid line",
              -15: "; next to a grid line", -20: "; on the 0.1 mm grid line", -13: "; lower curve merges with the frame line",
              -16: "; lower curve merges with the frame line", -17: "; lower curve merges with the frame line"}
FIRST = (2159.5, 3162.0, 5, 4, "first point: where the curves' ink ends at the fine end, just below the dashed 0.074 mm (No. 200) line; the three curves end together on the 0 percent frame")
LAST = (691.0, 1406.5, 6, 4, "last point: where the curves' ink ends at the coarse end, on the 100 percent frame near the No. 4 (4.75 mm) sieve; the three curves end together")
KNEES = {"lower": [(2094.0, 1986.0, 6, 6, "knee: the lower curve turns from about 35 degrees to nearly vertical on the page where it crosses the dashed 1.18 mm (No. 16) sieve line")]}


def v_on(k, u):
    return T.v_of_grain(10 ** (0.05 * k), u)


def main(out_csv):
    pts = Bd.load([str(Path(__file__).parent / "trk1.json"), str(Path(__file__).parent / "trkD.json")])
    rows = {s: [] for s in ("upper", "average", "lower")}
    for s in rows:
        P = Bd.chain(pts[s])
        def add(kind, level, cands):
            if (s, kind, level) in OVERRIDE:
                u, v, ub, vb, note = OVERRIDE[(s, kind, level)]
                rows[s].append((u, v, ub, vb, note))
                return
            if len(cands) != 1:
                raise SystemExit(f"{s} {kind}={level}: {len(cands)} crossings {cands}")
            u, v, how, i = cands[0]
            if how.startswith("gap"):
                a, b = P[i], P[i + 1]
                end = a if math.dist((u, v), a[:2]) <= math.dist((u, v), b[:2]) else b
                rows[s].append((end[0], end[1], HALF, HALF, "dash end (sample in a dash gap, moved to the nearer end, rule 7)"))
            elif how.startswith("bridge"):
                rows[s].append((u, v, HALF, HALF + 1, "stroke crosses a grid line here; centre interpolated through the grid line's ink"))
            else:
                rows[s].append((u, v, HALF, HALF, ""))
        for k in K_TRACKED[s]:
            add("k", k, Bd.crossings(P, Bd.g_of, 0.05 * k))
        for p in P_TRACKED[s]:
            add("p", p, Bd.crossings(P, Bd.p_of, p))
        for kind, level, u, v, ub, vb, note in MANUAL[s]:
            rows[s].append((u, v if v is not None else v_on(level, u), ub, vb, note))
        for k, trip in FINE_ROWS.items():
            item, b = trip[("upper", "average", "lower").index(s)]
            note = FINE + FINE_NOTES.get(k, "")
            if isinstance(item, tuple):
                rows[s].append((item[0], item[1], b, 4, note + "; in a dash gap at the sampling line, moved to the nearer dash end (rule 7)"))
            else:
                rows[s].append((item, v_on(k, item), b, 4, note))
    out = []
    for s in ("upper", "average", "lower"):
        tr = sorted(rows[s], key=lambda r: -(r[0] + r[1]))   # drawing order from the fine end
        seq = [FIRST] + tr + [LAST]
        for i, (u, v, ub, vb, note) in enumerate(seq, 1):
            out.append({"figure_id": "FA-2", "panel": 1, "series_id": s, "point_kind": "trace", "sequence": i,
                        "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": ub, "v_bound_px": vb,
                        "symbol": "", "note": note})
        feats = [FIRST] + KNEES.get(s, []) + [LAST]
        for i, (u, v, ub, vb, note) in enumerate(feats, 1):
            out.append({"figure_id": "FA-2", "panel": 1, "series_id": s, "point_kind": "feature", "sequence": i,
                        "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": ub, "v_bound_px": vb,
                        "symbol": "", "note": note})
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    # check of the extra-sample rule: rises between consecutive k samples
    for s in ("upper", "average", "lower"):
        ks = {}
        for r in out:
            if r["series_id"] == s and r["point_kind"] == "trace":
                g = T.X.value(r["pixel_u"], r["pixel_v"])[0]
                k = round(math.log10(g) / 0.05, 2)
                if abs(k - round(k)) < 0.02:
                    ks[round(k)] = T.Y.value(r["pixel_u"], r["pixel_v"])[0]
        print(s, "k samples:", len(ks), "rises > 10:", [(k + 1, k, round(ks[k + 1] - ks[k], 1)) for k in sorted(ks) if k + 1 in ks and ks[k + 1] - ks[k] > 10])
    print(f"wrote {out_csv}: {len(out)} rows")


if __name__ == "__main__":
    main(sys.argv[1])
