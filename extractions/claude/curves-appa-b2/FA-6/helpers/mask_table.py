"""Write a copy of the page with the parameter table (and its white surround, where the grid is not printed)
set to white, for grid-line detection only. Pixel coordinates are unchanged (same size, nothing moved).
The table's edges otherwise pass for the 80 and 40 percent lines inside the table's height."""
import sys
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
u0, v0, u1, v1 = 1058, 2246, 1697, 3644   # measured on crops tab_tl, tab_tr, tab_bl, tab_br
im = Image.open(src).convert("L")
im.paste(255, (u0, v0, u1 + 1, v1 + 1))
im.save(dst)
print(f"masked u {u0}..{u1}, v {v0}..{v1} -> {dst}")
