"""points-p1.csv for Fig. A-26 from the readings made on the page (pixel coordinates of the unrotated scan).
Each entry: (u, v, u_bound, v_bound, note). Order: drawing order from the fine end (small grain size)."""
import csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import calib
base = Path(__file__).resolve().parents[1]
M = "three curves run together into one stroke along the 0 percent frame; identity not separable, bound covers the stroke"
R = {
 "lower": [
  (2026, 2976, 8, 6, "first point: lower end of the ink; " + M),
  (2028, 2973, 8, 6, "0.1413 mm; " + M),
  (2026, 2925, 7, 5, "0.1585 mm; lower and average run together beside the 0 percent frame (frame at u 2027-2037); bound widened"),
  (2013.5, 2876, 6, 5, "0.1778 mm; right line of the three-line band (1989-2018)"),
  (1997, 2828, 7, 5, "0.1995 mm; band on the 0.2 mm grid line; right line of the merged band (about 1966-2002)"),
  (1976, 2780, 5, 5, "0.2239 mm; right line, near its dash end at v 2782"),
  (1936, 2732, 5, 5, "0.2512 mm; right line, near its dash end at v 2735"),
  (1893, 2684, 6, 5, "0.2818 mm; right part of the average+lower stroke, near the dash end at v 2686"),
  (1816, 2635.5, 7, 5, "0.3162 mm; right part of the merged average+lower stroke (1782-1826)"),
  (1714, 2587, 5, 5, "0.3548 mm; top line of the band"),
  (1573, 2541, 5, 5, "0.3981 mm falls in a dash gap (u 1556-1572); moved to the start of the next dash (rule 7)"),
  (1521, 2530.5, 5, 5, "35 percent; top line of the three-line band"),
  (1452, 2516, 5, 5, "40 percent falls in a dash gap ending behind the 40 percent grid line; moved to the dash start"),
  (1373, 2501, 5, 5, "45 percent falls in a dash gap (u 1374-1385); moved to the dash end"),
  (1303, 2491, 5, 5, "0.4467 mm; top line"),
  (1228, 2480.5, 5, 5, "55 percent; top line (edge touches the grid row at 2475-2479)"),
  (1154, 2468.5, 5, 5, "60 percent; top line, interpolated across the 60 percent grid line from u 1145 and 1160"),
  (1083, 2458.5, 5, 5, "65 percent; top line of the three-line band"),
  (1014, 2452.5, 6, 6, "70 percent falls in a dash gap (u 998-1013); moved to the dash start; its top edge touches the 0.5 mm grid line"),
  (988, 2443, 5, 6, "0.5012 mm; on the 0.5 mm grid line, centre from the band lower edge"),
  (934, 2437, 5, 5, "75 percent falls in a dash gap (u 936-950); moved to the dash end"),
  (865, 2426, 5, 5, "80 percent; top line (upper series in a gap here)"),
  (792, 2411.5, 5, 5, "85 percent; top line"),
  (723, 2394, 5, 5, "0.5623 mm; top line of the three-line band"),
  (634, 2344, 6, 5, "0.6310 mm; right line of the band, near its dash end at v 2344"),
  (596.5, 2296, 5, 5, "0.7079 mm; right stroke, dash ending at v 2299"),
  (571, 2245, 6, 5, "0.7943 mm falls in a dash gap (v 2246-2253); moved to the end of the stroke along the 100 percent frame"),
  (566, 2222, 7, 6, "last point: top of the ink beside the 100 percent frame, at the #20 sieve line; beyond 100 percent as drawn"),
 ],
 "average": [
  (2026, 2976, 8, 6, "first point: lower end of the ink; " + M),
  (2028, 2973, 8, 6, "0.1413 mm; " + M),
  (2021, 2925, 7, 5, "0.1585 mm; average and lower run together beside the 0 percent frame; bound widened"),
  (2004, 2876, 6, 5, "0.1778 mm; middle of the three-line band (1989-2018)"),
  (1984, 2828, 7, 5, "0.1995 mm; band on the 0.2 mm grid line; middle of the merged band"),
  (1959, 2780, 7, 5, "0.2239 mm; right part of the merged upper+average stroke (1942-1966)"),
  (1925, 2732, 6, 5, "0.2512 mm; middle line"),
  (1876, 2684, 7, 5, "0.2818 mm; left part of the merged average+lower stroke (1865-1900)"),
  (1794, 2635.5, 7, 5, "0.3162 mm; left part of the merged average+lower stroke"),
  (1680, 2587, 5, 5, "0.3548 mm; middle line, on the 20 percent grid line"),
  (1667, 2582.5, 5, 5, "25 percent; lower of the two lines (upper series in a gap)"),
  (1594, 2560, 5, 5, "30 percent; lower of the two lines left of the grid line"),
  (1521, 2542, 5, 6, "35 percent; middle of the three-line band"),
  (1508, 2539, 5, 6, "0.3981 mm; middle line, near the #40 sieve line"),
  (1448, 2524.5, 5, 6, "40 percent; middle line, interpolated across the grid line from u 1442 and 1452"),
  (1375, 2511.5, 5, 5, "45 percent; separate middle run 2507-2516"),
  (1302, 2499, 5, 5, "50 percent; lower of the two lines"),
  (1238, 2491, 5, 5, "0.4467 mm; middle line"),
  (1228, 2489.5, 5, 5, "55 percent; middle line (upper series in a gap)"),
  (1154, 2479, 5, 5, "60 percent; middle line, interpolated across the grid line"),
  (1083, 2468, 5, 5, "65 percent; middle of the three-line band"),
  (1011, 2459, 5, 6, "70 percent; middle line; band top merged with the 0.5 mm grid line"),
  (938, 2448, 5, 6, "75 percent; middle line; its top edge on the 0.5 mm grid line"),
  (896, 2443, 5, 6, "0.5012 mm; middle of the band between two grid rows"),
  (865, 2437, 5, 5, "80 percent; lower of the two lines"),
  (792, 2422, 5, 5, "85 percent; middle line"),
  (719.5, 2403, 5, 5, "90 percent; middle of the three-line band"),
  (688, 2394, 5, 5, "0.5623 mm; separate middle run at u 686-688"),
  (621, 2345, 6, 5, "0.6310 mm; middle of the three-line band"),
  (581.5, 2296, 7, 5, "0.7079 mm; average and upper run together in one stroke beside the 100 percent frame; bound widened"),
  (566, 2269, 7, 5, "last point: top end of the stroke the average shares with the upper series, at the 100 percent frame"),
 ],
 "upper": [
  (2026, 2976, 8, 6, "first point: lower end of the ink; " + M),
  (2028, 2973, 8, 6, "0.1413 mm; " + M),
  (2015.5, 2934, 5, 5, "0.1585 mm falls in a dash gap (v 2917-2932); moved to the start of the next dash"),
  (1994, 2876, 6, 5, "0.1778 mm; left line of the three-line band"),
  (1972, 2828, 7, 5, "0.1995 mm; band on the 0.2 mm grid line; left line of the merged band"),
  (1949, 2780, 7, 5, "0.2239 mm; left part of the merged upper+average stroke"),
  (1907.5, 2732, 5, 5, "0.2512 mm; left line"),
  (1850, 2684, 5, 5, "0.2818 mm; left line"),
  (1762, 2635.5, 5, 5, "0.3162 mm; left line, near its dash end at v 2641"),
  (1649, 2586, 5, 5, "0.3548 mm falls in a dash gap (u 1652-1667); moved to the dash end; bottom edge on a grid row"),
  (1590, 2573, 5, 5, "30 percent falls in a dash gap behind the 30 percent grid line; moved to the dash end"),
  (1521, 2554.5, 5, 5, "35 percent; bottom line of the three-line band"),
  (1445, 2539, 5, 5, "0.3981 mm; bottom line (40 percent column sample coincides, not repeated)"),
  (1375, 2525, 5, 5, "45 percent; separate bottom run 2520-2530"),
  (1305, 2513, 5, 6, "50 percent falls in a dash gap (u 1289-1300); moved to the dash start; bottom edge on the #40 sieve line"),
  (1225, 2498.5, 5, 5, "55 percent falls in a dash gap (u 1226-1242); moved to the dash end"),
  (1159, 2491, 5, 5, "0.4467 mm; bottom line near its dash end at u 1161"),
  (1154, 2489, 5, 5, "60 percent; bottom line, interpolated across the 60 percent grid line from u 1145 and 1160"),
  (1083, 2477.5, 5, 5, "65 percent; bottom line"),
  (1011, 2472.5, 5, 5, "70 percent; bottom line"),
  (938, 2458.5, 5, 5, "75 percent; bottom line"),
  (871, 2448, 5, 5, "80 percent falls in a dash gap (u 853-870); moved to the dash start"),
  (845, 2443, 5, 6, "0.5012 mm; bottom line, its lower edge on the 0.5 mm grid line"),
  (790, 2430, 5, 5, "85 percent falls in a dash gap (u 791-805); moved to the dash end"),
  (719.5, 2414, 5, 5, "90 percent; bottom line"),
  (659, 2394, 5, 5, "0.5623 mm; separate bottom run"),
  (609, 2345, 6, 5, "0.6310 mm; left line of the three-line band"),
  (576.5, 2296, 7, 5, "0.7079 mm; upper and average run together in one stroke over the 100 percent frame; bound widened"),
  (557.5, 2247, 5, 5, "0.7943 mm; dash left of the 100 percent frame (beyond 100 percent as drawn)"),
  (551, 2236, 5, 5, "last point: top end of that dash, beyond 100 percent as drawn"),
 ],
}
rows = []
for s in ("upper", "average", "lower"):
    for k, (u, v, bu, bv, note) in enumerate(R[s], 1):
        rows.append({"figure_id": "FA-26", "panel": 1, "series_id": s, "point_kind": "trace", "sequence": k,
                     "pixel_u": u, "pixel_v": v, "u_bound_px": bu, "v_bound_px": bv, "symbol": "", "note": note})
    first, last = R[s][0], R[s][-1]
    rows.append({"figure_id": "FA-26", "panel": 1, "series_id": s, "point_kind": "feature", "sequence": 1,
                 "pixel_u": first[0], "pixel_v": first[1], "u_bound_px": first[2], "v_bound_px": first[3], "symbol": "",
                 "note": "first point (fine end); " + M})
    rows.append({"figure_id": "FA-26", "panel": 1, "series_id": s, "point_kind": "feature", "sequence": 2,
                 "pixel_u": last[0], "pixel_v": last[1], "u_bound_px": last[2], "v_bound_px": last[3], "symbol": "",
                 "note": "last point (coarse end; also the maximum of the trace)"})
with (base / "points-p1.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
if __name__ == "__main__":
    for s in ("upper", "average", "lower"):
        print(s)
        prev = None
        for u, v, bu, bv, note in R[s]:
            x, y = calib.val(u, v)
            flag = ""
            if prev is not None and y - prev > 10:
                flag = f"  RISE {y - prev:.1f}"
            print(f"   ({u:7.1f},{v:7.1f}) {x:7.4f} mm {y:6.1f} %{flag}  {note[:50]}")
            prev = y
