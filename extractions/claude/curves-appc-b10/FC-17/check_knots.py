"""Helper (reader's own): load the piecewise maps of a calibration dir with the ink check and print a summary."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca
cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
s = ca.knots_summary(X, Y)
for ax in ("x", "y"):
    for kn in s[ax]:
        c = kn["ink_check"]
        print(ax, kn["value"], "err_px", kn["location_error_px"], "found", len(c.get("found", [])), "/", c.get("positions"),
              "span", c.get("span_fraction"), "ink_off", c.get("ink_line_offset_px"), "scatter", c.get("ink_scatter_px"))
    for kn in s["rejected_" + ax]:
        print("REJECTED", ax, kn["value"], kn.get("reason"))
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(s, indent=1), encoding="utf-8")
