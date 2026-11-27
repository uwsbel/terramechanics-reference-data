"""Independent page-ink measurements, guided by this reader's inspected crops."""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import calibrate_axes as ca

CFG={
16:dict(page=152,soil='RS',markers=[(641,2460,18,'pair 1 left; cut by left frame; overlaps mean',10),(793,2450,18,'pair 1 right; overlaps vertical grid',4),(1566,1919,18,'pair 2 left; overlaps upper and vertical grid',10),(1680,1923,18,'pair 2 right; overlaps mean',9),(1927,1854,18,'pair 3 left; overlaps mean',9),(2151,1850,18,'pair 3 right',2),(2349,1537,18,'pair 4 left; overlaps upper and vertical grid',10),(2555,1530,18,'pair 4 right; outside right frame',2),(2506,1390,18,'single; cut by right frame; overlaps upper',12),(2507,1623,18,'single; cut by right frame; overlaps mean',12),(2511,1850,18,'single; cut by right frame; overlaps lower',12)],
mean=[(665,2440),(850,2340.5),(1050,2234),(1250,2132),(1450,2033),(1650,1944),(1850,1867),(2050,1793.5),(2250,1717),(2450,1628),(2546,1581.5)],
upper=[(649,2416),(850,2300),(1050,2187),(1250,2079.5),(1450,1970.5),(1650,1875.5),(2050,1676),(2250,1563),(2450,1432.5),(2531,1367.5)],
lower=[(650,2525),(850,2432),(1050,2345.5),(1450,2180),(1650,2103),(1850,2029),(2050,1960),(2250,1898),(2450,1855),(2480,1851)]),
17:dict(page=153,soil='PS',markers=[(1133,2180,18,'single; overlaps mean',9),(1340,2150,18,'single; overlaps vertical grid',4),(1475,2171,18,'single; near lower curve',5),(1365,1941,18,'pair 1 left; overlaps upper',9),(1678,1934,18,'pair 1 right',2),(2645,1670,18,'single; outside right frame; interior ink speck',3)],
mean=[(867,2220),(1050,2186),(1250,2133),(1450,2067.5),(1850,1927.5),(2050,1863),(2250,1798),(2450,1738),(2571,1705.5)],
upper=[(875,2074),(1050,2033),(1250,1972),(1450,1895),(1850,1768),(2050,1706.5),(2250,1650),(2450,1594),(2570,1564)],
lower=[(864,2350.5),(1050,2314.5),(1250,2258),(1450,2189),(1650,2120),(1850,2036),(2050,1968.5),(2250,1900.5),(2450,1835),(2591,1792.5)]),
18:dict(page=154,soil='RSM-a',markers=[(895,2418,18,'pair 1 left; overlaps upper and vertical grid',9),(1113,2412,18,'pair 1 right; overlaps mean',10),(929,2538,18,'single; overlaps neighboring circle',18),(946,2513,18,'single; overlaps neighboring circle and mean',18),(932,2616,18,'single; overlaps lower',9),(2455,1727,18,'single; overlaps vertical grid',4)],
mean=[(898,2528),(1050,2443),(1250,2337),(1450,2235.5),(1650,2136.5),(1850,2041),(2050,1950),(2250,1863),(2450,1784.5),(2593,1736)],
upper=[(908,2399),(1050,2318),(1250,2211),(1450,2108),(1650,2010),(1850,1915),(2050,1821),(2250,1732.5),(2450,1653),(2590,1606)],
lower=[(898,2639),(1050,2556),(1250,2457),(1450,2360),(1650,2265.5),(1850,2175),(2050,2088),(2250,2004),(2450,1929.5),(2596,1884)]),
19:dict(page=155,soil='RC2',markers=[(974,2213,18,'single; overlaps mean and vertical grid',10),(2435,1425,18,'single',2)],
mean=[(995,2220),(1150,2178.5),(1350,2088),(1550,1978),(1750,1852),(1950,1729),(2150,1612),(2350,1505.5),(2500,1440),(2510,1435)],
upper=[(965,2119),(1050,2091),(1200,2037),(1300,1992),(1400,1943),(1500,1891),(1600,1837),(1700,1782),(1800,1727.5),(1850,1697),(2000,1607),(2100,1550.5),(2250,1470),(2300,1445),(2400,1400.5),(2450,1382.5),(2515,1360.5)],
lower=[(966,2324),(1150,2264),(1350,2181),(1550,2080),(1750,1975),(1950,1859),(2150,1738),(2350,1630),(2518,1530)])}

def circle(g,u,v,r):
    # Ring and white neighbors; obstructed sectors have little influence.
    th=np.linspace(0,2*np.pi,180,endpoint=False)
    best=(-1,None)
    for uu in np.arange(u-5,u+5.01,0.5):
      for vv in np.arange(v-5,v+5.01,0.5):
       for rr in (r-2,r-1,r,r+1,r+2):
        def vals(rad):
          return g[np.rint(vv+rad*np.sin(th)).astype(int),np.rint(uu+rad*np.cos(th)).astype(int)]
        black=255-vals(rr)
        contrast=(vals(rr-7)+vals(rr+7))/2-vals(rr)
        score=np.mean(np.clip(contrast,0,255))+np.mean(black)*.2
        if score>best[0]: best=(score,(uu,vv,rr))
    return best[1]

def guide_y(nodes,u): return float(np.interp(u,np.array(nodes)[:,0],np.array(nodes)[:,1]))

def column(g,u,pred,cal,markers):
    # Reject grid ink and circle outlines; the remaining run must track the inspected curve.
    for line in cal['vertical_lines']:
      if abs(u-(line['u_at_v0']+line['slope_du_dv']*pred))<7: return None
    lo,hi=int(pred-13),int(pred+14)
    ix=np.where(g[lo:hi,u]<160)[0]
    groups=np.split(ix,np.where(np.diff(ix)>1)[0]+1)
    cand=[]
    for ids in groups:
      if len(ids)<4 or len(ids)>19: continue
      v=lo+(ids[0]+ids[-1])/2
      if abs(v-pred)>9: continue
      if any(abs(v-(l['v_at_u0']+l['slope_dv_du']*u))<9 for l in cal['horizontal_lines']): continue
      if any(np.hypot(u-m[0],v-m[1])<32 for m in markers): continue
      cand.append((abs(v-pred),v,max(2.5,len(ids)/2)))
    if not cand:return None
    _,v,b=min(cand)
    return v,b

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--run',action='store_true');args=ap.parse_args()
 if not args.run:return
 for n,cfg in CFG.items():
  folder=Path(f'out/FC-{n}'); im=Image.open(f"packet/p{cfg['page']:04d}.png").convert('RGB');g=np.asarray(im.convert('L'),dtype=float)
  cal,X,Y=ca.piecewise_maps(folder/'cal-p1',f"packet/p{cfg['page']:04d}.png")
  rows=[]
  def point(s,kind,seq,u,v,b,notes,symbol=''):
    rows.append(dict(figure_id=f'FC-{n}',panel=1,series_id=s,point_kind=kind,sequence=seq,pixel_u=round(u,2),pixel_v=round(v,2),u_bound_px=b,v_bound_px=b,symbol=symbol,note=notes))
  marks=[];skipped=[]
  for j,(u,v,r,note,b) in enumerate(cfg['markers'],1):
    uu,vv,rr=circle(g,u,v,r);marks.append((uu,vv,rr))
    if 'cut by' in note:b=20
    elif 'overlaps' in note and ('curve' in note or 'mean' in note or 'upper' in note or 'lower' in note or 'neighboring' in note):b=18
    point('data','marker',j,uu,vv,b,note,'circle')
  # Markers are recorded before any curve measurements.
  print(n,'markers',marks)
  for s in ['mean','upper','lower']:
    nodes=cfg[s];a,z=nodes[0][0],nodes[-1][0]
    # The guide locates each branch; every output point is a measured ink center.
    track={u:column(g,u,guide_y(nodes,u),cal,marks) for u in range(int(a),int(z)+1)}
    valid=[u for u,vb in track.items() if vb is not None]
    samples=[]
    def sample(target,label):
      u=min(valid,key=lambda u:abs(u-target));v,b=track[u]
      # At grid intersections, a short local fit recovers the curve center on the ink.
      pred=guide_y(nodes,target)
      obstruct_grid=any(abs(target-(l['u_at_v0']+l['slope_du_dv']*pred))<7 for l in cal['vertical_lines']) or any(abs(pred-(l['v_at_u0']+l['slope_dv_du']*target))<9 for l in cal['horizontal_lines'])
      obstruct_marker=any(np.hypot(target-m[0],pred-m[1])<32 for m in marks)
      if obstruct_grid and not obstruct_marker and abs(u-target)<28:
        near=[k for k in valid if abs(k-target)<(60 if s=='mean' else 30)]
        if len(near)>=10:
          vv=np.array([track[k][0] for k in near]);fit=np.polyfit(near,vv,1)
          q=float(np.polyval(fit,target))
          fitus=np.arange(int(target)-12,int(target)+13)
          fitvs=np.polyval(fit,fitus).round().astype(int)
          support=np.mean(np.min(np.stack([g[fitvs+d,fitus] for d in [-1,0,1]]),axis=0)<160)
          both=any(0<target-k<23 for k in near) and any(0<k-target<23 for k in near)
          if (s=='mean' or (support>=.92 and both)) and g[int(round(q)),int(round(target))]<160:
            u=target;v=q;b=float(np.median([track[k][1] for k in near]));label+='; curve/grid crossing read from adjoining curve ink'
      if abs(u-target)>1:label+=f'; moved {u-target:+.1f} px to nearest visible curve ink'
      samples.append((u,v,b,label))
    samples.append((a,nodes[0][1],4.5,'left end; first identifiable curve ink; terminal merged with frame/symbol where noted'))
    xl=X.value(a,guide_y(nodes,a))[0];xr=X.value(z,guide_y(nodes,z))[0]
    for val in np.arange(-.1,1.201,.05):
      if val<=xl+.002 or val>=xr-.002:continue
      u=(val-cal['ax'][2]-cal['ax'][1]*guide_y(nodes,(a+z)/2))/cal['ax'][0]
      for _ in range(5):u+=(val-X.value(u,guide_y(nodes,u))[0])/cal['x_per_px']
      pred=guide_y(nodes,u)
      if s=='mean' and any(np.hypot(u-m[0],pred-m[1])<32 for m in marks):
        skipped.append(f'mean Dr={val:.2f}: curve ink is merged with a circle outline at the nominal abscissa; omitted under rule 6, rather than reading the symbol or shifting a solid-curve sample.')
        continue
      sample(u,f'Dr target {val:.2f}'+('; dash end when target is in gap' if s!='mean' else ''))
    samples.append((z,nodes[-1][1],4.5,'right end; last identifiable curve ink; terminal merged with frame/symbol where noted'))
    # Shifted targets can coincide at one dash end; preserve one sample per requested target.
    for j,(u,v,b,note) in enumerate(samples,1):point(s,'trace',j,u,v,b,note)
    u,v,b,_=samples[0];point(s,'feature',1,u,v,b,'first point; left end of identifiable curve ink')
    if (n,s) in [(16,'mean'),(19,'mean'),(18,'upper')]:
      rows[-1].update(u_bound_px=35,v_bound_px=20,note=rows[-1]['note']+'; terminal obscured by circle/frame; widened interval includes merged terminal')
    u,v,b,_=samples[-1];point(s,'feature',2,u,v,b,'last point; right end; peak of increasing trace')
    if (n,s)==(16,'lower'):
      rows[-1].update(u_bound_px=35,v_bound_px=20,note=rows[-1]['note']+'; terminal obscured by circle/frame; widened interval includes merged terminal')
  (folder/'omitted-samples.txt').write_text('\n'.join(skipped)+'\n',encoding='utf-8')
  cols=list(rows[0]);
  with (folder/'points-p1.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,cols,lineterminator='\n');w.writeheader();w.writerows(rows)
  ca.piecewise_rows(cal,X,Y,rows)
  with (folder/'points-p1-native.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
  (folder/'cal-p1/verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
  # Contact sheet of exact trace positions for visual ink QA; each original crop is enlarged.
  tr=[r for r in rows if r['point_kind']=='trace'];tilew,tileh=260,170;sheet=Image.new('RGB',(tilew*6,tileh*((len(tr)+5)//6)),'white');d=ImageDraw.Draw(sheet)
  for j,r in enumerate(tr):
    u,v=r['pixel_u'],r['pixel_v'];left,top=int(u)-35,int(v)-22
    tile=im.crop((left,top,left+70,top+44)).resize((210,132))
    td=ImageDraw.Draw(tile);xx=(u-left)*3;yy=(v-top)*3;td.line([(xx-10,yy),(xx+10,yy)],fill='red',width=1);td.line([(xx,yy-10),(xx,yy+10)],fill='red',width=1)
    x=j%6*tilew;y=j//6*tileh;sheet.paste(tile,(x,y+25));d.text((x,y),f"{r['series_id']} {r['sequence']} x={r['x_native']:.3f} ({u:.1f},{v:.1f})",fill='black')
  sheet.save(folder/'trace-ink-check.png')

if __name__=='__main__': main()
