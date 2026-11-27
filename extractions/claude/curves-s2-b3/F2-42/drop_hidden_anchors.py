"""Remove anchors of a calibration directory that lie where a grid line is not drawn (hidden under the
key box), refit the affine map on the rest, and record what was removed in calibration.json.

usage: drop_hidden_anchors.py <cal_dir> <y_value> <x_value>[,<x_value>...] <note>

Written for Fig. 2-42 (F2-42): the 400 lb line is drawn only from the left frame (0 in) to the left
edge of the key box (about 1.18 in); its intersections with the 2 in and 3 in lines lie under the key,
where detect could only extrapolate the line's tilt measured on the visible stretch."""
import csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca

d = Path(sys.argv[1]); yv = float(sys.argv[2]); xs = [float(x) for x in sys.argv[3].split(",")]; note = sys.argv[4]
with (d / "anchors.csv").open(encoding="utf-8-sig", newline="") as f:
    rd = csv.DictReader(f); cols = rd.fieldnames; rows = list(rd)
keep = [r for r in rows if not (float(r["y_value"]) == yv and float(r["x_value"]) in xs)]
gone = [r for r in rows if r not in keep]
with (d / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(keep)
cal = json.loads((d / "calibration.json").read_text(encoding="utf-8"))
an = [{"x_value": float(r["x_value"]), "y_value": float(r["y_value"]), "u": float(r["u"]), "v": float(r["v"])} for r in keep]
ax, ay, rmsx, rmsy, maxx, maxy = ca.fit_affine(an)
cal.update({"ax": ax, "ay": ay, "x_per_px": float((ax[0] ** 2 + ax[1] ** 2) ** 0.5), "y_per_px": float((ay[0] ** 2 + ay[1] ** 2) ** 0.5),
            "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy, "n_anchors": len(keep)})
cal.setdefault("anchors_removed", []).extend([{**{k: r[k] for k in ("x_value", "y_value", "u", "v")}, "reason": note} for r in gone])
(d / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
print(f"removed {len(gone)} anchors; {len(keep)} left; x rms {rmsx:.4f} max {maxx:.4f}; y rms {rmsy:.3f} max {maxy:.3f}")
