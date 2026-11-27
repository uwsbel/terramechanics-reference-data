"""Write the piecewise knots of cal-p1 with their ink verification (tools/calibrate_axes.py knots_summary)
to out/F2-45/cal-p1/knots-check.json and print a short table."""
import sys, json
sys.path.insert(0, 'tools')
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps('out/F2-45/cal-p1', 'packet/p0106.png')
s = ca.knots_summary(X, Y)
json.dump(s, open('out/F2-45/cal-p1/knots-check.json', 'w'), indent=1)
for ax in ('x', 'y', 'rejected_x', 'rejected_y'):
    for kn in s[ax]:
        print(ax, kn['value'], 'err_px', kn['location_error_px'], kn['ink_check'], kn.get('reason', ''))
