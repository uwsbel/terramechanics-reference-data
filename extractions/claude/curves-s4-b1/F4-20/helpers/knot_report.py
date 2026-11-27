"""Print the ink check of every line of a calibration directory (uses tools/calibrate_axes.py, unmodified)."""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3] / "tools"))
import calibrate_axes as ca

cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for kn in s[ax]:
        c = kn["ink_check"]
        print(f"{ax:11s} {kn['value']:>6g} s0 {kn['s0_px']:8.2f} tilt {kn['tilt']:+.5f} err {kn['location_error_px']:.2f} px "
              f"found {len(c.get('found', []))}/{c.get('positions')} ink-line offsets {c.get('ink_line_offset_px')} "
              f"scatter {c.get('ink_scatter_px')} set aside {c.get('set_aside')} {kn.get('reason', '')}")
