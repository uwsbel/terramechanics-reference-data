from pathlib import Path

OUT = Path(__file__).resolve().parent

def write_page(n, page, fig, body):
    header = f'''---
source: bendix-1968-vol2
pdf_page: {n}
printed_page: "{page}"
sections: []
figures: ["FC-{fig}"]
tables: []
equations: []
rotation: 0
image: corpus/1968-vol2/images/p{n:04d}.png
transcriber: codex
review_status: single-reading
---
'''
    (OUT / f'p{n:04d}.md').write_text(header + body + '\n', encoding='utf-8')

# Manually read from the supplied PNGs; no text-recognition input.
envelopes = [
    (138, 'C-24', '8', 'RS LOOSE', 'RS Loose', '40.40', '38.63', '.7992', '242.12'),
    (139, 'C-25', '9A', 'RS Dense', 'RS Dense', '54.20', '52.55', '1.3059', '634.20'),
    (140, 'C-26', '9B', 'RS DENSE', 'RS Dense', '54.40', '46.65', '1.0594', '698.23'),
    (141, 'C-27', '9C', 'RS DENSE', 'RS Dense', '54.30', '49.39', '1.1663', '700.44'),
    (142, 'C-28', '10A', 'PS Loose', 'PS Loose', '25.90', '43.44', '.9471', '488.69'),
    (143, 'C-29', '10B', 'PS Loose', 'PS Loose', '24.60', '43.40', '.9459', '169.22'),
    (144, 'C-30', '10C', 'PS Loose', 'PS Loose', '25.40', '43.70', '.9558', '359.69'),
    (145, 'C-31', '11A', 'RSM Loose', 'RSM Loose', '58.20', '35.92', '.7244', '444.69'),
    (146, 'C-32', '11B', 'RSM Loose', 'RSM Loose', '58.30', '37.38', '.7641', '785.77'),
    (147, 'C-35', '13', 'SS Loose', 'SS Loose', '95.20', '29.76', '.5718', '-1.87 [?]'),
    (148, 'C-34', '12', 'RC2 Loose', 'RC2 Loose', '58.00', '43.07', '.9349', '145.81'),
    (149, 'C-33', '11C', 'RSM Loose', 'RSM Loose', '58.20', '37.07', '.7556', '584.29'),
    (150, 'C-36', '14', 'LSM Loose', 'LSM Loose', '75.20', '43.95', '.9642', '-109.97'),
    (151, 'C-37', '15', 'LSM Dense', 'LSM Dense', '91.20', '41.05', '.8710', '213.76 [?]'),
]

for n, page, fig, heading, caption, density, angle, tangent, cohesion in envelopes:
    write_page(n, page, fig, f'''
{heading}

Avg. Density = {density}

Angle of Friction = {angle}

Tan Theta = {tangent}

Cohesion = {cohesion}

::: figure FC-{fig}
caption: Figure C-{fig}. {caption}
axes: x Normal Stress (PSF) (x 10^1); y Shear Strength (PSF) (x 10^1)
legend:
description: A single panel shows shear strength against normal stress with open triangle markers and a solid fitted line.
:::
''')

friction = [
    (152, 'C-38', '16', 'RS Soil', 'A single panel shows friction angle against relative density with open circles, horizontal connecting segments, a solid curve, and two dashed bounding curves.'),
    (153, 'C-39', '17', 'PS Soil', 'A single panel shows friction angle against relative density with open circles, a horizontal connecting segment, a solid curve, and two dashed bounding curves.'),
    (154, 'C-40', '18', 'RSM-a Soil', 'A single panel shows friction angle against relative density with open circles, a horizontal connecting segment, a solid curve, and two dashed bounding curves.'),
    (155, 'C-41', '19', 'RC2 Soil', 'A single panel shows friction angle against relative density with two open circles, a solid curve, and two dashed bounding curves.'),
    (156, 'C-42', '20', 'SS Soil', 'A single panel shows friction angle against relative density with open circles, a horizontal connecting segment, a solid S-shaped curve, and two dashed bounding curves.'),
    (157, 'C-43', '21', 'LSM Soil', 'A single panel shows friction angle against relative density with open circles and horizontal connecting segments in a crosshatched horizontal band.'),
    (158, 'C-44', '22', 'RSM-b Soil', 'A single panel shows friction angle against relative density with two open circles, a solid line, and two dashed bounding lines.'),
]

for n, page, fig, heading, description in friction:
    write_page(n, page, fig, f'''
{heading}

::: figure FC-{fig}
caption: Figure C-{fig}. Angle of Internal Friction vs. Relative Density
axes: x $D_r$; y $φ_{{DS}}$ - Degrees
legend:
description: {description}
:::
''')

write_page(159, 'C-45/C-46', '23', '''
::: figure FC-23
caption: Figure C-23. Angle of Internal Friction Versus Relative Density (From Direct Shear Test Results)
axes: x $D_r$; y $φ_{DS}$ - Degrees
legend: RC2; PS; RS; RSM-b; RSM-a; SS
description: A single panel compares six labeled soil curves of friction angle against relative density using solid and broken line styles.
:::
''')
