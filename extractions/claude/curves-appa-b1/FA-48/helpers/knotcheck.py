"""Print the ink check of every line of a calibration directory (piecewise map, D-025).
usage: knotcheck.py <tools_dir> <cal_dir> <image>"""
import json, sys
sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(sys.argv[2], sys.argv[3])
s = ca.knots_summary(X, Y)
print("rms x", cal["rms_residual_x"], "max x", cal["max_residual_x"], "rms y", cal["rms_residual_y"], "max y", cal["max_residual_y"])
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for k in s[ax]:
        c = k["ink_check"]
        print(ax, k["value"], "err", k["location_error_px"], "found", len(c.get("found", [])), "/", c.get("positions"),
              "span", c.get("span_fraction"), "ink_off", c.get("ink_line_offset_px"), "scatter", c.get("ink_scatter_px"),
              k.get("reason", ""))
