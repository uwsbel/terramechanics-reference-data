"""Zoomed crops of the page with the reading's points drawn on them, for checking by eye."""
import csv
from PIL import Image, ImageDraw

im = Image.open('packet/p0088.png').convert('RGB')
pts = list(csv.DictReader(open('out/F2-32/points-p1.csv', encoding='utf-8')))
col = {'lpt93': (220, 0, 0), 'lpt53': (0, 150, 0), 'lpt52': (0, 0, 230), 'fit': (210, 120, 0)}
boxes = {'ov_a': (1700, 3380, 2000, 3700), 'ov_b': (1450, 3080, 1800, 3400), 'ov_c': (1250, 2750, 1600, 3100),
         'ov_d': (1050, 2400, 1400, 2750), 'ov_e': (880, 2150, 1230, 2450), 'ov_f': (700, 1880, 1050, 2200),
         'ov_g': (1650, 3150, 2000, 3300)}
for name, (u0, v0, u1, v1) in boxes.items():
    z = 4
    cr = im.crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
    d = ImageDraw.Draw(cr)
    for p in pts:
        u, v = float(p['pixel_u']), float(p['pixel_v'])
        if not (u0 <= u <= u1 and v0 <= v <= v1):
            continue
        ub, vb = float(p['u_bound_px']), float(p['v_bound_px'])
        c = col[p['series_id']]
        x, y = (u - u0) * z, (v - v0) * z
        r = 5 if p['point_kind'] == 'trace' else 8
        d.ellipse((x - r, y - r, x + r, y + r), outline=c, width=2)
        d.rectangle((x - ub * z, y - vb * z, x + ub * z, y + vb * z), outline=c, width=1)
        d.text((x + 8, y - 6), f"{p['series_id'][-2:]}{p['sequence']}", fill=c)
    cr.save(f'out/F2-32/crops/{name}.png')
    print('wrote', name, cr.size)
