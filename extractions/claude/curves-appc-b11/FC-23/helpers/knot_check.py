"""Print the ink check of every line of a calibration directory (uses tools/calibrate_axes.py, unmodified)."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import calibrate_axes as ca
cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for kn in s[ax]:
        c = kn["ink_check"]
        print(ax, kn["value"], "err_px", kn["location_error_px"], "tilt", kn["tilt"], "found", len(c.get("found", [])), "/", c.get("positions"),
              "span", c.get("span_fraction"), "ink_off", c.get("ink_line_offset_px"), "scatter", c.get("ink_scatter_px"), "aside", c.get("set_aside"), kn.get("reason", ""))
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(s, indent=1), encoding="utf-8")
