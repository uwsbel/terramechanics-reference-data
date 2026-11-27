"""FA-22, reader Claude: keep each grid line's anchors on the stretch where the line is drawn.

The grain-size parameter table is printed over the lower left of the plot (page u 768..1367,
v 2238..3752). Inside it no grid line is drawn, and the lines x = 0.05, 0.1, 0.2, 0.5 mm and
y = 60, 70, 80, 90 percent are drawn only on one side of it. `calibrate_axes.py detect` intersects
every fitted line with every other, so it places anchors inside the table and on the far side of it
(x lines at the y = 100 frame, y lines at the x = 0.02 frame) by extrapolating each line's fit across
the table; the ink check then extrapolates the ink's line the same way and rejects lines that lie on
the ink where they are drawn (0.1, 0.5 mm; 60, 80, 90 percent). This helper
  1. drops every anchor inside the table (neither line is drawn there);
  2. for a line that crosses the table, blanks its value in the anchors beyond the table (the row stays
     an anchor of the other axis, whose line is drawn there), so the line is anchored and checked on
     its drawn stretch only;
  3. refits the diagnostic affine maps on what is kept.
The fitted lines themselves (positions and tilts from detect) are not changed.
Usage: python restrict_anchors.py <detect dir> <out dir>"""
import csv, json, sys, math
from pathlib import Path
import numpy as np

TABLE = (768.0, 2232.0, 1372.0, 3754.0)   # u0, v0, u1, v1: the table, measured on the page (crops table_*.png)

def inside(u, v):
    return TABLE[0] < u < TABLE[2] and TABLE[1] < v < TABLE[3]

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
cal = json.loads((src / "calibration.json").read_text(encoding="utf-8"))
with (src / "anchors.csv").open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
hidden_x = {r["x_value"] for r in rows if inside(float(r["u"]), float(r["v"]))}
hidden_y = {r["y_value"] for r in rows if inside(float(r["u"]), float(r["v"]))}
out, log = [], []
for r in rows:
    u, v = float(r["u"]), float(r["v"])
    if inside(u, v):
        log.append(f"dropped ({r['x_value']}, {r['y_value']}) at ({u}, {v}): inside the table")
        continue
    r = dict(r)
    if r["x_value"] in hidden_x and u < TABLE[0]:      # x line beyond the table, at the left frame
        log.append(f"x = {r['x_value']} not anchored at ({u}, {v}) (y = {r['y_value']} frame, across the table)")
        r["x_value"], r["x_source"] = "", ""
    if r["y_value"] in hidden_y and v > TABLE[3]:      # y line beyond the table, at the bottom frame
        log.append(f"y = {r['y_value']} not anchored at ({u}, {v}) (x = {r['x_value'] or '0.02'} frame, across the table)")
        r["y_value"], r["y_source"] = "", ""
    if r["x_value"] or r["y_value"]:
        out.append(r)
dst.mkdir(parents=True, exist_ok=True)
with (dst / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader(); w.writerows(out)
# diagnostic affine maps refitted on the kept anchors, each axis on the rows that anchor it (x in log10)
def fit(rs, col, tf):
    U = np.array([[float(r["u"]), float(r["v"]), 1.0] for r in rs])
    Z = np.array([tf(float(r[col])) for r in rs])
    a, *_ = np.linalg.lstsq(U, Z, rcond=None)
    res = Z - U @ a
    return a.tolist(), float(np.sqrt((res ** 2).mean())), float(np.abs(res).max())
rx = [r for r in out if r["x_value"]]; ry = [r for r in out if r["y_value"]]
cal["ax"], cal["rms_residual_x"], cal["max_residual_x"] = fit(rx, "x_value", math.log10)
cal["ay"], cal["rms_residual_y"], cal["max_residual_y"] = fit(ry, "y_value", float)
cal["x_per_px"], cal["y_per_px"] = float(np.hypot(*cal["ax"][:2])), float(np.hypot(*cal["ay"][:2]))
cal["n_anchors"] = len(out)
cal["reader_edit"] = ("anchors restricted to the drawn stretch of each line by out/FA-22/helpers/restrict_anchors.py "
                      f"(table u {TABLE[0]:g}..{TABLE[2]:g}, v {TABLE[1]:g}..{TABLE[3]:g}); affine refitted on the kept anchors; "
                      "line positions and tilts as detected")
(dst / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
(dst / "restrict-log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
print(f"{len(rows)} anchors in, {len(out)} rows out ({len(rx)} anchor x, {len(ry)} anchor y); "
      f"x rms {cal['rms_residual_x']:.4f} max {cal['max_residual_x']:.4f} (log10); y rms {cal['rms_residual_y']:.3f} max {cal['max_residual_y']:.3f}")
print("lines crossing the table: x", sorted(hidden_x, key=float), "y", sorted(hidden_y, key=float))
