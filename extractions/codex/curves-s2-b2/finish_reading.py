from read_curves import *
from collections import Counter

DETAILS={
'F2-45':'''Printed identity: solid = Four-Inch Cylinder, LPT No. 95, Gp = 16.2; dotted = Four-Inch Footpad, LPT No. 79, Gp = 15.2. These match the supplied series IDs. No plotted markers or straight fit lines.

The page is sideways: penetration increases up and load left. Penetration labels run 0 through 7. Load labels checked against their own lines include 0, 25, 50, 75, 100, 150, 200 and 250; the intervening 25-lb subdivisions are drawn. Calibration stops at the verified 250-lb line. The frame and cylinder continue beyond it; their load values are explicitly extrapolated from the final verified interval, rather than assigning 250 to the far frame. The cylinder reaches about 300 lb at the 7-inch end. The dotted trace ends just above 6 inches, around 177 lb.

The two records coalesce at the origin, then separate, with the solid cylinder carrying more load. Their origin location is hidden in the thick axes/trace junction and has widened bounds. The cylinder's terminal ink merges with the far frame; its endpoint bound includes that junction. The slight jagged shoulders on the solid line are recorder features, not fitted segments. The dotted line is sampled on actual dots, shifted from nominal quarter inches as necessary.''',
'F2-46':'''Printed identity: solid = LPT No. 98: Four-Inch Cylinder, Gp = 27.3; dotted = LPT No. 89: Four-Inch Footpad, Gp = 22.4. These match the supplied series IDs. No plotted markers or straight fit lines.

This panel is upright: penetration right, load up. The right frame is 6 inches; the short mark beyond it is not another inch. The highest labelled load line is 600 lb, below the upper frame. Only the labelled 0 through 600 lb grid lines calibrate load; the solid trace above 600 lb is flagged extrapolated.

The solid line first becomes visible at the penetration-zero frame above load zero (about 15 lb); it has not been extended down to the geometric origin. The dotted line's first visible dot is just inside the frame, with a bound covering the obscured start. The records do not cross after their obscured initial region. The final dot is distinct from the right frame: its final nominal sample and endpoint are placed on that dot, not on the frame. The solid has an abrupt upper recorder step and a small subsequent load decrease; these are retained in drawing order.''',
'F2-47':'''Printed identity: dashed = Four-Inch Cylinder, LPT No. 101, Gp = 63.9; solid = Four-Inch Footpad, LPT No. 91, Gp = 62.8. These match the supplied IDs. The leader arrow from the cylinder label ends on the dashed first hump, around (725,2940), not the solid shoulder below it. The leader is annotation, not a third curve. No plotted markers or straight fit lines.

This panel is upright. The top frame is labelled 2000 lb. The x = 7 right-frame line initially failed the ink verification by 2.14 px at an end; it was recovered from the same page and refitted to 31 ink positions (RMS about 0.68 px). Both the original detection and the recovery samples are saved. The final piecewise map verifies all eight penetration and five load lines.

Identity through encounters: near the origin the dashed rising strokes lie against/cross the thin solid rising segment, roughly 0.2 to 0.4 inch; the dash pattern and continuity into the arrow's hump distinguish them. The dashed record then lies above the solid shoulder near 0.5 inch. There is also a clear crossing near 1.3 inches: the falling dashed hump crosses the rising continuous line. Beyond that crossing the dashed rising record lies below the solid one until the terminal encounter near 6 inches. The last distinguishable dash cap touches/nearly merges into the solid and the 6-inch grid line. I cannot distinguish further dashed ink beyond approximately 6.0 inches. I stop lpt101 at that visible cap, with a wide overlap/dash bound; the continuous solid alone is independently traceable to 7 inches. This is an endpoint/continuation ambiguity, not evidence for a separately visible dashed branch after 6 inches.

The initial encounters, clear crossing around 1.3 inches, and close approach at 5.75 to 6 inches have widened bounds. The early dashed hump is a local maximum; the global peak is the terminal dash cap. The local trough and the nearly level solid shoulder are retained as features. No reassignment of identities is made at a crossing.''',
'F2-48':'''Printed identity: solid = Four-Inch Cylinder (LPT No. 87), Gp = 45; dotted = Four-Inch Footpad (LPT No. 85), Gp = 46. These match the supplied series IDs. No plotted markers or straight fit lines.

The page is sideways: penetration increases up and load left. The last labelled penetration line is 8 inches; the unlabelled frame beyond it is not treated as a labelled 9-inch anchor. All labelled load lines 0 to 1200 lb in steps of 200 are anchored.

Important drafting irregularity: at the penetration-axis edge the 0-to-1-inch spacing is about 233 px, while 1-to-2 is about 316 px. The printed 0, 1, 2 and 8 numbers have each been checked against their own drawn line. A tighter-box, higher-threshold detection confirms the irregularity; changing a genuine unequal grid to make an affine residual small would change the reading. Consequently the affine penetration residual exceeds the protocol diagnostic threshold of 0.5 percent of span. Values use only verified tilted grid lines and piecewise interpolation; the affine fit is diagnostic, not used for reported values.

The solid trace rises steeply, has a shallow decreasing-load shoulder near 0.6 to 1.1 inches, and then resumes increasing; the decrease stays in drawing order. The dotted trace has a flatter initial shoulder. The traces meet in the obscured origin junction but do not cross later. The solid terminates just beyond the 8-inch line. The last dotted mark joins the 8-inch grid; the endpoint bound covers the unresolved cap rather than extending the curve into white space.'''
}

def main():
 report=[]
 for fid,(page,box) in FIGS.items():
  root=Path('out')/fid;cal,X,Y=maps(fid)
  summary=ca.knots_summary(X,Y)
  (root/'cal-p1'/'piecewise-knots.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
  rows=list(csv.DictReader((root/'points-p1-native.csv').open()))
  counts=Counter((r['series_id'],r['point_kind']) for r in rows)
  print(fid,'counts',dict(counts))
  print('residuals',*[round(cal[k],6) for k in ('rms_residual_x','max_residual_x','rms_residual_y','max_residual_y')])
  print('bounds',min(float(r['u_bound_px']) for r in rows),max(float(r['u_bound_px']) for r in rows),min(float(r['v_bound_px']) for r in rows),max(float(r['v_bound_px']) for r in rows))
  print('endpoints',[(r['series_id'],r['x_native'],r['y_native']) for r in rows if r['point_kind']=='feature' and ('first;' in r['note'] or 'peak;' in r['note'])])
  sensitivity=[]
  for sid in GUIDES[fid]:
   rr=[r for r in rows if r['series_id']==sid]
   dx=max(abs(float(r['x_native'])-np.dot(cal['ax'],[float(r['pixel_u']),float(r['pixel_v']),1])) for r in rr)
   dy=max(abs(float(r['y_native'])-np.dot(cal['ay'],[float(r['pixel_u']),float(r['pixel_v']),1])) for r in rr)
   sensitivity.append(dict(series_id=sid,max_affine_vs_piecewise_x_in=round(float(dx),6),max_affine_vs_piecewise_y_lb=round(float(dy),4)))
  writecsv(root/'cal-p1'/'calibration-sensitivity.csv',sensitivity)
  g=np.asarray(Image.open(f'packet/p{page}.png').convert('L'))
  audit=[]
  for r in rows:
   p=np.array([float(r['pixel_u']),float(r['pixel_v'])]);u,v=np.rint(p).astype(int)
   vv,uu=np.mgrid[v-15:v+16,u-15:u+16];P=np.stack([uu,vv],axis=-1)
   dark=g[v-15:v+16,u-15:u+16]<180
   dist=np.linalg.norm(P-p,axis=-1)
   ink=float(dist[dark].min()) if np.any(dark) else 99
   nongrid=dark&(grid_dist(P,cal)>5)
   own=float(dist[nongrid].min()) if np.any(nongrid) else 99
   audit.append(dict(series_id=r['series_id'],point_kind=r['point_kind'],sequence=r['sequence'],nearest_dark_px=round(ink,2),nearest_non_grid_dark_px=round(own,2),visual_review='own trace ink checked on crops; grid/frame overlaps noted in points',method='threshold 180; fitted grid exclusion 5 px; no symbol/text removal; not D031'))
   if ink>2.01:print('OFF INK',fid,r['series_id'],r['sequence'],p,ink,r['note'])
  writecsv(root/'ink-distance-audit.csv',audit)
  ctext='; '.join(f'{sid}: {counts[(sid,"trace")]} trace, {counts[(sid,"feature")]} feature, 0 marker' for sid in GUIDES[fid])
  extra=sum('extrapolated' in r['cal_model'] for r in rows)
  note=f'''{fid}, panel 1 — independent blind reading, batch curves-s2-b2

Evidence: packet/p{page}.png, unrotated 300-dpi page; packet/p0105.png for setup only; packet/series.csv and CURVE-READING.md. No other reading or prior reading was consulted. Context describes the 4-inch cylinder/footpad comparison, including footpad shape, cylinder side friction and soil falling above the footpad; it supplies no plotted points.

{DETAILS[fid]}

Reading method and bounds

Quarter-inch requests are nominal sampling positions (target_x_in), not observations. For dots/dashes I move to actual ink, so x_native need not equal target_x_in. First and last visible ink points are also trace rows, even when they fall between quarter inches. Each series has separate first, peak and last feature rows; coincident roles are separate rows at the same pixel. Knees include changes in slope and recorder jogs; small recorder roughness is not interpreted as physical soil behavior. There are no penetration unloading loops; the small load decreases are followed in their original traversal order. Sequence includes both trace and feature rows.

On clean solid segments, bounds come from the local normal ink half-width measured near that sample, not a fixed global width. Dot/dash bounds also include half the measured local repeat spacing along the trace, projected to page u/v. Intersections, recorder corners and unresolved frame/trace junctions receive wider bounds. Pixel bounds are symmetric reading bounds, not standard deviations. The native output uses piecewise interpolation with each verified line's tilt and location error; it propagates the pixel rectangle and bracketing-line intervals without adding the global affine residual. Native units: penetration inches; load pounds. No SI output was requested.

Calibration and verification

Final affine diagnostic residuals: penetration RMS {cal['rms_residual_x']:.6f} in, maximum {cal['max_residual_x']:.6f} in; load RMS {cal['rms_residual_y']:.6f} lb, maximum {cal['max_residual_y']:.6f} lb. Verified knots: {len(X.knots)} penetration, {len(Y.knots)} load; {len(X.rejected)+len(Y.rejected)} rejected in the final map. No predicted line is used as a knot. The independent numerical ink check for every grid line, its location error, and its samples are in cal-p1/piecewise-knots.json. Three printed labels per axis (four penetration labels on F2-48) were checked by eye in calibration-eye-checks.csv; calibration-label-crops.png retains the actual number/line evidence. Affine-versus-piecewise differences by series are in cal-p1/calibration-sensitivity.csv. {extra} rows have an interval extending beyond a verified outer line, flagged in cal_model, including uncertain endpoints at a boundary.

Every regular sample was visually checked on magnified page crops; feature/endpoints were checked separately, and the final overlay was reviewed. The packet contains only calibrate_axes.py and plot_grid.py; check_trace_ink.py is not supplied. ink-distance-audit.csv is a supplementary raw-darkness/grid-exclusion check, not a claim of the project's D031 symbol/text-removal certification. The visual review is essential to distinguish label lettering, annotation leaders, frame/grid ink and each curve's own ink. No samples intentionally bridge blank dot/dash gaps.

Counts: {ctext}. Total {len(rows)} rows. All rows have panel = 1.

Deliverables: cal-p1/calibration.json, anchors.csv, piecewise-knots.json and calibration-sensitivity.csv; calibration-eye-checks.csv; points-p1.csv; points-p1-native.csv; overlay-p1.png; notes.md. Additional reading grids, labeled zoom crops, contact sheets, label crops and the ink-distance audit retain QA evidence. Helpers are in out/; tools/ is unchanged.
'''
  (root/'notes.md').write_text(note,encoding='utf-8')
  for (sid,kind),count in counts.items():report.append(dict(figure_id=fid,series_id=sid,point_kind=kind,count=count))
 writecsv('out/counts.csv',report)

if __name__=='__main__':main()
