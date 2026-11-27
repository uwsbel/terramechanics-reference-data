# helper: tile crops of both panels, zoom 3, grid every 25 px
P=<local path>
for u in 790 1290 1790; do for v in 1070 1520 1970 2420; do
  u1=$((u+500)); v1=$((v+450)); [ $u1 -gt 2310 ] && u1=2310; [ $v1 -gt 2860 ] && v1=2860
  $P tools/plot_grid.py crop packet/p0125.png --box $u $v $u1 $v1 --out out/FC-3C/crops/p1_u${u}_v${v}.png --zoom 3 --step 25
done; done
for u in 790 1290 1790; do
  u1=$((u+500)); [ $u1 -gt 2310 ] && u1=2310
  $P tools/plot_grid.py crop packet/p0125.png --box $u 2960 $u1 3590 --out out/FC-3C/crops/p2_u${u}.png --zoom 3 --step 25
done
