"""Reader helper: writes points-p1.csv from the readings below (pixel positions read on the page with
rowsraw.py / rawprof.py run profiles and checked on zoomed crops). Each reading: k (sample at 10^(0.05 k)
mm), then per series either a u (sample on the sample row, v computed from cal-p1 at that u) or a tuple
(u, v, u_bound, v_bound, note) for a sample moved to a dash end or otherwise placed explicitly
(v None: on the sample row). A leading "m" marks a row where the three curves run together in one band."""
import csv
from calmap import v_of_g

FIG = "FA-38"
MERGED = ("three curves run together in one band here; placed from the band edges (upper = left edge + 6 px, "
          "lower = right edge - 6 px, average = middle), bound widened")
R = {
    -22: (1381, 1419.5, (1435.0, 3160.5, 5, 3.5, "lower curve in a dash gap at the sample row (v 3164-3170 clean, no ink); moved to the nearest dash end, the lower end of the dash above, hidden under the grid line at v 3158-3163")),
    -21: (1361, 1392.5, (1418.5, 3119.0, 5, 2, "dash gap at the sample row; moved to the top end of the next dash")),
    -20: ((1341.0, None, 6, 4.5, "dash ends under the 0.1 mm grid line (v 3065-3072); sample on the line through the dash, end position hidden"), 1367.5, (1386.5, None, 6, 4.5, "next dash starts under the 0.1 mm grid line (v 3065-3073); sample on the line extrapolated from v 3073, end position hidden")),
    -19: ((1328.5, 3026.5, 5, 2, "dash gap at the sample row (v 3014-3025 clean, no ink); moved to the top end of the next dash"), 1346.5, 1362.5),
    -18: (1301.5, (1325.5, None, 6, 5, "average and lower touch (band u 1320-1345); average from the left edge of the band"), (1339.5, None, 6, 5, "average and lower touch; lower from the right edge of the band, which meets the grid line at u 1342-1346")),
    -17: ((1283.5, None, 6, 5, "stroke overlaps the 60 percent grid line (u 1280-1287)"), (1304, None, 6, 5, "average and lower touch (band u 1299-1324); from the left edge of the band"), (1319, None, 6, 5, "average and lower touch; from the right edge of the band")),
    -16: (1265, (1283, None, 6, 5, "stroke lies on the 60 percent grid line (u 1280-1287); centre from its visible edge"), 1296.5),
    -15: ((1247, None, 6, 5, "under the grid line v 2828-2833; from clean rows 2825-2827 and 2834-2838"), (1263.5, None, 6, 5, "under the grid line v 2828-2833; upper and average touch above it"), (1272.0, 2823.0, 6, 2, "dash gap at the sample row; moved to the lower end of the dash above")),
    -14: ((1226.0, 2774.5, 6, 1.5, "dash gap at the sample row; moved to the nearest dash end (lower end of the dash above, on the grid line u 1225-1227)"), (1244.5, None, 6, 5, "under the 0.2 mm grid line (v 2776-2784); interpolated between clean rows 2774 and 2786"), (1259.0, None, 6, 4.5, "next dash starts under the 0.2 mm grid line (v 2776-2784); sample on the line extrapolated from v 2785-2789, end position hidden")),
    -13: ("m", 1215, 1226, 1242.5),
    -12: ("m", 1200, 1210, 1225.5),
    -11: ("m", 1183.5, 1195, 1210.5),
    -10: ("m", 1169, 1181, (1193.5, 2582.0, 6, 2.5, "dash gap at the sample row (v 2585-2599 clean, no ink); moved to the lower end of the dash above, partly under a dotted grid line at v 2582-2584")),
    -9: ((1150.0, 2533.0, 5, 1.5, "dash gap at the sample row; moved to the lower end of the dash above (tip at v 2532-2533)"), 1165.5, (1181.0, 2541.0, 5, 1.5, "dash gap at the sample row; moved to the top end of the next dash (tip at v 2540-2542)")),
    -8: ("m", 1142, 1153.5, 1165),
    -7: ("m", 1128, 1139, 1150),
    -6: ("m", 1114.5, 1126.5, 1138.5),
    -5: ("m", 1103.5, 1113.5, (1120.0, 2347.0, 6, 2, "end of a dash at the sample row (tip at v 2346-2347, overlapping the average)")),
    -4: ((1092.0, 2303.5, 6, 1.5, "dash gap at the sample row; moved to the top end of the next dash"), 1101.5, (1115.5, None, 5, 2, "top end of a dash at the sample row (tip at v 2297)")),
    -3: ("m", 1079, 1088, 1102.5),
    -2: ("m", 1066.5, 1074.5, 1091.5),
    -1: ("m", 1052, 1064, 1079.5),
    0: ((1043.0, None, 6, 5, "dash ends under the 1.0 mm grid line (v 2099-2106); end position hidden, sample on the line through the dash"), (1053.3, None, 6, 5, "under the 1.0 mm grid line; interpolated between clean rows 2098 and 2108"), (1067.5, None, 6, 5, "dash ends under the 1.0 mm grid line (v 2099-2106); end position hidden, sample on the line through the dash")),
    1: ((1034.5, 2058.0, 6, 1.5, "dash gap at the sample row; moved to the top end of the next dash"), 1041.5, (1056.0, None, 5, 2, "top end of a dash at the sample row (tip at v 2054)")),
    2: ("m", 1016, 1028, 1040),
    3: ("m", 1001, 1012.5, 1024),
    4: ("m", 984, 995.5, 1007),
    5: ("m", 962.5, 974, (985.5, 1859.0, 6, 1.5, "dash gap at the sample row; moved to the lower end of the dash above")),
    6: ((942.0, None, 6, 5, "dash ends under the 2.0 mm grid line (v 1808-1817); end position hidden, sample on the line through the dash"), (954.0, None, 6, 5, "under the 2.0 mm grid line; interpolated between clean rows 1807 and 1818"), (968.0, None, 6, 5, "next dash starts under the 2.0 mm grid line (v 1808-1817); end position hidden")),
    7: ((922.5, 1766.0, 6, 1, "dash gap at the sample row; moved to the top end of the next dash"), 927.5, 944),
    8: ("m", 893, 902, 918.5),
    9: ("m", 862, 876.5, 891),
    10: ("m", 830, 844, 858),
    11: ("m", 799, 812.5, 826),
    12: ("m", 769.5, 781, 792.5),
    13: ("m", 740, 751, 762),
    14: ("m", 719.3, 727.5, (734.6, None, 6, 5, "dash ends under the 5.0 mm grid line (v 1419-1427); end position hidden")),
    15: ((695.0, 1371.0, 6, 1.5, "dash gap at the sample row; moved to the lower end of the dash above, which runs on the 100 percent frame line"), (710.5, None, 5, 5, "average and lower run together from about v 1373 to the top end: one stroke 11 to 12 px wide"), (710.5, None, 9, 5, "lower runs together with the average here (one stroke); a separate lower dash may begin at about u 719, v 1373, so the bound is widened")),
    16: ((684.5, None, 5, 3, "dash runs beyond the 100 percent frame line (u 689-697) by up to 0.6 percent near the top end"), (697.0, None, 6, 3, "average and lower run together (one stroke)"), (697.0, None, 6, 3, "lower runs together with the average (one stroke)")),
}
FIRST = {"upper": (1388.0, 3190.0, 3, 2, "first point: fine end of the ink (dash tip at v 3187-3189), just above the #200 sieve grid line"),
         "average": (1436.0, 3193.0, 5, 4, "first point: the line runs into the #200 sieve grid line (v 3191-3198); end hidden, no ink below v 3199"),
         "lower": (1452.0, 3193.0, 5, 4, "first point: the line runs into the #200 sieve grid line (v 3191-3198); end hidden, no ink below v 3199")}
LAST = {"upper": (684.5, 1323.0, 5, 3, "last point: top end of the ink (tip at v 1325-1327) at the #3 sieve grid line (v 1317-1324); left of the 100 percent frame line"),
        "average": (697.0, 1323.0, 6, 3, "last point: top end of the ink at the #3 sieve grid line (v 1317-1324); average and lower run together here"),
        "lower": (697.0, 1323.0, 6, 3, "last point: top end of the ink, shared with the average (the two run together above about v 1373)")}
SER = ["upper", "average", "lower"]


def main():
    rows = []
    for si, s in enumerate(SER):
        seq = 1
        u, v, ub, vb, note = FIRST[s]
        rows.append(dict(series_id=s, point_kind="trace", sequence=seq, pixel_u=u, pixel_v=v, u_bound_px=ub, v_bound_px=vb, note=note))
        seq += 1
        for k in sorted(R):
            e = R[k]
            merged = e[0] == "m"
            if merged:
                e = e[1:]
            x = e[si]
            g = 10 ** (0.05 * k)
            if isinstance(x, tuple):
                uu, vv, ub, vb, note = x
                if vv is None:
                    vv = v_of_g(g, uu)
                note = f"sample {g:.4f} mm: " + note
            else:
                uu = x
                vv = v_of_g(g, uu)
                ub, vb = (6, 5) if merged else (5, 5)
                note = f"sample {g:.4f} mm" + ("; " + MERGED if merged else "")
            rows.append(dict(series_id=s, point_kind="trace", sequence=seq, pixel_u=uu, pixel_v=round(vv, 1), u_bound_px=ub, v_bound_px=vb, note=note))
            seq += 1
        u, v, ub, vb, note = LAST[s]
        rows.append(dict(series_id=s, point_kind="trace", sequence=seq, pixel_u=u, pixel_v=v, u_bound_px=ub, v_bound_px=vb, note=note))
        u, v, ub, vb, note = FIRST[s]
        rows.append(dict(series_id=s, point_kind="feature", sequence=1, pixel_u=u, pixel_v=v, u_bound_px=ub, v_bound_px=vb,
                         note="first point (fine end); " + note.split(": ", 1)[1]))
        u, v, ub, vb, note = LAST[s]
        rows.append(dict(series_id=s, point_kind="feature", sequence=2, pixel_u=u, pixel_v=v, u_bound_px=ub, v_bound_px=vb,
                         note="last point (coarse end, maximum of the trace); " + note.split(": ", 1)[1]))
    with open("points-p1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
                                          "u_bound_px", "v_bound_px", "symbol", "note"], lineterminator="\n")
        w.writeheader()
        for r in rows:
            r.update(figure_id=FIG, panel=1, symbol="")
            w.writerow(r)
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
