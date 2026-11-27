"""Print the ink check of each line of a calibration directory (uses tools/calibrate_axes.py, unmodified)."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca
cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for kn in s[ax]:
        ck = kn["ink_check"]
        print(f"{ax:10s} {kn['value']:>6g} err {kn['location_error_px']:5.2f} n_anch {kn['n_anchors']:2d} "
              f"found {len(ck.get('found', []))}/{ck.get('positions')} span {ck.get('span_fraction')} "
              f"inkline {ck.get('ink_line_offset_px')} scat {ck.get('ink_scatter_px')} aside {ck.get('set_aside')} {kn.get('reason','')}")
