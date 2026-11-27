from pathlib import Path
import json
O=Path('out')
def page(n,label,body,sections=[],figures=[],equations=[],rotation=0):
 h='---\nsource: bendix-1968-vol1\npdf_page: '+str(n)+'\nprinted_page: '+json.dumps(label)+'\nsections: '+json.dumps(sections)+'\nfigures: '+json.dumps(figures)+'\ntables: []\nequations: '+json.dumps(equations)+'\nrotation: '+str(rotation)+'\nimage: corpus/1968/images/p'+str(n).zfill(4)+'.png\ntranscriber: codex\nreview_status: single-reading\n---\n'
 (O/f'p{n:04}.md').write_text(h+body.strip()+'\n',encoding='utf-8')
page(71,'2-46','''::: figure F2-23
caption: Figure 2-23. Angle of Internal Friction (as Determined by the Direct Shear Test) Versus Relative Density
axes: x Relative Density, $D_r$; y Angle of Internal Friction φ, (Degrees)
legend: RC2; PS; RS; RSM-b; RSM-a; SS
description: Six curves show angle of internal friction versus relative density.
:::''',figures=['F2-23'])
page(73,'2-48','''1/8 Inch

::: figure F2-24
caption: Figure 2-24. Photomicrograph of RS Soil; Note Pronounced Angularity and Vesicularity
axes: none
legend: none
description: A photomicrograph shows angular and vesicular soil particles with a scale bar.
:::''',figures=['F2-24'])
page(74,'2-49','''It has been suggested that the interlocking of soil particles can also contribute an "apparent cohesion." This might be a possible explanation of the apparent cohesion value exhibited on the failure envelope graphs for the cinder soils in Appendix C.

Another possible explanation for the apparent cohesion value exhibited by these soils postulates that shear failure occurs by the rolling and sliding of soil grains on the failure plane at low stress levels and by crushing of soil particles at higher stress levels. If such behavior did take place failure envelopes such as those shown in Figure 2-25 would tend to be produced. In this figure, $σ_{ncr}$ represents the normal stress at which some of the soil particles will crush before achieving the rolling and sliding phase, thus limiting the maximum shear stress that can be achieved. If most of the data points are in the range of normal stress above $σ_{ncr}$, the "best" straight line through the data points will be that having the slope φ' and interpolated back to the σ axis (as shown by the dashed lines) will exhibit an apparent cohesion as shown. The limiting effect of the breaking strength of the particles might also tend to make the value of φ' for both loose and dense soils similar, thus explaining the relatively small range of values of angle of internal friction reported for the PS soil. The distribution of the data points on the failure envelopes for the cinder soils tends to exhibit such an effect, but the scatter of these points does not permit a definite conclusion.

Bendix performed a limited number of triaxial tests on the cinder soils using the apparatus shown in Figure 2-26. In the triaxial test a cylindrical prism of soil is subjected to a constant hydrostatic confining stress while a steadily increasing axial stress is applied until the sample fails in shear. Mohr's circle analysis of the tests, run at various confining pressures, yields a failure envelope similar to that described for the direct shear tests. Triaxial tests were performed on the RS soil in intermediate and dense states. The apparent cohesion obtained was on the same order of magnitude as that obtained in the direct shear tests and the value for angle of internal friction was about 38° in both cases. When the data was re-examined for the effects illustrated in Figure 2-25 (crushing of grains and a lower value of φ at higher confining pressures) it was found that this interpretation of the tests did yield values of φ of 39° and 43° for the RS intermediate and RS dense soils, respectively, at low confining pressures, and values of 36° for both soils at high confining pressures.''')
page(75,'2-50','''$φ_L$ = Angle of Internal Friction for loose soil

$φ_D$ = Angle of Internal Friction for dense soil

φ' = Angle of Internal Friction due to crushing of particles ($σ_n > σ_{ncr}$)

$σ_{ncr}$ = Critical Normal Stress (Normal stress above which particles tend to break rather than roll and slide)

$(C_a)_D$ = Apparent cohesion for dense soil

$(C_a)_L$ = Apparent cohesion for loose soil

φ'

φ'

$(C_a)_D$

$(C_a)_L$

$φ_D$

$φ_L$

$σ_{ncr}$

::: figure F2-25
caption: Figure 2-25. Hypothetical Failure Envelopes for Shear Failure Due to Breaking of Soil Particles
axes: x Normal Stress, $σ_n$; y Shear Stress τ
legend: Dense Soil; Loose Soil
description: Two schematic failure envelopes have angle guides and dashed extrapolations to apparent cohesion intercepts.
:::''',figures=['F2-25'],rotation=90)
page(76,'2-51','''::: figure F2-26
caption: Figure 2-26. Triaxial Shear Test Machine
axes: none
legend: A; B [?]
description: A photograph shows an operator at the triaxial shear test machine with lettered components.
:::''',figures=['F2-26'],rotation=90)
page(77,'2-52','''The scope of the present program did not allow for a detailed investigation of the various aspects of the direct shear test results. In view of the lack of correlation between the apparent cohesion intercept data for the cinder soils and the resulting static and dynamic strength levels, the apparent cohesion was not used as a soil descriptor.

The fact that the direct shear test data for the LSM soil does not indicate any significant change in φ with $D_r$ can be explained, in part, by density changes occurring in the soil during the progress of the test. Examination of the normal displacement readings ("Dilation") for the loose LSM soil indicates that the soil densified upon the application of the normal load prior to the actual shearing operation. For the higher normal loads, the densification produced is about equal to the density of the dense LSM soil. The φ relationship shown for the LSM soil in Figure 2-23 is based on a failure envelope constructed using the lowest values of normal load used in the direct shear test on the loose LSM soil.

## 2.5.3 Sonic Velocity Test

The sonic velocity tests used to determine the modulus of elasticity or initial tangent modulus of the test soils were conducted by IITRI. Their report of the tests is given in Appendix B.

# 2.6 BEARING STRENGTH TEST

Tests to determine the bearing strength or bearing capacity of the test soils were performed in the load-penetration test (LPT) apparatus shown in Figures 2-27 and 2-28. A test cylinder or subscale footpad is advanced into the soil under hydraulic pressure at a specific rate of penetration and a record made on an x-y plotter of the load-penetration history of the test. An example of such a plot is shown in Figure 2-29.

In addition to using the LPT as a direct measurement of bearing strength of the soil, the LPT data was compared to the value of bearing strength obtained by using Terzaghi's bearing capacity equation (38, pp. 124-134) in conjunction with the values of angle of internal friction obtained from the direct shear tests performed on the test soils. Finally various methods of soil placement were investigated for use in the development of soil placement procedures for the drag, impact, and drop tests.''',sections=['2.5.3','2.6'])
page(78,'2-53','''::: figure F2-27
caption: Figure 2-27. Penetrometer Test Fixture (LPT)
axes: none
legend: A; B; C; D; E; F; G
description: A photograph shows the penetrometer fixture with lettered components.
:::''',figures=['F2-27'])
page(79,'2-54','''::: figure F2-28
caption: Figure 2-28. Load-Penetration Test (LPT) Setup
axes: none
legend: H; I; J; K; L; M
description: A photograph shows the load-penetration apparatus and recording equipment with lettered components.
:::''',figures=['F2-28'],rotation=90)
page(80,'2-55','''::: figure F2-29
caption: Figure 2-29. Load-Penetration Test (RS Dense)
axes: x Penetration (in.); y Load (Lbs.)
legend: LPT #27; 2" Diameter Cylinder; D.P.T. Record No. 54074; Pen Rate 1/2" Per Min.; Plate Compactor
description: A single load-penetration trace is plotted on a rectangular grid.
:::''',figures=['F2-29'],rotation=90)
page(82,'2-57','''Figure 2-30 shows an adaptation of the LPT apparatus made to fit the subscale impact test bin so that the effect of container size might be investigated and that LPT might be run in the bin used in the subscale impact tests in soil prepared in the same manner as for for [sic] the impact tests. This test setup was also used to perform LPT using the 4-inch and 6.17-inch diameter subscale footpads used in the impact tests. The equipment and procedures used for these tests are essentially the same as those used for the other test setup. The labeled parts are described below.

1. Test Load Cell - Instrumented load cell used to record force on x-y plotter.

2. Hydraulic Cylinder - Used to force test cylinder into soil.

3. Test Cylinder - The test cylinder shown is 2" in diameter with the 6.17" diameter subscale footpad attached.

4. Support Hinges - Hinges supporting hydraulic cylinder which take bending and transverse-loads during loading of test cylinder.

## 2.6.2 Test Procedure

Soil Bed Preparation: The soil box is marked off in volume increments of 4, 6, 8, 10, 12, and 13.78 cubic feet (full box). As the soil placed in the box reaches each level, a weight determination is made. The unit weight of the soil was computed for each increment to check on the uniformity of the soil bed (i.e., the variation of unit weight from layer to layer) and for the full box to provide the value of average unit weight of the soil bed. The relative density of the soil beds is determined utilizing the relationships found for the various test soils by the minimum-maximum density test (2.5.2.2 of this section). A description of the various methods of soil placement investigated and used in the load-penetration test is given in Appendix C.

Test Operation: At the completion of test bed preparation and measurement, a test cylinder is affixed to the bottom of the hydraulic cylinder and pressure admitted to the top of the hydraulic cylinder. Load versus penetration is recorded on one x-y plotter and the rate of penetration regulated by a plot of penetration versus time on the second [cont. next page]''',sections=['2.6.2'])
page(83,'2-58','''::: figure F2-30
caption: Figure 2-30. Load-Penetration Test (LPT) Setup
axes: none
legend: 1; 2; 3; 4
description: A photograph shows the load-penetration apparatus with four numbered components.
:::''',figures=['F2-30'])
page(84,'2-59','''[cont.] x-y plotter. The pressure to the cylinder is controlled so that the plotting pen follows a predetermined line on the penetration versus time graph corresponding to the desired rate of penetration. The cylinder is forced into the soil a distance of 8 inches or until the capacity of the hydraulic power supply has been reached.

## 2.6.3 Load-Penetration Test Results

Bearing strength or bearing capacity represents the summation of shear strength on a failure plane whose shape and size is a function of the size of the footing or test cylinder, its depth below the soil surface and the relative density of the soil. Thus, one aspect of the determination of the bearing capacity of the test soils was to investigate the effect of size of cylinder or footing on the bearing capacity of a given soil at a given depth. The standard method for determining bearing capacity generally involves the progressive application of load increments, each increment being added only after the settlement occasioned by the previous load increment had ceased (e.g., ASTM Designation D1194-57) (31, pp. 517=520 [sic]). Since the performance of the LPT involves advancing the test cylinder into the soil continuously and at some specified rate of penetration, tests were run to determine the relationship between the LPT and the standard type of bearing test and to determine the effect of changing the rate of penetration of the cylinder on the load-penetration curve.

A bearing capacity failure (i.e., application of that unit force on the soil which exceeds the bearing strength of the soil) is generally envisioned as causing the soil to undergo a transition from a state of elastic equilibrium to plastic equilibrium. This generally results in displacements, laterally and upward, of wedges of soil below and beside the footing (38, p. 119-121). Terzaghi reports that small-scale model tests indicate that the greatest heave of the ground surface around a loaded circular area with a radius R occurs within 3R of the center of the loaded area, and that, beyond 5R from the center, the heave is imperceptible (38, p. 134). Since the closest boundary of the LPT bin for the 4-inch diameter cylinder is 9 inches (i.e., 4.5R) from the center of the cylinder, this size of bin would appear to satisfy the condition that the bin be large enough to eliminate significant boundary effects. However, it was noticed during an LPT in dense SS soil that a failure plane did intersect the glass face of the LPT bin and that this resulted in a noticeable upward displacement of a large portion of the soil. This observation [cont. next page]''',sections=['2.6.3'])
page(85,'2-60',r'''[cont.] suggested that there could be a significant boundary effect for such soils in this size of bin and hence tests were made in larger bins to check this possibility.

Some tests were run with subscale footpads to investigate the effect of the footpad shape on the LPT curve. Both 4-inch diameter and 6-inch diameter footpads were used so that the size effect might also be investigated for each footpad shape.

Finally, an attempt was made to relate a bearing capacity factor determined from the LPT to soil strength coefficients developed in the analysis of the drag and impact tests.

The most common method of analysis employs the bearing capacity equation formulated by Karl Terzaghi (38, p. 118-134) given below:

$$q = D_f γ N_q + 0.3Dγ N_γ + 1.3c N_c$$ (3-1)

where:

q = bearing capacity of footing (FL⁻² units)

γ = unit weight of soil (FL⁻³ units)

$D_f$ = surcharge depth; depth of soil above bottom of footing (L units)

D = diameter of circular footing (L units)

C = cohesive strength (FL⁻² units)

$N_q$, $N_γ$, $N_c$ = bearing capacity factors dependent solely on the angle of internal friction, φ, of the soil (dimensionless)

For loose or very compressible soils, the bearing capacity factors given as applicable by Terzaghi are $N_q'$, $N_γ'$, and $N_c$*.

Footnotes:

*Terzaghi distinguishes between general shear, the massive lateral displacement of soil during a bearing capacity failure, and local shear, a failure condition whereby lateral compression of the soil is of such magnitude that the failure surface cannot extend to the soil surface laterally and, hence no heave is observed. The bearing capacity factors for local shear were computed using the relationship: tanφ' = 2/3 tanφ where φ is the angle of internal friction for a loose soil. For soils of intermediate relative density, interpolation between the general shear and local shear values may be used.''',equations=['3-1'])
page(86,'2-61','''Figure 2-31 gives the values of the bearing capacity factors versus angle of internal friction. The values of $N_q$, $N_q'$ and $N_c$ shown were computed using the equations given by Terzaghi (38, p. 127). The values of $N_γ$ and $N_γ'$ shown were interpolated using the values given in the Navdocks Design Manual, DM-7 (39, p. 7-11-2).

Since the soils used in this study are essentially cohesionless soils, the cohesion term in Equation 3-1 was eliminated. Solving the remaining part of this equation for load or force on the footing at failure we obtain:

$$Q = Aγ N_q D_f + 0.3ADγ N_γ$$ (3-2)

where: γ, $N_q$, $D_f$, D, $N_γ$ are defined as for Equation 3-1.

Q = load on footing at failure (F units)

A = area of bottom of footing (L² units)

On a graph of load versus penetration (Q versus $D_f$), Equation 3-2 would plot as a straight line with a Q intercept of $0.3ADγ N_γ$ and a slope of $Aγ N_q$.

Figures 2-32 through 2-34 summarize the comparison of the bearing capacity equation to the LPT results. Since the bearing capacity equation predicts only a point of failure rather than the continuous penetration of a footing, LPT were performed starting at the surface and one or two positions below the surface. A straight line was passed through the various points of failure observed and the slope and load intercept value used to evaluate φ in the corresponding terms of the bearing capacity equation. The values of φ obtained in this manner were then compared to the values of φ obtained in the direct shear tests (see Figure 2-23).

Figure 2-32 showed the results of this for LPT in soil No. 1 (RS loose) using the 2-inch diameter cylinder. The comparison between the values of φ obtained using the bearing capacity equation (φ = 40° for the slope requirement and φ = 39.5° for the load intercept value) compare quite well with the value of φ = 38.5° in the direct shear tests.''',equations=['3-2'])
page(87,'2-62','''::: figure F2-31
caption: Figure 2-31. Bearing Capacity Factors
axes: x φ (Degrees); y $N_c$, $N_q$, $N_q'$, $N_γ$, $N_γ'$, $N_c'$
legend: $N_γ$, $N_q$, $N_c$ (General Shear); $N_γ'$, $N_q'$, $N_c'$ (Load [sic] Shear); $N_γ$; $N_q$; $N_c$; $N_γ'$; $N_q'$; $N_c'$
description: Six bearing-capacity curves are plotted against friction angle on a logarithmic vertical scale.
:::''',figures=['F2-31'])
page(88,'2-63',r'''Slope = 6.5 lbs./in. = $AγN_q$

$$N_q = \frac{6.5(1730)}{3.14\ (45)} = 79$$

⇒φ = 40°

φ(Direct Shear Tests) = 38.5°

Intercept = 4.7 lbs. = $0.3 ADγN_γ$

$$N_γ = \frac{4.7(1730)}{0.3(3.14)\ 2(45)} = 96$$

⇒φ = 39.5°

::: figure F2-32
caption: Figure 2-32. Load-Penetration Curves for Two-Inch Diameter Cylinder in Soil No. 1 (RS Loose) ($D_r ≈ 0.0$)
axes: x Penetration (In.); y Load (Lb.)
legend: LPT No. 93, $G_p$ = 16.2; LPT No. 53, $G_p$ = 15.6; LPT No. 52, $G_p$ = 15.4
description: Three load-penetration traces and a slope construction are shown with printed calculations.
:::''',figures=['F2-32'],rotation=90)
page(89,'2-64',r'''Four-Inch Dia. Cyl.

Test Run in 36" by 36" Bin

Slope = $AγN_g$ [sic] = 316 lbs./in.

$$∴ N_q = \frac{316}{Aγ} = \frac{316\ (1730)}{12.6\ (54.5)} = 796$$

∴φ ≅ 53°

φ (Direct Shear Test) = 49.5°

Intercept = 720 lbs. = $0.3 ADγN_γ$

$$N_γ = \frac{720\ (1730)}{0.3(12.6)\ 4(54.5)} = 1512$$

⇒φ = 55°

::: figure F2-33
caption: Figure 2-33. Load-Penetration Curves in RS Dense ($D_r ≈ 0.94$)
axes: x Penetration (In.); y Load (Lb.)
legend: A Started at Soil Surface; B Started Two Inches Below Soil Surface; A LPT No. 74, $G_p$ = 103; B LPT No. 75, $G_p$ = 105; Bearing Capacity Equation, φ = 49.5°
description: Two test traces, a fitted slope line, and a bearing-capacity line are plotted with printed calculations.
:::''',figures=['F2-33'],rotation=90)
page(90,'2-65',r'''Test Bin 108 Inches by 36 Inches

Slope = $AγN_q$ = 54 lbs./in.

$$∴ N_q = \frac{54}{Aγ} = \frac{54(1730)}{12.6(108)} ≅ 69$$

∴ φ ≅ 39°

φ (Direct Shear Test) = 39.5°

Intercept = 140 lbs. = $0.3 ADγN_γ$

$$N_γ = \frac{140(1730)}{0.3(12.6)\ 4(108)} = 148$$

⇒φ = 42°

::: figure F2-34
caption: Figure 2-34. Load-Penetration Curves for Four-Inch Cylinder in Soil No. 9 ($D_r ≈ 0.76$)
axes: x Penetration (In.); y Load - Lbs. x 100
legend: A LPT Started at Soil Surface; B LPT Started Two Inches Below Soil Surface; A LPT No. 87; B LPT No. 88
description: Two load-penetration traces and a slope line are shown with printed calculations.
:::''',figures=['F2-34'],rotation=90)
page(91,'2-66','''Note also that the line joining the failure points of the three LPT more or less follows the straight line portion of the LPT curves*.

Figure 2-33 shows the results of a similar analysis on LPT run in dense RS soil (note that this soil is much more dense than soil No. 4 which is also designated as RS dense) using a 4-inch diameter cylinder. Although it might not appear that the values of φ obtained by use of the bearing capacity equation are not appreciably higher than that obtained by the direct shear test (i.e., 49.5°), it can be seen that the difference is appreciable when the straight line obtained from the LPT data is compared to the line representing the solution of the bearing capacity equation for φ = 49.5°**.

Note that the line joining the failure points has a slope similar to that of the LPT curve after the initial failure point.

Figure 2-34 shows the results of analysis of the LPT curves obtained using a 4-inch cylinder in soil No. 9 (SS dense). Here, the results yielded by the bearing capacity equation compare-quite [sic] favorably with the results obtained by the direct shear test.

Figure 2-35 shows the results of the previously described analysis on LPT curves obtained using a 4-inch cylinder in dense RS soil in a smaller bin than that used for the tests of Figure 2-33. It can be seen that the value of φ obtained from the slope term in the bearing capacity equation is higher than that obtained in the larger bin. Note that [cont. next page]

Footnotes:

*Note that, even though soil No. 1 is very loose and would appear to require the use of the bearing capacity factors relating to local shear failure, the values of φ obtained using these local shear values are unrealistically high (i.e., φ = 51° for the slope requirement, and φ = 51° for the intercept value).

**It should be pointed out, however, that one series of direct shear tests on dense RS soil ($D_r ≈ 1.0$) yielded a value of φ = 52.6°. The value of φ = 49.5° used above represents the average of several direct shear tests on dense RS soil. It has also been previously pointed out that the direct shear tests may provide low values of φ for the cinder soils (i.e., the RS, PS, RC2, and RSM soils) if crushing of particles occurs at higher normal stresses which are appreciably higher than those actually present on a failure plane during a bearing capacity failure.''')
page(92,'2-67',r'''Slope = $AγN_q$ = 400 lbs./in.

$$∴ N_q = \frac{400\ (1730)}{12.6\ (54.5)} = 1008$$

⇒φ = 54.5°

φ (Direct Shear Test) = 49.5°

Intercept = 700 lbs. = $0.3 ADγN_γ$

$$N_γ = \frac{700\ (1730)}{0.3\ (12.6)\ 4\ (54.5)} = 1470$$

⇒φ = 55°

::: figure F2-35
caption: Figure 2-35. Load-Penetration Curves for Four-Inch Cylinder in RS Dense ($D_r ≈ 0.97$); Bin Size: 18 Inches by 36 Inches
axes: x Penetration (In.); y Load (Lb.)
legend: A Started at Soil Surface; B Started Two Inches Below Soil Surface; A LPT No. 73, $G_p$ = 117; B LPT No. 76, $G_p$ = 103
description: Two load-penetration traces and a slope line are plotted with printed calculations.
:::''',figures=['F2-35'])
page(93,'2-68',r'''[cont.] although the value of φ is only increased by 1.5° in the smaller bin, the corresponding value of $N_q$ obtained is about 50% larger than that obtained in the larger bin.

The scope of this program did not permit an intensive investigation of the bearing capacity equation. However, the results described above indicate that the bearing capacity equation and direct shear test values of φ do compare approximately to the LPT results. Where the discrepancy is fairly large, such as in the results obtained for the LPT in dense RS soil, it is uncertain whether this discrepancy is due to the lack of applicability of the bearing capacity equation or error in the determination of φ in the direct shear tests. As has been pointed out previously, even small differences in the value of φ can have a pronounced effect on the values yielded by the bearing capacity equation, especially for values of φ greater than 50°.

It is believed that the poor success of the bearing capacity equation using the bearing capacity factors for local shear to provide realistic values of φ (e.g., the analysis for local shear of the LPT in Figure 2-32) is due to the fact that in loose soils excessive settlement takes place before failure is reached. Thus, the bearing capacity factors for local shear are probably intended to yield allowable bearing values to limit excessive settlements prior to bearing capacity failure.

If the bearing capacity equation (Equation 3-1) is divided through by the quantity Dγ and the cohesion term dropped, the result is:

$$\frac{q}{Dγ} = N_q\ \frac{D_f}{D} + 0.3\ N_γ$$ (3-3)

where the symbols used are as previously described for Equation 3-1. This form of the bearing capacity equation indicates that for any size of footing or test cylinder in a given soil a plot of the dimensionless pressure parameter, q/Dγ versus relative depth $D_f/D$, will fall on the same line regardless of the size of the footing.''',equations=['3-3'])
