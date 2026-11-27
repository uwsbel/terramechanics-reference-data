"""Symbol centers from outer extents, by symbol type (reader's aid; every center is checked by eye).

Reads extents.csv (from extents.py, masked extents m_*) and an overrides CSV (id, u0, v0, u1, v1,
uc, vc, note: any non-empty field replaces the computed one), applies the center rule per symbol
and writes centers.csv. Rules, for the page as scanned (load to the left, motion up):
  circle, square, diamond: center of the outer box
  triangle (apex to the left on the page, base on the right): centroid, u = u1 - h/3, v = mid
  star (one point to the left): u = u0 + R, R = (u1 - u0)/1.809; v = mid
  quarter-circle (straight edges on top and right, corner top-right): area centroid,
      u = u1 - 0.4244 (u1 - u0), v = v0 + 0.4244 (v1 - v0)
"""
import csv, sys

ext = {r['id']: r for r in csv.DictReader(open(sys.argv[1]))}
ov = {}
if len(sys.argv) > 3:
    for r in csv.DictReader(open(sys.argv[3])):
        ov[r['id']] = r
out = []
for i, r in ext.items():
    u0, v0, u1, v1 = (float(r[k]) for k in ('m_u0', 'm_v0', 'm_u1', 'm_v1'))
    o = ov.get(i, {})
    u0 =float(o['u0']) if o.get('u0') else u0
    v0 = float(o['v0']) if o.get('v0') else v0
    u1 = float(o['u1']) if o.get('u1') else u1
    v1 = float(o['v1']) if o.get('v1') else v1
    s = r['symbol']
    if s in ('circle', 'square', 'diamond'):
        uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
    elif s == 'triangle-up':
        uc, vc = u1 - (u1 - u0) / 3, (v0 + v1) / 2
    elif s == 'star':
        uc, vc = u0 + (u1 - u0) / 1.809, (v0 + v1) / 2
    elif s == 'quarter-circle':
        uc, vc = u1 - 0.4244 * (u1 - u0), v0 + 0.4244 * (v1 - v0)
    else:
        raise SystemExit('unknown symbol ' + s)
    if o.get('uc'):
        uc = float(o['uc'])
    if o.get('vc'):
        vc = float(o['vc'])
    out.append(dict(id=i, series_id=r['series'], symbol=s, u0=u0, v0=v0, u1=u1, v1=v1,
                    uc=round(uc, 1), vc=round(vc, 1), note=o.get('note', '')))
w = csv.DictWriter(open(sys.argv[2], 'w', newline=''), fieldnames=list(out[0].keys()))
w.writeheader()
w.writerows(out)
print('wrote', len(out))
