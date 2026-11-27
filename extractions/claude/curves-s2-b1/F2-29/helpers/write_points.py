"""Write points-p1.csv for Figure 2-29 from the reader's decisions (pixel centres chosen on the
scans and crops; v of a trace sample is the tilted row of its penetration from the affine map)."""
import csv, json
cal = json.load(open("out/F2-29/cal-p1/calibration.json"))
ax = cal["ax"]
def v_of_p(p, u):
    return (p - ax[0] * u - ax[2]) / ax[1]

# (penetration, u centre, u half-width, v override or None, v half-width, note)
samples = [
 (0.00, 2358, 8, 3779, 5, "first ink: trace starts at the right frame (load 0) about 0.03 in above the bottom frame; merged with the frame corner"),
 (0.25, 2068, 11, None, 4, "oblique run; trace adjoins the 200 lb grid line"),
 (0.50, 2051, 10, None, 4, "trace runs on the 200 lb grid line; merged, centre uncertain"),
 (0.75, 2120, 5, None, 4, ""),
 (1.00, 2130, 6, 3483, 4, "on the 1 in grid line; centre interpolated from the rows 13 px above and below"),
 (1.25, 2110.5, 6, None, 4, ""),
 (1.50, 2045, 6, 3329, 4, "trace crosses the 200 lb grid line here; merged"),
 (1.75, 1938.5, 12, None, 4, "oblique run (shallow angle to the row)"),
 (2.00, 1810, 12, 3177, 4, "on the 2 in grid line, crossed at a shallow angle; centre interpolated from rows above and below"),
 (2.25, 1707, 7, None, 4, ""),
 (2.50, 1609.5, 4, None, 4, "just below the S-shaped step at 2.55 in"),
 (2.75, 1535.5, 4, None, 4, ""),
 (3.00, 1471, 12, 2874, 4, "on the 3 in grid line; centre interpolated from rows above and below"),
 (3.25, 1412, 8, 2796, 4, "trace crosses the 600 lb grid line here; merged"),
 (3.50, 1342.5, 6, None, 4, ""),
 (3.75, 1300.5, 4, None, 4, ""),
 (4.00, 1252, 12, 2566, 4, "on the 4 in grid line; centre interpolated from rows above and below"),
 (4.25, 1182, 5, None, 4, ""),
 (4.50, 1140, 5, None, 4, ""),
 (4.75, 1065.5, 4, None, 4, ""),
 (5.00, 1041, 7, 2261, 4, "on the 5 in grid line; centre interpolated from rows above and below"),
 (5.25, 969.5, 4, None, 4, ""),
 (5.50, 922.5, 6, None, 4, ""),
 (5.75, 852, 5, None, 4, ""),
 (6.00, 825, 5, 1955, 4, "on the 6 in grid line; centre interpolated from rows above and below"),
 (6.25, 814, 7, None, 4, "inside the near-constant-load stretch 5.9 to 6.4 in"),
 (6.50, 765, 8, 1800, 4, "thin spot in the ink, 1 px gap; 1000 lb grid line 15 px to the left"),
 (6.75, 734.5, 4, None, 4, ""),
 (7.00, 720, 7, 1647, 4, "on the 7 in grid line; centre interpolated from rows above and below"),
 (7.25, 677, 5, None, 4, ""),
 (7.50, 642.5, 4, None, 4, ""),
 (7.75, 620.5, 4, None, 4, ""),
 (8.00, 573, 5, 1340, 4, "on the 8 in grid line; the trace ends about 5 px beyond it"),
]
features = [
 ("first", 2358, 3779, 8, 5, "first: ink starts at the right frame (load 0), about 0.03 in above the bottom frame, merged with the frame corner"),
 ("knee", 2028, 3680, 4, 8, "knee: initial local maximum of load (about 216 lb at 0.36 in), the trace then falls back"),
 ("knee", 2136, 3504, 4, 12, "knee: local minimum of load after the initial peak (trough, about 144 lb at 0.92 in); flat bottom, v uncertain"),
 ("knee", 1602, 3012, 4, 12, "knee: S-shaped step at 2.5 to 2.6 in (load nearly constant over the step)"),
 ("knee", 822.5, 1982, 4, 6, "knee: start of a near-constant-load stretch (about 980 lb) from 5.9 to 6.4 in"),
 ("knee", 819.5, 1836, 4, 6, "knee: end of the near-constant-load stretch at 6.4 in"),
 ("peak", 574, 1335, 4, 4, "peak: the maximum load is at the end of the trace (about 1150 lb at 8.0 in); same pixel as last"),
 ("last", 574, 1335, 4, 4, "last: ink ends just above the 8 in grid line, merged with it"),
]
cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
rows = []
for i, (p, u, ub, v, vb, note) in enumerate(samples, 1):
    vv = v if v is not None else round(v_of_p(p, u))
    rows.append(dict(figure_id="F2-29", panel=1, series_id="lpt27", point_kind="trace", sequence=i,
                     pixel_u=u, pixel_v=vv, u_bound_px=ub, v_bound_px=vb, symbol="",
                     note=(f"sample at {p:.2f} in" + ("; " + note if note else ""))))
for i, (role, u, v, ub, vb, note) in enumerate(features, 1):
    rows.append(dict(figure_id="F2-29", panel=1, series_id="lpt27", point_kind="feature", sequence=i,
                     pixel_u=u, pixel_v=v, u_bound_px=ub, v_bound_px=vb, symbol="", note=note))
with open("out/F2-29/points-p1.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
