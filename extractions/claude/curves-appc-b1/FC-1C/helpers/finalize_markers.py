"""Merge the refined marker centers with the by-eye overrides into points-p<n>.csv (markers only).

Rule: where the symmetry refinement moved a center by more than 3 px from the by-eye read
(clutter pulls the score toward a neighbour), the by-eye value from the zoomed crop is kept;
otherwise the refined value is used. Explicit overrides come from zoom-6 crops.
"""
import csv, sys
src, dst = sys.argv[1], sys.argv[2]
overrides = {}
if len(sys.argv) > 3:
    for r in csv.DictReader(open(sys.argv[3], newline='')):
        overrides[(r['series_id'], int(r['sequence']))] = r
cols = ['figure_id', 'panel', 'series_id', 'point_kind', 'sequence', 'pixel_u', 'pixel_v',
        'u_bound_px', 'v_bound_px', 'symbol', 'note']
w = csv.writer(open(dst, 'w', newline=''))
w.writerow(cols)
for r in csv.DictReader(open(src, newline='')):
    u, v = int(r['pixel_u']), int(r['pixel_v'])
    ru, rv = int(r['rough_u']), int(r['rough_v'])
    note = r['note']
    bu = bv = int(r['u_bound_px'])
    key = (r['series_id'], int(r['sequence']))
    if key in overrides:
        o = overrides[key]
        u, v = int(o['u']), int(o['v'])
        bu = bv = max(bu, int(o['bound']))
        if o['note']:
            note = (note + '; ' if note else '') + o['note']
    elif abs(u - ru) > 3 or abs(v - rv) > 3 or float(r['score']) < 0:
        u, v = ru, rv
        bu = bv = max(bu, 3)
    r2 = [r['figure_id'], r['panel'], r['series_id'], 'marker', r['sequence'], u, v, bu, bv,
          r['symbol'], note]
    w.writerow(r2)
