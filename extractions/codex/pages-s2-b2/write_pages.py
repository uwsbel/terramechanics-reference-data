from pathlib import Path
import json

def w(n, body, sections=[], figures=[], equations=[], rotation=0, tables=[]):
    header = ['---', 'source: bendix-1968-vol1', f'pdf_page: {n}', f'printed_page: "2-{n-25}"']
    for key, value in [('sections',sections),('figures',figures),('tables',tables),('equations',equations)]:
        header.append(f'{key}: {json.dumps(value)}')
    header += [f'rotation: {rotation}', f'image: corpus/1968/images/p{n:04d}.png', 'transcriber: codex', 'review_status: single-reading', '---']
    Path(f'out/p{n:04d}.md').write_text('\n'.join(header)+'\n'+body.strip()+'\n', encoding='utf-8')

w(48, r'''
GRAIN SIZE (SIEVE) ANALYSIS

Project: LM Soil Mechanics Study

Date: 2-6-67. Perf. By: J.M.

Soil Type: RC2 used for test bed for SS Drag Test #8-1 [?]

Soil Symbol RS RC2 RSM PS SS LSM

Soil Preparation: Washed through #200 sieve; dried

1. Total weight soil plus tare = 655.2

2. Total OD* weight soil plus tare = 653.7

3. Weight water (① - ②) = 1.5

4. Weight OD washed soil plus tare = 595.2

5. Weight - 200 material (② - ④) = 58.5

6. Weight tare = 121.8

7. Total OD weight soil (② - ⑥) = 531.9

8. OD weight SA sample (④ - ⑥) = 473.4

All weights in Grams Lbs. (circle)

$$M C = \frac{100③}{⑦} = 0.3\%$$

$$\%\ \text{Sieve Loss} = \frac{[⑧ - (⑨ - ⑤)]\ 100}{⑧} = \underline{\qquad} = 0.2\%$$

| SIEVE NO. (U.S. STD.) | SIEVE SIZE (MM) | WGT. RET. "W" | % WGT. RET. 100W/⑨ | CUM. % RET. | % PASSING |
| --- | --- | --- | --- | --- | --- |
| 3 8" ⊕ | 9.52 | 0.0 | 0.00 | 0.00 | 100.00 |
| 3 | 6.35 | | | | |
| 4 ⊕ + | 4.76 | 32.1 | 6.05 | 6.05 | 93.95 |
| 6 ⊕ + | 3.36 | 77.7 | 14.63 | 20.68 | 79.32 |
| 8 ⊕ + | 2.38 | 62.7 | 11.80- [sic] | 32.48 | 67.52 |
| 10 + | 2.00 | | | | |
| 12 ⊕ + | 1.68 | 44.9 | 8.46 | 40.94 | 59.06 |
| 16 ⊕ + | 1.19 | | | | |
| 20 ⊕ + | 0.84 | 64.7 | 12.19 | 53.13 | 46.87 |
| 40 ⊕ + | 0.42 | 54.5 | 10.27 | 63.40 | 36.60 |
| 60 ⊕ | 0.25 | 42.5 | 8.01 | 71.41 | 28.59 |
| 80 | 0.177 | | | | |
| 100 ⊕ + | 0.149 | 40.3 | 7.59 | 79.00 | 21.00 |
| 120 | 0.125 | | | | |
| 200 ⊕ + | 0.074 | 48.9 | 9.21 | 88.21 | 11.79 |
| PAN | | 4.1 | | | |
| ⑤ | | 58.5 | | | |
| TOTAL - 200 | | 62.3 [?] | 11.79 | 100.00 | 0.00 |
| TOTAL WGT. (⑨) | | 530.9 | | | |

⊕ For Broadly-Graded Soils (e.g., RC2, LSM)

+ For Coarse, Narrowly-Graded Soils (e.g., RS, PS, RSM)

::: figure F2-12
caption: Figure 2-12 Grain Size (Sieve) Analysis
axes: none
legend: none
description: A filled grain size analysis worksheet with weight calculations and a sieve table.
:::

Footnotes:

* OD - Oven-Dried at 110 C (230 F)
''', figures=['F2-12'])

w(49, r'''
[cont.] The soil sample is placed in the top of the set of sieves and the shaker put in operation for 10 minutes.*

e. After the shaking operation, the weight of soil retained on each sieve and the pan is recorded on the data sheet (the third column in our example). The amount of - #200 material previously washed out (line 5) is added to that obtained in the pan ** to obtain the total weight of - #200 material. These weights are then converted to "% weight retained" as shown in the fourth column in our example (computed as a percentage of the total weights used in the "weight retained" column - line 9)***. The sum of the "% weight retained" values should be 100 per cent. The "% passing" can then be computed by successively subtracting the "% weight retained" figure from the preceding "% passing" figure (starting with 100%), or, subtracting the "cumulative % weight retained" from 100% for each sieve.

f. The resulting "% passing" or "percent finer than by weight" is then plotted versus sieve size or grain size on a graph similar to that shown in Figure [?] 2-13. (The data points shown are those from the data sheet example.) The [?] "% passing" is shown on the ordinate of this graph to a linear scale. The [?] U.S. Standard Sieve Size is shown on the upper abscissa. Also shown, below [?] the bottom abscissa, is the ASEE (American Society for Engineering Education) definitions of soil components as reported by D. M. Burmister in his article "Suggested Methods of Test for Identification of Soils" (31, pp. 222-223).

Footnotes:

*For finer-grained soils, the time is increased to 15 minutes (30, p. 31).

**Note that the amount retained in the pan will be a function of how well the sample was washed and/or the amount of particle breakdown during sieving.

***The "% Sieve Loss" is computed as shown in the upper right-hand corner of our example. If this figure is greater than 1%, the procedure or computations should be examined for the source of error or loss.
''')

w(50, r'''
GRAIN SIZE ANALYSIS CURVES - LM SMS

::: figure F2-13
caption: Figure 2-13. Grain Size Curve for Example Data in Figure 2-12
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: none
description: A grain size curve with circular data markers on a logarithmic grain size axis.
:::

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |
''', figures=['F2-13'], rotation=90)

w(51, r'''
The major grain size parameters used in this study are mean grain size (by weight), $D_{50}$* ($ℓ$ [?], $μ_S$ [?]) and the coefficient of uniformity, $C_u$, which is defined as the ratio of $D_{60}$ to $D_{10}$, these values being taken from the grain size curve. Other grain size parameters which further define the grain size curve are effective size, $D_{10}$; the "%-#200,"** and the value of $D_{95}$. Knowledge of all these-values [sic] will allow a fairly accurate reproduction of the grain size curve.

Other quantities describing characteristics of the grain size distribution curve are described in the referenced literature (35, pp. 21-25; 46, pp. 25-27). These other grain size curve characteristics were not used because they were considered either redundant or of unproven value to the present study, or represented a degree of refinement not warranted by the scope of this study.

The-values [sic] for the grain size curve characteristics described above for our example data are:

Mean Grain Size, $D_{50}$, = 1.0 mm

Coefficient of Uniformity, $C_u$, = $D_{60}/D_{10}$ = 1.8/0.064*** = 28

Effective Size, $D_{10}$, = 0.064 mm***

Percent by weight of clay and silt size particles, "% -#200" = 11%

$D_{95}$ = 5.5 mm

The grain size curves on the graph in Figure 2-14 show the results of the averaging of several grain size analyses run on each of the six basic soil types being used in the LM [cont. next page]

Footnotes:

*"$D_x$" indicates the grain size or sieve opening corresponding to the "X% finer than by weight" point on the grain size curve.

**"% -#200" is the value of "Percent Finer Than by Weight" at the point where the grain size curve crosses the #200 sieve line and represents the percentage (by weight) of clay and silt size particles in the soil.

***Note that the value of $D_{10}$ is interpolated since the last data point corresponds to about $D_{11}$.
''')

w(52, r'''
GRAIN SIZE ANALYSIS CURVES - LM SMS

::: figure F2-14
caption: Figure 2-14. Average Curve for Six Basic Test Soils
axes: x Grain Size - mm; x2 U.S. Std. Sieve No.; y Percent Finer Than By Weight
legend: LSM; SS; RC2; RSM-a; RS; PS
description: Six labeled grain size curves on a logarithmic grain size axis.
:::

| ASEE Class. | SILT (Nonplastic) | Fine | Medium | Coarse | Fine |
| --- | --- | --- | --- | --- | --- |
| | CLAY (Plastic) | SAND | | | GRAVEL |
''', figures=['F2-14'], rotation=90)

w(53, r'''
[cont.] soil mechanics study.* Table 2-3 summarizes the grain size distribution parameters derived from the curves shown in Figure 2-14.

Since the finest size that sieve analysis measures is 0.074 mm (i.e., that material passing the #200 sieve), any size measurement in the clay and silt size range necessary to determine a grain size distribution parameter is not available except, possibly, by extrapolation. Note that extrapolation is necessary to get the value of $D_{10}$ for our example curve in Figure 2-13 and the value of $D_{50}$ for the LSM soil in Figure 2-14.

Since these interpolated values are relatively close to the last data points they are fairly reliable. An estimate of $D_{10}$ for the LSM soil, however, could not be made with any great degree of confidence, and, hence, no definite quantitative values are given for these parameters in Table 2-3.

It can be seen that movement of a curve upward and to the left on the grain size analysis graph indicates increasing fineness (decreasing $D_{50}$) of the soil and movement downward and to the right increasing coarseness (increasing $D_{50}$). The slope of the central portion of the curve indicates the broadness of gradation - a steep slope indicating a narrowly-graded soil ($C_u$ approaching one) and a flat slope indicating a broadly-graded soil ($C_u$ large).

Samples of the soil beds were taken from the drag and impact test bins periodically for grain size analysis and minimum-maximum density tests to provide a check on possible grain size distribution changes taking place throughout a test series. The periodic check tests provide quantitative information about these changes, and these values can be incorporated into the overall analysis of the force law investigation.

### 2.5.2.2 Minimum-Maximum Density Test

The minimum-maximum density test established the relative density scale for a given soil. Minimum density is that unit weight representing the least compact condition of a soil. In this state the soil possesses its maximum void ratio (i.e., ratio of volume of [cont. next page]

Footnotes:

*The results shown are for tests run on previously unused, undegraded samples of soil.
''', sections=['2.5.2.2'])

w(54, r'''
[cont.] voids to volume of solids) and has, by definition, a relative density equal to zero. Maximum density is the unit weight of the soil in its most compact condition when it has its smallest possible void ratio and a relative density equal to one.

The concept of relative density was originally expressed in terms of void ratio as shown:

$$D_r = \frac{e_{max} - e}{e_{max} - e_{min}}$$ (2-1)

where: $D_r$ = relative density

e = void ratio

$$= \frac{V_v}{V_s}$$

$V_v$ = volume of voids or pore spaces in a soil mass of unit volume

$V_s$ = volume of soil grains in a soil mass of unit volume

$e_{max}$ = maximum possible value of "e" for a given soil

$e_{min}$ = minimum possible value of "e" for a given soil.

Void ratio is related to the dry unit weight of a soil by the expression:

$$e = \frac{Gγ_w}{γ} - 1$$

where:

G = specific gravity of the soil grains

$γ_w$ = unit weight of water

$γ$ = dry unit weight or density of the soil.
''', equations=['2-1'])

w(55, r'''
If we replace this expression for "e" in the equation for "$D_r$" given above, we obtain:

$$D_r = \frac{γ - γ_{min}}{γ_{max} - γ_{min}} \cdot \frac{γ_{max}}{γ}$$ (2-2)

where:

$γ_{min}$ = minimum density or unit weight (corresponding to $e_{max}$)

$γ_{max}$ = maximum density or unit weight (corresponding to $e_{min}$).

As can be seen from equation (2-2) above, there is a linear relationship between $D_r$ (relative density and the reciprocal of unit weight (i.e., $1/γ$)). Hence, a plot of density or unit weight on a linear scale allows one to join minimum and maximum density with a straight line to represent the relationship between $D_r$ and $γ$.

Figure 2-15 shows a graphical solution of equation (2-2) for a density range of 55-115 pcf. The slanting line on this graph represents a hypothetical soil having a minimum density of 64.0 pcf and a maximum density of 78.0 pcf which represents relative densities of 0.0 and 1.0, respectively, for this soil as shown. The relative density of this soil having a density between the minimum and maximum densities can be found by noting the value of relative density corresponding to the given density along the line joining the minimum and maximum density points.

Figure 2-16 illustrates some of the equipment used in the performance of the minimum-maximum density test. This apparatus includes a standard compaction mold* (volume: [cont. next page]

Footnotes:

*Available from Soiltest, Inc., Model No. CN404 (33, p. 38).
''', equations=['2-2'])

w(56, r'''
::: figure F2-15
caption: Figure 2-15. Unit Weight vs. Relative Density Graph
axes: x Relative Density, $D_r$; y Minimum Density, $γ_{min}$ (pcf); y2 Maximum Density, $γ_{max}$ (pcf)
legend: none
description: A sloping density conversion line with dashed arrows illustrating a graphical reading.
:::
''', figures=['F2-15'])

w(57, r'''
::: figure F2-16
caption: Figure 2-16. Vibrating Tool and Proctor Mold
axes: none
legend: none
description: A photograph of a person operating a vibrating tool over a mold on a laboratory bench.
:::
''', figures=['F2-16'])

w(58, r'''
[cont.] 1/30 cu. ft.), a small vibratory compactor*, a pound scale (sensitivity: -0.01 lb.)**, a sample splitter***, a funnel, various scoops, brushes, and pans.

The method used for determining minimum and maximum density of the test soils is that developed by D. M. Burmister (31, pp. 175-177). To determine the minimum density, obtain a representative sample of air-dried soil sufficient to make 3 or 4 determinations without reusing material (about 1/6 cu. ft.). Mix soil thoroughly before each determination to minimize segregation effects****.

Deposit soil into mold through a funnel***** such that the distance from the bottom of the funnel and the soil already placed is the minimum necessary to allow the flow of the soil through the funnel. The soil is placed by moving the funnel in a concentric motion from side to center of the mold, bringing the soil level up in more or less horizontal layers.

Footnotes:

*The small vibratory compactor pictured is an electrically-operated engraving tool which has been modified to hold a tamping foot (the one shown is 3-1/2 inches in diameter). The engraving tool is commercially available as the "Vibro-graver," Model V-73, manufactured by Burgess Vibrocrafters, Inc., Grayslake, Illinois.

**Available from Soiltest, Inc., Model No. L-770 (33, p. 49).

***Available from Testlab Corp., Model No. S2512 (34, p. 32).

****Variation in test results due to segregation of grain sizes is especially noticeable with broadly-graded soils. This variation can be substantially reduced if the test sample is quartered in the sample-splitter and each quarter used to determine a test point.

*****A funnel with an inside diameter of 5/8 inches was used in this study. Too large a diameter will allow the soil to flow from the funnel too quickly and cause higher values of minimum density. Too small a diameter will not allow the soil to flow. The appropriate diameter for a given soil is the minimum that will allow free flow of the soil.
''')

w(59, r'''
When soil is placed to overflowing in mold, screed off excess level with top of mold with a straight edge*.

Determine the weight of the soil and divide this by the volume of the mold (1/30 cu.ft.) to obtain value of minimum density.

Make three or four determinations of minimum density to obtain average and range of values for several different samples of soil.

The maximum density test is performed with soil used for minimum density test using same precautions for ensuring uniformity of sample.

Place 1.0-inch thick layer of soil in mold and tamp with vibratory compactor for two minutes**.

Place successive layers (compacting each for the specified time) until the soil extends over the top of the mold.

Screed off excess soil level with top of mold; weigh mold and soil as previously described for minimum density test, and determine the value for maximum density.

Make-three [sic] or four determinations of maximum density in this manner on several different samples of the soil to obtain the average and range of values for the soil.

Footnotes:

*At no time during the filling process and final screeding should the mold be subjected to vibration or impact as this will tend to densify the soil.

**The thickness of layer and time required for compaction of each layer to achieve maximum density depends on the type of soil and type of compactor used. Studies by Bendix indicated that 1/2-inch layers compacted with the small vibratory compactor (fitted with a 1-1/4-inch diameter tamping foot) for 1-1/2 minutes produced a satisfactory value for maximum density. Subsequent investigations showed that use of a 3-1/2-inch diameter tamping foot on the vibratory compactor, placement of 1-inch layers, and a time of compaction (per layer) of two minutes produced equivalent values of maximum density. Since the latter method is much less time-consuming its use is preferable.
''')

w(60, r'''
The minimum-maximum density test data was evaluated using the following criteria:

Those values of minimum or maximum density obtained from a series of tests on a given sample which varied more than 3% from the overall average were eliminated from the final computation of the average reported.

The minimum requirement for the number of tests run on a given soil sample was that at least 75% of the test results fall within 3% of the reported average.

The average minimum and maximum densities obtained by the test procedures described above and using the evaluation criteria outlined are then plotted on a graph similar to that shown in Figure 2-15. Figure 2-17 shows the results of tests done on several different samples of each of the six basic soil types being used in the LM soil mechanics study. The values shown were obtained on previously unused, undegraded soil materials or on soils that did not suffer appreciable degradation.

Considerable variation in test results can be obtained if the conditions leading to such variation are not recognized and eliminated in the test procedures used. Basically, such variation results from variation of the soil material and inadequate control of the test procedures and apparatus.

Variation of the Soil - This type of variation is due to nonuniformity of the grain size distribution and the material comprising the soil grains which occurs at the source of supply of the soil material. The use of proper sampling techniques to choose the samples to be tested from the soil material supplied will ensure that statistical analysis of the test results incorporate the influence of such nonuniformity.

Inadequate Control of Test Procedures - Certain variations in test results are bound to occur such that the results fall above and below some "true" value which can adequately be described by the average value. Such variation can be defined by statistical analysis. However, inadequate control over the test procedure can introduce variation [cont. next page]
''')

w(61, r'''
::: figure F2-17
caption: Figure 2-17. Average Density vs. Relative Density Curves for Six Basic Soil Types
axes: x Relative Density, $D_r$; y Minimum Density, $γ_{min}$ (pcf); y2 Maximum Density, $γ_{max}$ (pcf)
legend: none
description: Six straight density conversion lines on a reciprocal density scale.
:::
''', figures=['F2-17'])

w(62, r'''
[cont.] which is more or less consistently above or below the "true" value and the average of these values is not an adequate representation of the "true" value. These effects and the procedures used to eliminate or minimize them are discussed below.

Variation in Grain Size Distribution - The density of a given soil depends primarily on the width of the grain size distribution and distribution of particle sizes within that range. A well graded soil is a broadly-graded soil whose particle sizes are distributed in such a manner that an optimum unit weight can be achieved. A poorly graded soil is one in which the majority of soil particles fall into a narrow range of sizes and the unit weight of the soil falls below the optimum mentioned above to a degree dependent on the width of gradation and the distribution of particle sizes.

If a soil sample which is being tested is poorly mixed (i.e., nonuniform in terms of grain size distribution, or, particle sizes are segregated) the soil placed in the test mold will not be representative of the sample and, thus, the unit weight achieved will not be representative. This type of variation will be especially acute with broadly-graded soils (e.g., the RC2 soil, in this study). The variations due to such nonuniformity can be minimized by splitting the sample down into size units close to that required for one test determination.

Nonuniformity of grain size distribution can also occur during placement of the soil into the mold if the soil is placed in such a manner that the soil particles are allowed to roll down a slope. This can be prevented by placing the soil from the funnel in a concentric circling motion from the side of the mold to the center such that the soil is built up in relatively level layers.

If the soil grains are relatively weak the compaction process used to achieve maximum density may produce a change in grain size distribution which has a significant effect on the value of maximum density achieved. Grain size analysis of the soil before and after being tested for maximum density will indicate whether or not such a change is taking place.
''')

w(63, r'''
Variation in Soil Placement - If the soil is not placed in the mold with the minimum free fall from the funnel, higher densities will be produced.

Allowing the soil to flow too quickly from the funnel will also tend to produce higher values for minimum density.

Vibration of Loose Soil - Vibration or impact of the mold during performance of the minimum density test will tend to produce high values of density.

Variation in Compactive Effort - Since vibratory compaction has been found to be the most effective way to compact dry, granular materials, this method was used to determine the maximum density of the soils used in this study*. The degree of compaction achieved is a function of the thickness of the layer being compacted, the time taken to compact each layer and the size of the tamping foot. In practice, if a given size of layer is specified and a tamping foot of given size is used, maximum density can be expressed as that density at which additional compactive effort will effect no significant increase in density. A study was made by Bendix in which 1/2-inch layers of RS soil were compacted for various time increments using the small vibratory compactor, previously described, fitted with a 1-1/4-inch diameter tamping foot. Figure 2-18 shows the results of these tests. These graphs indicate that very little increase in density was obtained after 1-1/2 minutes of compaction per layer. Subsequently, it was found that similar maximum densities were achieved using 1-inch layers compacted for two minutes using a 3-1/2-inch diameter tamping foot. Since this configuration allowed for quicker determinations, this was the standard technique adapted for the latter part of our study.

As discussed previously, it was found that the compaction process can result in some breakdown of the cinder soil particles and, thus, the maximum densities reported for these soils might tend to be slightly higher than the "true" value for these soils. Care should be taken that these soils are not compacted for greater periods of time than [cont. next page]

Footnotes:

*The vibratory methods also produce much less breakage of the particles of the cinder soils used in this study than the standard "impact" compaction methods.
''')

w(64, r'''
NOTE: Soil compacted in 1/2 inch layers with small vibratory compactor fitted with 1-1/4 inch diameter tamping foot.

RS Soil (used)

::: figure F2-18
caption: Figure 2-18. LM Soil Mechanics Study - Time of Compaction Study
axes: x Unit Weight ~ pcf; y Duration of Compaction per Layer - Seconds
legend: Test No.; □ #13; ○ #14; △ #15
description: Three compaction curves with square, circular, and triangular markers and a dashed duration guide.
:::

1-1/2 Min. Per Layer
''', figures=['F2-18'], rotation=90)

w(66, r'''
D

F

A

E

C

[illegible]

G

B

::: figure F2-19
caption: Figure 2-19. Direct Shear Test Measurement
axes: none
legend: none
description: A photograph of direct shear equipment with parts labeled A through G.
:::
''', figures=['F2-19'], rotation=90)

w(67, r'''
Dial Extensometer to Measure Volume Change of Sample

Static Normal Load

Soil Sample

Shear Box - Upper Frame

Load Cell to Measure Shear Load

Shear Box - Lower Frame

Shear Load

Dial Extensometer to Measure Strain

Porous Stone

Weep Holes

Rate of Strain ≈ 0.07 In./Min.

Constant Speed Motor

::: figure F2-20
caption: Figure 2-20. Schematic Drawing of Direct Shear Test Equipment
axes: none
legend: none
description: A labeled schematic of a split shear box, loading mechanism, and measurement instruments.
:::
''', figures=['F2-20'], rotation=90)

w(68, r'''
RS Soil

$γ$ = 46.5 to 47.4 Lb./Ft.³ ($D_r$ = .5 to .57)

::: figure F2-21
caption: Figure 2-21. Direct Shear Test Data
axes: x Shear Displacement $δ_σ$ x 10³ (In.); y Shear Stress $τ$ (psf); y2 Dilation or Normal Displacement $δ_σ$ x 10³ (In.)
legend: Normal Stress σ (psf), Unit Weight γ (pcf); × 3520, 46.7; * 2935, 46.5; □ 2345, 46.7; + 1760, 46.7; ▽ 1172, 46.8; △ 587, 47.2; ○ 294, 47.4
description: Two panels show shear stress and normal displacement against shear displacement for seven test series.
:::

Same Notation as Above
''', figures=['F2-21'])

w(69, r'''
FAILURE ENVELOPE

(Maximum Shear Stress vs. Normal Stress)

RS SOIL, $D_r$ ≈ 0.55

Average Unit Weight, $γ_{avg}$ = 46.9 pcf

::: figure F2-22
caption: Figure 2-22. Failure Envelope
axes: x Normal Stress, σ (psf); y Maximum Shear Stress, $τ_{max}$ (psf)
legend: none
description: Circular test points and a straight failure envelope with angle and cohesion annotations.
:::

45°

Apparent Cohesion
''', figures=['F2-22'])

w(70, r'''
[cont.] S = Shear resistance or strength of the soil (or, the maximum shear stress recorded in a direct shear test, $τ_{max}$).

C = Cohesion; shear strength due to cohesion.

$σ_n$ = Normal stress on plane of shear.

$φ$ = Angle of internal friction.

Solving this equation for $φ$ yields:

$$φ = \tan^{-1} \frac{S - C}{σ_n} = \text{slope of failure envelope}$$

All of the direct shear test data and failure envelopes obtained on the test soils is presented in Appendix C. Figure 2-23 summarizes the average relationship found between angle of internal friction and relative density* for all the test soils except soil number 10 as determined by the direct shear tests.

Examination of the failure envelopes obtained for the test soils (see Appendix C) and the relationships between $φ$ and $D_r$ shown in Figure C-1b reveals the following noteworthy characteristics:

The values of angle of internal friction for the cinder soils are substantially higher than those for the silica sand (which values are more or less typical of earth-type granular noncohesive soils). The failure envelopes indicate appreciable values of "cohesion" for the cinder soils. The curves for the cinder soils tend to be relatively flat.

The data for the LSM soil indicates no change of $φ$ with $D_r$ and, at least nominally, shows a higher value of $φ$ for the test run at the lower relative density.

The relatively high value for angle of internal friction obtained for the cinder soils can be explained by the difference in particle surface characteristics between the cinder particles and earth-type soils such as silica sand. Although it has been found that [cont. next page]

Footnotes:

*The value of relative density used is the value existing prior to application of the normal load.
''')
