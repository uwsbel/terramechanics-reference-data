"""Print a native points file compactly. usage: show.py points-native.csv"""
import sys, csv
for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")):
    print(f"{r['series_id']:7s} {r['point_kind']:7s} {r['sequence']:>2s} u {float(r['pixel_u']):7.1f} v {float(r['pixel_v']):7.1f}"
          f"  x {float(r['x_native']):6.0f} y {float(r['y_native']):6.0f}  bx {float(r['x_read_bound']):4.0f} by {float(r['y_read_bound']):4.0f}  {r['note'][:60]}")
