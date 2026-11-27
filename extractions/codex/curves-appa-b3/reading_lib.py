import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import calibrate_axes as ca
original_check=ca.AxisKnots.check_line
bottom_value=None
def checked(self,gray,kn):
 ca.INK_HALF_WIDTH_PX=14 if self.transform=='reciprocal' and kn['value']==bottom_value else 6
 return original_check(self,gray,kn)
ca.AxisKnots.check_line=checked
def load_maps(fig,c):
 global bottom_value
 bottom_value=c['yr'][1]
 return ca.piecewise_maps(Path('out')/fig/'cal-p1','packet/'+c['page']+'.png')
