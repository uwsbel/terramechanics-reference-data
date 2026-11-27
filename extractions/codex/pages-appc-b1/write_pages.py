from pathlib import Path

OUT = Path(__file__).parent

def page(n, body, fid=None, rotation=0, sections='[]'):
    figures = f'["{fid}"]' if fid else '[]'
    header = f'''---
source: bendix-1968-vol2
pdf_page: {n}
printed_page: "C-{n-114}"
sections: {sections}
figures: {figures}
tables: []
equations: []
rotation: {rotation}
image: corpus/1968-vol2/images/p{n:04}.png
transcriber: codex
review_status: single-reading
---
'''
    (OUT / f'p{n:04}.md').write_text(header + body.strip() + '\n', encoding='utf-8')

def figure(n, fid, caption, axes, legend, description, text='', rotation=0, annotations=''):
    caption = caption.replace('\n', ' ')
    body = f'''::: figure {fid}
caption: {caption}
axes: {axes}
legend: {legend}
description: {description}
:::
'''
    if text:
        body = text + '\n\n' + body
    if annotations:
        body += '\n' + annotations + '\n'
    page(n, body, fid, rotation)

def sheet(n, fid, heading, rows, xexp='-3', yexp='-3', ysymbol='δ_σ', cols='σ (PSF), γ (PCF)', dash='-', caption=None, markers=None, ysic=False, inch='in.', annotations='Same Notation As Above'):
    if caption is None:
        caption = f'Figure {fid[1:]}. Direct Shear Test Data {dash} Shear Stress vs. Shear Displacement\nDilation Displacement vs. Shear Displacement'
    if markers is None:
        markers = ['×', '*', '□', '+', '▽', '△', '○'] if len(rows)==7 else ['×', '*', '□', '▽', '△', '○'] if len(rows)==6 else ['×', '*', '□', '△', '○']
    legend = cols + '; ' + '; '.join(f'{m} {a}, {b}' for m,(a,b) in zip(markers,rows))
    sic = ' [sic]' if ysic else ''
    figure(n, fid, caption, f'x $δ_τ$ x 10^{xexp} ({inch}); y τ (PSF); y2 ${ysymbol}${sic} x 10^{yexp} ({inch})', legend, f'Two panels showing shear stress and dilation displacement against shear displacement, with {len(rows)} test series in each panel.', heading, annotations=annotations)

page(115, '''# APPENDIX C

# DIRECT SHEAR TEST DATA

The direct shear test data presented in this appendix was obtained from tests performed by the Civil Engineering Department of the University of Notre Dame under the supervision of Dr. Bruce B. Schimming, Associate Professor. One exception on Figure C-5A is noted.

Figures C-1A through C-7B are the data sheets and failure envelopes for the original series of tests performed on the test soils. Figures C-8 through C-15 present the failure envelopes plotted by the Univac 1107 computer on a CAL-COMP PLOTTER at Notre Dame. Where more than one series of tests were performed on a given soil, the figures are numbered "A," "B," "C," etc., and the last figure in the series represents a combined plot of all tests.

Finally, Figures C-16 through C-22 show the relationship between angle of internal friction and relative density indicated by the direct shear tests for each soil. Figure C-23 plots the average relationship for all soils except soil number 10.''', sections='["C"]')

figure(116, 'FC-1A', 'Figure C-1A. Failure Envelopes (Maximum Shear Stress vs. Normal Stress)',
        'x (PSF); y max (PSF)',
        'RS SOIL; ○ γ = 46.7 to 47.4 Lb./Ft.³ ($D_r$ = .50 to .57); ● γ = 49.2 to 51.1 Lb./Ft.³ ($D_r$ = .73 to .88); △ γ = 53 to 55.4 Lb./Ft.³ ($D_r$ = 1.0 to 1.16)',
        'One panel with three failure envelopes and test markers.', annotations='51°\n\n47°\n\n45.5°')

sheet(117, 'FC-1B', 'RS Soil\n\nγ = 46.7 to 47.4 Lb./Ft.³ ($D_r$ = .5 to .57)',
      [('3520','46.7'),('2935','46.8'),('2345','46.7'),('1760','46.7'),('1172','46.8'),('587','47.2'),('294','47.4')], xexp='3', yexp='3', dash='= [sic]')
sheet(118, 'FC-1C', 'RS Soil\n\nγ = 49.2 to 51.1 Lb./Ft.³ ($D_r$ = .73 to .88)',
      [('3520','49.5'),('2935','49.7'),('2345','49.2'),('1760','50.3'),('1172','49.4'),('587','51.1'),('294','49.4')], yexp='3')
sheet(119, 'FC-1D', 'RS Soil\n\nγ = 53 to 55.4 Lb./Ft.³ ($D_r$ = 1.0 to 1.16)',
      [('3520','54.3'),('2935','53.6'),('2345','55.4'),('1468','53.0'),('587','54.1'),('294','54.5'),('0','54.5')], markers=['×','*','□','▽','△','○','●'])
figure(120, 'FC-2A', 'Figure C-2A. Failure Envelopes - Maximum Shear Stress vs. Normal Stress',
        'x σ (PSF); y τ (PSF)',
        'PS Soil; □ γ = 25.6 to 26.8 Lb./Ft.³ ($D_r$ = .33 to .53); ○ γ = 31.7 to 33.1 Lb./Ft.³ ($D_r$ = 1.15 to 1.3)',
        'One panel with two failure envelopes and test markers.', annotations='49.5°\n\n46.7°')

sheet(121, 'FC-2B', 'PS Soil\n\nγ = 25.6 to 26.8 Lb./Ft.³ ($D_r$ = .33 to .53)',
      [('4400','25.7'),('3660','25.9'),('2935','26.8'),('2200','25.6'),('1468','25.6'),('734','25.6')], ysymbol='γ_σ', ysic=True, markers=['*','×','□','△','○','●'])
sheet(122, 'FC-2C', 'PS Soil\n\nγ = 31.7 to 33.1 Lb./Ft.³ ($D_r$ = 1.15 to 1.3)',
      [('4400','32.8'),('3660','32.1'),('2935','31.7'),('2200','32.2'),('1468','31.8'),('734','33.1')], cols='σ (PSF), τ [sic] (PCF)', markers=['*','×','□','△','○','●'])
figure(123, 'FC-3A', 'Figure C-3A. Failure Envelopes - Maximum Shear Stress vs. Normal Stress',
        'x σ (PSF); y τ (PSF)',
        'RSM-a Soil; ○ γ = 57.9 to 59.4 Lb./Ft.³ ($D_r$ = 0 to .15); □ γ = 75 Lb./Ft.³ ($D_r$ = 1.0 to 1.3)',
        'One panel with two failure envelopes and test markers.', annotations='47°\n\n38°')
sheet(124, 'FC-3B', 'RSM-a Soil\n\nγ = 57.9 to 59.4 Lb./Ft.³ ($D_r$ = 0 to .15)',
      [('4695','57.9'),('3815','57.9'),('2934','57.9'),('1761','57.9'),('734','59.4')], cols='τ [sic] (PSF), γ (PCF)', markers=['+','○','▽','□','△'])

sheet(125, 'FC-3C', 'RSM-a Soil\n\nγ = 75 Lb./Ft.³ ($D_r$ = 1.0 to 1.3)',
      [('4695','75.0'),('3815','75.0'),('2934','75.0'),('1761','75.0'),('734','75.0')], markers=['+','○','▽','□','△'])
figure(126, 'FC-4A', 'Figure C-4A. Failure Envelopes - Maximum Shear Stress vs. Normal Stress',
        'x σ (PSF); y τ (PSF)',
        'RC2 Soil; □ γ = 81.8 Lb./Ft.³ ($D_r$ = .95); ○ γ = 58.7 Lb./Ft.³ ($D_r$ = 0)',
        'One panel with two failure envelopes and test markers.', annotations='53°\n\n43°')
sheet(127, 'FC-4B', 'RC2 Soil\n\nγ = 58.7 Lb./Ft.³ ($D_r$ = 0)',
      [('4695','58.7'),('3815','58.7'),('2934','58.7'),('1761','58.7'),('734','58.7')], markers=['+','○','▽','□','△'])
sheet(128, 'FC-4C', 'RC2 Soil\n\nγ = 81.8 Lb./Ft.³ ($D_r$ = .95)',
      [('4695','81.8'),('3815','81.8'),('2934','81.8'),('1761','81.8'),('741','81.8')], markers=['+','○','△','□','▽'])

figure(129, 'FC-5A', 'Figure C-5A. Failure Envelopes - Maximum Shear Stress vs. Normal Stress',
        'x σ (PSF); y τ (PSF)',
        'SS Soil; ○ γ = 95.2 to 97.6 Lb./Ft.³ ($D_r$ = .02 to .13); □ γ = 100 Lb./Ft.³ ($D_r$ = .30); ▽ γ = 103 Lb./Ft.³ ($D_r$ = .48); △ γ = 107 Lb./Ft.³ ($D_r$ = .77)',
        'One panel with four failure envelopes and test markers; a brace groups the last three legend entries with the Bendix report attribution.',
        annotations='Bendix Report No. MM-65-2\nInterim Report of Lunar Landing Dynamics Specific Systems Engineering Study\n\n41.5°\n\n36.9°\n\n32.8°\n\n29°')
sheet(130, 'FC-5B', 'SS Soil\n\nγ = 95.2 to 97.3 Lb./Ft.³ ($D_r$ = .02 to .13)',
      [('4695','96.4'),('3815','96.4'),('2934','97.6'),('1761','96.4'),('734','95.2')], markers=['+','▽','○','□','△'], ysymbol='δ_τ', ysic=True, dash='= [sic]')
figure(131, 'FC-6A', 'Figure C-6A. Failure Envelopes - Maximum Shear Stress vs. Normal Stress',
        'x σ (PSF); y τ (PSF)',
        'LSM Soil; △ γ = 66.8 to 75.2 Lb./Ft.³ ($D_r$ = .05 to .40); ○ γ = 71.1 to 73 Lb./Ft.³ ($D_r$ [?] = .19 to .28); □ γ = 91 to 93.3 Lb./Ft.³ ($D_r$ = 1.03 to 1.07)',
        'One panel with three failure envelopes, test markers, and dashed construction lines.', annotations='3680\n\n3820')
sheet(132, 'FC-6B', 'LSM Soil\n\nγ = 71.1 to 73 Lb./Ft.³ ($D_r$ = .19 to .28)',
      [('4695','73.0'),('3815','71.1'),('2934','71.1'),('1761','71.1'),('734','71.1')], markers=['△','□','▽','○','+'], inch='in')
sheet(133, 'FC-6C', 'LSM Soil\n\nγ = 91 to 93.3 Lb./Ft.³ ($D_r$ = 1.03 to 1.07)',
      [('4695','91.0'),('3815','91.0'),('2934','91.0'),('1961','91.0'),('714','93.3')], markers=['+','▽','□','△','○'], inch='in', caption='Figure C-6C. LSM Soil Dense - Shear Stress vs. Shear Displacement\nDilation Displacement vs. Shear Displacement')
sheet(134, 'FC-6D', 'LSM Soil\n\n= 66.8 to 75.2 Lb./Ft.³ ($D_r$ = .05 to .40)',
      [('4695','73.0'),('3814','75.2'),('2934','66.8'),('1761','70.3'),('147','71.9')], markers=['+','▽','□','○','△'], inch='in', cols='σ, γ', annotations='Rebound\n\nSame Notation As Above')
figure(135, 'FC-7A', 'Figure C-7A. Failure Envelopes - Maximum Shear Stress vs. Normal Shear Stress',
        'x Normal Load - PSI; y Shear Load - PSI',
        'RSM-b Soil; ⊙ γ = 82 Lb/ft³ ($D_r$ = 0.53); dotted triangle γ = 89 Lb/ft³ ($D_r$ = 1.0)',
        'One panel with two failure envelopes and test markers.', annotations='50.5°\n\n45°')
figure(136, 'FC-7B', 'Figure C-7B. Direct Shear Test Data - Shear Stress vs. Shear Displacement',
        'x Horizontal Motion - Inches; y Horizontal Load - PSI',
        '(PSI), (PCF); open quarter-circle 27.1, 89; ☆ 13.8, 89; △ 10.2, 89; ◇ 6.6, 89; □ 5.1, 89; ○ 3.4, 89',
        'One panel with six series of test markers showing horizontal load against horizontal motion.', rotation=90)
figure(137, 'FC-7C', 'Figure C-7C. Direct Shear Test Data - Shear Stress vs. Shear Displacement',
        'x Horizontal Motion - Inches; y Horizontal Load - PSI',
        '(PSI), (PCF); open quarter-circle 26.5, 82; ☆ 13.8, 82; △ 10.2, 82; ◇ 6.6, 82; □ 5.1, 82; ○ 3.4, 82',
        'One panel with six series of test markers showing horizontal load against horizontal motion.', rotation=90)
