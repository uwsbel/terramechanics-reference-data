"""Print the piecewise knots of a calibration directory with their ink checks (reads tools/ without changing it)."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import calibrate_axes as ca
cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
s = ca.knots_summary(X, Y)
for ax in ("x", "y", "rejected_x", "rejected_y"):
    print(ax)
    for kn in s[ax]:
        ch = kn["ink_check"]
        print(f"  {kn['value']:>6g} s0={kn['s0_px']:8.2f} tilt={kn['tilt']:+.5f} err={kn['location_error_px']:.2f} "
              f"found={len(ch.get('found', []))}/{ch.get('positions')} span={ch.get('span_fraction')} "
              f"inkoff={ch.get('ink_line_offset_px')} scat={ch.get('ink_scatter_px')} aside={ch.get('set_aside')} {kn.get('reason','')}")
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(s, indent=1), encoding="utf-8")
