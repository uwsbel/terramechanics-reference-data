"""Reader helper: print the piecewise knots of a calibration directory, with the ink check of each line.
usage: knots_check.py <tools_dir> <cal_dir> <image>"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca  # noqa: E402

cal, X, Y = ca.piecewise_maps(sys.argv[2], sys.argv[3])
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    print(ax)
    for k in s[ax]:
        ch = k["ink_check"]
        print(f"  {k['value']:>8g} s0={k['s0_px']:9.2f} tilt={k['tilt']:+.5f} err={k['location_error_px']:.2f} n_anch={k['n_anchors']}"
              f" found={len(ch.get('found', []))}/{ch.get('positions')} span={ch.get('span_fraction')} ink_off={ch.get('ink_line_offset_px')}"
              f" scat={ch.get('ink_scatter_px')} {k.get('reason', '')}")
