"""Assemble points-p1.csv for FC-16: circle markers (fitted ring centres, circles.py), trace samples
(sample.py) and features (first and last point of each trace)."""
import csv, json
MARKERS = [
 ("p1L", 642.2, 2458.4, 3, "pair 1 left; cut by the left frame, which runs through its centre (Dr about -0.1); the solid curve runs into its top right"),
 ("p1R", 793.5, 2453.0, 2, "pair 1 right; the Dr 0 grid line runs through it; the lower dashed curve has a gap around it (dashes end 20 px either side)"),
 ("p2L", 1563.6, 1919.4, 3, "pair 2 left; the Dr 0.5 grid line runs through it; it sits in a gap of the upper dashed curve, whose next dash starts at its ring"),
 ("p2R", 1679.0, 1921.8, 3, "pair 2 right; overlaps the solid curve, which crosses its lower half"),
 ("p3L", 1923.7, 1848.3, 3, "pair 3 left; overlaps the solid curve, which crosses its upper half"),
 ("p3R", 2146.5, 1847.0, 2, "pair 3 right"),
 ("p4L", 2345.2, 1532.3, 3, "pair 4 left; the Dr 1.0 grid line runs through it; the upper dashed curve touches the top of its ring"),
 ("sTop", 2498.5, 1391.8, 3, "single; cut by the right frame, which runs through its centre (Dr about 1.1); the upper dashed curve passes through it"),
 ("sMid", 2501.3, 1617.0, 3, "single; cut by the right frame, which runs through its centre (Dr about 1.1); the solid curve passes through it"),
 ("sLow", 2500.2, 1846.6, 3, "single; cut by the right frame, which runs through its centre (Dr about 1.1); the lower dashed curve ends at its ring"),
 ("p4R", 2547.7, 1528.6, 2, "pair 4 right; outside the plot frame, right of the right frame (Dr about 1.13); its joining line crosses the frame"),
]
rows = []
for i, (k, u, v, b, note) in enumerate(MARKERS, 1):
    rows.append(dict(figure_id="FC-16", panel=1, series_id="data", point_kind="marker", sequence=i, pixel_u=u, pixel_v=v,
                     u_bound_px=b, v_bound_px=b, symbol="circle", note=note))
tr = json.load(open("out/FC-16/traces.json"))
for name in ("mean", "upper", "lower"):
    ts = [t for t in tr if t["series_id"] == name]
    for i, t in enumerate(ts, 1):
        rows.append(dict(figure_id="FC-16", panel=1, series_id=name, point_kind="trace", sequence=i, pixel_u=t["pixel_u"],
                         pixel_v=t["pixel_v"], u_bound_px=t["u_bound_px"], v_bound_px=t["v_bound_px"], symbol=t["symbol"], note=t["note"]))
    f, l = ts[0], ts[-1]
    rows.append(dict(figure_id="FC-16", panel=1, series_id=name, point_kind="feature", sequence=1, pixel_u=f["pixel_u"], pixel_v=f["pixel_v"],
                     u_bound_px=f["u_bound_px"], v_bound_px=f["v_bound_px"], symbol=f["symbol"], note="first point; " + f["note"]))
    rows.append(dict(figure_id="FC-16", panel=1, series_id=name, point_kind="feature", sequence=2, pixel_u=l["pixel_u"], pixel_v=l["pixel_v"],
                     u_bound_px=l["u_bound_px"], v_bound_px=l["v_bound_px"], symbol=l["symbol"],
                     note="last point, also the maximum of the trace (the curve rises monotonically, no knee); " + l["note"]))
cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with open("out/FC-16/points-p1.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
