"""Build out/inventory.csv for batch inventory-s6-b1 (Claude blind reading) from the readings below.
Every value here was read from the page images in packet/pages (PDF 345 to 440)."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'inventory.csv')

COLS = ['id', 'kind', 'title_as_printed', 'printed_page', 'pdf_page', 'section', 'test_type', 'soils', 'states',
        'apparatus', 'rate_or_dynamics', 'data_form', 'panels', 'curves', 'trace_classes', 'x_quantity', 'x_unit',
        'x_axis_type', 'y_quantity', 'y_unit', 'y_axis_type', 'legend_entries', 'rotation', 'in_scope', 'transcribe',
        'priority', 'mcc_relevant', 'relation', 'relation_target', 'notes']

rows = []


def add(**kw):
    r = {c: '' for c in COLS}
    r.update({k: str(v) for k, v in kw.items()})
    for c in COLS:
        if r[c] == '' and c != 'relation_target':
            raise SystemExit('missing %s in %s' % (c, r['id']))
    rows.append(r)


NA = 'n/a'


def nodata(**kw):
    base = dict(panels=0, curves=0, x_quantity=NA, x_unit=NA, x_axis_type=NA, y_quantity=NA, y_unit=NA,
                y_axis_type=NA, legend_entries=NA, transcribe='yes', mcc_relevant='no')
    base.update(kw)
    add(**base)


def pp6(pdf):
    return '6-%d' % (pdf - 358)


# ---------------------------------------------------------------- Section V, end
prof_common = dict(kind='figure', section='V', test_type='model drop', data_form='curve', panels=1,
                   x_quantity='horizontal velocity', x_unit='ft_s', x_axis_type='linear',
                   y_quantity='vertical velocity', y_unit='ft_s', y_axis_type='linear', rotation=0, in_scope='yes',
                   transcribe='yes', priority=1, mcc_relevant='no')
add(id='F5-40', title_as_printed='Stability Profile for Model Landings in RS Dense Soil, 2-2 Downhill',
    printed_page='5-70', pdf_page=350, soils='RS', states='dense (Dr 0.71 to 0.81 per F6-6)',
    apparatus='1/6-scale LM model; 15 deg sloped soil box',
    rate_or_dynamics='free drop, 45 deg yaw (2-2 landing), level vehicle, ground slope 15 deg downhill',
    curves=4, trace_classes='measurement-markers;author-fit',
    legend_entries='Stable;Unstable;Unstable but Close to Balancing;Transition from Stable to Unstable Landings',
    relation='derived-from', relation_target='F6-6',
    notes='Gross correlation group 1, drops 22 to 34 (13 markers, all numbered); inset "RS Dense Soil, 45 deg Yaw, '
          'Level Vehicle at Impact, Ground Slope = 15 deg". Curves: 3 marker classes plus the hatched transition band. '
          'Axes printed "Ft./Sec.", x 0 to 10, y 0 to 15. Compared with F6-6: VV, VH and stable/unstable agree except '
          'drop 25, plotted at VH about 6 (filled) where F6-6 prints VH 5; markers sit about 0.1 ft/s left of the '
          'tabulated VH. Drop 27 drawn with a partly filled mark (F6-6: Yes, borderline). The same drops are in T5-2 '
          '(page not identified; T5-2 not in packet).', **prof_common)
add(id='F5-41', title_as_printed='Stability Profile for Model Landing in RSM-b Soil, 2-2 Downhill',
    printed_page='5-71', pdf_page=351, soils='RSM-b', states='rolled, dense (Dr 0.65 to 0.86 per F6-8)',
    apparatus='1/6-scale LM model; 15 deg sloped soil box',
    rate_or_dynamics='free drop, 45 deg yaw (2-2 landing), level vehicle, ground slope 15 deg downhill',
    curves=4, trace_classes='measurement-markers;author-fit',
    legend_entries='Stable;Unstable;Unstable but Close to Balance',
    relation='derived-from', relation_target='F6-8',
    notes='Gross correlation group 3, drops 64 to 67 and 69 to 77 (65/66 and 73/77 share points); drops 63 (22.5 '
          'deg yaw) and 68 (Dr 0.10, not rolled) are not plotted. Curves: 3 marker classes plus hatched transition '
          'band (no legend entry for the band). Inset prints "RS Dense Soil, 45 deg Yaw" although the caption and '
          'F6-8 say RSM-b. Axes "Ft./Sec.", x 0 to 10, y 0 to 15. Marker positions agree with F6-8 VV, VH.',
    **prof_common)
add(id='F5-42', title_as_printed='Stability Profile for Model Landing in RS Dense Soil, 22 1/2° Yaw Downhill',
    printed_page='5-72', pdf_page=352, soils='RS', states='dense',
    apparatus='1/6-scale LM model; 15 deg sloped soil box',
    rate_or_dynamics='free drop, 22.5 deg yaw, level vehicle, ground slope 15 deg downhill',
    curves=1, trace_classes='measurement-markers', legend_entries=NA,
    relation='derived-from', relation_target='T5-2',
    notes='Gross correlation group 2, drops 35 to 44; inset "RS Dense Soil, 22.5 deg Yaw, Level Vehicle at Impact, '
          'Ground Slope = 15 deg, All Drops Stable". 10 open markers (stable), no transition band; markers labeled '
          '35 to 42 and 44, one marker near VH 8, VV 3.9 carries no number (43 is the number not printed). Axes '
          '"Ft./Sec.", x 0 to 10, y 0 to 17. No Section VI table lists drops 35 to 44; T5-2 page not identified.',
    **prof_common)

expl = [
    ('F5-43', 2, '5-75', 355, 'yaw -160 deg (strut 7 leading, strut 1 trailing), VV 7 fps, VH 4 fps; three 4 inch deep '
                                'depressions under footpads 2 to 4', 'prose 5-74: shows the test setup prior to the drop'),
    ('F5-44', 3, '5-75', 355, 'yaw +140 deg, VV 6 fps, VH 2.46 fps; one 4 inch depression under footpad 2',
     'prose 5-74 cites it for the depression'),
    ('F5-45', 4, '5-75', 355, 'same ground and attitude as drop 3, VV 10 fps, VH 2.45 fps',
     'prose 5-74: shows the model after the drop'),
    ('F5-46', 5, '5-76', 356, 'yaw +50 deg, VV 5 fps, VH 2.46 fps; waxed hard blocks under pads 2 and 4, sandpaper '
                                'pad 3 on hard surface, pad 1 into 4 1/2 inch depression',
     'prose 5-74: shows the test site arrangement before the drop tests; photo partly washed out'),
    ('F5-47', 6, '5-76', 356, 'same ground as drop 5, VV 10 fps, VH 2.46 fps',
     'prose 5-74: shows the model after the fifth test'),
]
for fid, n, pp, pdf, cond, extra in expl:
    soils = 'RS; wooden blocks' if n >= 5 else 'RS'
    nodata(id=fid, kind='figure', title_as_printed='Exploratory Model Drop No. %d' % n, printed_page=pp, pdf_page=pdf,
           section='V', test_type='model drop', soils=soils, states='dense',
           apparatus='1/6-scale LM model', rate_or_dynamics='exploratory drop (secondary strut tension), slope 3 1/2 '
                                                             'deg: ' + cond,
           data_form='photo', trace_classes='setup-evidence', rotation=0, in_scope='no', priority=3,
           relation='same-as', relation_target='T5-2',
           notes='Photograph. Exploratory drop No. %d (Section 5.7; prose 5-73 says these are drops Nos. 2 through 6 '
                 'of Paragraph 5.3, numbering distinct from NASA detail correlation drops 2 to 6). Conditions from '
                 'prose 5-74 (PDF 354). %s. T5-2 page not identified.' % (n, extra))

# ---------------------------------------------------------------- Section VI program figures
nodata(id='F6-1', kind='figure', title_as_printed='Block Diagram for Typical Landing Dynamics Computer Program',
       printed_page='6-2', pdf_page=360, section='VI', test_type='soil model', soils='none', states=NA,
       apparatus='LM Landing Dynamics Computer Program (NASA-MSC)', rate_or_dynamics=NA, data_form='schematic',
       trace_classes='schematic', rotation=0, in_scope='no', priority=3, relation='none', relation_target='',
       notes='Flow chart: initial conditions, footpad and c.g. set-up, soil and strut forces, integration, test for '
             'maximum time and stability, print output.')
nodata(id='F6-2', kind='figure', title_as_printed='Flow Diagram for Subroutine SOIL', printed_page='6-4', pdf_page=362,
       section='VI', test_type='soil model', soils='none', states=NA,
       apparatus='LM Landing Dynamics Computer Program, subroutine SOIL', rate_or_dynamics=NA, data_form='schematic',
       trace_classes='schematic', rotation=0, in_scope='no', priority=3, relation='none', relation_target='',
       notes='Logic chart with FORTRAN variable names (NON, ZDTPR, ZDTP, FZ, D-Dmax, VAPH, IFLAG, IFLA, STHET); '
             'calls BEN, INTEGR, SLIDE. Small type, legible at zoom.')
nodata(id='F6-3', kind='figure', title_as_printed='Flow Diagram for Subroutine BEN', printed_page='6-5', pdf_page=363,
       section='VI', test_type='soil model', soils='none', states=NA,
       apparatus='LM Landing Dynamics Computer Program, subroutine BEN', rate_or_dynamics=NA, data_form='schematic',
       trace_classes='schematic', rotation=0, in_scope='no', priority=3, relation='none', relation_target='',
       notes='Branches on IFLAG to soil force from elastic properties, dynamic relationships (calls INTEGER for soil '
             'wedge and footpad motion) or static equilibrium. Page map has no printed label; folio 6-5 is printed.')

# ---------------------------------------------------------------- Section VI stability tables and profiles
tab = dict(kind='figure', section='VI', test_type='model drop', data_form='table', panels=0, curves=0,
           trace_classes='setup-evidence', x_quantity=NA, x_unit=NA, x_axis_type=NA, y_quantity=NA, y_unit=NA,
           y_axis_type=NA, legend_entries=NA, transcribe='yes', mcc_relevant='no')
COLS_STAB = ('Bendix Drop No. and Date; Soil; VV; VH (no unit printed, ft/s per prose); Ground Slope (Deg.) Zeta; '
             'Yaw Angle (Deg.); Relative Density Dr; Density gamma (Lbs./Ft.3); Friction Angle phi (Deg.); Stable; '
             'Remarks')
add(id='F6-4', title_as_printed='Rigid Surface LM Model Drops', printed_page='6-7', pdf_page=365,
    soils='plywood blocks', states='rigid', apparatus='1/6-scale LM model with spiked footpads; rigid surface',
    rate_or_dynamics='free drop, 22.5 deg yaw, slope 10 deg, VV 6 to 12, VH 4.5 to 7', rotation=0, in_scope='yes',
    priority=1, relation='same-as', relation_target='T5-2-p310;T5-2-p311',
    notes='Columns: ' + COLS_STAB + '. Rows: Bendix drops 45 (9-27-67) to 62 (10-13-67), all Plywood Blocks, slope '
          '10, yaw 22.5 (drop 49 prints a value reading like 22.3); Dr, density, phi printed "--". Remarks on 45 '
          '(borderline, spiked footpad, 10 deg board slope), 46 (borderline; tests 45 and 46 to check rubber '
          'capsules), 49 and 52 (very unstable), 50 (borderline), 51 (repeat of 47 and 48). Same drops as F5-20 '
          '(agreed index, T5-2-p310 and p311); T5-2 content not compared (not in packet).', **tab)
add(id='F6-5', kind='figure',
    title_as_printed='Stability Profile for Model Landing on Wooden Surface (Fir Wood) with Spiked Feet - 22 1/2° Yaw',
    printed_page='6-8', pdf_page=366, section='VI', test_type='model drop', soils='none (wooden surface)',
    states='rigid', apparatus='1/6-scale LM model with spiked feet; LM Landing Dynamics Computer Program (rigid surface)',
    rate_or_dynamics='free drop, 22.5 deg yaw, ground slope 10 deg, level vehicle', data_form='curve', panels=1,
    curves=5, trace_classes='measurement-markers;author-fit;computed', x_quantity='horizontal velocity',
    x_unit='ft_s', x_axis_type='linear', y_quantity='vertical velocity', y_unit='ft_s', y_axis_type='linear',
    legend_entries='Calculated;Experimental;Stable;Unstable;Unstable But Close to Balance;Stable But Close to Unbalance',
    rotation=0, in_scope='maybe', transcribe='yes', priority=2, mcc_relevant='no', relation='derived-from',
    relation_target='F6-4;F5-20',
    notes='Markers are drops 45 to 62 (18, all numbered); VV, VH and stable/unstable agree with F6-4. Curves: open, '
          'filled and a partly filled marker class (cluster 45/46/50 at VH 4.7, VV 8 hard to separate) plus two '
          'bands, Experimental (hatched) and Calculated (rigid surface program, black and white). Calculated band is '
          'computed; markers already tabulated in F6-4; F5-20 link by caption and conditions only (not in packet). '
          'Axes "Ft./Sec.", x 0 to 10, y 0 to 15.')
add(id='F6-6', title_as_printed='LM Model Drops on RS Dense Soil', printed_page='6-9', pdf_page=367, soils='RS',
    states='dense (Dr 0.71 to 0.81, 56.7 to 59.3 pcf)', apparatus='1/6-scale LM model; 15 deg sloped soil box',
    rate_or_dynamics='free drop, 45 deg yaw, slope 15 deg, VV 7 to 14, VH 4 to 7.5', rotation=0, in_scope='yes',
    priority=1, relation='same-as', relation_target='T5-2',
    notes='Columns: ' + COLS_STAB + '. Rows: drops 22 (8-3-67) to 34 (8-11-67), RS Dense, slope 15, yaw 45, phi 47 to '
          '48. Remarks: 22 "RS Dense soil- 10 rolls per two-inch layer", 27 and 30 "Borderline stability". Drop 32 '
          'row partly illegible (number "3\'", date "8-1 -67", Stable "N)" read as No). Drop 25 VH printed 5 while '
          'F5-40 and F6-7 plot it at VH 6. Same drops as F5-40 (gross correlation group 1); T5-2 page not identified.',
    **tab)
add(id='F6-7', kind='figure', title_as_printed='Stability Profile for Model Landings on RS Dense Soil, 2-2 Downhill',
    printed_page='6-10', pdf_page=368, section='VI', test_type='model drop', soils='RS',
    states='dense (Dr 0.71 to 0.81 per F6-6)',
    apparatus='1/6-scale LM model; LM Landing Dynamics Computer Program (rigid surface and soil versions)',
    rate_or_dynamics='free drop, 45 deg yaw (2-2), slope 15 deg downhill, level vehicle; computed with original '
                     'damping 10 Sdot and increased damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary',
    data_form='curve', panels=1, curves=7, trace_classes='measurement-markers;author-fit;computed',
    x_quantity='horizontal velocity', x_unit='ft_s', x_axis_type='linear', y_quantity='vertical velocity',
    y_unit='ft_s', y_axis_type='linear',
    legend_entries='Experimental Data;Rigid Surface;Original Soil Equations;Modified Soil Equations;Increased Strut '
                   'Damping;Stable;Unstable;Unstable But Close to Balancing;Transition From Stable to Unstable Landings',
    rotation=0, in_scope='maybe', transcribe='yes', priority=2, mcc_relevant='no', relation='derived-from',
    relation_target='F6-6;F5-40',
    notes='Same 13 drops (22 to 34) as F5-40 with the experimental band, plus four computed profiles (rigid surface, '
          'original soil equations, modified soil equations with zero lift force, increased strut damping). Curves: '
          'open and filled marker classes (no clearly partly filled marker) plus 5 patterned lines. Legend says "Dr '
          '(From DPT Tests) as Marked" but no Dr values are printed on the plot. Measured content is in F6-6 and '
          'F5-40; the computed profiles are not measurements. Page map label 2-2 is a misread; folio 6-10 printed.')
add(id='F6-8', title_as_printed='LM Model Drops for RSM-b Soil', printed_page='6-12', pdf_page=370, soils='RSM-b',
    states='rolled (10 rolls); not rolled (drop 68, Dr 0.10); Dr 0.10 to 0.86',
    apparatus='1/6-scale LM model; 15 deg sloped soil box',
    rate_or_dynamics='free drop, 45 deg yaw (drop 63 at 22.5), slope 15 deg, VV 7 to 14, VH 4 to 7.5', rotation=0,
    in_scope='yes', priority=1, relation='same-as', relation_target='T5-2-p311;T5-2-p312',
    notes='Columns: ' + COLS_STAB + '. Rows: drops 63 (10-18-67) to 77 (10-26-67); Soil "RSM 10 Rolls" (63 to 67), '
          '"RSM" (68, 69), "RSM Rolled" (70 to 77); density 75.7 (drop 68) to 86 or 88 pcf (digits 6 and 8 hard to '
          'tell apart in this column), phi 39 (68), 47 (65), 48 others. Remarks: 66 rerun of 65; 68 soil not rolled; '
          '69 repeat of 68 on hard dense soil; 73 borderline; 77 borderline, rerun of 73. Target pages are the RSM '
          'pages of T5-2 per the agreed index soils column; content not compared.', **tab)
add(id='F6-9', kind='figure', title_as_printed='Stability Profile for Model Landing in RSM-b Soil, 2-2 Downhill',
    printed_page='6-13', pdf_page=371, section='VI', test_type='model drop', soils='RSM-b',
    states='rolled, dense (Dr 0.65 to 0.86 per F6-8)',
    apparatus='1/6-scale LM model; LM Landing Dynamics Computer Program (rigid surface and soil versions)',
    rate_or_dynamics='free drop, 45 deg yaw (2-2), slope 15 deg downhill, level vehicle; computed with original and '
                     'increased strut damping',
    data_form='curve', panels=1, curves=8, trace_classes='measurement-markers;author-fit;computed',
    x_quantity='horizontal velocity', x_unit='ft_s', x_axis_type='linear', y_quantity='vertical velocity',
    y_unit='ft_s', y_axis_type='linear',
    legend_entries='Experimental Data;Rigid Surface;Original Soil Equations;Modified Soil Equations;Increased Strut '
                   'Damping;Stable;Unstable;Unstable But Close to Balance',
    rotation=0, in_scope='maybe', transcribe='yes', priority=2, mcc_relevant='no', relation='derived-from',
    relation_target='F6-8;F5-41',
    notes='Same markers as F5-41 (drops 64 to 67, 69 to 77; 63 and 68 absent) with the experimental band plus four '
          'computed profiles. Curves: 3 marker classes plus 5 patterned lines. Axes "Ft./Sec.", x 0 to 10, y 0 to 15. '
          'Measured content in F6-8 and F5-41; computed profiles are not measurements.')

DROPS = {
    1: dict(bendix='10, 7-18-67', soil='RS', state='loose (Dr 0, 46.9 pcf, phi 41)', vv=10, vh=0),
    2: dict(bendix='11, 7-19-67', soil='RS', state='loose (Dr 0, 46.9 pcf, phi 41)', vv=5, vh=7),
    3: dict(bendix='12, 7-20-67', soil='RS', state='loose (Dr 0, 47.1 pcf, phi 41)', vv=5, vh=7),
    4: dict(bendix='13, 7-20-67', soil='RS', state='loose (Dr 0, 47.1 pcf, phi 41)', vv=10, vh=0),
    5: dict(bendix='16, 7-25-67', soil='RS', state='intermediate (Dr printed "3", 53.0 pcf, phi 42.5)', vv=5, vh=7),
    6: dict(bendix='17, 7-25-67', soil='RS', state='intermediate (Dr 0.3, 53.0 pcf, phi 42.5)', vv=10, vh=0),
    7: dict(bendix='20, 7-28-67', soil='SS', state='loose (Dr 0, 96.0 pcf, phi 30)', vv=5, vh=7),
    8: dict(bendix='21, 7-28-67', soil='SS', state='loose (Dr 0, 96.0 pcf, phi 30)', vv=10, vh=0),
}

add(id='F6-10', title_as_printed='LM Model Drop Tests for Detail Correlation Studies', printed_page='6-15',
    pdf_page=373, soils='RS; SS', states='loose (Dr 0); intermediate (Dr 0.3)',
    apparatus='1/6-scale LM model; level soil bed',
    rate_or_dynamics='free drop, 45 deg yaw, level ground; VV 10 fps VH 0 (drops 1, 4, 6, 8) or VV 5 fps VH 7 fps '
                     '(drops 2, 3, 5, 7)', rotation=90, in_scope='yes', priority=1, relation='same-as',
    relation_target='T5-3',
    notes='Columns: NASA Drop No.; Bendix Drop No. and Date; Soil; VV fps; VH fps; Ground Slope (Deg.); Yaw Angle '
          '(Deg.); Relative Density Dr; Absolute Density Lb./Ft.3; Friction Angle phi; Stable. Rows NASA 1 to 8 = '
          'Bendix 10, 11, 12, 13, 16, 17, 20, 21 (7-18-67 to 7-28-67); RS Loose 1 to 4 (46.9, 46.9, 47.1, 47.1 pcf, '
          'phi 41), RS Intermediate 5 and 6 (53.0 pcf, phi 42.5; drop 5 Dr printed "3" without the decimal point, '
          'drop 6 "0.3"), SS Loose 7 and 8 (96.0 pcf, phi 30); slope 0, yaw 45, all Stable Yes. Same eight drops as '
          'T5-3, whose values per the agreed index are measured velocities in in/s (Test 1 VV -114.9); these are the '
          'nominal fps values. Page printed sideways.', **tab)

# ---------------------------------------------------------------- detail correlation histories
LOW = {1: ('F6-13', 384), 2: ('F6-11', 375), 3: ('F6-14', 388), 4: ('F6-15', 392), 5: ('F6-16', 396),
       6: ('F6-17', 400), 7: ('F6-18', 404), 8: ('F6-19', 408)}
HIGH = {2: ('F6-12', 380), 1: ('F6-20', 412), 3: ('F6-21', 416), 4: ('F6-22', 420), 5: ('F6-23', 424),
        6: ('F6-24', 428), 7: ('F6-25', 432), 8: ('F6-26', 436)}

# per-sheet panel readings: (letter, caption quantity, printed y unit, range)
LOWP = {
    2: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '10 to 110'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '25 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 4.5'), ('d', 'Vehicle Pitch Acceleration', 'Degrees Second^2', '-8000 to 10000')],
        [('e', 'Vehicle Pitch Rate', 'Degrees Second', '-10 to 70'), ('f', 'Vehicle Pitch Angle', 'Degrees', '-0.5 to 3.5'),
         ('g', 'c.g. Vertical Position X', 'Inches', '21 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 7')],
        [('i', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-70 to 20'), ('j', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '35 to 85'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2', '-400 to 1200'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Second^2', '-1200 to 400')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-15 to 25'), ('n', 'Footpad Roll Angle beta', 'Degrees', '0 to 8')],
    ],
    1: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '-40 to 120'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 100'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 5'), ('d', 'Vehicle Pitch Acceleration', 'Degrees Second (no square)', '-5000 to 6000')],
        [('e', 'Vehicle Pitch Rate', 'Degrees Second', '-30 to 15'), ('f', 'Vehicle Pitch Angle', 'Degrees', '-1.5 to 1.5'),
         ('g', 'c.g. Vertical Position X', 'Inches', '18 to 25'), ('h', 'c.g. Horizontal Position Y', 'Inch', '-0.5 to 0.5')],
        [('i', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-120 to 10'), ('j', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '-200 to 200'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2', '-500 to 2000'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Second^2', '-1500 to 1750')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-5.5 to 0.5'), ('n', 'Footpad Roll Angle beta', 'Degrees', '-1 to 3')],
    ],
    3: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '10 to 110'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '25 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 4.5'), ('d', 'Vehicle Pitch Acceleration', 'Degrees Second (no square)', '-8000 to 10000')],
        [('e', 'Vehicle Pitch Rate', 'Degrees Second', '-10 to 70'), ('f', 'Vehicle Pitch Angle', 'Degrees', '-0.5 to 3.5'),
         ('g', 'c.g. Vertical Position X', 'Inches', '21 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 6.5')],
        [('i', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-70 to 20'), ('j', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '30 to 85'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2', '-400 to 1200'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Second^2', '-1200 to 0')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-20 to 25'), ('n', 'Footpad Roll Angle beta', 'Degrees', '0 to 8')],
    ],
    4: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 120'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 5.5'), ('d', 'Vehicle Pitch Acceleration', 'Degrees Second (no square)', '-1500 to 2500')],
        [('e', 'Vehicle Pitch Rate', 'Degrees Second', '-2 to 7'), ('f', 'Vehicle Pitch Angle', 'Degrees', '-0.05 to 0.35'),
         ('g', 'c.g. Vertical Position X', 'Inches', '19 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '-0.05 to 0.4')],
        [('i', 'c.g. Vertical Velocity Xdot (caption)', 'Inches Second^2', '-500 to 3000'), ('j', 'c.g. Horizontal Velocity Ydot (caption)', 'Inches Second', '-120 to 10'),
         ('k', 'c.g. Vertical Acceleration Xddot (caption)', 'Inches Second', '-0.5 to 5.5'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Second^2', '-200 to 500')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-5 to 25'), ('n', 'Footpad Roll Angle beta', 'Degrees', '0 to 4')],
    ],
    5: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 110'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 3.5'), ('d', 'Vehicle Pitch Acceleration', 'Degrees Second (no square)', 'to 12500 (lowest tick hard to read)')],
        [('e', 'Vehicle Pitch Rate (caption)', 'Degrees', '-0.5 to 3.5'), ('f', 'Vehicle Pitch Angle (caption)', 'Degrees Second', '-5 to 55'),
         ('g', 'c.g. Vertical Position X', 'Inches', 'about 21.5 to 24.4'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 6.5')],
        [('i', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-70 to 20'), ('j', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '20 to 85'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2', '-400 to 1600'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Second^2', '-1600 to 600')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-20 to 25'), ('n', 'Footpad Roll Angle beta', 'Degrees', '0 to 5.5')],
    ],
    6: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 120'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 70'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 3'), ('d', 'Vehicle Pitch Acceleration', 'Degrees Second (no square)', '-5000 to 9000')],
        [('e', 'Vehicle Pitch Rate', 'Degrees Second', '-15 to 25'), ('f', 'Vehicle Pitch Angle', 'Degrees', '-0.7 to 0.2'),
         ('g', 'c.g. Vertical Position X', 'Inches', '20.5 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '-0.05 to 0.55')],
        [('i', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-120 to 10'), ('j', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '-1 to 9'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches/Second^2', '-500 to 5000'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Second^2', '-400 to 800')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-10 to 25'), ('n', 'Footpad Roll Angle beta', 'Degrees', '0 to 8')],
    ],
    7: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 110'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '25 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 3.5'), ('d', 'Vehicle Pitch Acceleration', 'Degrees Second (no square)', '-10000 to 10000')],
        [('e', 'Vehicle Pitch Rate', 'Degrees Second', '-10 to 80'), ('f', 'Vehicle Pitch Angle', 'Degrees', '-0.5 to 4'),
         ('g', 'c.g. Vertical Position X', 'Inches', '21.5 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 6')],
        [('i', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-70 to 20'), ('j', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '30 to 85'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2', '-400 to 1600'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Second^2', '-1200 to 0')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-20 to 25'), ('n', 'Footpad Roll Angle beta', 'Degrees', '0 to 6.5')],
    ],
    8: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 120'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '-10 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 4'), ('d', 'Vehicle Pitch Angle (caption)', 'Degrees/Second^2', '-5000 to 5000')],
        [('e', 'Vehicle Pitch Rate', 'Degrees Seconds', '-20 to 20'), ('f', 'Vehicle Pitch Angle', 'Degrees', '-1 to 0.1'),
         ('g', 'c.g. Vertical Position X', 'Inches', '19.5 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '-0.05 to 0.6')],
        [('i', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-120 to 10'), ('j', 'c.g. Horizontal Velocity Ydot', 'Inches Seconds', '-1 to 9'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2', '-500 to 4000'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches Seconds^2', '-600 to 1400')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '-10 to 25'), ('n', 'Footpad Roll Angle beta', 'Degrees', '0 to 5.5')],
    ],
}
LOW_SHEET_QUIRK = {
    (4, 2): 'Panels i, j, k plot other quantities than captioned: i (captioned vertical velocity) has an '
            'acceleration-like curve with a 1500 plateau and unit Inches Second^2, j (captioned horizontal velocity) '
            'looks like vertical velocity, k (captioned vertical acceleration) looks like horizontal velocity.',
    (5, 1): 'Captions e and f do not match the axes: e (Pitch Rate) is labeled Degrees with an angle-like curve, f '
            '(Pitch Angle) is labeled Degrees Second with a rate-like curve.',
    (8, 0): 'Panel d is captioned "Vehicle Pitch Angle" but its axis is Degrees/Second^2 with an acceleration-like '
            'curve; no pitch acceleration caption on this sheet.',
}
SECV = {  # Section V figures of the same quantity, by NASA drop, per sheet
    1: ['F5-22;F5-23;F5-24', 'F5-28', 'F5-27;F5-26', ''],
    2: ['F5-29;F5-30;F5-31', 'F5-38;F5-39;F5-35;F5-37', 'F5-34;F5-36;F5-33', ''],
}

UNIT = {'Inches Second': 'in_s', 'Degrees': 'deg', 'Degrees Second': 'deg_s', 'Inches': 'inch',
        'Inches Second^2': 'in_s2', 'Inch': 'inch', 'Degrees Seconds': 'deg_s', 'Inches Seconds': 'in_s'}


def ysel(p):
    letter, q, u, rng = p
    unit = UNIT.get(u, None)
    if unit is None:
        unit = 'deg_s2' if u.startswith('Degrees') else u
    qq = q.replace(' (caption)', '')
    return qq, unit


def fmt_panels(ps):
    return '; '.join('%s) %s, %s, %s' % p for p in ps)


for n in range(1, 9):
    fid, pdf0 = LOW[n]
    d = DROPS[n]
    for k in range(4):
        pdf = pdf0 + k
        ps = LOWP[n][k]
        rid = fid if k == 0 else '%s-p%d' % (fid, pdf)
        if k < 3:
            curves = 8
        else:
            curves = 4 if n == 1 else 3
        yq, yu = ysel(ps[0])
        tgt = 'F6-10'
        if n in SECV and SECV[n][k]:
            tgt += ';' + SECV[n][k]
        cap = ('Detail Correlation Results %s LM Model Drop No. %d Using Low Strut Damping in Computer Simulation '
               '(See Figure 6-10 for drop conditions) (Sheet %d of 4)' % ('for' if n == 2 else 'For', n, k + 1))
        if k < 3:
            curvenote = 'Each panel has an Experimental and a Computer curve, labeled by arrows.'
        elif n == 1:
            curvenote = ('m: Experimental and Computer; n: Experimental and a Computer line at zero (labeled).')
        else:
            curvenote = ('m: Experimental and Computer; n: Experimental only (roll angle not computed, prose 6-16).')
        q = LOW_SHEET_QUIRK.get((n, k), '')
        secv = ''
        if n in SECV:
            secv = (' Same drop as NASA Test No. %d of Section V; traces not compared (Section V pages not in '
                    'packet).' % n)
        notes = ('NASA drop %d (Bendix %s), %s %s, VV %s fps, VH %s fps (F6-10). Computed with original strut damping '
                 '10 Sdot. %s Panels (y printed unit, range): %s. x "Elapsed Time, Second" 0 to 0.1.%s%s' %
                 (n, d['bendix'], d['soil'], d['state'], d['vv'], d['vh'], curvenote, fmt_panels(ps),
                  (' ' + q) if q else '', secv))
        add(id=rid, kind='figure', title_as_printed=cap, printed_page=pp6(pdf), pdf_page=pdf, section='VI',
            test_type='model drop', soils=d['soil'], states=d['state'],
            apparatus='1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program',
            rate_or_dynamics='free drop, 45 deg yaw, level ground, VV %s fps, VH %s fps (F6-10); computed with '
                             'strut damping 10 Sdot' % (d['vv'], d['vh']),
            data_form='curve', panels=len(ps), curves=curves, trace_classes='recorded-trace;computed',
            x_quantity='elapsed time', x_unit='s', x_axis_type='linear', y_quantity=yq, y_unit=yu,
            y_axis_type='linear', legend_entries='Experimental;Computer', rotation=0, in_scope='yes',
            transcribe='yes', priority=1, mcc_relevant='no', relation='same-as', relation_target=tgt, notes=notes)

HIGHP = {
    2: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '10 to 100'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '35 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 3.75'), ('d', 'Vehicle Pitch Acceleration (caption; axis and curve are pitch angle)', 'Degrees', '0 to 3.75')],
        [('e', 'Vehicle Pitch Acceleration', 'Degrees Second^2', '-2500 to 5000'), ('f', 'Vehicle Pitch Rate', 'Degrees Second', '-5 to 55 (a tick printed 15 where 25 belongs)'),
         ('g', 'c.g. Vertical Position X', 'Inches', '21.5 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 6')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '32.5 to 85'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-65 to 15'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches/Second^2', '-400 to 1200'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', '-800 to 0')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '0 to 22.5')],
    ],
    1: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 120'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 4'), ('e', 'Vehicle Pitch Acceleration (caption, lettered e)', 'Vehicle Pitch Degrees', 'every tick printed 0')],
        [('e', 'Vehicle Pitch Acceleration', 'Degrees Second^2', '-125 to 125'), ('f', 'Vehicle Pitch Rate', 'Degrees Second', '-0.001 to 0.002'),
         ('g', 'c.g. Vertical Position X', 'Inches', '20 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 1, trace flat at 0')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches/Second', 'tick labels truncated'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches/Second', '-120 to 0'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches/Second^2', '-500 to 3000'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', '-6 to 6')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '0 to 0.075')],
    ],
    3: [
        [('a', 'Footpad Velocity Vap', 'Inches/Second', '10 to 100'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '35 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 3.75'), ('d', 'Vehicle Pitch Angle', 'Degrees', '0 to 3.75')],
        [('e', 'Vehicle Pitch Acceleration', 'Inches (sic)', '-3000 to 5000'), ('f', 'Vehicle Pitch Rate', 'Degrees/Second', '-5 to 55'),
         ('g', 'c.g. Vertical Position X', 'Inches', '21.5 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 6')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '32.5 to 85'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-65 to 15'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2', '-400 to 1200'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', '-800 to 0')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', 'about 10 to 22')],
    ],
    4: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 120'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 4'), ('d', 'Vehicle Pitch Angle', 'Degrees', 'every tick printed 0')],
        [('e', 'Vehicle Pitch Acceleration', 'Degrees Second^2', '-150 to 850'), ('f', 'Vehicle Pitch Rate', 'Degrees/Second', 'about -0.001 to 0.0017, lower ticks printed -0'),
         ('g', 'c.g. Vertical Position X', 'Inches', '20 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', 'every tick printed 0.0020')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches Second', 'tick labels truncated (-0, 0, -0.001)'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches/Second', '-120 to 0'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches Second^2 (partly legible)', '-500 to 3000'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', '-6 to 6')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '0 to 22.5, trace along 0')],
    ],
    5: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '10 to 100'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '35 to 95'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 2.5'), ('d', 'Vehicle Pitch Angle', 'Degrees', '0 to 3.25')],
        [('e', 'Vehicle Pitch Acceleration', 'Degrees/Second^2', '-2500 to 3500'), ('f', 'Vehicle Pitch Rate', 'Degrees/Second', '-5 to 55'),
         ('g', 'c.g. Vertical Position X', 'Inches', '22.5 to 24.3'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 5')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '20 to 85'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-65 to 15'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches/Second^2', '-400 to 1600'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', '-1300 to -100')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '0 to 16')],
    ],
    6: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 120'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 2.25'), ('d', 'Vehicle Pitch Angle', 'Degrees', 'every tick printed 0')],
        [('e', 'Vehicle Pitch Acceleration', 'Degrees Second^2', 'ticks 250 to -2750 with signs dropped on 1250 and 1750; trace flat'),
         ('f', 'Vehicle Pitch Rate', 'Degrees/Second', '0.0001 to 0.0015, lower ticks printed -0'),
         ('g', 'c.g. Vertical Position X', 'Inches', '21.75 to 24.25; x ticks printed 0.2 to 0.8 for 0.02 to 0.08'),
         ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 1, trace flat at 0')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches Second', 'ticks printed 0 and -0'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches/Second', '-120 to 0'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches/Second^2', '-500 to 4500'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', '-0.25 to 2.25')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '0 to 16, trace along 0')],
    ],
    7: [
        [('a', 'Footpad Velocity Vap', 'Inches Second', '0 to 105'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '35 to 95'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 3'), ('d', 'Vehicle Pitch Angle', 'Pitch', '0 to 4')],
        [('e', 'Vehicle Pitch Acceleration', 'no label visible', '-2500 to 5000'), ('f', 'Vehicle Pitch Rate', 'Degrees/Second', '-5 to 55'),
         ('g', 'c.g. Vertical Position X', 'Inches', '22 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', '0 to 6')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches/Second', '25 to 85'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches/Second', '-65 to 15'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches/Second^2', '-400 to 1200'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', '-1100 to -100')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '0 to 20')],
    ],
    8: [
        [('a', 'Footpad Velocity Vap', 'Inches Seconds', '0 to 120 (x tick printed 0.00 at 0.04)'), ('b', 'Footpad Velocity Angle theta', 'Degrees', '0 to 90'),
         ('c', 'Footpad Penetration d', 'Inches', '0 to 3.5'), ('d', 'Vehicle Pitch Angle', 'Degrees', '0 to 0.0004, ticks repeated')],
        [('e', 'Vehicle Pitch Acceleration', 'Degrees/Second^2', '-50 to 700'), ('f', 'Vehicle Pitch Rate', 'Degrees/Second', '-0.001 to 0.011'),
         ('g', 'c.g. Vertical Position X', 'Inches', '20.75 to 24.5'), ('h', 'c.g. Horizontal Position Y', 'Inches', 'ticks 0.0028 and 0.0029 repeated')],
        [('i', 'c.g. Horizontal Velocity Ydot', 'Inches Second', '-0.001 to 0.0045'), ('j', 'c.g. Vertical Velocity Xdot', 'Inches Second', '-120 to 0'),
         ('k', 'c.g. Vertical Acceleration Xddot', 'Inches/Second^2', '-500 to 4000'), ('l', 'c.g. Horizontal Acceleration Yddot', 'Inches/Second^2', 'about -0.8 to 0.7')],
        [('m', 'Footpad Pitch Angle alpha', 'Degrees', '0 to 20, trace along 0')],
    ],
}
UNIT2 = dict(UNIT)
UNIT2.update({'Inches/Second': 'in_s', 'Inches/Second^2': 'in_s2', 'Degrees/Second': 'deg_s',
              'Degrees Second^2': 'deg_s2', 'Degrees/Second^2': 'deg_s2', 'Inches (sic)': 'inch',
              'no label visible': 'n/a'})
HIGH_QUIRK = {
    (3, 0): 'Computed traces of sheets 1 to 3 nearly coincide with F6-12 (drop 2, same nominal VV and VH); sheet '
            '4 axes differ.',
    (3, 1): 'Computed traces nearly coincide with F6-12 sheet 2; pitch acceleration axis labeled "Inches".',
    (3, 2): 'Computed traces nearly coincide with F6-12 sheet 3.',
    (4, 0): 'Panels a to c nearly coincide with F6-20 sheet 1 (drop 1, same nominal VV and VH); panel d differs.',
}
for n in range(1, 9):
    fid, pdf0 = HIGH[n]
    d = DROPS[n]
    for k in range(4):
        pdf = pdf0 + k
        ps = HIGHP[n][k]
        rid = fid if k == 0 else '%s-p%d' % (fid, pdf)
        p0 = ps[0]
        yu = UNIT2.get(p0[2], p0[2])
        yq = p0[1].split(' (')[0]
        if n == 2:
            cap = ('Computer Results for LM Model Drop No. 2 Using High Strut Damping In Simulation (See Figure 6-10 '
                   'for drop conditions) (Sheet %d of 4)' % (k + 1))
        else:
            cap = ('Computer Results For LM Model Drop No. %d Using High Strut Damping in Computer Simulation (See '
                   'Figure 6-10 for drop conditions) (Sheet %d of 4)' % (n, k + 1))
        q = HIGH_QUIRK.get((n, k), '')
        notes = ('Computed only, NASA drop %d (Bendix %s), %s %s, VV %s fps, VH %s fps (F6-10); higher strut damping '
                 'at low stroking velocity, 10 Sdot^1/2 primary and 30 Sdot^1/2 secondary (prose 6-11, 6-21). One '
                 'computed trace per panel; panels a to m only (no n). Panels (y printed unit, range): %s. x "Time '
                 'Seconds" or "Time/Seconds" 0 to 0.12.%s Not a measurement: in_scope maybe only as the report\'s own '
                 'simulation reference.' % (n, d['bendix'], d['soil'], d['state'], d['vv'], d['vh'], fmt_panels(ps),
                                           (' ' + q) if q else ''))
        add(id=rid, kind='figure', title_as_printed=cap, printed_page=pp6(pdf), pdf_page=pdf, section='VI',
            test_type='soil model', soils=d['soil'], states=d['state'],
            apparatus='LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws',
            rate_or_dynamics='computed landing, 45 deg yaw, level ground, VV %s fps, VH %s fps (F6-10); strut '
                             'damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary' % (d['vv'], d['vh']),
            data_form='curve', panels=len(ps), curves=len(ps), trace_classes='computed',
            x_quantity='time', x_unit='s', x_axis_type='linear', y_quantity=yq, y_unit=yu,
            y_axis_type='linear', legend_entries=NA, rotation=0, in_scope='maybe', transcribe='yes', priority=3,
            mcc_relevant='no', relation='derived-from', relation_target='F6-10', notes=notes)

add(id='F6-27', kind='figure', title_as_printed='Comparison of Computed and Experimental Footpad Penetration Depths',
    printed_page='6-82', pdf_page=440, section='VI', test_type='model drop', soils='RS; SS',
    states='loose (Dr 0); intermediate (Dr 0.3)',
    apparatus='1/6-scale LM model; LM Landing Dynamics Computer Program',
    rate_or_dynamics='NASA drops 1 to 8 (F6-10); damping of the computation not stated', data_form='curve',
    panels=1, curves=8, trace_classes='recorded-trace;computed', x_quantity='time', x_unit='s', x_axis_type='linear',
    y_quantity='computed depth minus experimental depth', y_unit='inch', y_axis_type='linear',
    legend_entries='Drop No. 1 Dmax = 4.3 in.;Drop No. 2 Dmax = 4.2 in.;Drop No. 3 Dmax = 4.2 in.;Drop No. 4 Dmax '
                   '= 5.3 in.;Drop No. 5 Dmax = 3.4 in.;Drop No. 6 Dmax = 3.0 in.;Drop No. 7 Dmax = 3.3 in.;Drop '
                   'No. 8 Dmax = 3.7 in.',
    rotation=0, in_scope='maybe', transcribe='yes', priority=2, mcc_relevant='no', relation='derived-from',
    relation_target='F6-11;F6-13;F6-14;F6-15;F6-16;F6-17;F6-18;F6-19',
    notes='Eight stacked strips, one per drop, each with its own 0 and +/- marks; y printed "Computed Depth - '
          'Experimental Depth 0.25 Inch Per Division"; x "Time-Seconds" 0 to .10. Each curve is a difference of a '
          'computed and a measured depth (from panels c of the detail figures). Dmax values match the maximum of the '
          'experimental penetration in panel c of each low damping figure (checked by eye). Which damping the '
          'computation used is not stated.')

rows = [r for _, r in sorted(enumerate(rows), key=lambda t: (int(t[1]['pdf_page']), t[0]))]
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(len(rows), 'rows ->', OUT)
for r in rows:
    for c in COLS:
        if '–' in r[c] or '—' in r[c]:
            print('DASH in', r['id'], c)
