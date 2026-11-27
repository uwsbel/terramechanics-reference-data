import sys, json
sys.path.insert(0, sys.argv[1])
import calibrate_axes as ca
cal, X, Y = ca.piecewise_maps(sys.argv[2], sys.argv[3])
want = [(a.split('=')[0], float(a.split('=')[1])) for a in sys.argv[4:]]
for axn, val in want:
    K = X if axn == 'x' else Y
    for kn in K.knots + K.rejected:
        if abs(kn['value'] - val) < 1e-9:
            print(axn, val, 'found', kn['check'].get('found'), 'missing', kn['check'].get('missing'))
