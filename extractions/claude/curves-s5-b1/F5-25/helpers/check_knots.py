"""Run the tool's piecewise maps with the page image on each cal-p<n>/ and print the ink check of every line."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import calibrate_axes as ca
image = sys.argv[2]
for d in sys.argv[3:]:
    cal, X, Y = ca.piecewise_maps(d, image)
    s = ca.knots_summary(X, Y)
    Path(d, "knots.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
    print(d)
    for ax in ("x", "y"):
        for kn in s[ax]:
            c = kn["ink_check"]
            print(f"  {ax} {kn['value']:>6g} ok  err {kn['location_error_px']:.2f} px  anchors {kn['n_anchors']:3d}  ink {len(c['found'])}/{c['positions']} span {c.get('span_fraction')} ends {c.get('ink_line_offset_px')} scatter {c.get('ink_scatter_px')}")
        for kn in s["rejected_" + ax]:
            print(f"  {ax} {kn['value']:>6g} REJECTED {kn['reason']}")
