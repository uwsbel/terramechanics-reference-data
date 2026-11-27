"""Print the ink check of every line of a calibration directory (tools/calibrate_axes.py piecewise_maps)."""
import json, sys
sys.path.insert(0, sys.argv[3])
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(sys.argv[1], sys.argv[2])
S = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for k in S[ax]:
        c = k["ink_check"]
        extra = {kk: c[kk] for kk in ("median_px", "ink_line_offset_px", "ink_scatter_px", "span_fraction", "set_aside") if kk in c}
        print(f"{ax:10s} {k['value']:>5g} s0 {k['s0_px']:9.2f} tilt {k['tilt']:+.5f} err {k['location_error_px']:.2f} px "
              f"anchors {k['n_anchors']:3d} ink {len(c.get('found', []))}/{c.get('positions')} {extra} {k.get('reason','')}")
print("across x", S["across_x"], "across y", S["across_y"])
if len(sys.argv) > 4:
    json.dump(S, open(sys.argv[4], "w", encoding="utf-8"), indent=1)
