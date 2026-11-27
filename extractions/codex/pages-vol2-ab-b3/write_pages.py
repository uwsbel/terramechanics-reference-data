from pathlib import Path

OUT = Path(__file__).parent

def page(n, body, sections=(), figures=(), tables=(), rotation=0, printed=None):
    def seq(v): return '[' + ', '.join(map(str,v)) + ']'
    head = f'''---
source: bendix-1968-vol2
pdf_page: {n}
printed_page: "{printed or 'A-'+str(n-1)}"
sections: {seq(sections)}
figures: {seq(figures)}
tables: {seq(tables)}
equations: []
rotation: {rotation}
image: corpus/1968-vol2/images/p{n:04d}.png
transcriber: codex
review_status: single-reading
---
'''
    (OUT/f'p{n:04d}.md').write_text(head+'\n'+body.strip()+'\n',encoding='utf-8')

def friction(n, fig, soil):
    page(n, f'''::: figure FA-{fig}
caption: Figure A-{fig}. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for {soil} Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction, φ, (Degrees)
legend: none
description: A single curve shows angle of internal friction against relative density.
:::''', figures=[f'FA-{fig}'])

friction(49,24,'the RC2')
page(50, '''# 14. Special Comments

The average curves in Figures A-22 and A-23 are combined values of used and unused soil. Since the soil was not handled using the vacuum system, no appreciable degradation effects were noted. The greatest variation in soil properties (e.g., grain size distribution and unit weight) was due primarily to unavoidable segregation of particle sizes (i.e., nonuniform grain size distribution with a soil bed and from test bed to test bed). This variation accounts for the wide range and confidence limits exhibited by this soil in Figures A-22 and A-23.''', sections=[14])

page(51, '''# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 7

# 1. Bendix Designation: SS Loose

# 2. Description: White narrowly-graded silica sand.

# 3. Source: Wedron Silica Company

135 S. LaSalle Street, Chicago, Illinois 60603

# 4. Source Name: Wedron 4040 sand.

# 5. Chemical Analysis: *

| | | |
| --- | --- | --- |
| Silica | ($SiO_2$) | 99.9% |
| Ferric | ($Fe_2O_3$) | Trace |
| Aluminum Oxide | ($Al_2O_3$) | 0.1% |
| Titanium Oxide | ($TiO_2$) | Trace |
| Calcium Oxide | (CaO) | Trace |
| Magnesium Oxide | (MgO) | Trace |

# 6. Petrological Description

Essentially pure quartz (silica) sand grains, rounded to subangular. It is mined from the St. Peter Sandstone formation in Wedron, Illinois.

Figure A-25 is a photomicrograph of the SS soil.

Footnotes:

*Provided by supplier.''', sections=range(1,7),tables=['TA-p051'])

def photo(n,fig):
    page(n,f'''::: figure FA-{fig}
caption: Figure A-{fig}. Photomicrograph SS Soil
axes: none
legend: SS
description: A photomicrograph of soil grains includes a graduated scale.
:::

Scale Graduated In 1/32 Inch Increments''',figures=[f'FA-{fig}'],rotation=90)

photo(52,25)
page(53, '''# 7. Mineralogical Description

Essentially the only mineral present in this soil is quartz (silica).

# 8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-26 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study.

# 10. Density and Relative Density

The average relative density of Soil No. 7 is about zero. Figure A-27 shows the relationship between soil unit weight (density) and relative density for the SS soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results.

Figure A-28 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests. This figure indicates that the angle of internal friction for Soil No. 7 is about 29.8°. The complete data obtained from the direct shear tests is given in Appendix C.

# 12. Sonic Velocity Test

The values of initial tangent modulus yielded for Soil No. 7 by this test is about 10,000 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio). A detailed description of the test apparatus and procedures is given in Appendix B.''',sections=range(7,13))

def grain(n,fig):
    page(n,f'''# GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{{50}}$ | 0.42mm | 0.40-0.43mm |
| Effective Diameter | $D_{{10}}$ | 0.28mm | 0.27-0.29mm |
| Coefficient of Uniformity ($D_{{60}}/D_{{10}}$) | $C_u$ | 1.5 | ---- |
| Coarseness | $D_{{95}}$ | 0.6mm | 0.58-0.62mm |

::: figure FA-{fig}
caption: Figure A-{fig}. Average and Range of Five Samples of SS Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: Grain-size distribution curves are accompanied by an inset parameter table and a soil classification strip.
:::

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |''',figures=[f'FA-{fig}'],rotation=90)

grain(54,26)

def density(n,fig):
    page(n,f'''95.4

95.8

110.5

112.7

114.9

::: figure FA-{fig}
caption: Figure A-{fig}. Density Versus Relative Density for SS Soil
axes: x Relative Density, $D_r$; y Minimum Density, $γ_{{min}}$ (pcf); y2 Maximum Density, $γ_{{max}}$ (pcf)
legend: none
description: A solid line and two dashed lines show density against relative density.
:::''',figures=[f'FA-{fig}'])

density(55,27)
friction(56,28,'SS')
page(57,'''# 13. Soil Test Bed Placement Procedure

Soil No. 7 was placed using the hopper method.

# 14. Special Conditions

This soil was not appreciably altered by degradation effects created by testing or handling with the vacuum system.''',sections=[13,14])

page(58,'''# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 8

# 1. Bendix Designation: SS Intermediate

# 2. Description: White narrowly-graded silica sand.

# 3. Source: Wedron Silica Company

135 S. LaSalle Street, Chicago, Illinois 60603

# 4. Source Name: Wedron 4040 Sand.

# 5. Chemical Analysis:*

| | | |
| --- | --- | --- |
| Silica | ($SiO_2$) | 99.9% |
| Ferric Oxide | ($Fe_2O_3$) | Trace |
| Aluminum | ($Al_2O_3$) | 0.1% |
| Titanium Oxide | ($TiO_2$) | Trace |
| Calcium Oxide | (CaO) | Trace |
| Magnesium Oxide | (MgO) | Trace |

# 6. Petrological Description

Essentially pure quartz (silica) sand grains, rounded to subangular. It is mined from the St. Peter Sandstone formation in Wedron, Illinois. Figure A-29 is a photomicrograph of the SS soil.

Footnotes:

*Provided by supplier.''',sections=range(1,7),tables=['TA-p058'])

photo(59,29)
page(60,'''# 7. _ [?] Mineralogical Description

Essentially the only mineral present in this soil is quartz (silica).

# 8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-30 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study.

# 10. Density and Relative Density

The average relative density of Soil No. 8 is about 0.53. Figure A-31 shows the relationship between soil unit weight (density) and relative density for the SS soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results

Figure A-32 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests.

This figure indicates that the angle of internal friction for Soil No. 8 is about 36.8°. The complete data obtained from the direct shear tests is given in Appendix C.

# 12. Sonic Velocity Test

The value of initial tangent modulus yielded for Soil No. 8 by this test is about 18,000 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio). A detailed description of the test apparatus and procedures is given in Appendix B.''',sections=range(7,13))

grain(61,30)
density(62,31)
friction(63,32,'SS')
page(64,'''# 13. Soil Test Bed Placement Procedure

Soil No. 8 was placed with a hopper and compacted with 8 passes of a roller.

# 14. Special Conditions

This soil was not appreciably altered by degradation effects created by testing or handling with the vacuum system.''',sections=[13,14])

page(65,'''# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 9

# 1. Bendix Designation: SS Dense

# 2. Description: White narrowly-graded silica sand.

# 3. Source: Wedron Silica Company

135 S. LaSalle Street, Chicago, Illinois 60603

# 4. Source Name: Wedron 4040 Sand.

# 5. Chemical Analysis:*

| | | |
| --- | --- | --- |
| Silica | ($SiO_2$) | 99.9% |
| Ferric Oxide | ($Fe_2O_3$) | Trace |
| Aluminum Oxide | ($Al_2O_3$) | 0.1% |
| Titanium Oxide | ($TiO_2$) | Trace |
| Calcium Oxide | (CaO) [?] | Trace |
| Magnesium Oxide | (MgO) | Trace |

# 6. Petrological Description

Essentially pure quartz (silica) sand grains, rounded to subangular. It is mined from the St. Peter Sandstone formation in Wedron, Illinois. Figure A-33 is a photomicrograph of the SS soil.

Footnotes:

*Provided by supplier.''',sections=range(1,7),tables=['TA-p065'])

photo(66,33)
page(67,'''# 7. Mineralogical Description

Essentially the only mineral present in this soil is quartz (silica).

# 8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-34 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study.

# 10. Density and Relative Density

The average relative density of Soil No. 9 is about 0.69. Figure A-35 shows the relationship between soil unit weight (density) and relative density for the SS soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results.

Figure A-36 shows the relationship between angle [?] of internal friction and relative density obtained from the direct shear tests. This figure indicates that the angle of internal friction for Soil No. 9 is about 39°. The complete data obtained from the direct shear tests is given in Appendix C.

# 12. Sonic Velocity Test

The values of initial tangent modulus yielded for Soil No. 9 by this test is about 24,000 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio). A detailed description of the test apparatus and procedures is given in Appendix B.''',sections=range(7,13))

grain(68,34)
density(69,35)
friction(70,36,'SS')
page(71,'''# 13. Soil Test Bed Placement Procedure

Soil No. 9 was placed by a hopper and compacted with 24 passes of a roller.

# 14. Special Conditions

This soil was not appreciably altered by degradation effects created by testing or handling with the vacuum system.''',sections=[13,14])

page(72,'''# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 10

# 1. Bendix Designation: LSM intermediate

# 2. Description: Mixture of red broadly-graded crushed andesitic volcanic scoria (volcanic cinders) and light gray kaolin-type clay.- [?]

# 3. Source:

(a) Volcanic cinders - Cinder Products Company 3450 Lakeshore Avenue, Oakland, California 94610

(b) Clay - Cedar Heights Clay Company 50 Portsmouth Road, Oak Hill, Ohio

# 4. Source Name:

(a) Volcanic cinders - Volcalite

(b) Clay - Cedar Heights Airfloated Bonding Clay

# 5. Chemical Analysis:

(a) Volcanic cinders.

| | | Volcalite* | Hypersthene Andesite (a, p. 458) |
| --- | --- | --- | --- |
| Silica | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25- [?] |

Footnotes:

*Chemical analysis provided by supplier.''',sections=range(1,6),tables=['TA-p072'])

# Page-specific readings established from enlarged image crops.
for n in [55,62,69]:
    p=OUT/f'p{n:04d}.md'
    s=p.read_text(encoding='utf-8').replace('$γ_{min}$','γ min').replace('$γ_{max}$','γ max')
    if n==69: s=s.replace('Maximum Density,','Maximum [?] Density [?],')
    p.write_text(s,encoding='utf-8')
p=OUT/'p0061.md'
p.write_text(p.read_text(encoding='utf-8').replace('| 1.5 | ---- |','| 1.5 | --- |'),encoding='utf-8')
p=OUT/'p0068.md'
p.write_text(p.read_text(encoding='utf-8').replace('| 0.58-0.62mm |','| 0.58-0.62mm [?] |'),encoding='utf-8')

p=OUT/'p0050.md'
s=p.read_text(encoding='utf-8').replace('Special Comments\n','Special Comments- [?]\n').replace('primarily to unavoidable','primarily to-unavoidable [sic]')
p.write_text(s,encoding='utf-8')
p=OUT/'p0060.md'
s=p.read_text(encoding='utf-8').replace('quartz (silica).','quartz (silica).- [?]')
p.write_text(s,encoding='utf-8')
p=OUT/'p0072.md'
s=p.read_text(encoding='utf-8').replace('| 25.04 |','| 25.04- [?] |')
p.write_text(s,encoding='utf-8')

# Place the outside annotations ahead of the caption block in printed order.
for n in [52,59,66]:
    p=OUT/f'p{n:04d}.md'
    s=p.read_text(encoding='utf-8')
    annotation='Scale Graduated In 1/32 Inch Increments'
    s=s.replace('\n\n'+annotation+'\n','\n').replace('::: figure ',annotation+'\n\n::: figure ',1)
    p.write_text(s,encoding='utf-8')
for n in [54,61,68]:
    p=OUT/f'p{n:04d}.md'
    s=p.read_text(encoding='utf-8')
    start=s.index('::: figure ')
    end=s.index('\n:::',start)+4
    block=s[start:end]
    s=s[:start]+s[end:].strip()+'\n\n'+block+'\n'
    p.write_text(s,encoding='utf-8')
