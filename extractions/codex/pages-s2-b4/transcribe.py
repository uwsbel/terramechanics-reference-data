from pathlib import Path
import json
OUT=Path('out')
def page(n, body, figures=[], sections=[], equations=[], rotation=0, printed=None):
 h={'source':'bendix-1968-vol1','pdf_page':n,'printed_page':printed or f'2-{n-25}','sections':sections,'figures':figures,'tables':[],'equations':equations,'rotation':rotation,'image':f'corpus/1968/images/p{n:04}.png','transcriber':'codex','review_status':'single-reading'}
 s='---\n'+'\n'.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in h.items())+'\n---\n\n'+body.strip()+'\n'
 (OUT/f'p{n:04}.md').write_text(s,encoding='utf-8')
page(94,'''Figures 2-36, 2-38, and 2-39 show the results of load-penetration tests in the RS, PS, and SS soil using 2-inch and 4-inch diameter test cylinders. The results are generally averaged from several tests done in 18" x 36" bin and are plotted as the dimensionless pressure parameter versus relative depth. Figure 2-37 is a plot of several tests done in RS soil in several sizes of bin with 1-inch, 2-inch, and 4-inch test cylinders.

Figures 2-36 and 2-37 indicate that the size effect predicted by the bearing capacity equation (i.e., that a plot of the pressure parameter $q/Dγ$, versus relative depth, $D_f/D$ will plot as the same line for any size footing in a given soil) does tend to be confirmed in the loose and intermediate RS soil (i.e., with $0.0 ≤ D_r ≤ 0.7$). There is not sufficient data to determine whether the tendency for results for the large test cylinder to plot above those for the smaller cylinder is a characteristic due to size effect or due to the slight differences noted in relative density determinations.

It is possible that the pronounced dip observed in the curve obtained for the smaller cylinder below that for the larger cylinder in Figure 2-36 for the intermediate soil (i.e., $D_r ≈ 0.46$) is a result of the method used to produce an intermediate soil (in this instance, screeding). When intermediate density was produced by a roller, as for the bottom pair of curves on Figure 2-37, this pronounced dip is not observed.

In the tests performed in dense RS soil (in Figures 2-36 and 2-37, those tests for which $D_r ≤ 0.83$), the 2-inch cylinder tests generally exhibit significantly higher values of the pressure parameter for a given relative depth than the 4-inch cylinder tests. A similar but much more pronounced, tendency is exhibited by the test with the 1-inch cylinder (Figure 2-37) in the RS soil with a relative density of 0.69. In this soil, however, the curve for the 2-inch cylinder falls below that of the 4-inch cylinder. It appears that the size effect implied in the bearing capacity equation does not hold for small diameter cylinders penetrating a dense soil. The differences increase with increasing relative density and decreasing size of cylinder.

Figures 2-38 and 2-39 representing plots of the pressure parameter versus relative depth for the SS and PS soils, respectively, indicate conclusions similar to those given for the RS soil.''')
page(95,'''::: figure F2-36
caption: Figure 2-36. Load-Penetration Test Results in RS Soil Pressure Parameter vs. Relative Depth
axes: x Relative Depth, $D_f/D$; y Dimensionless Pressure Parameter, $q/Dγ$
legend: $D_r ≈ 0.95$ 2" Cyl.; $D_r ≈ 0.83$ 4" Cyl.; $D_r ≈ 0.50$ 4" Cyl.; $D_r ≈ 0.46$ 2" Cyl.; $D_r ≈ 0.16$ 4" Cyl.; $D_r ≈ 0.14$ 2" Cyl.
description: Six load-penetration curves compare cylinder sizes and relative densities.
:::''',figures=['F2-36'])
page(96,'''::: figure F2-37
caption: Figure 2-37. Pressure Parameter vs. Relative Depth in Intermediate and Dense RS Soil
axes: x Relative Depth, $D_f/D$; y Dimensionless Pressure Parameter, $q/Dγ$
legend: $D_r ≈ 0.93$ 2" Cyl., 54" x 36" Bin; $D_r ≈ 0.95$ 2" Cyl., 18" x 36" Bin; $D_r ≈ 0.96$; $D_r ≈ 0.93$ 4" Cyl., 54" x 36" Bin; $D_r ≈ 0.83$ 4" Cyl., 18" x 36" Bin; $D_r ≈ 0.96$; $D_r ≈ 0.69$, 1" Cyl. 18" x 36" Bin; $D_r ≈ 0.69$ 4" Cyl.; $D_r ≈ 0.69$ 2" Cyl.; $D_r ≈ 0.33$ 4" Cyl.; $D_r ≈ 0.33$ 2" Cyl.
description: Labeled curves and measurement symbols compare penetration responses for several cylinders and bins.
:::

4" Cyl., 54" x 36" Bin

4" Cyl., 18" x 36" Bin

$D_r ? 0.69$, 1" Cyl. 18" x 36" Bin

108" x 36" Bin''',figures=['F2-37'],rotation=90)
page(97,'''::: figure F2-38
caption: Figure 2-38. Load - Penetration Test Results in SS Soil Pressure Parameter vs. Relative Depth
axes: x Relative Depth, $D_f/D$; y Dimensionless Pressure Parameter, $q/Dγ$
legend: dashed line 2" Cylinder; solid line 4" Cylinder; $D_r ≈ 0.98$; $D_r ≈ 0.92$; $D_r ≈ 0.47$; $D_r ≈ 0.46$; $D_r ≈ 0.14$; $D_r ≈ 0.24$
description: Six curves compare two cylinder sizes at three soil states.
:::''',figures=['F2-38'])
page(98,'''::: figure F2-39
caption: Figure 2-39. Load-Penetration Test Results in PS Soil Pressure Parameter vs. Relative Depth
axes: x Relative Depth, $D_f/D$; y Dimensionless Pressure Parameter $q/Dγ$
legend: $D_r ≈ 1.0$ 2" Cylinder; $D_r ≈ 1.0$ 4" Cylinder; $D_r ≈ 0.52$ 4" Cylinder; $D_r ≈ 0.44$ 2" Cylinder; $D_r ≈ 0.14$ 2" Cylinder; $D_r ≈ 0.12$ 4" Cylinder
description: Six curves compare cylinder penetration responses on a logarithmic pressure axis.
:::''',figures=['F2-39'])
page(99,'''Figures 2-40 through 2-43 show the results of LPT performed to investigate the effect of rate of penetration on the magnitude and shape of the LPT curve.

Figure 2-40 shows LPT performed in the 36" x 18" bin with a 4-inch cylinder in loose RS soil ($D_r ≈ 0.15$). Penetration rates vary from 1 inch per minute to 4 inches per minute, and an attempt was made to perform a "static" load test (i.e., load applied in increments and each increment added after no further penetration is produced by the previous increment) to provide a comparison of the magnitude and shape of a static load penetration curve with one produced by advancing the cylinder into the soil continously [sic] at some specified rate of penetration. Curve A represents the static load-penetration curve, and the remaining curves are those obtained for the rates of penetration noted on the figure. These curves indicate that the continous [sic] rate of penetration tests give quite good approximations of the static test, and that the LPT curves are relatively insensitive to rate of penetration up to the rate of 4 inches per minute which was the highest rate used.

Figures 2-41, 2-42, and 2-43, show similar results in RS soils of different relative density and using a different size of cylinder.

Figure 2-44 summarizes the results of a brief investigation into the effects of bin size (Boundary Effects) on the shape of LPT curve 5 [sic]. The tests shown were run in three different sizes of bin, as noted, in dense RS soil having an average relative density of about 0.96. Although the relative density of each soil bed is about the same, the dynamic penetrometer readings ($G_p$) have been given to indicate possible variation between them. These curves indicate that there is a tendency for the tests in the larger bins to have higher values of load at failure (i.e., the magnitude of the peak in the curve) and lower slopes in the approximate straight line portion after failure. As pointed out previously in the discussion of the bearing capacity equation, tests in the smallest bin tend to give higher apparent values of equivalent angles of internal friction than tests run in the same soil with the same test cylinder in a larger bin. If this tendency is valid it would explain at least in part, why the smaller cylinders tend to give higher values for the dense soils (e.g., Figures 2-36 through 2-39), since a bin of a given size would be larger, relative to the size of the cylinder, for the smaller cylinders than for the large cylinders.''')
page(100,'''::: figure F2-40
caption: Figure 2-40. Load-Penetration Curves for Four-Inch Cylinder in RS Loose at Different Rates of Penetration
axes: x Penetration - Inches; y Load - Lbs.
legend: A "Static" Test; B Penetration Rate = One Inch per Min.; C Penetration Rate = Two Inches per Min.; D Penetration Rate = Four Inches per Min.
description: Four labeled curves compare static loading and three penetration rates.
:::''',figures=['F2-40'],rotation=90)
page(101,'''::: figure F2-41
caption: Figure 2-41. Load-Penetration Curves for Four-Inch Cylinder in RS Intermediate at Different Rates of Penetration
axes: x Penetration (In.); y Load (Lbs.)
legend: A LPT No. 28 Penetration Rate = 0.5 In./Min.; B LPT No. 29 Penetration Rate = 2 In./Min.
description: Two labeled curves compare penetration rates in intermediate RS soil.
:::''',figures=['F2-41'],rotation=90)
page(102,'''::: figure F2-42
caption: Figure 2-42. Load-Penetration Curves for Four-Inch Cylinder in RS Dense at Different Rates of Penetration
axes: x Penetration (In.); y Load (Lb.)
legend: A LPT No. 22 (130), $γ$ = 51.2 pcf, rate = 4"/min.; B LPT No. 23 (99), $γ$ = 50.6 pcf, rate = 1"/min.; C LPT No. 24 (83), $γ$ = 51.5 pcf, rate = 1"/min.; D LPT No. 25 (130), $γ$ = 51.6 pcf, rate = 2"/min.
description: Four labeled curves compare penetration rates in dense RS soil.
:::

(130) - Gp values in parentheses''',figures=['F2-42'])
page(103,'''::: figure F2-43
caption: Figure 2-43. Load-Penetration Curves for Two-Inch Cylinder in RS Intermediate at Different Rates of Penetration
axes: x Penetration (In.); y Load (Lbs.)
legend: A LPT No. 26 Penetration Rate = 2 In./Min.; B LPT No. 27 Penetration Rate = 0.5 In./Min.
description: Two curves compare penetration rates for a two-inch cylinder.
:::''',figures=['F2-43'],rotation=90)
page(104,'''(117) Gp values in parentheses

::: figure F2-44
caption: Figure 2-44. Load-Penetration Curves for Four-Inch Cylinder in RS Dense Soil in Bins of Various Sizes
axes: x Penetration (In.); y Load (Lb.)
legend: A 18 Inch by 36 Inch Bin; B 36 Inch by 36 Inch Bin; C 54 Inch by 36 Inch Bin; A LPT No. 73 (117); C LPT No. 69 (103); C LPT No. 64A (112); B LPT No. 74 (103); A LPT No. 24 (83)
description: Five curves compare penetration responses in three bin sizes.
:::''',figures=['F2-44'])
page(105,'''The effect of footpad shape versus flat cylinder was studied and Figures 2-45 through 2-48 were prepared to show the results of LPT performed in four of the test soils (Nos. 1, 3, 4, and 9) using the 4-inch cylinder and 4-inch subscale footpad. It will be observed that the LPT curve for the footpad generally lies appreciably below the LPT curve for the cylinder. Part or all of this difference can be explained by the following:

a. At any given depth the average force on the bottom of the footpad will tend to be less than that on the bottom of the cylinder since the outer portion of the footpad is at a lesser depth and, hence, has a lower pressure exerted against it than the inner portion at the central lowermost part of the footpad.

b. With increasing penetration, the sides of the cylinder would tend to provide some resistance due to friction forces between the soil and the sides of the cylinder. Since there are no vertical sides on the footpad, there should be no side friction added. This effect would tend to make the LPT curve for the cylinder rise at a faster rate than that for the footpad.

c. Since there is open space above the footpad, when it is penetrating part of the soil would tend to fall in above the top of the footpad thus. [?] decreasing the amount of soil resisting soil failure and the force necessary to cause failure.

Figures 2-49 and 2-50 show plots of LPT results using 4-inch and 6-inch subscale footpads in the RS and SS soils (soils Nos. 1, 3, and 4; and soils Nos. 7, 8, and 9 respectively). Also shown are LPT results for a 4-inch cylinder in soils Nos. 1, 3, 4, and 9.

The analysis of the subscale drag test results has yielded an expression for the forces on a footpad as a function of mass, velocity and soil properties. One of the terms of this expression is called the "mechanical strength coefficient" of the soil, a term related to soil strength. Figure 2-51 shows a plot of the pressure parameter, $q/Dγ$, derived from LPT performed using a 4-inch cylinder, 4-inch footpad and 6-inch footpad, versus the mechanical strength coefficient, $C_{ms}$, derived from the analysis of the subscale drag tests.''')
page(106,'''::: figure F2-45
caption: Figure 2-45. Load-Penetration Curves in Soil No. 1 (RS Loose) ($D_r ≈ 0.0$)
axes: x Penetration - In.; y Load (lb.)
legend: Four-Inch Cylinder - LPT No. 95, Gp = 16.2; Four-Inch Footpad - LPT No. 79, Gp = 15.2
description: Two curves compare a four-inch cylinder and footpad in loose RS soil.
:::''',figures=['F2-45'],rotation=90)
page(107,'''::: figure F2-46
caption: Figure 2-46. Load-Penetration Curves in Soil No. 3 (RS Intermediate) ($D_r ≈ 0.29$)
axes: x Penetration (In.); y Load (Lb.)
legend: LPT No. 98 : Four-Inch Cylinder, Gp = 27.3; LPT No. 89 : Four-Inch Footpad, Gp = 22.4
description: Two curves compare a four-inch cylinder and footpad in intermediate RS soil.
:::''',figures=['F2-46'])
page(108,'''::: figure F2-47
caption: Figure 2-4[illegible]. Load-Penetration Curves in Soil No. 4 (RS Dense) ($D_r ≈ 0.69$)
axes: x Penetration (In.); y Load (Lb.)
legend: Four-Inch Cylinder - LPT No. 101, Gp = 63.9; Four-Inch Footpad - LPT No. 91, Gp = 62.8
description: Two curves compare a four-inch cylinder and footpad in dense RS soil.
:::''',figures=['F2-47'])
page(109,'''::: figure F2-48
caption: Figure 2-48. Load-Penetration Curves for Four-Inch Cylinder and Four-Inch Footpad in Soil No. 9 (SS Dense) ($D_r ≈ 0.76$)
axes: x Penetration (In.); y Load (Lbs.)
legend: Four-Inch Cylinder (LPT No. 87) Gp = 45; Four-Inch Footpad (LPT No. 85) Gp = 46
description: Two curves compare a four-inch cylinder and footpad in dense SS soil.
:::''',figures=['F2-48'],rotation=90)
page(110,'''::: figure F2-49
caption: Figure 2-49. Comparison of Footpad and Cylinder Load-Penetration Tests Pressure Parameter vs. Relative Depth in RS Soil
axes: x Relative Depth, $D_f/D$; y Dimensionless Pressure Parameter, $q/Dγ$
legend: $D_r ≈ 0.68$ 4" FP; $D_r ≈ 0.69$ 4" Cyl.; 6" FP $D_r ≈ 0.68$; $D_r ≈ 0.33$ 4" Cyl.; $D_r ≈ 0.25$ 4" FP; $D_r ≈ 0.25$ 6" FP; $D_r ≈ 0.0$ 4" Cyl.; $D_r ≈ 0.0$ 6" FP; $D_r ≈ 0.0$ 4" FP
description: Curves compare footpad and cylinder penetration responses at several RS soil states.
:::''',figures=['F2-49'])
page(111,'''::: figure F2-50
caption: Figure 2-50. Load-Penetration Test Results Using Footpad in SS Soil Pressure Parameter vs. Relative Depth
axes: x Relative Depth, $D_f/D$; y Dimensionless Pressure Parameter, $q/Dγ$
legend: Solid lines: $D_r ≈ 0.75$; Dashed lines: $D_r ≈ 0.63$; Dotted lines: $D_r ≈ 0.0$
description: Curves compare cylinder and footpad responses for three SS soil states.
:::

4" Cyl.

4" FP

6" FP

6" FP

4" FP''',figures=['F2-50'])
page(112,'''::: figure F2-51
caption: Figure 2-51. Mechanical Strength Coefficient from Subscale Drag Test Analysis, $C_{ms}$
axes: x $C_{ms}$; y Dimensionless Pressure Parameter, $q/Dγ$ at Dt/D = 0.2
legend: RS: ◌ Four-Inch Footpad; ○ Six-Inch Footpad; ⊕ Four-Inch Cylinder; SS: dashed triangle Four-Inch Footpad; △ Six-Inch Footpad
description: Five marker series and fitted lines relate pressure parameter to mechanical strength coefficient.
:::''',figures=['F2-51'])
page(113,'''Figure 2-52 shows a plot of the pressure parameter, $q/Dγ$, at a relative depth of 0.2 versus the peak magnitude of deceleration measured in the dynamic penetrometer test, $G_p$.

# 2.7 SOIL BED CONTROL TESTS

Five types of tests were used to measure and control the soil properties of the test beds used for the drag, impact and model drop tests;

Dynamic Penetrometer Test,

Static Penetrometer Test,

Grain Size Analysis,

Minimum-Maximum Density Test,

In-Place Density Measurement.

In addition, a limited number of load-penetration tests (LPT) were performed in some of the test soils using different sizes of cylinder and subscale footpads as penetrating devices. The performance and results of these tests have already been described in Section 2.6.

## 2.7.1 Dynamic Penetrometer Test

The Dynamic Penetrometer Test (DPT) is used primarily as an index of the relative density and uniformity of a soil bed. It has been found that the peak deceleration experienced by a body of fixed mass falling freely from a fixed height can be correlated with the relative density of a given soil type. The correlation studies were run in soil beds whose relative density was determined by direct weight-volume measurements. Correlation curves were plotted of the peak magnitude of deceleration observed versus the measured relative density. These correlation curves were then used to determine the relative density of the soil beds by means of the DPT in these soil beds where the relative density could not be measured directly.''',sections=['2.7','2.7.1'])
page(114,'''::: figure F2-52
caption: Figure 2-52. Pressure Parameter at a Relative Depth of 0.2 vs. Dynamic Penetrometer Test Results
axes: x Peak Magnitude of Deceleration in Dynamic Penetrometer Test, $G_p$ (g.); y Dimensionless Pressure Parameter, $q/Dγ$ (at $D_f/D = 0.2$)
legend: RS Soil 4" Cyl.; 4" Footpad; 6" Footpad; SS Soil 4" Footpad; 6" Footpad
description: Five lines relate pressure parameter to dynamic penetrometer deceleration.
:::''',figures=['F2-52'])
page(116,'''2 3/4" D.

2 1/4" D.

1/2"

1 3/4"

4 1/8"

Consolidated Engineering Corp. D. C. Accel. Type 4-202-0001

7075 Aluminum Body

1 3/8" R

::: figure F2-53
caption: Figure 2-53. Dynamic Penetrometer (DPT) and Schematic
axes:
legend:
description: A photograph and dimensioned sectional drawing show the dynamic penetrometer and its accelerometer.
:::''',figures=['F2-53'])
