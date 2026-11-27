"""Report the piecewise knots of a calibration directory and their ink checks (reader helper, F5-31)."""
import sys
from pathlib import Path
ws = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ws / "tools"))
import calibrate_axes as ca

cal_dir, image = sys.argv[1], sys.argv[2]
cal, X, Y = ca.piecewise_maps(cal_dir, image)
for name, K in (("x", X), ("y", Y)):
    print(f"{name}: {len(K.knots)} verified, {len(K.rejected)} rejected")
    for kn in K.knots:
        c = kn["check"]
        print(f"  {name}={kn['value']:g} err {kn['err']:.2f} px; ink found {len(c.get('found', []))}/{c.get('positions')} "
              f"span {c.get('span_fraction')} offset {c.get('ink_line_offset_px')} scatter {c.get('ink_scatter_px')} set aside {c.get('set_aside')}")
    for kn in K.rejected:
        print(f"  REJECTED {name}={kn['value']:g}: {kn['reason']}")
