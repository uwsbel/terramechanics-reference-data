"""Print the piecewise knots of cal-p1 with the ink check (tools/calibrate_axes.py, read only)."""
import json, sys
sys.path.insert(0, "tools")
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps("out/F2-48/cal-p1", "packet/p0109.png")
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for k in s[ax]:
        print(ax, k)
