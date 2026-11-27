"""Builds points-p1.csv from helpers/readings.csv: one marker row per plotted symbol, sequence
1 up in order of increasing horizontal motion (the order of the readings in a test; on this
sideways page, decreasing pixel_v). Usage: python build_points.py readings.csv points-p1.csv"""
import csv, json, sys

rows = list(csv.DictReader(open(sys.argv[1])))
cal = json.load(open('cal-p1/calibration.json'))
ax = cal['ax']
out = []
for s in ['n26p5psi', 'n13p8psi', 'n10p2psi', 'n6p6psi', 'n5p1psi', 'n3p4psi']:
    rs = [r for r in rows if r['series_id'] == s]
    rs.sort(key=lambda r: ax[0] * float(r['pixel_u']) + ax[1] * float(r['pixel_v']))
    for k, r in enumerate(rs, 1):
        note = ('reader id %s; ' % r['id']) + (r['note'] or '')
        out.append(dict(figure_id='FC-7C', panel=1, series_id=s, point_kind='marker', sequence=k,
                        pixel_u=r['pixel_u'], pixel_v=r['pixel_v'], u_bound_px=r['u_bound_px'],
                        v_bound_px=r['v_bound_px'], symbol=r['symbol'], note=note.rstrip('; ')))
w = csv.DictWriter(open(sys.argv[2], 'w', newline=''), fieldnames=list(out[0].keys()))
w.writeheader()
w.writerows(out)
print('wrote', len(out))
