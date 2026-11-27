"""Print the piecewise knots (verified and rejected lines) of a calibration directory."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca
cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for kn in s[ax]:
        ic = kn["ink_check"]
        print(ax, kn["value"], "s0", kn["s0_px"], "tilt", kn["tilt"], "err", kn["location_error_px"],
              "found", len(ic.get("found", [])), "/", ic.get("positions"), "span", ic.get("span_fraction"),
              "inkline", ic.get("ink_line_offset_px"), "scatter", ic.get("ink_scatter_px"), kn.get("reason", ""))
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(s, indent=1), encoding="utf-8")
