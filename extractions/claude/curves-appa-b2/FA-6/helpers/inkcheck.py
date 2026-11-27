"""Print the ink check (D-025) of every line of a calibration directory, using the tool's own code (read-only import)."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import calibrate_axes as ca

cal_dir, image = sys.argv[1], sys.argv[2]
cal = json.loads((Path(cal_dir) / "calibration.json").read_text(encoding="utf-8"))
an = ca.load_anchors(cal_dir)
import numpy as np
from PIL import Image
gray = np.asarray(Image.open(image).convert("L"), dtype=float)
tx, ty = ca.axis_transforms(cal)
for name, col, src, grad, tr in (("x", "x_value", "x_source", cal["ax"][:2], tx), ("y", "y_value", "y_source", cal["ay"][:2], ty)):
    try:
        K = ca.AxisKnots(an, col, src, grad, gray, tr)
    except ValueError as e:
        print(name, "ERROR", e); continue
    for kn in K.knots:
        c = kn["check"]
        print(f"{name} {kn['value']:>6g} OK   err {kn['err']:.2f} px  ink_line_offset {c.get('ink_line_offset_px')} scatter {c.get('ink_scatter_px')} found {len(c.get('found', []))}/{c.get('positions')} set_aside {c.get('set_aside')}")
    for kn in K.rejected:
        c = kn["check"]
        print(f"{name} {kn['value']:>6g} REJ  {kn['reason']}  ink_line_offset {c.get('ink_line_offset_px')} found {len(c.get('found', []))}/{c.get('positions')}")
