from pathlib import Path
for p in Path('out').glob('FC-*/notes.md'):
 s=p.read_text(encoding='utf-8').replace('See cal-p1/knots.json and points-p1-native.knots.json for each ink check and location error.','See cal-p1/knots.json for each ink check and location error.')
 p.write_text(s,encoding='utf-8')
p=Path('out/finalize_reading.py');s=p.read_text(encoding='utf-8').replace('See cal-p1/knots.json and points-p1-native.knots.json for each ink check and location error.','See cal-p1/knots.json for each ink check and location error.');p.write_text(s,encoding='utf-8')
p=Path('out/README.md');s=p.read_text(encoding='utf-8').replace('two cap samples adjacent to marker gaps','a cap sample adjacent to a marker gap');p.write_text(s,encoding='utf-8')
p=Path('out/write_index.py');s=p.read_text(encoding='utf-8').replace('two cap samples adjacent to marker gaps','a cap sample adjacent to a marker gap');p.write_text(s,encoding='utf-8')
print('Final document references corrected and required artifacts retained.')
