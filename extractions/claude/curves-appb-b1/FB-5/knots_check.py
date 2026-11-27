"""Print the piecewise knots of a calibration directory and their ink checks (tools/calibrate_axes.py).
Usage: python knots_check.py <cal_dir> <image> [out.json]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from calibrate_axes import piecewise_maps, knots_summary
cal, X, Y = piecewise_maps(sys.argv[1], sys.argv[2])
s = knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    for k in s[ax]:
        c = k["ink_check"]
        print(f"{ax:10s} {k['value']:>5g} s0 {k['s0_px']:9.2f} tilt {k['tilt']:+.5f} err {k['location_error_px']:.2f} n_anch {k['n_anchors']} "
              f"found {len(c.get('found', []))}/{c.get('positions')} median {c.get('median_px', '')} ink_off {c.get('ink_line_offset_px', '')} scat {c.get('ink_scatter_px', '')} {k.get('reason', '')}")
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(s, indent=1), encoding="utf-8")
