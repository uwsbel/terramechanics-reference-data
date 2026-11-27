"""Print the piecewise knots (D-025) of a calibration directory with their ink checks, using
tools/calibrate_axes.py unchanged (imported, not modified). Writes knots.json next to it."""
import json
import sys
from pathlib import Path

tools = Path(sys.argv[1])
sys.path.insert(0, str(tools))
import calibrate_axes as ca  # noqa: E402

cal_dir, image = sys.argv[2], sys.argv[3]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
S = ca.knots_summary(X, Y)
(Path(cal_dir) / "knots.json").write_text(json.dumps(S, indent=1), encoding="utf-8")
for ax in ("x", "y", "rejected_x", "rejected_y"):
    print(ax)
    for kn in S[ax]:
        ch = kn["ink_check"]
        extra = {k: ch[k] for k in ("median_px", "ink_line_offset_px", "ink_scatter_px", "span_fraction", "set_aside") if k in ch}
        print(f"  {kn['value']:>5g}  s0 {kn['s0_px']:9.2f}  tilt {kn['tilt']:+.5f}  err {kn['location_error_px']:.2f} px  "
              f"anchors {kn['n_anchors']}  found {len(ch.get('found', []))}/{ch.get('positions')}  {extra}  {kn.get('reason', '')}")
