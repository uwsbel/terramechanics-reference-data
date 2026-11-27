"""Print the piecewise knots of cal-p1 and their ink checks (uses tools/calibrate_axes.py unchanged)."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
WS = HERE.parents[1]
sys.path.insert(0, str(WS / "tools"))
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(HERE / "cal-p1", WS / "packet" / "p0104.png")
s = ca.knots_summary(X, Y)
for k in ("x", "y", "rejected_x", "rejected_y"):
    for kn in s[k]:
        c = kn["ink_check"]
        print(k, kn["value"], "err", kn["location_error_px"], "n_anch", kn["n_anchors"], "pos", c.get("positions"),
              "found", len(c.get("found", [])), "span", c.get("span_fraction"), "ink_off", c.get("ink_line_offset_px"),
              "scat", c.get("ink_scatter_px"), "aside", c.get("set_aside"), kn.get("reason", ""))
(HERE / "cal-p1" / "knots.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
