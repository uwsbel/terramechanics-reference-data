"""Save the grid masks of the de-gridding aid as .npy: hline (ink on horizontal runs >= L px), vline
(ink on vertical runs >= L px). Usage: python masks.py [L]"""
import sys
import numpy as np
from PIL import Image
import fa22lib as L
sys.argv = [sys.argv[0]] + sys.argv[1:]
import importlib.util
spec = importlib.util.spec_from_file_location("dg", L.OUT / "helpers" / "degrid.py")
src = (L.OUT / "helpers" / "degrid.py").read_text(encoding="utf-8").split("g = np.asarray")[0]
ns = {}
exec(src, ns)
Lr = int(sys.argv[1]) if len(sys.argv) > 1 else 45
b = L.page() < 128
h = ns["win_any"](ns["win_all"](b, Lr, 1), Lr, 1) & b
v = ns["win_any"](ns["win_all"](b, Lr, 0), Lr, 0) & b
np.save(L.OUT / "helpers" / "hline.npy", h); np.save(L.OUT / "helpers" / "vline.npy", v)
print("saved", int(h.sum()), int(v.sum()))
