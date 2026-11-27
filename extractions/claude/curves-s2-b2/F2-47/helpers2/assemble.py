"""Write out/F2-47/points-p1.csv from the automated samples (work/auto-samples.csv) and the points
read by hand on the zoomed crops (start of both traces, x = 0.25 in, ends, features).

Every hand point below was read on crops3/*.png and the row/column run listings (rows.py, cols.py);
the comment on each says where it comes from. Bounds follow rule 7 (half the line thickness across
the line; the dashed line widened along the line by half its dash gap); features add the
uncertainty of the feature's location along the line.
"""
import csv, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import ROOT

W = ROOT + 'out/F2-47/work/'
cl = {}
for fn, k in (('solid-cl.csv', 'lpt91'), ('dash-cl.csv', 'lpt101')):
    cl[k] = {int(r['u']): float(r['center']) for r in csv.DictReader(open(W + fn))}
auto = list(csv.DictReader(open(W + 'auto-samples.csv')))

RT = 'the two traces run side by side and touch from about 0.07 to 0.29 in (about 95 to 240 lb)'
trace = {
 'lpt91': [
  (505, 3239, 4, 4, 'start of the ink at the corner of the frame (x about 0); its first pixels merge with the axis lines'),
  (580, 3078, 4.5, 4.5, 'target 0.25 in (sampled at 0.26 to stay clear of the dashed ink); ' + RT + '; the dashed line ends a dash 6 px to the left here; bound widened'),
 ],
 'lpt101': [
  (506, 3215, 8, 10, 'start of the visible ink: the first dash meets the left frame line here and only its right edge shows (the sample is on that ink; the dash center is about 3 px further left, inside the bound); below this it is hidden in the 9 px axis line, toward the origin'),
  (584, 3055.5, 8.6, 9.4, 'target 0.25 in falls in a dash gap: sampled 3 columns inside the start of the next dash (x about 0.27); ' + RT + '; LPT No. 91 ink 7 px below'),
 ]}
ends = {
 'lpt91': (2638, 2103, 4, 4, 'end of the ink: the trace runs into the right frame line (x = 7) and does not continue past it; also serves as the 7.0 in sample'),
 'lpt101': (2353, 2259, 8, 8, 'end of the ink: the last dash ends touching the underside of LPT No. 91 (solid) at about 6.05 in; no dashed ink beyond it'),
}
feats = {
 'lpt91': [
  ('first', 505, 3239, 4, 4, 'ink starts at the corner of the frame (x about 0, load about 0); its first pixels merge with the axis lines'),
  ('knee', 656, 3021.5, 10, 5, 'end of the initial rise: the trace bends onto the plateau near 0.5 in (gradual bend, located within about 10 px along the line)'),
  ('knee', 762, 3015.5, 12, 5, 'end of the plateau (flat from about 0.52 to 0.85 in): the trace starts to rise again; gradual, located within about 12 px'),
  ('knee', 1716, 2547, 6, 5, 'minor kink just before the x = 4 grid line: the slope drops to about half for some 0.15 in'),
  ('knee', 2026, 2412, 5, 5, 'minor kink: start of a small step up (about 20 lb) across the x = 5 grid line'),
  ('knee', 2050, 2394.5, 6, 5, 'minor kink: end of that small step, the trace flattens again'),
  ('knee', 2379, 2224.5, 8, 5, 'onset of the steep step near 6.1 in (the trace already steepens gradually from about 6.05 in, where the dashed line ends)'),
  ('knee', 2401, 2194, 4, 5, 'end of the steep step near 6.2 in: sharp kink, the trace flattens'),
  ('peak', 2638, 2103, 4, 4, 'maximum of the trace: at its last point, where it runs into the right frame line (x = 7); the load still rises there'),
  ('last', 2638, 2103, 4, 4, 'end of the ink at the right frame line (x = 7)'),
 ],
 'lpt101': [
  ('first', 506, 3215, 8, 10, 'lowest visible ink of the first dash, where it meets the left frame line; it may continue hidden in the axis line toward the origin'),
  ('knee', 663, 2962.5, 9, 8, 'end of the steep initial rise: bend between two dashes, located at the start of the dash after it (x about 0.54)'),
  ('knee', 753, 2937, 14, 7, 'local maximum of the hump (flat top from about u 740 to 762, x 0.79 to 0.86); the arrow of the LPT No. 101 label points at this dash; this is not the peak of the trace'),
  ('knee', 941, 2970, 25, 7, 'local minimum after the hump (flat bottom from about u 926 to 975, x 1.39 to 1.55), just after the crossing with LPT No. 91'),
  ('peak', 2353, 2259, 8, 8, 'maximum of the trace: at its last point (about 6.05 in), touching LPT No. 91'),
  ('last', 2353, 2259, 8, 8, 'end of the ink: the last dash ends touching the underside of LPT No. 91 (solid); no dashed ink beyond it'),
 ]}

rows = []
for sid in ('lpt91', 'lpt101'):
    seq = 0
    for u, v, bu, bv, note in trace[sid]:
        seq += 1
        rows.append(['F2-47', 1, sid, 'trace', seq, u, v, bu, bv, '', note])
    for r in auto:
        if r['series'] != sid: continue
        seq += 1
        note = f"target {float(r['x_target']):.2f} in"
        extra = r['note']
        if r['seg'] == 'D7':
            extra = ('at the target column the arrowhead of the LPT No. 101 label is merged on the dash: sampled '
                     'just to the right, where the dash is clear and the arrowhead ink is separate above it')
        if extra: note += '; ' + extra
        if r['seg'] == 'D7':
            pass
        elif r['seg'].startswith('D') and abs(float(r['dx'])) > 0.012:
            note += '; target falls in a dash gap or on a grid line: sampled on the nearest clean ink'
        elif not r['seg'].startswith('D') and abs(float(r['dx'])) > 0.012:
            note += '; target on a grid line: sampled on the nearest clean ink beside it'
        rows.append(['F2-47', 1, sid, 'trace', seq, int(r['u']), float(r['v']), float(r['bu']), float(r['bv']), '', note])
    u, v, bu, bv, note = ends[sid]
    seq += 1
    rows.append(['F2-47', 1, sid, 'trace', seq, u, v, bu, bv, '', note])
    for k, (role, u, v, bu, bv, note) in enumerate(feats[sid], 1):
        if v is None: v = cl[sid][u]
        rows.append(['F2-47', 1, sid, 'feature', k, u, v, bu, bv, '', role + ': ' + note])
with open(ROOT + 'out/F2-47/points-p1.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['figure_id', 'panel', 'series_id', 'point_kind', 'sequence', 'pixel_u', 'pixel_v', 'u_bound_px', 'v_bound_px', 'symbol', 'note'])
    w.writerows(rows)
from collections import Counter
print(Counter((r[2], r[3]) for r in rows))
