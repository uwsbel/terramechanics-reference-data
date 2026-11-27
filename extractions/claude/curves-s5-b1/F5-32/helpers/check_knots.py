"""Run the ink check of tools/calibrate_axes.py (piecewise_maps with the page image) on a calibration
directory and print which lines are verified knots and which are rejected, with the reasons.
usage: check_knots.py <tools_dir> <cal_dir> <image> [<out.json>]"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca  # noqa: E402

cal, X, Y = ca.piecewise_maps(sys.argv[2], sys.argv[3])
s = ca.knots_summary(X, Y)
for ax in ("x", "y"):
    for kn in s[ax]:
        ck = kn["ink_check"]
        print(f"  {ax} {kn['value']:>7g} verified  err {kn['location_error_px']:.2f} px  anchors {kn['n_anchors']}  "
              f"found {len(ck.get('found', []))}/{ck.get('positions')}  span {ck.get('span_fraction', '-')}  "
              f"ink line offset {ck.get('ink_line_offset_px', ck.get('median_px', '-'))}")
    for kn in s["rejected_" + ax]:
        print(f"  {ax} {kn['value']:>7g} REJECTED  {kn['reason']}")
if len(sys.argv) > 4:
    json.dump(s, open(sys.argv[4], "w", encoding="utf-8"), indent=1)
