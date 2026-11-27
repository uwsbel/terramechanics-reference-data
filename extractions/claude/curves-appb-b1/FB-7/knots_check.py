"""Print the piecewise knots of a calibration directory and their ink checks (uses tools/calibrate_axes.py as is)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(sys.argv[1], sys.argv[2])
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for k in s[ax]:
        c = k["ink_check"]
        print(ax, k["value"], "err", k["location_error_px"], "n", k["n_anchors"], "tilt", k["tilt"],
              {kk: c.get(kk) for kk in ("positions", "median_px", "span_fraction", "ink_line_offset_px", "ink_scatter_px", "set_aside")},
              "found", len(c.get("found", [])), "missing", len(c.get("missing", [])), k.get("reason", ""))
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(s, indent=1), encoding="utf-8")
