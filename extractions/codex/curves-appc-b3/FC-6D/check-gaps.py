import csv
rr=[r for r in csv.DictReader(open('out/FC-6D/points-p1-native.csv')) if r['series_id']=='n2934' and r['point_kind']=='trace']
for a,b in zip(rr,rr[1:]):
 if float(b['x_native'])-float(a['x_native'])>10:print(a['pixel_u'],a['pixel_v'],b['pixel_u'],b['pixel_v'])
