"""Run the piecewise map's ink check of tools/calibrate_axes.py on a calibration directory and write
its knots summary (verified lines, rejected lines, location errors) to <cal_dir>/knots-check.json."""
import json
import sys
from pathlib import Path

tools = Path(sys.argv[3])
sys.path.insert(0, str(tools))
import calibrate_axes as ca  # noqa: E402

cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
summ = ca.knots_summary(X, Y)
(Path(cal_dir) / "knots-check.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
for ax in ("x", "y"):
    for kn in summ[ax]:
        ck = kn["ink_check"]
        print(f"{ax}={kn['value']:g}: verified, err {kn['location_error_px']} px, tilt {kn['tilt']}, anchors {kn['n_anchors']}, "
              f"ink at {len(ck.get('found', []))}/{ck.get('positions')} offsets {ck.get('ink_line_offset_px', ck.get('median_px'))} "
              f"scatter {ck.get('ink_scatter_px')} set aside {ck.get('set_aside')}")
    for kn in summ["rejected_" + ax]:
        print(f"{ax}={kn['value']:g}: REJECTED {kn['reason']}; {kn['ink_check']}")
