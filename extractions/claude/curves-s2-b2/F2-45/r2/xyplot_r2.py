"""x-y check plot of the solid center line and the dots (values from common.x_of/y_of)."""
import csv, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import x_of, y_of
C=[r for r in csv.DictReader(open('out/F2-45/r2/solid-centerline.csv'))]
D=[r for r in csv.DictReader(open('out/F2-45/r2/dots.csv'))]
x=np.array([float(r['x']) for r in C]); y=np.array([float(r['y']) for r in C]); ok=np.array([r['clean'] in ('1','True') for r in C])
dx=np.array([x_of(float(r['u']),float(r['v'])) for r in D]); dy=np.array([y_of(float(r['u']),float(r['v'])) for r in D])
xlo,xhi=float(sys.argv[1]),float(sys.argv[2])
fig,ax=plt.subplots(figsize=(9,7))
m=(x>=xlo)&(x<=xhi)
ax.plot(x[m],y[m],'-',color='0.6',lw=0.8); ax.plot(x[m&ok],y[m&ok],'r.',ms=2)
md=(dx>=xlo)&(dx<=xhi)
ax.plot(dx[md],dy[md],'bo',ms=3)
for k in np.nonzero(md)[0][::5]: ax.annotate(D[k]['k'],(dx[k],dy[k]),fontsize=7,color='b')
ax.set_xlabel('penetration (in)'); ax.set_ylabel('load (lb)'); ax.grid(True,which='both',lw=0.3); ax.minorticks_on()
fig.savefig(sys.argv[3],dpi=90,bbox_inches='tight')
