"""ASCII dump of a page region: '#' dark (<160), '+' mid (<200), '.' light. Usage: pixdump.py u0 u1 v0 v1"""
import sys
import numpy as np
from PIL import Image
img = np.array(Image.open('packet/p0090.png').convert('L'))
u0, u1, v0, v1 = [int(x) for x in sys.argv[1:5]]
print('      ' + ''.join(str((u//10)%10) if u%10==0 else ' ' for u in range(u0,u1)))
print('      ' + ''.join(str(u%10) for u in range(u0,u1)))
for v in range(v0, v1):
    print('%5d ' % v + ''.join('#' if p<160 else ('+' if p<200 else '.') for p in img[v, u0:u1]))
