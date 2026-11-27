"""Viewing/tracking aid: page ink (all of it, grid included) opened with a k x k square, i.e. only
strokes at least about k px thick survive (the curves are 8 to 10 px thick, grid lines 3 to 6 px in most places).
Writes thick.png (0 = thick ink). Usage: python thick.py [k]"""
import sys
import numpy as np
from PIL import Image, ImageFilter
import fa22lib as L
k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
im = Image.open(L.PAGE).convert("L")
er = im.filter(ImageFilter.MaxFilter(k))     # erode the dark ink
op = er.filter(ImageFilter.MinFilter(k))     # dilate back
op.save(L.OUT / "helpers" / "thick.png")
print("dark px", int((np.asarray(op) < 128).sum()))
