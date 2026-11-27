from pathlib import Path
import json

def page(n, body, sections=(), figures=(), tables=(), equations=(), rotation=0):
    header = f'''---
source: bendix-1968-vol1
pdf_page: {n}
printed_page: "2-{n-25}"
sections: {json.dumps(sections)}
figures: {json.dumps(figures)}
tables: {json.dumps(tables)}
equations: {json.dumps(equations)}
rotation: {rotation}
image: corpus/1968/images/p{n:04}.png
transcriber: codex
review_status: single-reading
---
'''
    Path(f'out/p{n:04}.md').write_text(header + body.strip() + '\n', encoding='utf-8')

page(26, '''
# SECTION II

# SOIL SELECTION AND CONTROL

# 2.1 INTRODUCTION

This section of the report discusses the selection of the test soils for the LM soil mechanics study, the test procedures used to measure the properties of the soils, and the methods used to prepare the soils in the test beds to obtain repeatable soil properties for multiple test bed preparations. The development of methods of monitoring the soil properties of the test beds throughout the program are also discussed.

Two preliminary questions must be answered before making any attempts at soil selection. The first of these is, "What are the soil properties which contribute to the soil dynamic strength?" This question is important since the essential aim of the study is to define the footpad reaction in terms of these properties. The second question is, "What are the estimated values of these properties for the lunar soil?"

The first two parts of this section of the report discuss the effort carried out to answer these two questions.

A summary of the main results of the "Soil Selection and Control" phase of the program is given at the end of this section.

## 2.1.1 Abbreviations of Units and Names in Soil Testing

BC - Black crusher run volcanic scoria.

C.E.C. - Consolidated Electrodynamics Corporation (refers to manufacturer of strain-gauge type accelerometer used in Dynamic Penetrometer).
''', ['2.1','2.1.1'])

page(27, '''
Dense (i.e. describing a soil in a dense state of compaction; a soil for which $0.7 ≤ D_r ≤ 1.0$).

DD - Density Determination (refers to a determination of soil unit weight or density made in a weighed test bin of known volume and weight).

DPT - Dynamic Penetrometer Test.

DST - Density Scoop Test (refers to in [sic] In-Place Density Test done with a density scoop apparatus designed by E.T. Selig).

fps - feet per second.

fps² - feet per second per second.

FSIT, FSIMP Test - Full Scale Oblique Impact Test.

g., G. - gravitational constant (earth =-32.2 fps²; moon = 5.3 fps²).

G.S.A. - Grain Size Analysis.

INTER - Intermediate; describing a soil in an intermediate state of compaction; a soil for which $0.3 ≤ D_r ≤ 0.7$.

ksi, KSI --Kips per square inch.

ksf, KSF - Kips per square foot.

LOOSE - Loose; describing a soil in a loose state of compaction; a soil for which $0.0 ≤ D_r ≤ 0.3$.

LM SMS - Lunar Excursion Module Soil Mechanics Study.

LPT - Load-Penetration Test; a test for determination of bearing strength of a soil.

LSM - A basic test soil type used in the LM SMS; a mixture of crushed volcanic scoria (RC2) and air-floated clay designed to simulate certain features of the lunar soil as indicated by the Surveyor I photographs.

mm - millimeter(s).

MMDT - Minimum-Maximum Density Test; test used to establish relative density of granular soil.

ms, msec - millisecond(s); 1 ms = 0.001 sec.
''')

page(28, '''
pcf, PCF - pounds per cubic foot.

PFT - Passive Failure Test; a model retaining wall test used to determine angle of internal friction of a soil.

PS - White narrowly graded crushed pumice; a basic test soil type used in the LM SMS.

psi, PSI - pounds per square inch.

psf, PSF - pounds per square foot.

RC - Red broadly-graded "crusher run" andesitic volcanic scoria; one of the basic soil types investigated for use in the LM SMS. It was later replaced with the RC2 since it was not available in the amounts needed for the program.

RC2 - Red broadly-graded "crusher run" andesitic volcanic scoria; one of the basic soil types used in the LM SMS. It was obtained from the same source as the RS material.

RS - Red narrowly-graded crushed volcanic scoria; one of the basic soil types used in the LM SMS.

RSM-a - A narrowly-graded mixture of five parts of RS material and seven parts of crushed marble by weight; one of the basic soil types used in the LM SMS.

RSM-b - A narrowly-graded mixture of one part of RS material and three parts of crushed marble by weight; one of the basic soil types used in the LM SMS.

SSDT, SSDRAG Test - Subscale Drag Test; one of the tests made with a scaled-down LEM footpad used in the development of the soil-footpad force laws in the LM SMS.

SSIT, SSIMP Test - Subscale Oblique-Impact Test; one of the tests made with a scaled-down LEM footpad used in the development of the soil-footpad force laws in the LM SMS.

tsf, TSF - Tons per square foot.

VPT - Visual Penetration Test; a type of Load-Penetration Test utilizing a half-cylinder against a glass plate for the purpose of viewing soil movement or failure during penetration.
''')

page(29, '''
# 2.2 SOIL PROPERTIES AFFECTING DYNAMIC STRENGTH OF DRY SOILS

As previously stated in the Introduction, the central purpose of this program is to find an interrelationship between soil descriptors and the resulting forces acting on the LM footpads for a prescribed motion of the footpads. Before attempting this, however, considerable care is required to establish a realistic set of descriptors. The form the force laws will take, their range of applicability, and their accuracy all depend on the initial set of descriptors. The selection of descriptors must be given particular attention in this program in that none of the various test soils used to establish empirical constants for the force laws is likely to be identical to the actual lunar surface. Interpolations and extrapolations will eventually be necessary, and this is only possible when the variable actually causing the change in resistance functions from soil to soil has been pinpointed.

There are two extremes possible in the initial selection of descriptors. An overly conservative approach, in which too many descriptors are investigated, will result in a wasteful expenditure of time and resources. On the other hand, the exclusion of significant descriptors will result in either complete confusion or in ascribing variation in forces to incidental variation in soil properties; that is, an erroneous force law.

At the outset a reasonable compromise between too few and too many descriptors is to include those that are known to affect the response with a subsequent sensitivity analysis, possibly reducing the initial selection.

A rational guide to the initial selection of experimental variables is the examination of variables necessary for a formal analysis. Common to all solid mechanics problems, the following requirements must be considered:

1. Boundary conditions.

2. Field equations.

3. Equation of state.
''', ['2.2'])

page(30, '''
Each of these factors will now be considered, as summarized in Figure 2-1, in relation to the particular problem of the prediction of the LM landing performance of the lunar surface.

## 2.2.1 Boundary Conditions

In a broad sense, boundary conditions may be considered synonymous with environmental conditions. In particular, the lunar environment can be characterized as a vacuum, having extreme temperature variations with a reduced gravitational constant, compared to that of the earth.

These conditions immediately comment on the exclusion of certain soil parameters which would ordinarily be of importance in the earth environment. All moisture factors, such as moisture content, degree of saturation, permeability, pore fluid pressure, etc., are nonexistent and can thus be eliminated from consideration.

## 2.2.2 Field Equations

The description of the behavior of a material mass subjected to dynamic forces involves the satisfaction of the equations of motion, as stated in Figure 2-2, and a continuity or compatibility requirement. This requirement can be stated in a number of ways, but it basically involves kinematic requirements and functions of the material density.

It can be seen that the bulk density ($γ$) of the material must be known from an analytical point of view and thus must be included in an empirical study.

## 2.2.3 Equation of State

To transform the stresses in the equations of motion into displacements, an equation of state relating stresses to strain and/or strain rates for the material under consideration must be stated. This element of the analysis is precisely the reason this problem is so complex.

For a dry particulate material, schematically shown in Figure 2-3; the strain mechanism involves the deformation of the individual grains and the rolling, sliding, interlocking action of one grain relative to another.
''', ['2.2.1','2.2.2','2.2.3'])

page(31, r'''
ENVIRONMENT (boundary conditions)

FIELD EQUATIONS (eqs. of motion-continuity)

EQUATION OF STATE (stress - strain law)

::: figure F2-1
caption: Figure 2-1. Factors Considered in Two Forms (Analysis)
axes: none
legend: none
description: A lunar module above the ground illustrates environment, field equations and equation of state.
:::

$$\frac{∂σ_x}{∂x} + \frac{∂τ_{yx}}{∂y} + \frac{∂τ_{zx}}{∂z} = \frac{γ}{g}\frac{∂^2u}{∂t^2}$$

$$\frac{∂τ_{xy}}{∂x} + \frac{∂σ_y}{∂y} + \frac{∂τ_{zy}}{∂z} = \frac{γ}{g}\frac{∂^2v}{∂t^2}$$

$$\frac{∂τ_{xz}}{∂x} + \frac{∂τ_{yz}}{∂y} + \frac{∂σ_z}{∂z} + γ = \frac{γ}{g}\frac{∂^2w}{∂t^2}$$

::: figure F2-2
caption: Figure 2-2. General Force-Equilibrium Relationships for Dynamic Loading
axes: none
legend: none
description: Three equations give the components of force equilibrium for dynamic loading.
:::
''', figures=['F2-1','F2-2'])

page(32, '''
If the discipline of soil mechanics could provide a functional relationship describing a typical stress-strain curve as shown in Figure 2-4, in terms of the aforementioned strain mechanism, the issue would be greatly simplified. Unable to do this, it is only possible to state qualitatively which soil properties control the stress-strain behavior [?] of the material under study. This qualitative relationship is summarized in Figure 2-5.

For conventional cohesionless earth soils the magnitude of the deformation of individual grains is usually small compared to the relative motion between grains. The magnitude of this deformation may not be negligible for highly vesicular volcanic lunar simulants. Figure 2-6 shows a magnified view of individual grains of a volcanic scoria used as one of the test soils in this study. It can be seen that the grain structure differs drastically from that of more typical terrestrial soils.

A measure of the stress-strain behavior or [sic] individual grains is provided by the slope (elastic or Young modulus) of the approximately linear portion of the overall stress-strain curve at very small (recoverable) strain values. Relative grain motion is essentially nonrecoverable (16)*; thus the above criterion is a fairly reliable estimate of individual grain elasticity. This tends to be substantiated by BARKAN (10) in view of the insensitivity of E, the elastic modulus, to certain variables, such as porosity, which are known to influence relative grain motion in conventional sands.

The factors which influence the relative movement between individual grains as a function of stress level have not received much attention, with one outstanding exception, namely, the ultimate stress level. Obviously, this particular point of the stress-strain curve has been studied intensively by the foundation engineer because of his interest in stability calculations. Basically, the argument concerning relative grain motion at all stress levels will rest on conclusions made at the peak or maximum point of the stress-strain curve.

Footnotes:

* Numbers in parentheses indicate References.
''')

page(33, '''
::: figure F2-3
caption: Figure 2-3. Schematic of Dry Particulate Soil
axes: none
legend: none
description: Irregular grains are packed into an open container with voids between them.
:::

::: figure F2-4
caption: Figure 2-4. Idealized Stress-Strain Curve
axes: x $E_{ij}$; y $σ_{ij}$
legend: none
description: An uncalibrated stress-strain curve has dashed guides at its initial slope and maximum.
:::
''', figures=['F2-3','F2-4'])

page(34, '''
TOTAL DEFORMATION $σ (ε)$ = INDIVIDUAL GRAIN DEFORMATIONS (Recoverable) + RELATIVE GRAIN MOTIONS (Sliding, rolling, interlocking)

E

GRAIN TO GRAIN FRICTION COEFF.

GRAIN SIZE $μ$

SIZE DISTRIBUTION S

GRAIN SHAPE

SPACING $D_R$

C, $φ$

::: figure F2-5
caption: Figure 2-5. Factors Influencing Stress-Strain Behavior of Soil
axes: none
legend: none
description: A flowchart separates total deformation into individual grain deformations and relative grain motions and lists their contributing factors.
:::

1/8 Inch

::: figure F2-6
caption: Figure 2-6. Magnified View of Volcanic Scoria Grains
axes: none
legend: none
description: A magnified photograph shows the irregular porous surfaces of volcanic scoria grains with a scale marker.
:::
''', figures=['F2-5','F2-6'])

page(35, '''
There is general agreement (12, 15) regarding those factors which control the "strength" of dry granular soils and thus the ability of one grain to move with respect to another while offering maximum resistance. These factors are the grain-to-grain frictional resistance (dictated by the texture of individual grain surfaces), grain shape, grain size, grain size distribution, and spacing between grains. Each of these variables must be quantitively [sic] described for the subsequent experimental investigation. Size and spacing effects are conveniently handled with the following descriptors:

grain size - mean grain size ($μ$)

grain size distribution - standard deviation of size distribution (S) or uniformity coefficient ($C_u$)

spacing - relative density ($D_r$).

Grain shape and grain-to-grain frictional resistance are not as easily described and, in fact, must be measured indirectly. The strength of a soil is typically described in terms of the intercept, C (cohesion), and slope, $φ$ (internal friction angle), of the envelope of maximum shearing resistance versus normal stress on the failure plane. Thus if size and spacing effects ($μ$, S, $D_r$) are held constant, the "angle of internal friction" would provide a relative measure of grain shape and grain-to-grain friction for two different soils. The cohesion for lunar simulants would reflect "cementation" between particles.

No viscous or strain rate dependent properties have been considered for inclusion in the equation of state. This omission is based on the findings of a considerable amount of recent soil dynamics research which is summarized in reference (14) and indicates the insensitivity of the strength of dry granular material to strain rate variations.

Hence, in conclusion, the force displacement relation for a footpad as a function of soil parameters can be stated as shown below:

$$F(δ) = f(γ, μ, S, D_r, E, C, Φ)$$

Soil Parameters
''')

page(36, '''
where, F = force on footpad (F)

$δ$ = displacement of footpad (L)

$γ$ = soil density (F/L³)

$μ$ = mean grain size (L)

S = standard deviation in size (L)

$D_r$ = relative density (F⁰ L⁰ T⁰)

E = elastic (Young's) modulus (F/L²)

C = cohesive strength parameter (F/L²)

$Φ$ = angle of internal friction (F⁰ L⁰ T⁰)

f = function of

# 2.3 ESTIMATIONS OF THE PROPERTIES OF THE LUNAR SOIL

In order for the test results and analysis to be meaningful, the test soils used in the LM Soil Mechanics Study must have property values which include those of the lunar soil. When the final set of soils was being selected for the test work of this study, the lunar soil property estimation had to be made on the basis of Luna 9, Luna 13, and Surveyor I results, combined with postulations based on visual observations and theories on the origin of the surface topography of the moon. Since that time Surveyors III, V, VI and VII landed successfully on the moon and have provided considerably more information on surface properties so that more precise estimates could be made on the soil properties of concern here.

Table 2-1 shows the initial and present estimation of the lunar soil properties and a comparison with the soil properties of the test soils used in the LM Soil Mechanics Study. The initial estimates of the lunar soil properties were based on studies covered in References 17 through 29. The present estimates were based on studies covered in these references plus the Surveyor III report (Reference 9).
''', ['2.3'])

page(37, '''
TABLE 2-1. ESTIMATED LUNAR SOIL PROPERTIES AND COMPARISON WITH RANGE OF APPLICABILITY OF FORCE LAWS FROM LM SOIL MECHANICS STUDY (TARGET)

| | Estimated Lunar Soil Characteristics From Various Sources* | Range of Applicability of Force Laws (Target) | Present Estimates |
| --- | --- | --- | --- |
| Density | 40 to 100 lb./ft.³ (if on earth) | 20 to 110 lb./ft.³ | 60 to 130 |
| Relative Density | 30% to 85% | 0 to <100% | 50% to 100% |
| Angle of Internal Friction | 25° to 50° | 25° to 50°+ | 35° to 45° |
| Cohesive Shear Strength | 0 to <200 lb./ft.² | 0 to <100 lb./ft.² | .02 to .10 psi |
| Mean Grain Size | 10$μ$ to 100$μ$ | <70$μ$ to 2000$μ$ | 10$μ$ to 100$μ$ |
| Gradational Uniformity | Wide | Uniform to Very Wide | WIDE |
| Elastic Modulus (Recoverable Strains) | Probably Roughly Comparable to Earth Soils | | LOW |
| Grain Shape | Angular | Smooth to Highly Angular | ANGULAR |
| Uniformity with Depth | Uniform to Approximately 3 ft. Depths | Uniform | Uniform in composition to at least 3 feet. Possible higher compaction below 2-3 inches of surface. |

Footnotes:

*References 17 through 29.
''', tables=['T2-1'], rotation=90)

page(38, '''
It can be seen that the properties of the test soils generally encompass the estimates of the lunar soil properties. The one exception to this is mean grain size which overlaps only the higher region of the lunar soil mean grain size estimated range. This was found to be necessary since the fine grain size would exhibit considerable pore air effects in atmospheric tests.

Fortunately, analyses of the test results indicate that grain size and grain size distribution do not appear explicitly in the resistance equations for a soil in a vacuum. Therefore atmospheric tests on a soil having a large enough grain size that pore air effects are insignificant is a good simulation of the performance of a similar fine grain soil in a vacuum test.

# 2.4 SELECTION OF THE TEST SOILS

The basic requirements governing the types of soils to be used to develop the force interaction model were modified several times in the early stages of the program. This was primarily a result of Surveyor I and subsequent data narrowing the somewhat broad speculations of possible lunar surface characteristics that, in turn, had influenced the initial program requirements. The modifications resulted, eventually, in limiting the study to dry particulate materials of relatively small grain size that would fail, essentially, by particle displacement or compaction in combination with particle displacement.

The initial requirements, in comparison, were quite broad and called for a selection of relatively low bearing strength materials that would fail only or predominantly under each of several specified failure mechanisms. These included particle displacement, compaction, crushing or compression, and perimeter-shear-type failure. These and other requirements led to initial consideration of a relatively large number and variety of both natural and artificial materials as potential soil candidates.

Table 2-2 lists materials that were obtained in small sample lots for preliminary evaluation purposes. Many of these materials were eliminated from further consideration when it was determined that the lunar surface was a soil-like material as opposed to a weak rock-like structure, and some reasonable estimates were made of its bearing and cohesive strengths.
''', ['2.4'])

page(39, '''
TABLE 2-2. POTENTIAL TEST SOILS AND PRELIMINARY EVALUATION

| Material | Description | Approx. Density (#/Cu.Ft.) | Approx. Strength Range | Failure Type | Comments | Final Select'n [?] |
| --- | --- | --- | --- | --- | --- | --- |
| Silica Sand | AASCO [?] #4, White | 100-107 | 2-15 psi | Particle Displ. and Compaction | Satisfactory | |
| Silica Sand | WEDRON 4040, White | 100 | 2-15 psi | Particle Displ. and Compaction | Satisfactory | Used |
| Salt - Coarse | | 72-82 | 2-15 psi | Particle Displ. and Compaction | Satisfactory | |
| Salt - Fine | 200 Mesh | 40-65 | 0-15 psi | Particle Displ. and Compaction | Satisfactory | |
| Aluminum Oxide | 100 and 80 Mesh, Powdered | 110-140 | 5-15 psi | Particle Displ. and Compaction | Satisfactory, Very Expensive | |
| Air Floated Clay | Dry-200 Mesh | 80-100 | 0-15 psi | | Entrapped Air Effects, Potential Use Mixed With Other Materials | Used |
| Petroleum Coke | Graded, 0-5/32" Particle, Some Moisture | 50 | --- | Particle Displ. and Compaction | Excessive Moisture, Costs to Dry | |
| Charcoal - | #10 Granular, Commercial | 14-20 | --- | Particle Displ. and Compaction | | |
| Pumice-Powdered - | White, Screened, 200 + Mesh | 20-35 | 0-20 psi | | Entrapped Air Effects, Potential Use as Mix | |
| Pumice-Navajo and Grey Crushed | Approximately 1/4" to 5/8" Irregular Lumps | 25 | 3-10 psi | Particle Displ. and Compaction | Particles Too Large | |
| Pumice-Grey Crushed Fine | Narrowly Graded, Approximately 1/8" to 1/4" Particle Size | 25-30 | 3-10 psi | Particle Displ. and Compaction | Satisfactory | Used |
| Pumice-Block Grey and Black | "Featherock," Sawed, Black is Highly Vesicular | 35 | 100-200 psi | Compaction | Strength Too High, Similar to Rigid Surface | |
| Pumice-Charcoal | Grey-1/8" to 1/4" Broadly Graded Lumps | 25 | 3-10 psi | Particle Displ. and Compaction | Potentially Satisfactory | |
| Microballoons | Bakelite No. BJO-0930 [?] .0002" to .005" Diameter Hollow Spheres | 12 | Very Low | Particle Displ. and Compaction | Air Effects May Be Large | |
| Dylite-Unexpanded -- | Polystyrene Plastic Beads, "ISO-Fills" [?] | 40 | --- | Particle Displ. and Compaction | Particles Highly Elastic | |
| Dylite-Expanded | Made From Above, Vary From 8-40 Mesh, Can Be Tailored to Densities Between 1 and 10 #/Cu.Ft. | 1 to 10 | Very Low | --------- | Highly Elastic-Trapped Air | |
| CAB-O-SIL 2.2<br>CAB-O-SIL M-7,M-D-7<br>CAB-O-SIL M-5 | Fumed Silica, White | 2-7<br>7<br>6 | Extremely Low | Compaction | Extremely Low Strength, Entrapped Air Effects Predominate | |
| Pearlite | Granular, Commercial | Low | Low | Particle Displ. and Compaction | Spongy-Excessive Particle Breakdown | |
| Vermiculite | Granular, Commercial | Low | Low | | Particle Breakdown | |
| Pelaspan | Foamed Polystyrene | 1-10 | 10 psi up | Compaction and Compression | Highly Elastic | |
| Foamglas | Low Density Cellular Glass Insulation | 9 | 60 psi | Compaction-Brittle Fracture of Cell Walls | Strength Too High, Similar to Rigid Surface | |
| Foamthane | Foamed Polyurethane | 2 | 25 | Compaction and Compression | Highly Elastic, Strength Too High | |
| Foamthane (S.E.) | Self-Extinguishing Foamed Polyurethane | 2 | 25 | Compaction and Compression | Strength Too High, Material Elastic but More Brittle Than Regular | |
| Polylite | Foamed Polystyrene - | --- | 10 psi up | Compaction and Compression | Highly Elastic | |
| Marble Chips- | Narrowly Graded #10 Georgia, White Crushed- | 100 | 2-15 psi | Particle Displ. and Compaction | Satisfactory- | Used |
| Volcanic Cinders-Black | Crush, Screened, Dust to 1/4" Particle Size | 50-65 | 2-15 psi | Particle Displ. and Compaction | Satisfactory | |
| Volcanic Cinders-Red | Crushed, Screened, Dust to 1/4" Particle Size | 55-80 | 2-15 psi | Particle Displ. and Compaction | Satisfactory | Used |
| Volcanic Cinders-Black | Crushed, Narrowly Graded, Approximately 1/8" to 1/4" Particle | 40-65 | 2-15 psi | Particle Displ. and Compaction | Satisfactory | |
| Volcanic Cinders-Red | Crushed, Narrowly Graded, Approximately 1/8" to 1/4" Particle | 40-55 | 2-15 psi | Particle Displ. and Compaction | Satisfactory | Used |
| Aluminum Oxide Crust | Artificially Formed Top Surface Crust | 130 | 10 psi up | Perimeter Shear, Then Compaction and Particle Displ. | Extremely Difficult to Prepare in Large Quantities | |
| Sugar Bonded Silica, Low Cohesion<br>Sugar Bonded Silica, High Cohesion<br>Sugar Bonded Aluminum Oxide | Uniformly Permeated With Weak Solution of Sugar Water, Then Cured | 100<br>100<br>130 | 5 psi up<br>25 psi up<br>15 psi up | Particle Displacement and Compaction | | |
''', tables=['T2-2'])

page(40, '''
In addition to the requirement that the test soils must have properties which encompass the estimated properties of the lunar soil, the test soils must also have a large enough range of each soil descriptor that specific soil property effects can be identified. Ideally, the test soils should allow evaluation of a particular parameter effect by selecting several soils which are identical except for a single property. In practice this is extremely difficult and often impossible to achieve since a variation in one property usually results in variations of several of the other soil properties. This factor compounds the complexity of the analysis of the test data.

The soils selected for the LM Soil Mechanics Study and details of their properties are given in Table 2-3. It can be seen that they consist of various preparations or combinations of volcanic cinders, crushed pumice, silica sand, crushed marble and air-floated kaolin clay. Detailed description of each of these 12 soils is given in Appendix A.

The chart given in Figure 2-7 illustrates schematically how these soils may be evaluated in various ways to yield specific soil property effects. For example, the PS loose soil and RS loose soil are similar in all respects except for the bulk density. Therefore by examining the differences in test results for both the oblique impact tests and the drag tests the effect of bulk density can be identified. Knowing the effect of bulk density, the PS loose and RS loose, intermediate and dense results then allows the separation of relative density and angles of internal friction effects. Proceeding in this manner each of the various property effects can be categorized.

# 2.5 TEST PROCEDURES USED TO DETERMINE SOIL PROPERTIES

## 2.5.1 Types of Tests

The soil testing for this project falls into three categories.

a. Tests to determine the basic properties of the test soils used

b. Bearing strength tests

c. Control tests to determine the properties and uniformity of the soil beds for the drag, impact, and model drop tests.
''', ['2.5','2.5.1'])

page(41, '''
TABLE 2-3. TEST SOILS AND PROPERTIES

| No. | Bendix Designation | Description | Relative Density $D_r$ | Unit Weight $γ$ pcf | Friction Angle $φ$ | Elastic Modulus E,psi* | Grain Size Parameters<br>Mean Size $μ_w$ mm | Uniform Coeff. $C_μ$ | %** [?] -200 | $D_{95}$*** mm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RS Loose | Red Crushed Volcanic Scoria (narrowly graded) | 0 | 41.4 | 40° | 5,500 | 1.8 | 1.7 | <3% [?] | 2.7 |
| 2 | PS Loose | White Crushed Pumice (narrowly graded) | 0 | 23.8 | 43° | 4,500 | 1.8 | 1.7 | <3% | 2.7 |
| 3 | RS Inter. | Red Crushed Volcanic Scoria (narrowly graded) | .45 | 45.9 | 44.5° | 8,600 | 1.8 | 1.7 | <3% | 2.7 |
| 4 | RS Dense | Red Crushed Volcanic Scoria (narrowly graded) | .80 | 50.6 | 47.3° | 10,900 | 1.8 | 1.7 | <3% | 2.7 |
| 5 | RSM-a Loose | Mixture of RS and Crushed Marble (MS) (narrowly graded) | 0 | 58.2 | 37° | 7,800 | 2.4 | 1.6 | <3% | 2.7 |
| 6 | RC2 Loose | Red Crushed Volcanic Scoria (Broadly graded) | 0 | 61.4 | 43° | 8,000 | 1.1 | 17.0 | 11% | 4.7 |
| 7 | SS Loose | White Silica Sand (Wedron 4040-narrowly graded) | 0 | 94.7 | 29° | 10,000 | 0.4 | 1.3 | 0% | 0.52 |
| 8 | SS Inter. | White Silica Sand (Wedron 4040-narrowly graded) | .53 | 104 | 36.8° | 18,000 | 0.4 | 1.3 | 0% | 0.52 |
| 9 | SS Dense | White Silica Sand (Wedron 4040-narrowly graded) | .69 | 107 | 39° | 24,000 | 0.4 | 1.3 | 0% | 0.52 |
| 10 | LSM Inter. | Mixture of RC and Air-Floated Clay | .50 | 77.5 | 42° | 4,000 | .07 | large | 51% | 4 |
| 11 | LSM Dense | Mixture of RC and Air-Floated Clay | .70 | 82 | 42° | 6,000 | .07 | large | 51% | 4 |
| 12 | RSM-b Dense | Mixture of RS and Crushed Marbel [sic] (MS) (narrowly graded) | .75 | 85 | 48° | 20,000 | 2.15 | 1.87 | <1% | 2.9 |

Footnotes:

*Measured by sonic means at 4 psi confining pressure.

**Percent of material (by weight) passing thru' a No. 200 sieve (ACS).

***Diameter at 95% "smaller than" point in standard sieve analysis.
''', tables=['T2-3'])

page(42, '''
PS Loose

RS Loose

RSM Loose

Effect of Bulk Density $γ$

RS Loose

PS Inter

RS Dense

Effect of Relative Density $D_r$

Effect of Friction Angle $φ$, $γ$, $D_r$

SS Loose

SS Inter

SS Dense

Vacuum Studies

Pore Gas Effects

Vacuum Studies

Pore Gas Effects

RSM

RC2

Effect of $μ$ and $C_u$ Combined

Separation of $μ$ and $C_u$ Effects

Effects of $γ$, $D_r$, $φ$, $μ$, $C_n$ [sic]

RS Dense

LSM Dense

RS Loose & RSM Loose

LSM Loose

All Soils

Effects of Variations in E

Effects of $γ$, $D_r$, $φ$, $μ$, $C_u$, E With C ≈ 0

::: figure F2-7
caption: Figure 2-7. Flow Chart Illustrating Separation of Soil Property Effects
axes: none
legend: none
description: A flowchart links groups of soils and vacuum studies to the separation of soil property effects.
:::
''', figures=['F2-7'], rotation=90)

page(43, '''
## 2.5.2 Basic Soil Tests

By basic soil tests are meant those performed on previously unused samples of the soil, that is, prior to any changes induced by testing or handling procedures. They include the minimum-maximum density test, grain size analysis, the direct shear test, and the sonic velocity test. Table 2-3 summarizes the results of these tests and a detailed description of the procedures is given below.

### 2.5.2.1 Grain Size Analysis

Grain size analysis was performed in a manner similar to that outlined by Lambe (30, pp. 29-42)* and ASTM** (31, pp. 95-105).

Figure 2-8 shows the shaker used (Soiltest, Inc., Model No. CL 370C [32, p. 31]). Mounted on top of this shaker is a holder fabricated by Bendix for 8-inch diameter sieves. The large shaker holds five 20-inch by 20-inch sieve trays and a pan and is used for analysis of large soil samples (up to one cubic foot).

The 8-inch diameter sieves were used for smaller soil samples ranging from 0.01 to 0.03 cubic foot. The 8-inch diameter sieves were used for most of the analyses done for this program.

The other basic equipment required for grain size analysis is a thermostatically-controlled, constant-temperature drying oven (Figure 2-9), a beam balance scale with a sensitivity of 0.10 gram (Figure 2-10)***, and a sample splitter (Figure 2-11)****.

Footnotes:

*The numbers in brackets refer to the keyed references given in the Bibliography and the page numbers in the referenced publication.

**American Society for Testing and Materials.

***The beam balance scale shown is Model No. L-415 in the Soiltest, Inc., Catalog (33, p. 244).

****The sample splitter shown is Model No. S2512 in the Testlab Corporation Catalog (34, p. 32).
''', ['2.5.2','2.5.2.1'])

page(44, '''
::: figure F2-8
caption: Figure 2-8. Sieve Shaker
axes: none
legend: none
description: A photograph shows stacked circular sieves mounted above a shaker with rectangular sieve trays.
:::
''', figures=['F2-8'])

page(45, '''
::: figure F2-9
caption: Figure 2-9. Constant Temperature Oven
axes: none
legend: none
description: A photograph shows an open drying oven containing pans of soil and a wall-mounted controller.
:::
''', figures=['F2-9'])

page(46, '''
::: figure F2-10
caption: Figure 2-10. Triple Beam Balance
axes: none
legend: none
description: A photograph shows a triple beam balance and a set of weights.
:::

::: figure F2-11
caption: Figure 2-11. Sample Splitter
axes: none
legend: none
description: A photograph shows a person operating a sample splitter.
:::
''', figures=['F2-10','F2-11'])

page(47, '''
The grain size analysis is determined in the following manner.

a. A large sample (i.e., on the order of one cubic foot) is taken from a test bin or other batch of soil and successively halved in the sample splitter until a sample of convenient size is obtained.

b. The small sample is weighed (to the nearest 0.1 g), oven-dried (at 110°C, 230°F) and then reweighed. Figure 2-12 shows a typical grain size analysis data sheet for this study. Lines 1 and 2 show the values obtained for the operations described above. Line 3 shows the difference between these two weighings, the weight of water in the sample, and the computation to the right of line 3 shows the determination of moisture content (M.C.).

c. The oven-dried sample is placed in a #200* sieve and the material finer than the #200 sieve openings (called the "minus #200 material" or the "silt and clay" portion) washed out of the sample through the sieve (wet sieving).** The washed sample is oven-dried and weighed. This weight is recorded on line 4. The tare weight (weight of the pan the soil is in) is recorded on line 6 and this value is subtracted from the weight recorded on line 4 to obtain the weight of the grain size analysis sample for the dry sieving operation (line 8).

d. An appropriate set of sieves*** is placed together (in our example, those indicated by the symbol + on the data sheet) with the coarsest sieve at the top and a pan at the bottom beneath the finest sieve (a #200 sieve in our example).

Footnotes:

*The sieves used in this study are referred to by the number applied to them by the U.S. Bureau of Standards. The numbers are related to the size of the sieve openings (30, p. 31) and are commonly called the "U.S. Standard Sieve Numbers."

**Normally, removing the silt and clay portion from a sample by wet sieving prior to dry sieving is not considered necessary for soil containing less than about 10% finer than the #200 sieve. However, our studies indicated that prior washing resulted in doubling the amount of soil retained on the #40 and finer sieves even for soils containing only 1-2% "-#200" material.

***The uppermost sieve in the series should be the finest sieve through which all the samples will pass. The following sieves are generally chosen such that each succeeding sieve has openings half the size of the previous one.
''')
