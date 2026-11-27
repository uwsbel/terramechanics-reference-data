#!/bin/sh
# Zoom-4 tiles of both panels for marker reading (helper, run from the FC-1D workspace).
PY="<local path>"
T=out/FC-1D/crops/tiles; mkdir -p $T
for u0 in 540 860 1180 1500 1820; do
  u1=$((u0+320))
  for v0 in 1400 1720 2040 2360 2680; do
    v1=$((v0+320)); [ $v1 -gt 2940 ] && v1=2940
    $PY tools/plot_grid.py crop packet/p0119.png --box $u0 $v0 $u1 $v1 --out $T/p1-u${u0}-v${v0}.png --zoom 4 --step 20
  done
  for v0 in 2920 3240; do
    v1=$((v0+320))
    $PY tools/plot_grid.py crop packet/p0119.png --box $u0 $v0 $u1 $v1 --out $T/p2-u${u0}-v${v0}.png --zoom 4 --step 20
  done
done
