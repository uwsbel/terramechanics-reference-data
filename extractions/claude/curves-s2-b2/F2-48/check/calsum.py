import json, sys
for p in sys.argv[1:]:
    c = json.load(open(p))
    print(p, c['box'], c.get('bands'), c.get('dark'), 'rms', round(c['rms_residual_x'],4), round(c['rms_residual_y'],3), 'max', round(c['max_residual_x'],4), round(c['max_residual_y'],3), c['n_anchors'], c.get('x_direction'), c.get('y_direction'))
    for L in c['horizontal_lines']:
        print('  x', L['x_value'], round(L['v_at_u0']+L['slope_dv_du']*2260,1), round(L['v_at_u0']+L['slope_dv_du']*500,1), L['source'])
    for L in c['vertical_lines']:
        print('  y', L['y_value'], round(L['u_at_v0']+L['slope_du_dv']*3700,1), round(L['u_at_v0']+L['slope_du_dv']*1400,1), L['source'])
