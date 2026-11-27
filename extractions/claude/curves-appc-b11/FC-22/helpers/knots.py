import sys, json
sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(sys.argv[2], sys.argv[3])
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for k in s[ax]:
        ic = k["ink_check"]
        print(ax, k["value"], "err", k["location_error_px"], "found", len(ic.get("found", [])), "/", ic.get("positions"),
              "span", ic.get("span_fraction"), "inkoff", ic.get("ink_line_offset_px"), "scat", ic.get("ink_scatter_px"), k.get("reason", ""))
json.dump(s, open(sys.argv[4], "w"), indent=1)
