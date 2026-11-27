"""Print the piecewise knots of a calibration dir with their ink checks (reads tools/calibrate_axes.py, does not modify it)."""
import sys, json, importlib.util
from pathlib import Path
ws = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("cal", ws / "tools" / "calibrate_axes.py")
cal = importlib.util.module_from_spec(spec); spec.loader.exec_module(cal)
c, X, Y = cal.piecewise_maps(sys.argv[1], sys.argv[2])
s = cal.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for k in s[ax]:
        ic = k["ink_check"]
        print(ax, k["value"], "s0", k["s0_px"], "tilt", k["tilt"], "err", k["location_error_px"],
              "found", len(ic.get("found", [])), "/", ic.get("positions"), "span", ic.get("span_fraction"),
              "inkoff", ic.get("ink_line_offset_px"), "scat", ic.get("ink_scatter_px"), "aside", ic.get("set_aside"), k.get("reason", ""))
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(s, indent=1), encoding="utf-8")
