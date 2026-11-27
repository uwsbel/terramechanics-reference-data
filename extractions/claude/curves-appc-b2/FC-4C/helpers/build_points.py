"""Assemble points-p1.csv and points-p2.csv for FC-4C from the refined marker lists, the by-eye
overrides recorded below, and the drawn-line samples (sample_lines.py) of the upper panel.

    python build_points.py <workdir>   (the out/FC-4C folder; reads work/, writes points-p*.csv)

Columns written: figure_id, panel, series_id, point_kind, sequence, pixel_u, pixel_v, u_bound_px,
v_bound_px, symbol, note.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

FIG = "FC-4C"
root = Path(sys.argv[1])
work = root / "work"
helpers = root / "helpers"
image = root.parent.parent / "packet" / "p0128.png"
PY = sys.executable

# ---- by-eye overrides of the refined centres: index in refined-p*.csv -> (u, v, bu, bv, note)
OVR_P1 = {
    10: (1860.5, 1767.0, 2, 2, "plus just below the drawn plateau; read by eye at zoom 10"),
    12: (2226.5, 1743.0, 2, 3, "plus on the 250 gridline (right end of the data); horizontal stroke merged with the drawn plateau; read by eye"),
    21: (1278.0, 1867.0, 3, 3, "ring open on its right side (broken circle); centre read from the left arc, top and bottom"),
    38: (1625.5, 1910.0, 3, 3, "triangle on the 4000 gridline and against the 150 gridline; centroid from apex and base corners read by eye"),
    42: (2207.5, 2066.0, 3, 3, "triangle whose right side is hidden by the 250 gridline; right corner taken by symmetry"),
    48: (1102.0, 1850.0, 2, 2, "drawn line passes through the square; centre from the four sides read by eye"),
    52: (1455.5, 2071.0, 2, 2, "square outline open at the bottom; centre from the sides read by eye"),
    56: (2219.0, 2160.5, 3, 3, "square cut by the 250 gridline; centre from the left and right sides read by eye"),
    74: (2211.0, 2374.0, 3, 3, "triangle-down whose right corner is hidden by the 250 gridline; corner taken by symmetry"),
}
B3_P1 = {8: "plus on the 150 gridline", 14: "circle on the 6000 gridline", 26: "circle on the 200 gridline",
         28: "circle on the 250 gridline", 33: "triangle on the 50 gridline", 53: "square touching the 150 gridline",
         55: "square on the 200 gridline", 58: "triangle-down on the 2000 gridline", 61: "triangle-down on the 50 gridline",
         3: "plus overlapping the n3815 peak circle and the drawn lines", 5: "plus partly on the n4695 drawn line"}
OVR_P2 = {
    43: (769.0, 3093.0, 4, 4, "square on the left frame (x about 0); right side hidden by the frame line"),
    44: (892.0, 3072.0, 4, 4, "square outline whose top is hidden under the 0 gridline, 18 px left of the next square; could instead be a triangle-down of n741 (flat hole favours square)"),
    46: (1063.0, 3016.0, 3, 3, "square split by the 50 gridline; centre from both halves of the hole"),
    57: (768.0, 3112.0, 4, 4, "triangle-down on the left frame (x about 0), stacked under the square; top band merged"),
    59: (949.4, 3073.0, 4, 4, "triangle-down whose top edge is hidden under the 0 gridline; a second triangle-down sits 29 px above it"),
    70: (2218.0, 2886.0, 4, 4, "triangle-down in the stack of three symbols on the 250 gridline; right part under the gridline"),
}
B3_P2 = {0: "plus on the left frame (x about 0), lowest of the x=0 stack", 4: "plus on the 50 gridline (vertical stroke coincides with it)",
         12: "plus on the 200 gridline", 14: "plus on the 250 gridline; vertical stroke coincides with it, u uncertain",
         9: "plus on the 150 gridline", 25: "circle on the 150 gridline", 28: "circle on the 200 gridline",
         30: "circle on the 250 gridline", 37: "triangle on the 100 gridline", 40: "triangle on the 200 gridline, base touching the square below",
         42: "triangle, top of the stack of three symbols on the 250 gridline", 49: "square on the 100 gridline",
         54: "square on the 200 gridline, under the triangle", 56: "square, bottom of the stack of three on the 250 gridline",
         61: "triangle-down on the 50 gridline", 66: "triangle-down on the 150 gridline",
         31: "triangle-up on the left frame (x about 0), third of the stack; outline merged with neighbours",
         34: "triangle-up whose apex runs into the 0 gridline; overlaps the square at u 910",
         15: "circle drawn left of the frame (x below 0)", 60: "second triangle-down at the same x as the one on the 0 gridline",
         41: "triangle sitting on the square below it"}
B3_P2_B = {31: 4, 34: 4}


def load_markers(name, ovr, b3, b3b):
    rows = list(csv.DictReader(open(work / name, encoding="utf-8-sig", newline="")))
    out = []
    for i, r in enumerate(rows):
        u, v = float(r["u_ref"]), float(r["v_ref"])
        bu = bv = 2
        note = r.get("note", "") or ""
        if i in ovr:
            u, v, bu, bv, n2 = ovr[i]
            note = n2
        elif i in b3:
            bu = bv = b3b.get(i, 3)
            note = b3[i]
        out.append(dict(panel=r["panel"], series_id=r["series_id"], symbol=r["symbol"], u=u, v=v, bu=bu, bv=bv, note=note))
    return out


def write_points(path, rows):
    cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def marker_rows(markers, panel):
    rows = []
    by = {}
    for m in markers:
        by.setdefault(m["series_id"], []).append(m)
    for sid, ms in by.items():
        ms.sort(key=lambda m: (m["u"], m["v"]))
        for k, m in enumerate(ms, 1):
            rows.append(dict(figure_id=FIG, panel=panel, series_id=sid, point_kind="marker", sequence=k,
                             pixel_u=f"{m['u']:.1f}", pixel_v=f"{m['v']:.1f}", u_bound_px=m["bu"], v_bound_px=m["bv"],
                             symbol=m["symbol"], note=m["note"]))
    return rows


# ---------------- panel 2: markers only (no drawn lines in the lower panel)
m2 = load_markers("refined-p2.csv", OVR_P2, B3_P2, B3_P2_B)
rows2 = marker_rows(m2, 2)
write_points(root / "points-p2.csv", rows2)
print("points-p2.csv:", len(rows2), "marker rows")

# ---------------- panel 1: markers, then traces and features from the tracks
m1 = load_markers("refined-p1.csv", OVR_P1, B3_P1, {})
rows1 = marker_rows(m1, 1)
write_points(work / "markers-p1.csv", rows1)

cmd = [PY, str(helpers / "sample_lines.py"), str(image), str(root / "cal-p1" / "calibration.json"),
       str(work / "markers-p1.csv"), str(work / "lines-p1.csv")]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
print(res.stdout.strip(), res.stderr.strip()[-800:])
line_rows = list(csv.DictReader(open(work / "lines-p1.csv", encoding="utf-8", newline="")))
# by-eye overrides of line features (series, sequence) -> (u, v, bu, bv, note)
FEAT_OVR = {
    ("n3815", 2): (976.2, 1440.8, 6, 6, "peak of the drawn line lies under the circle symbol at x about 39 (the line enters from the lower left and leaves to the lower right); position taken as the symbol centre, bound = symbol half-size"),
}
for r in line_rows:
    key = (r["series_id"], int(r["sequence"]))
    if r["point_kind"] == "feature" and key in FEAT_OVR:
        u, v, bu, bv, note = FEAT_OVR[key]
        r.update(pixel_u=f"{u:.1f}", pixel_v=f"{v:.1f}", u_bound_px=bu, v_bound_px=bv, note=note)
rows1_all = rows1 + line_rows
write_points(root / "points-p1.csv", rows1_all)
print("points-p1.csv:", len(rows1), "markers,", sum(1 for r in line_rows if r["point_kind"] == "trace"), "trace samples,",
      sum(1 for r in line_rows if r["point_kind"] == "feature"), "features")
sys.exit(0)

cal = json.load(open(root / "cal-p1" / "calibration.json", encoding="utf-8"))
ax = cal["ax"]
series = ["n4695", "n3815", "n2934", "n1761", "n741"]
# tracking parameters per series: start a little before the first marker, end at the 250 gridline
TRACK = {
    "n4695": dict(u0=800, v0=1786, u1=2232, tol=12, slope0=-1.8),
    "n3815": dict(u0=808, v0=1856, u1=2232, tol=12, slope0=-2.0),
    "n2934": dict(u0=810, v0=2027, u1=2232, tol=12, slope0=-2.2),
    "n1761": dict(u0=812, v0=2185, u1=2232, tol=12, slope0=-2.4),
    "n741": dict(u0=810, v0=2322, u1=2232, tol=12, slope0=-1.8),
}
tracks = {}
for sid in series:
    p = TRACK[sid]
    out = work / f"track-{sid}.csv"
    cmd = [PY, str(helpers / "trace2.py"), str(image), str(work / "markers-p1.csv"),
           sid, str(out), "--u0", str(p["u0"]), "--v0", str(p["v0"]), "--u1", str(p["u1"]), "--tol", str(p["tol"]),
           "--slope0", str(p["slope0"]), "--maxgap", "50"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout.strip(), res.stderr.strip()[-500:])
    tracks[sid] = [dict(u=float(r["u"]), v=float(r["v"]), t=float(r["thickness"]), s=r["state"])
                   for r in csv.DictReader(open(out, encoding="utf-8", newline=""))]


def u_of_x(x, v):
    return (x - ax[1] * v - ax[2]) / ax[0]


def ink_near(tr, u, within):
    best = None
    for r in tr:
        if r["s"] == "ink" and abs(r["u"] - u) <= within:
            d = abs(r["u"] - u)
            if best is None or d < best[0]:
                best = (d, r)
    return best[1] if best else None


def shares_ink(sid, r):
    """other series whose track at the same column lies within the summed half thicknesses + 2 px."""
    others = []
    for o in series:
        if o == sid:
            continue
        q = ink_near(tracks[o], r["u"], 1)
        if q and abs(q["v"] - r["v"]) <= (q["t"] + r["t"]) / 2 + 2:
            others.append(o)
    return others


trace_rows = []
feat_rows = []
gaps = {}
for sid in series:
    tr = tracks[sid]
    ink = [r for r in tr if r["s"] == "ink"]
    first, last = ink[0], ink[-1]
    # samples every 5 thousandths at x = 12.5, 17.5, ... (never on a vertical gridline)
    seq = 0
    x = 7.5
    vprev = first["v"]
    while True:
        u = u_of_x(x, vprev)
        if u > last["u"] + 4:
            break
        r = ink_near(tr, u, 2) or ink_near(tr, u, 8)
        if r is None or u < first["u"] - 4:
            gaps.setdefault(sid, []).append(x)
            x += 5
            continue
        vprev = r["v"]
        seq += 1
        b = max(2, (r["t"] + 1) // 2)
        sh = shares_ink(sid, r)
        note = f"drawn line sampled near x={x:g}"
        bu = 2
        if sh:
            note += "; shares ink with " + ",".join(sh) + " at this column (bound widened to the full thickness)"
            b = r["t"]
        if r["t"] >= 16:
            note += "; thick run (line over a symbol or another line)"
        trace_rows.append(dict(figure_id=FIG, panel=1, series_id=sid, point_kind="trace", sequence=seq,
                               pixel_u=f"{r['u']:.1f}", pixel_v=f"{r['v']:.1f}", u_bound_px=bu, v_bound_px=b, symbol="", note=note))
        x += 5
    # features: first ink, peak of the drawn line (smallest v), last ink
    peak = min(ink, key=lambda r: r["v"])
    for k, (r, what) in enumerate([(first, "first point of the drawn line"), (peak, "peak of the drawn line (highest point of the ink track)"),
                                   (last, "last point of the drawn line")], 1):
        b = max(2, (r["t"] + 1) // 2)
        feat_rows.append(dict(figure_id=FIG, panel=1, series_id=sid, point_kind="feature", sequence=k,
                              pixel_u=f"{r['u']:.1f}", pixel_v=f"{r['v']:.1f}", u_bound_px=3, v_bound_px=b, symbol="", note=what))

rows1_all = rows1 + trace_rows + feat_rows
write_points(root / "points-p1.csv", rows1_all)
print("points-p1.csv:", len(rows1), "markers,", len(trace_rows), "trace samples,", len(feat_rows), "features")
for sid, g in gaps.items():
    print(f"  {sid}: no ink within 8 px of the sample column at x = {g}")
