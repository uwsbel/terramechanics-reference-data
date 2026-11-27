"""Assemble out/FA-22/points-p1.csv from the working table (checked samples) and the reader's manual
decisions below (all positions in page pixels, read on the page: pixel rows, check tiles, soft views)."""
import csv, json
from collections import Counter
import fa22lib as L

wk = json.loads((L.OUT / "helpers" / "working.json").read_text(encoding="utf-8"))
B = 5.0   # half the drawn line thickness (the curves are about 10 px thick)
MERGE_ALL = ("the three curves and the 100 percent line run together here; centre of the merged curve ink, "
             "bound half its width")
MERGE_AL = ("average and lower run together in one band here (13 to 35 px wide); centre of the band, "
            "bound half its width")

# manual trace samples: series -> {log step: (u, v, ub, vb, note)}; None drops the sample
MAN = {
    "upper": {
        -0.85: (1860.0, 2946.0, B, B, "sampling line 0.141 mm falls inside the #100 symbol; moved to the line ink just below it"),
        -0.70: (1757.0, 2787.0, B, B, "gap between dashes at the 0.2 mm grid line; moved to the nearest dash end (above)"),
        -0.65: (1737.5, 2747.5, B, B, "gap between dashes; moved to the nearest dash end (below)"),
        -0.60: (1688.0, 2685.0, B, B, "sampling line 0.251 mm falls inside the #60 symbol; moved to the end of the dash above it"),
        0.00: (1283.0, 2111.0, B, B, "gap at the 1.0 mm grid line; moved to the end of the dash above (it may continue under the grid line)"),
        0.05: (1259.5, 2073.0, B, B, "gap between dashes; moved to the nearest dash end (below; the dash above ends 0.4 px farther)"),
        0.70: (793.5, 1433.0, B, B, "on the 5.0 mm grid line; centre from the dash above and below it"),
        0.75: (774.5, 1385.0, B, B, "strand just right of the 100 percent line; the dash ends at v 1387"),
        0.80: (766.5, 1336.0, 6.0, B, "touches the 100 percent line on its left; centre from its right edge and the stroke width"),
        0.85: (773.5, 1287.0, 13.0, B, MERGE_ALL),
        0.90: (762.0, 1238.0, 14.0, B, MERGE_ALL),
    },
    "average": {
        -0.85: (1970.5, 2945.0, B, B, "sampling line 0.141 mm touches the lower edge of the #100 symbol; moved to the line ink just below it"),
        -0.60: (1839.0, 2684.0, B, B, "sampling line 0.251 mm falls inside the #60 symbol; moved to the line ink just above it"),
        0.70: (841.0, 1433.0, 7.0, B, "on the 5.0 mm grid line, where the lower curve separates from this one; centre between the band above and the stroke below"),
        0.75: (818.5, 1385.0, 18.0, B, MERGE_AL),
        0.80: (790.0, 1336.0, 10.0, B, MERGE_AL),
        0.85: (773.5, 1287.0, 13.0, B, MERGE_ALL),
        0.90: (762.0, 1238.0, 14.0, B, MERGE_ALL),
    },
    "lower": {
        -1.10: None,
        -0.85: (2021.0, 2944.0, B, B, "sampling line 0.141 mm falls inside the #100 symbol; moved to the line ink just below it"),
        -0.80: (1998.0, 2886.0, B, B, "gap between the dash and the #100 symbol; moved to the dash end"),
        -0.75: (1984.0, 2841.0, B, B, "top of a dash, crossed by the dashed 0.177 mm sieve line"),
        -0.60: (1917.0, 2678.5, B, B, "sampling line 0.251 mm falls inside the #60 symbol; moved to the line ink just above it"),
        -0.50: (1882.0, 2599.5, B, B, "at the lower end of a dash"),
        -0.45: (1864.0, 2553.0, B, B, "gap between dashes; moved to the nearest dash end (top of the dash below)"),
        -0.15: (1728.0, 2259.5, B, B, "gap between dashes at a grid line; moved to the nearest dash end (above)"),
        0.40: (1337.0, 1730.5, B, B, "gap between dashes at the 2.5 mm grid line; moved to the nearest dash end (top of the stroke below, which runs into the #8 symbol)"),
        0.70: (871.0, 1439.0, 6.0, B, "the lower curve's first separate dash, just below the 5.0 mm grid line; above it this curve runs together with the average"),
        0.75: (818.5, 1385.0, 18.0, B, MERGE_AL),
        0.80: (790.0, 1336.0, 10.0, B, MERGE_AL),
        0.85: (773.5, 1287.0, 13.0, B, MERGE_ALL),
        0.90: (762.0, 1238.0, 14.0, B, MERGE_ALL),
    },
}
FIRST = {
    "upper": (2009.5, 3194.0, B, B, "fine end: the line's ink starts at the #200 circle"),
    "average": (2070.0, 3190.0, 6.0, 6.0, "fine end: the line meets the #200 symbol (merged with vertical grid lines there)"),
    "lower": (2105.0, 3175.0, B, B, "fine end: lower end of the last dash above the #200 symbol (gap of about 10 px to the symbol); the 0.0794 mm sample would move here and is not repeated"),
}
LAST = (759.0, 1191.0, 14.0, 4.0, "coarse end: the merged curves meet the 3/8 in. circle; the three curves and the 100 percent line run together here; the 8.91 mm sample would fall on the circle and is not taken")
SHARED = "one circle at 100 percent on the 3/8 in. (9.5 mm) sieve line where all three curves end; recorded under each series"
CIRC = "binarized scan: open or filled not reliably told apart"
MK = {
    "upper": [("#200", 2019.5, 3212.0, 4, 4, "circle", "open circle"),
              ("#100", 1847.0, 2925.0, 6, 6, "circle", "blob merged with grid lines; shape not resolvable (filled circle or asterisk)"),
              ("#60", 1706.0, 2702.0, 6, 6, "circle", "merged with the 0.25 mm grid line; " + CIRC),
              ("#40", 1556.0, 2485.0, 4, 4, "x", "two crossing strokes on the #40 line"),
              ("#20", 1342.0, 2191.0, 5, 5, "circle", "filled"),
              ("#12", 1141.0, 1903.0, 5, 5, "circle", CIRC),
              ("#8", 1029.0, 1757.0, 5, 5, "circle", CIRC),
              ("#6", 896.0, 1603.0, 5, 5, "circle", CIRC),
              ("#4", 800.0, 1463.0, 5, 5, "circle", "open interior visible"),
              ("3/8 in.", 759.5, 1162.0, 5, 5, "circle", SHARED)],
    "average": [("#200", 2073.0, 3205.0, 6, 6, "circle", "merged with vertical grid lines; " + CIRC),
                ("#100", 1956.0, 2922.0, 4, 4, "circle", "open interior visible"),
                ("#60", 1847.0, 2702.0, 6, 6, "circle", "merged with the 0.25 mm grid line; " + CIRC),
                ("#40", 1722.0, 2485.0, 4, 4, "circle", "open interior visible"),
                ("#20", 1551.0, 2193.0, 5, 5, "circle", "filled"),
                ("#12", 1361.0, 1904.0, 5, 5, "circle", CIRC),
                ("#8", 1240.0, 1756.0, 5, 5, "circle", CIRC),
                ("#6", 1066.0, 1606.0, 5, 5, "circle", "filled"),
                ("#4", 865.0, 1465.0, 5, 5, "circle", "open interior visible; the lower curve's stroke touches it on the right"),
                ("3/8 in.", 759.5, 1162.0, 5, 5, "circle", SHARED)],
    "lower": [("#200", 2119.0, 3206.0, 5, 5, "circle", CIRC),
              ("#100", 2012.0, 2924.0, 6, 6, "circle", "open interior visible"),
              ("#60", 1924.0, 2698.0, 6, 6, "circle", "merged with the 0.25 mm grid line and two vertical lines; " + CIRC),
              ("#40", 1832.0, 2485.0, 4, 4, "circle", "open interior visible"),
              ("#20", 1695.0, 2189.0, 5, 5, "circle", CIRC),
              ("#12", 1502.0, 1899.0, 4, 4, "circle", "open interior visible"),
              ("#8", 1367.0, 1754.0, 5, 5, "circle", CIRC),
              ("#6", 1146.0, 1602.0, 5, 5, "circle", "filled"),
              ("3/8 in.", 759.5, 1162.0, 5, 5, "circle", SHARED)],
}

rows = []


def add(s, kind, seq, u, v, ub, vb, sym, note):
    rows.append({"figure_id": "FA-22", "panel": 1, "series_id": s, "point_kind": kind, "sequence": seq,
                 "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": ub, "v_bound_px": vb,
                 "symbol": sym, "note": note})


for s in ("average", "upper", "lower"):
    for i, m in enumerate(MK[s], 1):
        add(s, "marker", i, m[1], m[2], m[3], m[4], m[5], f"{m[0]} sieve; " + m[6])
    seq = 1
    f = FIRST[s]
    add(s, "trace", seq, f[0], f[1], f[2], f[3], "", "first point; " + f[4]); seq += 1
    man = {round(k, 2): v for k, v in MAN[s].items()}
    done = set()
    for m in wk[s]:
        e = round(m["e"], 2); done.add(e)
        if e in man:
            if man[e] is None:
                continue
            u, v, ub, vb, note = man[e]
            add(s, "trace", seq, u, v, ub, vb, "", f"log10 d {e:+.2f}; " + note); seq += 1
        else:
            assert m["u"] is not None, (s, e)
            add(s, "trace", seq, m["u"], m["v"], B, B, "", f"log10 d {e:+.2f}"); seq += 1
    for e in sorted(k for k in man if k not in done):
        if man[e] is None:
            continue
        u, v, ub, vb, note = man[e]
        add(s, "trace", seq, u, v, ub, vb, "", f"log10 d {e:+.2f}; " + note); seq += 1
    add(s, "trace", seq, LAST[0], LAST[1], LAST[2], LAST[3], "", "last point; " + LAST[4])
    add(s, "feature", 1, f[0], f[1], f[2], f[3], "", "first point (start of the line's ink at the fine end)")
    add(s, "feature", 2, LAST[0], LAST[1], LAST[2], LAST[3], "",
        "last point; also the maximum of the trace (100 percent); no knee or kink: the curve bends smoothly into the 100 percent line, merged with the others")

cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with (L.OUT / "points-p1.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(Counter((r["series_id"], r["point_kind"]) for r in rows))
