from pathlib import Path

OUT = Path(__file__).parent
def page(n, body, sections=(), figures=(), tables=(), rotation=0):
    def seq(v): return '[' + ', '.join(map(str,v)) + ']'
    header = f'''---
source: bendix-1968-vol2
pdf_page: {n}
printed_page: "A-{n-1}"
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
    (OUT / f'p{n:04d}.md').write_text(header + body.strip() + '\n', encoding='utf-8')

page(73, '''
(a) Volcanic cinders (Continued)

| | | Volcalite* | Hypersthene Andesite (a, p. 458) |
| --- | --- | --- | --- |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |
| Calcium Oxide | (CaO) | 5.58 | 4.07 |
| Sodium Oxide | (NaO) [sic] | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

(b) Clay

| | |
| --- | --- |
| Ignition loss | 9.4% |
| Silica | 57.3% |
| Alumina | 28.5% |
| Iron Oxide | 1.1% |
| Titania | 2.0% |
| Lime | 0.1% |
| Magnesia | 0.2% |
| Alkalies | 1.2% |
| Sulphur | 0.2% |
| Total | 100.0% |

# 6. Petrological Description

(a) Volcanic cinders.

Highly porous volcanic (extrusive) rock of "basic" composition commonly termed volcanic scoria. A comparison of the chemical analysis provided by the producer with other published analyses (a, pp. 456-466; (b, pp. 126-131) indicates that the rock type is an andesite.

Footnotes:

*Chemical analysis provided by supplier.
''', sections=[6], tables=['TA-p073'])

page(74, '''
(b) Clay.

The supplier reports that this material is essentially a kaolin-type clay.

The volcanic cinders (RC2 type) and clay are mixed 1:1 (by weight) to produce the LSM soil. Figure A-37 is a photomicrograph of the LSM soil.

# 7. Mineralogical Description

(a) Volcanic cinders.

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

The reddish color of the RC soil would indicate that this material contains iron hydroxides (e.g., limonite) rather than the magnetite and ilmenite referred to in the norm and probably constitutes a larger percentage of the RC material than the iron minerals used in the example.

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g., magnetite, ilmenite) tend to form iron hydroxides (e.g., limonite); the femic minerals (e.g., hypersthene) to [cont. next page]
''', sections=[7], tables=['TA-p074'])

page(75, '''
Scale Graduated In 1/32 Inch Increments

::: figure FA-37
caption: Figure A-37. Photomicrograph LSM Soil
axes: none
legend: none
description: Photomicrograph of soil grains beside a graduated scale.
:::
''', figures=['FA-37'], rotation=90)

page(76, '''
[cont.] form chlorite (chloritization); and the feldspars (e.g., orthoclase, albite) to form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.

(b) Clay

No mineralogic analysis of the clay was done but the supplier reports that the major component of the clay is kaolin.

# 8. Moisture Content

All test [sic] were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-38 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study.

# 10. Density and Relative Density

The average relative density of Soil No. 10 is about 0.5. Figure A-39 shows the relationship between soil unit weight (density) and relative density for the LSM soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests, and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results

Figure A-40 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests. This figure indicates that the angle of internal friction for Soil No. 10 is about 42°. The complete data obtained from the direct shear tests is given in Appendix C.
''', sections=[8,9,10,11])

page(77, '''
GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 0.07mm | 0.06-0.08mm |
| Effective Diameter | $D_{10}$ | Small | ---- |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | Large | ---- |
| Coarseness | $D_{95}$ | 4.1mm | 4.0-4.2mm |

| | | | | | |
| --- | --- | --- | --- | --- | --- |
| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| | CLAY (Plastic) | SAND | | | GRAVEL |

::: figure FA-38
caption: Figure A-38. Average and Range of Seven Samples of LSM
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: Grain size distribution curves with an inset parameter table and soil classification bands.
:::
''', figures=['FA-38'], rotation=90)

page(78, '''
66.6

67.8

69.0

88.1

90.2

92.3

::: figure FA-39
caption: Figure A-39. Density versus Relative Density for LSM Soil
axes: x Relative Density, $D_r$; y Minimum Density, $γ_{min}$ (pcf); y2 Maximum Density, $γ_{max}$ (pcf)
legend: none
description: A solid density line and two dashed lines connect the minimum and maximum density axes.
:::
''', figures=['FA-39'])

page(79, '''
::: figure FA-40
caption: Figure A-40. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for LSM Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction, φ, (Degrees)
legend: none
description: A crosshatched horizontal band shows the range of friction angles against relative density.
:::
''', figures=['FA-40'])

page(80, '''
# 12. Sonic Velocity Test

The value of initial tangent modulus was not obtained for Soil No. 10. Tests on LSM soil with $D_r$ = 0.77 gave values of initial tangent [?] modulus between 5,000 and 6,000 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio). The estimated initial tangent modulus for this soil is 4000 psi. A detailed description of the test apparatus and procedures is given in Appendix B.

# 13. Soil Test Bed Placement Procedure

Soil No. 10 was placed with a hopper but was handled by shovel rather than the vacuum system. Each layer (covered with a strip of cardboard) was rolled two times (one pass back and forth in the bin).

# 14. Special Conditions

The values of angle of internal friction obtained for the loose and dense LSM soil in the direct shear test were essentially the same - about 40° to 45°. This was due to the fact that the loose soil tended to densify upon application of the normal load.

For this reason it was not possible to construct a φ vs. $D_r$ curve. The scatter band shown in Figure A-40 is the estimated range of φ for $D_r$ values ranging from .40 to 1.00 based on examination of the direct shear test results.
''', sections=[12,13,14])

page(90, '''
# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 12

# 1. Bendix Designation: RSM-b Dense.

# 2. Description:

Mixture of red narrowly-graded crushed andesitic volcanic scoria (volcanic cinders) and white narrowly-graded crushed marble.

# 3. Source:

(a) Volcanic Cinders - Cinder Products Company 3450 Lakeshore Avenue, Oakland, California 94610

(b) Crushed Marble - Terrazzo Marble Supply 5700 S. Hamilton Street Chicago, Illinois 60636

# 4. Source Name:

(a) Volcanic Cinders - Volcalite

(b) Crushed Marble - #10 Georgia special white marble chips

# 5. Chemical Analysis:

(a) Volcalite Cinders

| | | Volcalite* | Hypersthene Andesite (a, pp. 456-466 [?]) |
| --- | --- | --- | --- |
| Silica | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25 |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |

Footnotes:

*Chemical analysis supplied by producer.
''', sections=[1,2,3,4,5], tables=['TA-p090'])

page(91, '''
(a) Volcanic Cinders. (Continued)

| | | Volcalite* | Hypersthene Andesite (a, pp. 456-466) |
| --- | --- | --- | --- |
| Calcium Oxide | (CaO) | 8.11 | 7.53 |
| Magnesium Oxide | (MgO) | 5.58 | 4.07 |
| Sodium Oxide | (NaO) [sic] | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

(b) Crushed Marble:

No chemical analysis available but primarily calcium carbonate ($CaCO_3$).

# 6. Petrological Description

(a) Volcanic Cinders.

Highly porous volcanic (extrusive) rock of "basic" composition. Commonly termed volcanic scoria. A comparison of the chemical analysis provided by the producer with other published analyses (a, pp. 456-466; b, pp. 126-131) indicates that the rock type is an andesite.

(b) Crushed Marble.

Marble is a crystaline [sic] compact variety of metamorphosed sedimentary limestone.

The volcanic cinders and crushed marble are mixed in the ratio of 1:3, respectively, by weight. Figure A-45 is a photomicrograph of the resulting RSM.

# 7. Mineralogical Description

(a) Volcanic Cinders.

Footnotes:

*Chemical analysis supplied by producer.
''', sections=[6,7])

page(92, '''
RSM

Scale Graduated In 1/32 Inch Increments

::: figure FA-45
caption: Figure A-45. Photomicrograph RSM Soil
axes: none
legend: none
description: Photomicrograph of soil grains with an RSM label and a graduated scale.
:::
''', figures=['FA-45'], rotation=90)

page(93, '''
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

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g., magnetite, ilmenite) tend to form iron hydroxides (e.g., limonite); the femic minerals (e.g., hypersthene) to form chlorite (chloritization); and the feldspars (e.g., orthoclase, albite) to form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.

(b) Crushed Marble.

No mineralogic analysis of the marble was done but it consists primarily of calcite.
''', tables=['TA-p093'])

page(94, '''
# 8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-46 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study. All data shown is for unused, undegraded material.

# 10. Density and Relative Density

The average relative density of Soil No. 12 is about 0.75. Figure A-47 shows the relationship between soil unit weight (density) and relative density for the RSM soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177 [?]).

# 11. Direct Shear Test Results

Figure A-48 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests.

This figure indicates that the angle of internal friction for Soil No. 12 is about 37°.

The complete data obtained from the direct shear tests is given in Appendix C.

# 12. Sonic Velocity Test

No determination of initial tangent modulus was made for Soil No. 12. Based on the results of tests with other soils the modulus is estimated to be in the vicinity of 20,000 psi.

# 13. Soil Test Bed Placement Procedure

Soil No. 12 was placed by shovel and rolled with 10 passes per two inch layer using the lawn roller equipment.
''', sections=[8,9,10,11,12,13])

page(95, '''
GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 2.15 | 2.1-2.2 |
| Effective Diameter | $D_{10}$ | 1.23 | 1.2-1.3 |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | 1.87 | --- |
| Coarseness | $D_{95}$ | 2.9 | 2.9 |

| | | | | | |
| --- | --- | --- | --- | --- | --- |
| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| | CLAY (Plastic) | SAND | | | GRAVEL |

::: figure FA-46
caption: Figure A-46. Average and Range of Sample of Unused RSM-b Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: Grain size distribution curves with an inset parameter table and soil classification bands.
:::
''', figures=['FA-46'], rotation=90)

page(96, '''
73.5

74.4

75.3

89.4

::: figure FA-47
caption: Figure A-47. Density Versus Relative Density for RSM Soil
axes: x Relative Density, $D_r$; y Minimum Density, $γ_{min}$ (pcf); y2 Maximum Density, $γ_{max}$ (pcf)
legend: none
description: Three density lines connect the minimum and maximum density axes.
:::
''', figures=['FA-47'])

page(97, '''
::: figure FA-48
caption: Figure A-48. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for RSM Soil
axes: x Relative Density, Dr; y Angle of Internal Friction, φ, (Degrees)
legend: none
description: A single curve shows friction angle against relative density.
:::
''', figures=['FA-48'])

page(81, '''
# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 11

# 1. Bendix Designation: LSM Dense

# 2. Description:

Mixture of red broadly-graded crushed andesitic (volcanic cinders) and light gray kaolin-type clay.

# 3. Source:

(a) Volcanic cinders - Cinder Products Company 3450 Lakeshore Avenue, Oakland, California 94610

(b) Clay - Cedar Heights Clay Company 50 Portsmouth Road, Oak Hill, Ohio

# 4. Source Name:

(a) Volcanic cinders - Volcalite

(b) Clay - Cedar Heights Airfloated Bonding Clay.

# 5. Chemical Analysis

(a) Volcanic cinders.

| | | Volcalite* | Hypersthene Andesite (a, p. 458) |
| --- | --- | --- | --- |
| Silica | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25 |

Footnotes:

*Chemical analysis provided by supplier.
''', sections=[1,2,3,4,5], tables=['TA-p081'])

page(82, '''
(a) Volcanic cinders (Continued)

| | | Volcalite* | Hypersthene Andesite (a, p. 458) |
| --- | --- | --- | --- |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |
| Calcium Oxide | (CaO) | 8.11 | 7.53 |
| Magnesium Oxide | (MgO) | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

(b) Clay

| | |
| --- | --- |
| Ignition loss | 9.4% |
| Silica | 57.3% |
| Alumina | 28.5% |
| Iron Oxide | 1.2% |
| Titania | 2.0% |
| Lime | 0.1% |
| Magnesia | 0.2% |
| Alkalies | 1.2% |
| Sulphur | 0.2% |
| Total | 100.0% |

# 6. Petrological Description

(a) Volcanic cinders

Highly porous volcanic (extrusive) rock of "basic" composition termed volcanic scoria. A comparison of the chemical analysis provider [sic] by the producer with other published analyses (a, pp. 456-466; b, pp. 126-131) indicates that the rock type is an andesite.

Footnotes:

*Chemical analysis provided by supplier.
''', sections=[6], tables=['TA-p082'])

page(83, '''
(b) Clay

The supplier reports that this material is essentially a kaolin-type clay.

The volcanic cinders (RC2 type) and clay are mixed 1:1 (by weight) to produce the LSM soil. Figure A-41 is a photomicrograph of the LSM soil.

# 7. Mineralogical Description

(a) Volcanic cinders.

No mineralogic analysis of the test soil has been done, but a normative analysis of the hypersthene andesite reported by Clarke (a, p. 458) gives the following:

| | |
| --- | --- |
| Quartz | 9.1% |
| Orthoclase | 8.3% |
| Albite. | 27.8% |
| Anorthite | 30.9% |
| Diopside | 5.3% |
| Hypersthene | 13.2% |
| Magnetite | 3.5% |
| Ilmenite | 0.8% |

The reddish color of the RC soil would indicate that this material contains iron hydroxides (e.g., limonite) rather than the magnetite and ilmenite referred to in the norm and probably constitutes a larger percentage of the RC material than the iron minerals used in the example.

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g., magnetite, ilmenite) tend to form iron hydroxides (e.g., limonite); the femic minerals (e.g., hypersthene) [cont. next page]
''', sections=[7], tables=['TA-p083'])

page(84, '''
Scale Graduated In 1/32 Inch Increments

::: figure FA-41
caption: Figure A-41. Photomicrograph LSM Soil
axes: none
legend: none
description: Photomicrograph of soil grains beside a graduated scale.
:::
''', figures=['FA-41'], rotation=90)

page(85, '''
[cont.] to form chlorite (chloritization); and the feldspars (e.g., orthoclase, albite) to form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.

(b) Clay

No mineralogic analysis of the clay was done but the supplier reports that the major component of the clay is kaolin.

# 8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

# 9. Grain Size Distribution

Figure A-42 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study.

# 10. Density and Relative Density

The average relative density of Soil No. 11 is about 0.70. Figure A-43 shows the relationship between soil unit weight (density) and relative density for the LSM soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests and the dashed lines indicate the 95% confidence limits for the data.

# 11. Direct Shear Test Results

Figure A-44 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests. This figure indicates that the angle of internal friction for Soil No. 11 is about 38.3°. The complete data obtained from the direct shear tests is given in Appendix C.
''', sections=[8,9,10,11])

page(86, '''
GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 0.07mm | 0.06-0.08mm |
| Effective Diameter | $D_{10}$ | Small | --- |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | Large | --- |
| Coarseness | $D_{95}$ | 4.1mm | 4.0-4.2mm |

| | | | | | |
| --- | --- | --- | --- | --- | --- |
| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| | CLAY (Plastic) | SAND | | | GRAVEL |

::: figure FA-42
caption: Figure A-42. Average and Range of Seven Samples of LSM Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: Grain size distribution curves with an inset parameter table and soil classification bands.
:::
''', figures=['FA-42'], rotation=90)

page(87, '''
66.6

67.8

69.0

88.1

90.2

92.3

::: figure FA-43
caption: Figure A-43. Density Versus Relative Density for LSM Soil
axes: x Relative Density, $D_r$; y Minimum Density, $γ_{min}$ (pcf); y2 Maximum Density, $γ_{max}$ (pcf)
legend: none
description: A solid density line and two dashed lines connect the minimum and maximum density axes.
:::
''', figures=['FA-43'])

page(88, '''
::: figure FA-44
caption: Figure A-44. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for LSM Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction, φ, (Degrees)
legend: none
description: A crosshatched horizontal band shows the range of friction angles against relative density.
:::
''', figures=['FA-44'])

page(89, '''
# 12. Sonic Velocity Test

The values of initial tangent modulus for Soil No. 11 by this test 6,000 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio). A detailed description of the test apparatus and procedures is given in Appendix B.

# 13. Soil Test Bed Placement Procedure

Soil No. 11 was placed with a hopper but was handled by shovel rather than the vacuum system. Each layer (covered with a strip of cardboard) was rolled six times (three passes back and forth in the bin).

# 14. Special Conditions

The values of angle of internal friction obtained for the loose and dense LSM soil in the direct shear were essentially the same - about 40° to 45°. This was due to the fact that the loose soil tended to densify upon application of the normal load.

For this reason it was not possible to construct a φ vs. $D_r$ curve. The scatter band shown in Figure A-44 is the estimated range of φ for $D_r$ values ranging from .40 to 1.00 based on examination of the direct shear test results.
''', sections=[12,13,14])
