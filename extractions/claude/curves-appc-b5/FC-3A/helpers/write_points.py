"""Assemble points-p1.csv for FC-3A from the marker readings and traces.json (helper)."""
import json, csv, sys
tr = json.load(open(sys.argv[1]))
rows = []
F = "FC-3A"
def add(series, kind, seq, u, v, bu, bv, sym, note):
    rows.append([F, 1, series, kind, seq, "%.1f" % u, "%.1f" % v, bu, bv, sym, note])
# markers: outline bounding-box centres read on pixel maps (outline extents in the note)
sq = [(1133.0, 2816.0, "outline u 1118-1148, v 2801-2831; sits on the 47 deg line where its dashed part ends and the solid part starts (line interrupted at the symbol)"),
      (1424.5, 2479.0, "outline u 1410-1439, v 2464-2494; lower-right corner touches the 47 deg line, centre about 19 px above it"),
      (1777.5, 2185.0, "outline u 1762-1793, v 2170-2200 (small ink bump on the top edge at u 1783-1785 ignored); clear of the line, below it"),
      (2023.5, 1816.0, "outline u 2008-2039, v 1800-1832; lower-right corner touches the 47 deg line (line interrupted at the symbol), centre about 23 px above it"),
      (2276.0, 1582.0, "outline u 2261-2291, v 1566-1598; upper-left corner on the 47 deg line where the solid part ends; the next dash starts on its top edge; centre about 20 px below the line")]
for i, (u, v, n) in enumerate(sq, 1):
    add("dr100-130", "marker", i, u, v, 2, 2, "square", "open square as in the legend (gamma = 75 pcf, Dr 1.0 to 1.3); " + n)
ci = [(1136.0, 2959.5, "outline u 1121-1151, v 2945-2974; on the 38 deg line where its dashed part ends and the solid part starts (line attaches at the upper right)"),
      (1425.0, 2657.0, "outline u 1410-1440, v 2642-2672; clear of the line, about 72 px above it"),
      (1778.5, 2407.5, "outline u 1764-1793, v 2393-2422; clear of the line, above a gap in the solid line"),
      (2023.5, 2331.5, "outline u 2009-2038, v 2317-2346; clear of the line, below it"),
      (2278.5, 2090.5, "outline u 2264-2293, v 2075-2106; clear of the line, below its dashed part")]
for i, (u, v, n) in enumerate(ci, 1):
    add("dr0-15", "marker", i, u, v, 2, 2, "circle", "open circle as in the legend (gamma = 57.9 to 59.4 pcf, Dr 0 to .15); " + n)
for name, lab in (("L47", "47°"), ("L38", "38°")):
    T = tr[name]; s = T["series"]; b = T["bound"]; seq = 0
    for smp in T["samples"]:
        if smp.get("skip"): continue
        seq += 1
        add(s, "trace", seq, smp["u"], smp["v"], b, b, "", smp["note"])
    u, v = T["intercept"]
    add(s, "feature", 1, u, v, b, b, "", "intercept")
lab_c = {"dr100-130": (1618.5, 2220.5, "47°"), "dr0-15": (1645.5, 2500.0, "38°")}
for s, (u, v, t) in lab_c.items():
    add(s, "feature", 2, u, v, 8, 8, "", "label: %s" % t)
with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"])
    w.writerows(rows)
print("wrote", len(rows), "rows")
