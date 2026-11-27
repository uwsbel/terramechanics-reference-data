from pathlib import Path
root=Path('out')
def page(n,sections,body,figures='',tables='',rotation=0):
 header=f'''---
source: bendix-1968-vol2
pdf_page: {n}
printed_page: "A-{n-1}"
sections: [{sections}]
figures: [{figures}]
tables: [{tables}]
equations: []
rotation: {rotation}
image: corpus/1968-vol2/images/p{n:04d}.png
transcriber: codex
review_status: single-reading
---
'''
 (root/f'p{n:04d}.md').write_text(header+body.strip()+'\n',encoding='utf-8')
page(25,'13, 14','''
# 13. Soil Test Bed Placement Procedure

Soil No. 3 was placed using a hopper and compacted with 2 passes of a roller.

# 14. Special Comments

The RS soil is susceptible to particle breakdown or degradation due to handling and testing. Such degradation leads to changes in some soil properties, unit weight in particular. If the handling method is such that this process cannot be prevented, or the soil cannot be replaced when these effects become prominent, periodic sampling of the soil test bed should be made in order that the effects be known quantitatively.
''')
page(26,'1, 2, 3, 4, 5','''
# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 4

# 1. Bendix Designation: RS, Dense

# 2. Description: Red narrowly-graded crushed andesitic volcanic scoria (volcanic cinders).

# 3. Source: Cinder Products Company

3450 Lakeshore Avenue, Oakland, California 94610

# 4. Source Name: Volcalite

# 5. Chemical Analysis:

| | | Volcalite* | Hypersthene Andesite (a, pp. 456-466) |
| --- | --- | --- | --- |
| Silica | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25 |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |
| Calcium Oxide | (CaO) | 8.11 | 7.53 |
| Magnesium Oxide | (MgO) | 5.58 | 4.07 |
| Sodium Oxide | (NaO) | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

Footnotes:

*Chemical analysis provided by producer.
''',tables='TA-p026')
page(27,'6, 7','''
# 6. Petrological Description

Highly porous volcanic (extrusive) rock of "basic" composition, commonly termed volcanic scoria. A comparison of the chemical analysis provided by the producer with other published analyses (a, pp. 456-466; b, pp. 126-131) indicates that the rock type is an andesite. Figure A-13 is a photomicrograph of the RS soil.

# 7. Mineralogical Description

No mineralogic analysis of the test soil has been done, but a normative analysis of the hypersthene andesite reported by Clarke (a, p. 458) gives the following:

| | |
| --- | --- |
| Quartz | 9.1% |
| Orthoclase | 8.3% |
| Albite | 27.8% |
| Anorthite | 30.9% |
| Diopside | 5.3% |
| Hypersthene | 13.2% |
| Magnetite | 3.5% |
| Ilmenite | 0.8% |

The reddish color of the RS soil would indicate that this material contains iron hydroxides (e.g., limonite) rather than the magnetite and ilmenite referred to in the norm and probably constitutes a larger percentage of the RS material than the iron minerals used in the example.

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g., magnetite, ilmenite) tend to form iron hydroxides (e.g., limonite); the femic minerals (e.g., hypersthene) to form chlorite (chloritization); and the feldspars (e.g. orthoclase, albite) to [cont. next page]
''',tables='TA-p027')
page(28,'','''
Scale Graduated In 1/32 Inch Increments

::: figure FA-13
caption: Figure A-13. Photomicrograph RS Soil
axes: none
legend: none
description: Photomicrograph of soil grains beside a graduated scale.
:::
''',figures='FA-13',rotation=90)
page(29,'8, 9, 10, 11, 12','''
[cont.] form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.

# 8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-14 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study. All data shown is for unused, undegraded material.

# 10. Density and Relative Density

The average relative density of Soil No. 4 is about 0.8. Figure A-15 shows the relationship between soil unit weight (density) and relative density for the RS soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests on unused, undegraded soil, and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results

Figure A-16 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests.

This figure indicates that the angle of internal friction for Soil No. 4 is about 47.9°.

The complete data obtained from the direct shear tests is given in Appendix C.

# 12. Sonic Velocity Test

The values of initial tangent modulus yielded for Soil No. 4 by this test is about 10,900 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio). A detailed description of the test apparatus and procedures is given in Appendix B.
''')
page(30,'','''
# GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 2.2mm | 2.1-2.3mm |
| Effective Diameter | $D_{10}$ | 1.3mm | 1.2-1.4mm |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | 1.7 | --- |
| Coarseness | $D_{95}$ | 2.8mm | 2.8-3.0mm |

::: figure FA-14
caption: Figure A-14. Average and Range of Three Examples of Unused RS Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: Grain size distribution curves with an inset table of grain size parameters.
:::

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |
''',figures='FA-14',rotation=90)
page(31,'','''
40.1

41.3

42.5

51.8

52.9

54.0

::: figure FA-15
caption: Figure A-15. Density Versus Relative Density for RS Soil
axes: x Relative Density, $D_r$; y Minimum Density, $γ_{min}$ (pcf); y2 Maximum Density, $γ_{max}$ (pcf)
legend: none
description: Density versus relative density shown by a solid line and two dashed lines.
:::
''',figures='FA-15')
page(32,'','''
::: figure FA-16
caption: Figure A-16. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for RS Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction, φ, (Degrees)
legend: none
description: A single curve shows angle of internal friction versus relative density.
:::
''',figures='FA-16')
page(33,'13, 14','''
# 13. Soil Test Bed Placement Procedure

Soil No. 4 was placed using a hopper and compacted with 16 passes of a roller.

# 14. Special Comments

The RS soil is susceptible to particle breakdown or degradation due to handling and testing. Such degradation leads to changes in some soil properties, unit weight in particular. If the handling method is such that this process cannot be prevented, or the soil cannot be replaced when these effects become prominent, periodic sampling of the soil test bed should be made in order that the effects be known quantitatively.
''')
page(34,'1, 2, 3, 4, 5','''
# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 5

# 1. Bendix Designation: RSM - a Loose.

# 2. Description: Mixture of red narrowly-graded crushed andesitic volcanic scoria (volcanic cinders) and white narrowly-graded crushed marble.

# 3. Source:

(a) Volcanic Cinders

Cinder Products Company

3450 Lakeshore Avenue, Oakland, California 94610

(b) Crushed Marble

Terrazzo Marble Supply

5700 S. Hamilton Street, Chicago, Illinois 60636

# 4. Source Name:

(a) Volcanic Cinders - Volcalite

(b) Crushed Marble - #10 Georgia special white marble chips

# 5. Chemical Analysis:

(a) Volcanic Cinders
''')
page(35,'6','''
| | | Volcalite* | Hypersthene andesite (a, pp. 456-466) |
| --- | --- | --- | --- |
| Silica | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25 |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |
| Calcium Oxide | (CaO) | 8.11 | 7.53 |
| Magnesium Oxide | (MgO) | 5.58 | 4.07 |
| Sodium Oxide | (NaO) | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

(b) Crushed Marble. No chemical analysis available but it is primarily calcium carbonate ($CaCO_3$).

# 6. Petrological Description

(a) Volcanic Cinders.

Highly porous volcanic (extrusive) rock of "basic" composition. Commonly termed volcanic scoria. A comparison of the chemical analysis provided by the producer with other published analyses (a, pp. 456-466; b, pp. 126-131) indicates that the rock type is an andesite.

(b) Crushed Marble.

Marble is a crystalline compact variety of metamorphosed sedimentary limestone.

The volcanic cinders and crushed marble are mixed in the ratio of 5:7, respectively, by weight. Figure A-17 is a photomicrograph of the resulting RSM soil.

Footnotes:

*Chemical analysis supplied by producer.
''',tables='TA-p035')
page(36,'','''
RSM

Scale Graduated In 1/32 Inch Increments

::: figure FA-17
caption: Figure A-17. Photomicrograph RSM Soil
axes: none
legend: none
description: Photomicrograph of soil grains with an RSM label and a graduated scale.
:::
''',figures='FA-17',rotation=90)
page(37,'7','''
# 7. Mineralogical Description

(a) Volcanic Cinders.

No mineralogic analysis of the test soil has been done, but a normative analysis of the hypersthene andesite reported by Clarke (a, p. 458) gives the following:

| | |
| --- | --- |
| Quartz | 9.1% |
| Orthoclase | 8.3% |
| Albite | 27.8% |
| Anorthite | 30.9% |
| Diopside | 5.3% |
| Hypersthene | 13.2% |
| Magnetite | 3.5% |
| Ilmenite | 0.8% |

The reddish color of the RS soil would indicate that this material contains iron hydroxides (e.g., limonite) rather than the magnetite and ilmenite referred to in the norm and probably constitutes a larger percentage of the RS material than the iron minerals used in the example.

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g. magnetite, ilmenite) tend to form iron hydroxides (e.g., limonite); the femic minerals (e.g., hypersthene) to form chlorite (chloritization); and the feldspars (e.g., orthoclase, albite) to form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.
''',tables='TA-p037')
page(38,'8, 9, 10, 11','''
(b) Crushed Marble.

No mineralogic analysis of the marble was done but it consists primarily of calcite.

# 8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-18 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study. All data shown is for unused, undegraded material.

# 10. Density and Relative Density

The average relative density of Soil No. 5 is about zero. Figure A-19 shows the relationship between soil unit weight (density) and relative density for the RSM - a soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177).

The solid line represents the average of several tests on unused, undegraded soil, and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results

Figure A-20 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests.

This figure indicates that the angle of internal friction for Soil No. 5 is about 37°. The complete data obtained from the direct shear tests is given in Appendix C.
''')
page(39,'','''
# GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 2.4mm | 2.3-2.4mm |
| Effective Diameter | $D_{10}$ | 1.5mm | 1.4-1.6mm |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | 1.6 | --- |
| Coarseness | $D_{95}$ | 2.7mm | 2.7-2.8mm |

::: figure FA-18
caption: Figure A-18. Average and Range of Three Samples of Unused RSM Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: Grain size distribution curves with an inset table of grain size parameters.
:::

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |
''',figures='FA-18',rotation=90)
page(40,'','''
57.3

57.9

58.5

65.1

70.3

75.5

::: figure FA-19
caption: Figure A-19. Density Versus Relative Density for RSM Soil
axes: x Relative Density, $D_r$; y Minimum Density, γ min (pcf); y2 Maximum Density, γ max (pcf)
legend: none
description: Density versus relative density shown by a solid line and two dashed lines.
:::
''',figures='FA-19')
page(41,'','''
::: figure FA-20
caption: Figure A-20. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for RSM Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction, φ, (Degrees)
legend: none
description: A single curve shows angle of internal friction versus relative density.
:::
''',figures='FA-20')
page(42,'12, 13, 14','''
# 12. Sonic Velocity Test

No determination of initial tangent modulus was made for Soil No. 5. However, based on data for the other soils the sonic modulus at 4 psi confining pressure is estimated to be 7800 psi.

# 13. Soil Test Bed Placement Procedure

Soil No. 5 was placed using the hopper method.

# 14. Special Comments

The RSM - a soil is susceptible to particle breakdown or degradation due to handling and testing. Such degradation leads to changes in some soil properties, unit weight in particular. If the handling method is such that this process cannot be prevented, or the soil cannot be replaced when these effects become prominent, periodic sampling of the soil bed should be made in order that the effects be known quantitatively.
''')
page(43,'1, 2, 3, 4, 5','''
# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 6

# 1. Bendix Designation: RC2 Loose

# 2. Description: Red broadly-graded crushed andesitic volcanic scoria (volcanic cinders)

# 3. Source: Cinder Products Company

3450 Lakeshore Avenue, Oakland, California[?] 94610

# 4. Source Name: Volcalite

# 5. Chemical Analysis:

| | | Volcalite* | Hypersthene Andesite (a, pp. 456-466) |
| --- | --- | --- | --- |
| Silica | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25 |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |
| Calcium Oxide | (CaO) | 8.11 | 7.53 |
| Magnesium Oxide | (MgO) | 5.58 | 4.07 |
| Sodium Oxide | (NaO) | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

Footnotes:

*Chemical analysis provided by producer.
''',tables='TA-p043')
page(44,'6, 7','''
# 6. Petrological Description

Highly porous volcanic (extrusive) rock of "basic" composition, commonly termed volcanic scoria. A comparison of the chemical analysis provided by the producer with other published analyses indicates that the rock type is an andesite. Figure A-21 is a photomicrograph of the RC2 soil.

# 7. Mineralogical Description

No mineralogic analysis of the test soil has been done, but a normative analysis of the hypersthene andesite reported by Clarke (a, p. 458) gives the following:

| | |
| --- | --- |
| Quartz | 9.1% |
| Orthoclase | 8.3% |
| Albite | 27.8% |
| Anorthite | 30.9% |
| Diopside | 5.3% |
| Hypersthene | 13.2% |
| Magnetite | 3.5% |
| Ilmenite | 0.8% |

The reddish color of the RS soil would indicate that this material contains iron hydroxides (e.g., limonite) rather than the magnetite and ilmenite referred to in the norm and probably constitutes a larger percentage of the RS material than the iron minerals used in the example.

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g., magnetite, ilmenite) tend to form iron hydroxides (e.g., limonite); the femic minerals (e.g. hypersthene) to form chlorite (chloritization); and the feldspars (e.g., orthoclase, albite) to form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.
''',tables='TA-p044')
page(45,'','''
Scale Graduated In 1/32 Inch Increments

::: figure FA-21
caption: Figure A-21. Photomicrograph RC Soil
axes: none
legend: none
description: Photomicrograph of soil grains beside a graduated scale.
:::
''',figures='FA-21',rotation=90)
page(46,'8, 9, 10, 11, 12, 13','''
# 8. Moisture Contents

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-22 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study.

# 10. Density and Relative Density

The average relative density of Soil No. 6 is about zero. Figure A-23 shows the relationship between soil unit weight (density) and relative density for the RC2 soil, as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests on unused, undegraded soil, and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results

Figure A-24 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests.

The figure indicates that the angle of internal friction for Soil No. 6 is about 43°. The complete data obtained from the direct shear tests is given in Appendix C.

# 12. Sonic Velocity Test

The values of initial tangent modulus yielded for Soil No. 6 by this test is about 8000 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio).

A detailed description of the test apparatus and procedures is given in Appendix B.

# 13. Soil Test Bed Placement Procedure

Soil No. 6 was placed using the hopper method. However, the soil handling was done by shovel rather than the vacuum system.
''')
page(47,'','''
# GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 1.1mm | 0.9-2.5mm |
| Effective Diameter | $D_{10}$ | 0.07mm | 0.06-0.1mm |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | 2 5 | 15-25 |
| Coarseness | $D_{95}$ | 5.0mm | 4.1-5.5mm |

::: figure FA-22
caption: Figure A-22. Average and Range of Six Samples of RC2 Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: Grain size distribution curves with an inset table of grain size parameters.
:::

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |
''',figures='FA-22',rotation=90)
page(48,'','''
53.6

61.4

69.2

71.2

83.1

94.0

::: figure FA-23
caption: Figure A-23. Density Versus Relative Density for RC2 Soil
axes: x Relative Density, $D_r$; y Minimum Density, γ min (pcf); y2 Maximum Density, γ max (pcf)
legend: none
description: Density versus relative density shown by a solid line and two dashed lines.
:::
''',figures='FA-23')
# Final image-based corrections.
for n in [26,35,43]:
 p=root/f'p{n:04d}.md'
 s=p.read_text(encoding='utf-8').replace('(NaO) |','(NaO) [sic] |')
 p.write_text(s,encoding='utf-8')
p=root/'p0031.md'
s=p.read_text(encoding='utf-8').replace('caption: Figure A-15.','caption: Eigure [sic] A-15.').replace('$γ_{min}$','γ min').replace('$γ_{max}$','γ max')
p.write_text(s,encoding='utf-8')
p=root/'p0047.md'
s=p.read_text(encoding='utf-8').replace('axes: x Grain Size - mm;','axes: x Grain Size -[?] mm;')
p.write_text(s,encoding='utf-8')
