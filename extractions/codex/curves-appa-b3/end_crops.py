import subprocess,json,sys
from pathlib import Path
cfg=json.loads(Path('out/config.json').read_text())
ends={
'FA-3':[(680,2760,1070,2900),(2280,3050,2750,3250)],
'FA-7':[(440,1750,820,1960),(2000,2290,2390,2600)],
'FA-19':[(530,1010,930,1220),(2160,1620,2520,2420)],
'FA-23':[(620,1300,1040,1435),(620,1950,1040,2580),(2110,2550,2450,3590)],
'FA-27':[(430,3120,900,3270),(2040,3540,2570,3780)],
'FA-39':[(600,1870,1080,2100),(2120,2880,2520,3130)],
'FA-47':[(710,2280,1080,2480),(2140,2920,2530,3010)]}
for fig,boxes in ends.items():
 for i,b in enumerate(boxes):
  subprocess.run([sys.executable,'tools/plot_grid.py','crop','packet/'+cfg[fig]['page']+'.png','--box',*map(str,b),'--out','out/'+fig+'/end'+str(i)+'.png','--zoom','3','--step','25'],capture_output=True)
