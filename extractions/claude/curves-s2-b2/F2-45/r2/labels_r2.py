"""Ink extent of the printed axis labels (boxes chosen by eye on the crops in checks/) against the fitted lines."""
from common import INK, VL, HL, vline_u, hline_v
import numpy as np
def ext(u0, v0, u1, v1):
    vs, us = np.nonzero(INK[v0:v1, u0:u1]); return us.min()+u0, us.max()+u0, vs.min()+v0, vs.max()+v0
X = {L['x_value']: L for L in HL}; Y = {L['y_value']: L for L in VL}
for lab, box in (('0', (2300, 3575, 2360, 3615)), ('1', (2300, 3265, 2365, 3300)), ('3', (2290, 2650, 2340, 2690)), ('7', (2270, 1415, 2330, 1450))):
    a, b, c, d = ext(*box); cu, cv = (a+b)/2, (c+d)/2
    lv = hline_v(X[float(lab)], cu)
    print('x', lab, 'label u %d-%d v %d-%d center v %.1f; line at u %.0f: v %.1f; offset %.1f' % (a, b, c, d, cv, cu, lv, cv-lv))
for lab, box in (('0', (2245, 3615, 2300, 3655)), ('25', (2095, 3615, 2150, 3700)), ('50', (1940, 3615, 1995, 3700)), ('100', (1630, 3615, 1690, 3730)), ('150', (1255, 3615, 1320, 3730)), ('250', (700, 3630, 760, 3740))):
    a, b, c, d = ext(*box); cu, cv = (a+b)/2, (c+d)/2
    lu = vline_u(Y[float(lab)], cv)
    print('y', lab, 'label u %d-%d v %d-%d center u %.1f; line at v %.0f: u %.1f; offset %.1f' % (a, b, c, d, cu, cv, lu, cu-lu))
