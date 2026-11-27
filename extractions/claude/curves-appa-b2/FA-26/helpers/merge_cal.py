"""Build cal-p1 from two runs of tools/calibrate_axes.py detect on page 54 (Fig. A-26).

The percent lines 90, 80, 70 and 60 are drawn only above the grain-size parameter table (u 701 to
1210, v 2560 to 3770 cover them); over the full frame the tool fitted them partly on the table's
border and text (90 found 4.5 px off at the bottom and rejected by the ink check). They are taken
from a second run whose box stops above the table (v 1207 to 2452), where they are found in 10 of 10
bands. Every other line is from the full-frame run. An anchor row anchors one axis only where its
other line comes from the other run (blank value, which calibrate_axes.AxisKnots skips)."""
import csv, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import calibrate_axes as ca

base = Path(__file__).resolve().parents[1]
full, upper, out = base / "cal-full-box", base / "cal-upper-box", base / "cal-p1"
FROM_UPPER = {90.0, 80.0, 70.0, 60.0}
rd = lambda d: list(csv.DictReader((d / "anchors.csv").open(encoding="utf-8-sig", newline="")))
cf = json.loads((full / "calibration.json").read_text(encoding="utf-8"))
cu = json.loads((upper / "calibration.json").read_text(encoding="utf-8"))
rows = []
for r in rd(full):
    if float(r["y_value"]) in FROM_UPPER:
        r["y_value"], r["y_source"] = "", ""
    rows.append(r)
for r in rd(upper):
    if float(r["y_value"]) in FROM_UPPER:
        r["x_value"], r["x_source"] = "", ""
        r["y_source"] = r["y_source"] + " (box above the table, 565 1207 2042 2452)"
        rows.append(r)
out.mkdir(parents=True, exist_ok=True)
with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader(); w.writerows(rows)

def fit(col, tr):
    A = [(float(r["u"]), float(r["v"]), ca.forward(tr, float(r[col]))) for r in rows if r[col].strip()]
    U = np.array([[a, b, 1.0] for a, b, _ in A]); Z = np.array([z for *_, z in A])
    c, *_ = np.linalg.lstsq(U, Z, rcond=None); res = Z - U @ c
    return c.tolist(), float(np.sqrt((res ** 2).mean())), float(np.abs(res).max()), len(A)

ax, rx, mx, nx = fit("x_value", "log10")
ay, ry, my, ny = fit("y_value", "linear")
vl = [l for l in cf["vertical_lines"] if l["y_value"] not in FROM_UPPER] + \
     [dict(l, source=l["source"] + " (box above the table)") for l in cu["vertical_lines"] if l["y_value"] in FROM_UPPER]
vl.sort(key=lambda l: l["u_at_v0"])
cal = dict(cf)
cal.update({"box": cf["box"], "box_upper": cu["box"], "ax": ax, "ay": ay,
            "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
            "rms_residual_x": rx, "rms_residual_y": ry, "max_residual_x": mx, "max_residual_y": my,
            "n_anchors": len(rows), "n_anchors_x": nx, "n_anchors_y": ny, "vertical_lines": vl,
            "merge_note": (__doc__ or "").strip().replace("\n", " ")})
(out / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(f"{len(rows)} rows; x anchors {nx}, rms {rx:.4f} max {mx:.4f} (log10); y anchors {ny}, rms {ry:.3f} max {my:.3f} (percent)")
