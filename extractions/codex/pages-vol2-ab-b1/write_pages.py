from pathlib import Path
import re

OUT = Path(__file__).parent
def page(n, body, figures=(), tables=(), rotation=0, sections=(), label=None):
    found = []
    def heading(match):
        found.append(match.group(1))
        return '# ' + match.group(0)
    body = re.sub(r'(?m)^(5\. Chemical Analysis:\*?|(?:6|7)\. (?:Petrological|Mineralogical) Description|8\. Moisture Content|9\. Grain Size Distribution|10\. Density and Relative Density|11\. Direct Shear Test Results|12\. Sonic Velocity Test|13\. Soil Test Bed Placement Procedures?|14\. Special Comments)$', lambda m: heading(re.match(r'(\d+)\..*', m.group(0))), body)
    if found:
        sections = tuple(found)
    header = f'''---
source: bendix-1968-vol2
pdf_page: {n}
printed_page: "{label or 'A-'+str(n-1)}"
sections: [{', '.join(sections)}]
figures: [{', '.join(figures)}]
tables: [{', '.join(tables)}]
equations: []
rotation: {rotation}
image: corpus/1968-vol2/images/p{n:04d}.png
transcriber: codex
review_status: single-reading
---
'''
    (OUT/f'p{n:04d}.md').write_text(header+'\n'+body.strip()+'\n', encoding='utf-8')

page(2, '''# APPENDIX A

# SOIL SPECIFICATIONS

The data presented in this appendix will give descriptions of the 12 basic soils used in the LM soil mechanics study. The descriptions will include pertinent chemical analysis, physical properties and handling methods used to maintain repeatable test bed preparation for each soil.

a. Clarke, F. W., The Data of Geochemistry, Bulletin 770, 5th Ed., U.S. Geol. Surv., Government Printing Office, Washington, D. C., 1924.

b. Tyrrell, G. W., The Principles of Petrology, Methuen and Co., Ltd., London, E. P. Dutton and Co., Inc., New York, 1926.

c. American Society for Testing and Materials, Procedures for Testing Soils, ASTM, Philadelphia 3, Pa., 4th Ed., 1964.''', sections=('A',))

page(3, '''# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 1

1. Bendix Designation: RS, Loose

2. Description: Red narrowly-graded crushed andesitic volcanic scoria (volcanic cinders).

3. Source: Cinder Products Company 3450 Lakeshore Avenue, Oakland, California 94610

4. Source Name: Volcalite

5. Chemical Analysis:

| | | Volcalite* | Hypersthene Andesite (a, pp. 456-466) |
| --- | --- | --- | --- |
| Silica | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25 |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |
| Calcium Oxide | (CaO) | 8.11 | 7.53 |
| Magnesium Oxide | (MgO) | 5.58 | 4.07 |
| Sodium Oxide | (NaO) [sic] | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

Footnotes:

* Chemical analysis provided by producer.''', tables=('TA-p003',))

page(4, '''6. Petrological Description

Highly porous volcanic (extrusive) rock of "basic" composition, commonly termed volcanic scoria. A comparison of the chemical analysis provided by the producer with other published analyses (a, pp. 456-466; b, pp. 126-131) indicates that the rock type is an andesite. Figure A-1 is a photomicrograph of the RS soil.

7. Mineralogical Description

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

The reddish color of the RS soil would indicate that this material contains iron hydroxides (e.g. limonite) rather than the magnetite and ilmenite referred to in the norm and probably constitutes a larger percentage of the RS material than the iron minerals used in the example.

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g., magnetite, ilmenite) tend to form iron hydroxides (e.g., ilmenite [sic]); the femic minerals (e.g., hypersthene) to form chlorite (chloritization); and the feldspars (e.g., orthoclase, albite) to form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.''', tables=('TA-p004',))

page(5, '''Scale Graduated In 1/32 Inch Increments

::: figure FA-1
caption: Figure A-1. Photomicrograph RS Soil
axes:
legend:
description: Photomicrograph of soil grains beside a graduated scale.
:::''', figures=('FA-1',), rotation=90)

page(6, '''8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

9. Grain Size Distribution

Figure A-2 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study. All data shown is for unused, undegraded material.

10. Density and Relative Density

The average relative density of Soil No. 1 is zero. Figure A-3 shows the relationship between soil unit weight (density) and relative density for the RS soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests on unused, undegraded soil, and the dashed lines indicate the 95% confidence limits for the data.

11. Direct Shear Test Results

Figure A-4 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests. This figure indicates that the angle of internal friction for Soil No. 1 is about 41°. The complete data obtained from the direct shear tests is given in Appendix C.

12. Sonic Velocity Test

The values of initial tangent modulus yielded for Soil No. 1 by this test is about 5500 psi at a confining pressure of .4 [?] psi (no correction made for Poisson's Ratio). A detailed description of the test apparatus and procedures is given in Appendix B.

13. Soil Test Bed Placement Procedure

Soil No. 1 was placed using the hopper method.''')

page(7, '''GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 2.2mm | 2.1-2.3mm |
| Effective Diameter | $D_{10}$ | 1.3mm | 1.2-1.4mm |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | 1.7 | --- |
| Coarseness | $D_{95}$ | 2.8mm | 2.8-3.0mm |

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |

::: figure FA-2
caption: Figure A-2. Average and Range of Three Samples of Unused RS Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend:
description: Grain size distribution curves with an inset parameter table and a soil classification strip.
:::''', figures=('FA-2',), rotation=90)

page(8, '''40.1

41.3

42.5

51.8

52.9

54.0

::: figure FA-3
caption: Figure A-3. Density Versus Relative Density for RS Soil
axes: x Relative Density, $D_r$; y Minimum Density, γ min (pcf); y2 Maximum Density, γ max (pcf)
legend:
description: A solid density line and two dashed limits plotted against relative density.
:::''', figures=('FA-3',))

page(9, '''::: figure FA-4
caption: Figure A-4. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for RS Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction φ, (Degrees)
legend:
description: A single curve of internal friction angle against relative density.
:::''', figures=('FA-4',))

page(10, '''14. Special Comments

The RS soil is susceptible to particle breakdown or degradation due to handling and testing. Such degradation leads to changes in some soil properties, unit weight in particular. If the handling method is such that this process cannot be prevented, or the soil cannot be replaced when these effects become prominent, periodic sampling of the soil test bed should be made in order that the effects be known quantitatively.''')

page(11, '''# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 2

1. Bendix Designation: PS Loose

2. Description: White narrowly-graded crushed pumice (volcanic cinders).

3. Source: James H. Rhodes and Company, 1026 W. Jackson Boulevard, Chicago, Illinois 60607

4. Source Name: Navajo Pumice

5. Chemical Analysis:*

| | | |
| --- | --- | --- |
| Silicon Dioxide | ($S_iO_2$) [sic] | 74.2% |
| Ferric Oxide | ($Fe_2O_3$) | 1.6% |
| Aluminum Oxide | ($Al_2O_3$) | 12.5% |
| Calcium Oxide | (CaO) | 0.4% |
| Magnesium Oxide _ [?] | (MgO) | 0.2% |
| Phosphorus | (P) | Trace |
| Alkalies not tested for:_ [?] | | |
| Sodium Oxide | (NaO) [sic] | 11.0% |
| Potassium Oxide | ($K_2O$) | 11.0% |
| Moisture | | 11.0% |

Footnotes:

*Provided by the supplier.''', tables=('TA-p011',))

page(12, '''6. Petrological Description

Very highly porous volcanic (extrusive) rock of "acid" or rhyolitic composition. The chemical analysis is typical of a pumice. The supplier reports that this material is mined in the area of Santa Fe, New Mexico. Pumice is formed when very silicic volcanic ejecta is deposited in water. The rapid cooling is responsible for the highly porous nature of this rock. Figure A-5 is a photomicrograph of the PS soil.

7. Mineralogical Description

No mineralogic analysis of the pumice has been done, but the chemical analysis would indicate that it was composed primarily of orthoclase and quartz.

8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

9. Grain Size Distribution

Figure A-6 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study. All data shown is for unused, undegraded material.

10. Density and Relative Density

The average relative density of Soil No. 2 is zero. Figure A-7 shows the relationship between soil unit weight (density) and relative density for PS soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests on unused, undegraded soil, and the dashed lines indicate the 95% confidence limits for the data.

11. Direct Shear Test Results

Figure A-8 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests. [cont. next page]''')

page(13, '''Scale Graduated In 1/32 Inch Increments

::: figure FA-5
caption: Figure A-5. Photomicrograph PS Soil
axes:
legend: PS
description: Photomicrograph of soil grains and a PS label beside a graduated scale.
:::''', figures=('FA-5',), rotation=90)

page(14, '''GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 1.8mm | --- |
| Effective Diameter | $D_{10}$ | 1.2mm | --- |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | 1.6 | --- |
| Coarseness | $D_{95}$ | 2.7mm | --- |

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |

::: figure FA-6
caption: Figure A-6. Average and Range for Three Samples of Unused PS Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend:
description: Grain size distribution curves with an inset parameter table and a soil classification strip.
:::''', figures=('FA-6',), rotation=90)

page(15, '''23.3

23.8

24.3

29.3

30.2

31.1

::: figure FA-7
caption: Figure A-7. Density Versus Relative Density for PS Soil
axes: x Relative Density, $D_r$; y Minimum Density, γ min (pcf); y2 Maximum Density, γ max (pcf)
legend:
description: A solid density line and two dashed limits plotted against relative density.
:::''', figures=('FA-7',))

page(16, '''::: figure FA-8
caption: Figure A-8. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for PS Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction, φ, (Degrees)
legend:
description: A single curve of internal friction angle against relative density.
:::''', figures=('FA-8',))

page(17, '''[cont.] This figure indicates that the angle of internal friction for Soil No. 2 is about 43°. The complete data obtained from the direct shear tests is given in Appendix C.

12. Sonic Velocity Test

The values of initial tangent modulus yielded for Soil No. 2 by this test is about 4500 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio). A detailed description of the test apparatus and procedures is given in Appendix B.

13. Soil Test Bed Placement Procedures

Soil No. 2 was placed using the hopper method.

14. Special Comments

The PS soil is susceptible to particle breakdown or degradation due to handling and testing. Such degradation leads to changes in some soil properties, unit weight in particular. If the handling method is such that this process cannot be prevented, or the soil cannot be replaced when these effects become prominent, periodic sampling of the soil test bed should be made in order that the effects be known quantitatively.''')

page(18, '''# LM SOIL MECHANICS STUDY

# SPECIFICATION FOR SOIL NO. 3

1. Bendix Designation: RS, Intermediate

2. Description: Red narrowly-graded crushed andesitic volcanic scoria (volcanic cinders).

3. Source: Cinder Products Company 3450 Lakeshore Avenue, Oakland, California 94610

4. Source Name: Volcalite.

5. Chemical Analysis:

| | | Volcalite* | Hypersthene Andesite (a, pp. 456-466) |
| --- | --- | --- | --- |
| Silica _ [?] | ($SiO_2$) | 54.22 | 56.88 |
| Aluminum Oxide | ($Al_2O_3$) | 25.04 | 18.25 |
| Ferric Oxide | ($Fe_2O_3$) | 4.28 | 2.35 |
| Calcium Oxide | (CaO) | 8.11 | 7.53 |
| Magnesium Oxide | (MgO) | 5.58 | 4.07 |
| Sodium Oxide | (NaO) [sic] | 1.61 | 3.29 |
| Potassium Oxide | ($K_2O$) | 0.41 | 1.42 |
| | | 99.25 | |

Footnotes:

*Chemical analysis provided by producer.''', tables=('TA-p018',))

page(19, '''6. Petrological Description

Highly porous volcanic (extrusive) rock of "basic" composition, commonly termed volcanic scoria. A comparison of the chemical analysis provided by the producer with other published analyses (a, pp. 456-466; b, pp. 126-131) indicates that the rock type is an andesite. Figure A-9 is a photomicrograph of the RS soil.

7. Mineralogical Description

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

Decomposition due to weathering tends to decrease the percentage of silica, calcium oxide and sodium oxide and increase the percentage of ferric oxides and aluminum oxide (leaching, chloritization and kaolinization). The iron oxides (e.g., magnetite, ilmenite) tend to form iron hydroxides (e.g., limonite); the femic minerals (e.g., hypersthene) to form chlorite (chloritization); and the feldspars (e.g., orthoclase, albite) to form clays (kaolinization). The chemical analyses exhibit these trends indicating that some decomposition due to weathering has occurred.''', tables=('TA-p019',))

page(20, '''Scale Graduated In 1/32 Inch Increments

::: figure FA-9
caption: Figure A-9. Photomicrograph RS Soil
axes:
legend:
description: Photomicrograph of soil grains beside a graduated scale.
:::''', figures=('FA-9',), rotation=90)

page(21, '''8. Moisture Content

All tests were run on air-dried material. Oven-drying of the air-dried soil at 230°F yielded moisture contents commonly in the range of 0.2 to 0.6% (percent of dry weight of soil).

9. Grain Size Distribution

Figure A-10 shows the range and average grain size distribution of this soil. The table on this figure lists some of the grain size parameters investigated in this study. All data shown is for unused undegraded material.

10. Density and Relative Density

The average relative density of Soil No. 3 is about 0.45. Figure A-11 shows the relationship between soil unit weight (density) and relative density for the RS soil as determined by the method of test suggested by D. M. Burmister (c, pp. 175-177). The solid line represents the average of several tests on unused, undegraded soil, and the dashed lines indicate the 95% confidence limits for the data.

11. Direct Shear Test Results

Figure A-12 shows the relationship between angle of internal friction and relative density obtained from the direct shear tests.

This figure indicates that the angle of internal friction for Soil No. 3 is about 43.9°. The complete data obtained from the direct shear tests is given in Appendix C.

12. Sonic Velocity Test

The values of initial tangent modulus yielded for Soil No. 3 by this test is about 8600 psi at a confining pressure of 4 psi (no correction made for Poisson's Ratio).

A detailed description of the test apparatus and procedures is given in Appendix B.''')

page(22, '''GRAIN SIZE ANALYSIS CURVES - LM SMS

Grain Size Parameters

| Name | Symbol | Value | |
| --- | --- | --- | --- |
| | | Average | Range |
| Mean Size | $D_{50}$ | 2.2mm | 2.1-2.3mm |
| Effective Diameter | $D_{10}$ | 1.3mm | 1.2-1.4mm |
| Coefficient of Uniformity ($D_{60}/D_{10}$) | $C_u$ | 1.7 | --- |
| Coarseness | $D_{95}$ | 2.8mm | 2.8-3.0mm |

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |

::: figure FA-10
caption: Figure A-10. Average and Range of Three Samples of Unused RS Soil
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend:
description: Grain size distribution curves with an inset parameter table and a soil classification strip.
:::''', figures=('FA-10',), rotation=90)

page(23, '''40.1

41.3

42.5

51.8

52.9

54.0

::: figure FA-11
caption: Figure A-11. Density Versus Relative Density for RS Soil
axes: x Relative Density, $D_r$; y Minimum Density, γ min (pcf); y2 Maximum Density, γ max (pcf)
legend:
description: A solid density line and two dashed limits plotted against relative density.
:::''', figures=('FA-11',), label='A=22')

page(24, '''::: figure FA-12
caption: Figure A-12. Angle of Internal Friction (as determined by the direct shear test) Versus Relative Density for RS Soil
axes: x Relative Density, $D_r$; y Angle of Internal Friction, φ, (Degrees)
legend:
description: A single curve of internal friction angle against relative density.
:::''', figures=('FA-12',))
