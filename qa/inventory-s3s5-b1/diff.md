# Table diff: claude vs codex

Files: `extractions/claude/inventory-s3s5-b1/inventory.csv` (claude), `extractions/codex/inventory-s3s5-b1/inventory.csv` (codex), compared after the page-qualified aliases of `qa/inventory-s3s5-b1/id-aliases.json`. Key: `id`. Column `notes` not compared.

Rows: 101 in claude, 102 in codex. Compared columns: 28.
Cells compared: 2828. Agreed: 2345 (82.9 percent).
Disagreements: 484 (43 numeric, 440 text, 1 missing rows).

| key | column | kind | claude | codex |
|---|---|---|---|---|
| F3-1 | soils | text | none | n/a |
| F3-1 | apparatus | text | subscale drag equipment | subscale drag rig |
| F3-1 | rate_or_dynamics | text | n/a | constant speed |
| F3-2 | soils | text | none | n/a |
| F3-2 | apparatus | text | subscale drag equipment; soil bin | subscale drag rig |
| F3-2 | rate_or_dynamics | text | n/a | constant speed |
| F3-2 | panels | number | 0 | 2 |
| F3-2 | trace_classes | text | setup-evidence | schematic |
| F3-3 | soils | text | none | n/a |
| F3-3 | apparatus | text | subscale drag equipment | subscale drag rig |
| F3-3 | rate_or_dynamics | text | n/a | acceleration |
| F3-4 | soils | text | none | n/a |
| F3-4 | apparatus | text | subscale drag equipment | subscale drag rig |
| F3-4 | rate_or_dynamics | text | n/a | constant speed |
| F3-5 | soils | text | none | n/a |
| F3-5 | apparatus | text | subscale drag 3D load cell | subscale drag load cell |
| F3-5 | panels | number | 0 | 1 |
| F3-5 | trace_classes | text | setup-evidence | schematic |
| F3-6 | soils | text | none | n/a |
| F3-6 | apparatus | text | subscale drag 3D load cell | subscale drag load cell |
| F3-6 | panels | number | 0 | 1 |
| F3-6 | trace_classes | text | setup-evidence | schematic |
| F3-7 | soils | text | none | n/a |
| F3-7 | apparatus | text | subscale drag 3D load cell | subscale drag load cell |
| F3-7 | panels | number | 0 | 1 |
| F3-7 | trace_classes | text | setup-evidence | schematic |
| F3-8 | soils | text | none | n/a |
| F3-8 | rate_or_dynamics | text | static calibration | calibration |
| F3-8 | trace_classes | text | measurement-markers;author-fit | measurement-markers;setup-evidence |
| F3-8 | in_scope | text | maybe | yes |
| F3-9 | soils | text | none | n/a |
| F3-9 | rate_or_dynamics | text | static calibration | calibration |
| F3-9 | trace_classes | text | measurement-markers;author-fit | measurement-markers;setup-evidence |
| F3-9 | y_unit | text | Min., In. | Min. In. |
| F3-9 | in_scope | text | maybe | yes |
| F4-1 | soils | text | none | n/a |
| F4-1 | apparatus | text | none | LM footpad |
| F4-1 | rate_or_dynamics | text | n/a | impact and slide out |
| F4-1 | panels | number | 0 | 1 |
| F4-2 | soils | text | all drag soils | soils 1-11 |
| F4-2 | states | text | n/a | multiple |
| F4-2 | apparatus | text | subscale drag equipment; 6 and 4 inch footpads | subscale drag rig |
| F4-2 | rate_or_dynamics | text | constant velocity VH 1.5 to 15 fps | constant penetration or pressure |
| F4-2 | priority | number | 2 | 1 |
| F4-3 | soils | text | RS; PS; RSM; RC2; SS; LSM | soils 1-11 |
| F4-3 | states | text | L; I; D | multiple |
| F4-3 | apparatus | text | subscale drag equipment | subscale drag rig |
| F4-3 | rate_or_dynamics | text | n/a | program totals |
| F4-3 | curves | number | 1 | 0 |
| F4-3 | trace_classes | text | measurement-markers | setup-evidence |
| F4-3 | x_quantity | text | soil (bars numbered 1 to 11) | soil number |
| F4-3 | y_quantity | text | number of tests (axis untitled) | number of tests |
| F4-3 | in_scope | text | maybe | no |
| F4-3 | priority | number | 2 | 3 |
| F4-4 | test_type | text | drag | apparatus |
| F4-4 | soils | text | none | n/a |
| F4-4 | rate_or_dynamics | text | n/a | constant penetration |
| F4-4 | panels | number | 0 | 1 |
| F4-4 | trace_classes | text | setup-evidence | schematic |
| F4-5 | apparatus | text | subscale drag equipment; 6 inch LM footpad | subscale drag rig |
| F4-5 | rate_or_dynamics | text | constant velocity, header 15 fps | constant penetration |
| F4-5 | data_form | text | curve | mixed |
| F4-5 | x_quantity | text | time (record travel, 1/10 second timing marks) | time |
| F4-5 | x_unit | text | 1/10 second marker | Second |
| F4-5 | y_quantity | text | nine channels A to I as record deflection | multiple chart channels |
| F4-5 | y_unit | text | per-channel sensitivity per inch of record | multiple |
| F4-5 | legend_entries | text | A horizontal displacement 30 inches/inch;B horizontal acceleration 2.78 g/inch;C vertical displacement d 0.744 inch/inch;D angle function hs 1 unit/inch;E side load Fs 17.7 lb./inch;F vertical load Fv 29.4 lb./inch;G angle function hp 1 unit/inch;H drag load FD 34.8 lb./inch;I horizontal velocity VH 5.75 fps/inch | A horizontal displacement;B horizontal acceleration;C vertical displacement;D angle function;E side load;F vertical load;G angle function;H drag load;I horizontal velocity |
| F4-5 | relation | text | none | same-as |
| F4-5 | relation_target | text |  | F4-7 |
| F4-7 | states | text | loose (Dr 0) | loose |
| F4-7 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-7 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-7 | relation | text | derived-from | none |
| F4-7 | relation_target | text | F4-5 |  |
| F4-8 | states | text | intermediate (Dr 0.45) | intermediate |
| F4-8 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-8 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-8 | relation | text | unresolved | none |
| F4-8 | relation_target | text | F2-60 |  |
| F4-9 | states | text | dense (Dr 0.80) | dense |
| F4-9 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-9 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-9 | relation | text | unresolved | none |
| F4-9 | relation_target | text | F2-60 |  |
| F5-1 | soils | text | none | n/a |
| F5-2 | printed_page | text | 5-5 | unknown |
| F5-2 | soils | text | none | n/a |
| F5-2 | panels | number | 0 | 1 |
| F5-2 | trace_classes | text | setup-evidence | schematic |
| F5-2 | in_scope | text | no | maybe |
| F5-3 | soils | text | none | n/a |
| F5-4 | soils | text | none | n/a |
| F5-4 | apparatus | text | 1/6-scale LM model legs | 1/6-scale LM leg assembly |
| F5-5 | soils | text | none | n/a |
| F5-5 | panels | number | 0 | 1 |
| F5-5 | trace_classes | text | setup-evidence | schematic |
| F5-6 | soils | text | none | n/a |
| F5-6 | apparatus | text | leg set 1 load cell; pad pots | 1/6-scale LM leg set No. 1 |
| F5-6 | panels | number | 0 | 1 |
| F5-6 | trace_classes | text | setup-evidence | schematic |
| F5-7 | soils | text | none | n/a |
| F5-7 | apparatus | text | leg set 1 load cell | 1/6-scale LM leg set No. 1 |
| F5-7 | panels | number | 0 | 3 |
| F5-7 | trace_classes | text | setup-evidence | schematic |
| F5-8 | soils | text | none | n/a |
| F5-8 | apparatus | text | leg set 1 footpad | 1/6-scale LM leg set No. 1 |
| F5-9 | soils | text | none | n/a |
| F5-9 | panels | number | 0 | 2 |
| F5-9 | trace_classes | text | setup-evidence | schematic |
| F5-9 | legend_entries | text | n/a | Modified Model;Present LM |
| T5-1 | soils | text | none | n/a |
| T5-1 | rate_or_dynamics | text | n/a | similarity |
| T5-1 | in_scope | text | yes | maybe |
| T5-2 | soils | text | RS; SS | RS;SS |
| T5-2 | states | text | dense; loose; intermediate | loose;intermediate;dense |
| T5-2 | apparatus | text | 1/6-scale LM model; six degree of freedom drop rig | 1/6-scale LM model |
| T5-2 | rate_or_dynamics | text | free drop, VV and VH per drop | vertical and oblique |
| T5-3 | soils | text | RS; SS | RS;SS |
| T5-3 | states | text | loose (Dr 0); intermediate (Dr .3) | loose;intermediate |
| T5-3 | apparatus | text | 1/6-scale LM model; level soil bed | 1/6-scale LM model |
| T5-3 | rate_or_dynamics | text | free drop, 45 deg yaw (2-2 landing) | vertical and oblique |
| T5-3 | relation_target | text | T5-2;T5-2-p309 | T5-2 |
| F3-10 | soils | text | none | n/a |
| F3-10 | apparatus | text | 1/6-scale drag footpad; strut | subscale drag footpad |
| F3-10 | panels | number | 0 | 2 |
| F3-10 | trace_classes | text | setup-evidence | schematic |
| F3-11 | soils | text | none | n/a |
| F3-11 | apparatus | text | subscale drag recording system | subscale drag rig |
| F3-11 | rate_or_dynamics | text | n/a | analog recording |
| F3-11 | panels | number | 0 | 1 |
| F3-11 | trace_classes | text | setup-evidence | schematic |
| F3-12 | soils | text | none | n/a |
| F3-12 | apparatus | text | subscale oblique impact equipment | subscale impact rig |
| F3-12 | rate_or_dynamics | text | n/a | vertical setup |
| F3-13 | soils | text | none | n/a |
| F3-13 | apparatus | text | subscale oblique impact equipment | subscale impact rig |
| F3-13 | rate_or_dynamics | text | n/a | vertical or oblique |
| F3-13 | panels | number | 0 | 3 |
| F3-13 | trace_classes | text | setup-evidence | schematic |
| F3-14 | soils | text | none | n/a |
| F3-14 | apparatus | text | subscale impact 3D load cell | subscale impact load cell |
| F3-14 | panels | number | 0 | 1 |
| F3-14 | trace_classes | text | setup-evidence | schematic |
| F3-15 | soils | text | none | n/a |
| F3-15 | apparatus | text | 1/6-scale impact footpad | subscale impact footpad |
| F3-15 | panels | number | 0 | 2 |
| F3-15 | trace_classes | text | setup-evidence | schematic |
| F3-16 | soils | text | none | n/a |
| F3-16 | rate_or_dynamics | text | static calibration | calibration |
| F3-16 | trace_classes | text | measurement-markers;author-fit | measurement-markers;setup-evidence |
| F3-16 | in_scope | text | maybe | yes |
| F3-17 | soils | text | none | n/a |
| F3-17 | rate_or_dynamics | text | static calibration | calibration |
| F3-17 | trace_classes | text | measurement-markers;author-fit | measurement-markers;setup-evidence |
| F3-17 | in_scope | text | maybe | yes |
| F3-18 | soils | text | none | n/a |
| F3-18 | rate_or_dynamics | text | static calibration | calibration |
| F3-18 | trace_classes | text | measurement-markers;author-fit | measurement-markers;setup-evidence |
| F3-18 | y_unit | text | mu In. In. | μ In. In. |
| F3-18 | in_scope | text | maybe | yes |
| F3-19 | soils | text | none | n/a |
| F3-19 | apparatus | text | subscale impact recording system | subscale impact rig |
| F3-19 | rate_or_dynamics | text | n/a | analog recording |
| F3-19 | panels | number | 0 | 1 |
| F3-19 | trace_classes | text | setup-evidence | schematic |
| F3-20 | soils | text | none | n/a |
| F3-20 | apparatus | text | full-scale oblique impact equipment | full-scale impact rig |
| F3-21 | soils | text | none | n/a |
| F3-21 | apparatus | text | full-scale oblique impact equipment | full-scale impact rig |
| F3-21 | rate_or_dynamics | text | n/a | oblique setup |
| F3-21 | panels | number | 0 | 1 |
| F3-21 | trace_classes | text | setup-evidence | schematic |
| F3-22 | soils | text | none | n/a |
| F3-22 | apparatus | text | full-scale oblique impact structure | full-scale impact rig |
| F3-22 | panels | number | 0 | 1 |
| F3-22 | trace_classes | text | setup-evidence | schematic |
| F3-22 | in_scope | text | no | maybe |
| F3-23 | soils | text | none | n/a |
| F3-23 | apparatus | text | full-scale two-axis load cell; footpad | full-scale impact load cell |
| F3-23 | panels | number | 0 | 1 |
| F3-23 | trace_classes | text | setup-evidence | schematic |
| F3-24 | soils | text | none | n/a |
| F3-24 | apparatus | text | full-scale load cell | full-scale impact load cell |
| F3-24 | rate_or_dynamics | text | static calibration | calibration |
| F3-24 | trace_classes | text | measurement-markers;author-fit | measurement-markers;setup-evidence |
| F3-24 | y_unit | text | 1,000 mu In./In. | 1,000 μIn./In. |
| F3-24 | in_scope | text | maybe | yes |
| F3-25 | soils | text | none | n/a |
| F3-25 | apparatus | text | full-scale load cell | full-scale impact load cell |
| F3-25 | rate_or_dynamics | text | static calibration | calibration |
| F3-25 | trace_classes | text | measurement-markers;author-fit | measurement-markers;setup-evidence |
| F3-25 | y_unit | text | mu In./In. | μIn./In. |
| F3-25 | in_scope | text | maybe | yes |
| F3-26 | soils | text | none | n/a |
| F3-26 | apparatus | text | full-scale simulated LM footpad | full-scale LM footpad |
| F3-26 | panels | number | 0 | 1 |
| F3-26 | trace_classes | text | setup-evidence | schematic |
| F3-26 | in_scope | text | no | maybe |
| F3-26 | priority | number | 2 | 1 |
| F3-27 | soils | text | none | n/a |
| F3-27 | apparatus | text | full-scale impact recording system | full-scale impact rig |
| F3-27 | rate_or_dynamics | text | n/a | analog recording |
| F3-27 | panels | number | 0 | 1 |
| F3-27 | trace_classes | text | setup-evidence | schematic |
| F3-28 | soils | text | none | n/a |
| F3-28 | apparatus | text | full-scale drag facility (design only) | full-scale drag facility |
| F3-28 | panels | number | 0 | 1 |
| F3-28 | trace_classes | text | setup-evidence | schematic |
| F3-29 | soils | text | none | n/a |
| F3-29 | apparatus | text | full-scale drag facility (design only) | full-scale drag facility |
| F3-29 | panels | number | 0 | 1 |
| F3-29 | trace_classes | text | setup-evidence | schematic |
| F3-29 | priority | number | 3 | 2 |
| F3-30 | soils | text | none | n/a |
| F3-30 | apparatus | text | full-scale drag facility (design only) | full-scale drag facility |
| F3-30 | panels | number | 0 | 1 |
| F3-30 | trace_classes | text | setup-evidence | schematic |
| F3-30 | priority | number | 3 | 2 |
| F4-10 | title_as_printed | text | Subscale Drag Test Results - Soil No. 5 - RSMa Loose | Subscale Drag Test Results - Soil No. 5 - RSMₐ Loose |
| F4-10 | states | text | loose (Dr 0) | loose |
| F4-10 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-10 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-11 | states | text | loose (Dr 0) | loose |
| F4-11 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-11 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-12 | states | text | loose (Dr 0) | loose |
| F4-12 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-12 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-13 | states | text | intermediate (Dr 0.53) | intermediate |
| F4-13 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-13 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-14 | states | text | dense (Dr 0.69) | dense |
| F4-14 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-14 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-15 | states | text | intermediate (Dr 0.50) | intermediate |
| F4-15 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-15 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-16 | states | text | dense (Dr 0.81; 0.70) | dense |
| F4-16 | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-16 | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-17 | soils | text | all impact soils | soils 1-11 |
| F4-17 | states | text | n/a | multiple |
| F4-17 | apparatus | text | subscale and full-scale oblique impact equipment | subscale and full-scale impact rigs |
| F4-17 | rate_or_dynamics | text | impact 1 to 15 fps | vertical and oblique |
| F4-17 | priority | number | 2 | 1 |
| F4-18 | soils | text | RS; PS; RSM; RC2; SS; LSM | soils 1-11 |
| F4-18 | states | text | L; I; D | multiple |
| F4-18 | apparatus | text | subscale and full-scale oblique impact equipment | subscale and full-scale impact rigs |
| F4-18 | rate_or_dynamics | text | n/a | program totals |
| F4-18 | curves | number | 2 | 0 |
| F4-18 | trace_classes | text | measurement-markers | setup-evidence |
| F4-18 | x_quantity | text | soil (bars numbered 1 to 11) | soil |
| F4-18 | in_scope | text | maybe | no |
| F4-18 | priority | number | 2 | 3 |
| F4-19 | states | text | Dr 0; 0.45; 0.65 | loose;intermediate;dense |
| F4-19 | apparatus | text | subscale oblique impact equipment; 6.17 inch footpad | subscale impact rig |
| F4-19 | rate_or_dynamics | text | vertical impact about 6 fps (text 4-22) | vertical at about 6 fps |
| F4-19 | y_quantity | text | vertical force (top); displacement (bottom) | vertical force;displacement |
| F4-19 | y_unit | text | Pounds; Inches | Pounds;Inches |
| F4-19 | legend_entries | text | Footpad Diameter = 6.17 Inches;Run No. 4, Dr = 0;Run No. 10, Dr = 0.45;Run No. 12, Dr = 0.65 | Run No. 4 D_r=0;Run No. 10 D_r=0.45;Run No. 12 D_r=0.65 |
| F4-20 | title_as_printed | text | Force versus Displacement for Vertical Impact Tests on Various RS Soils | Force versus Displacement for Vertical Impact Tests on Various RS Soils Footpad Diameter = 6.17 Inches |
| F4-20 | states | text | Dr 0; 0.45; 0.65 | loose;intermediate;dense |
| F4-20 | apparatus | text | subscale oblique impact equipment; 6.17 inch footpad | subscale impact rig |
| F4-20 | rate_or_dynamics | text | vertical impact about 6 fps (text 4-22) | vertical at about 6 fps |
| F4-20 | legend_entries | text | Footpad Diameter = 6.17 Inches;Run No. 4, Dr = 0;Run No. 10, Dr = 0.45;Run No. 12, Dr = 0.65 | Run No. 4 D_r=0;Run No. 10 D_r=0.45;Run No. 12 D_r=0.65 |
| F4-20 | priority | number | 2 | 1 |
| F4-21 | title_as_printed | text | Force versus Displacement for Vertical Impact Tests on RS Loose Soil Using Various Weight Impacting Bodies (M1) | Force versus Displacement for Vertical Impact Tests on RS Loose Soil Using Various Weight Impacting Bodies (M₁) |
| F4-21 | states | text | loose (Relative Density = 0) | loose |
| F4-21 | apparatus | text | subscale oblique impact equipment; 6.17 inch footpad | subscale impact rig |
| F4-21 | rate_or_dynamics | text | vertical impact about 6 fps (text 4-22) | vertical at about 6 fps |
| F4-21 | legend_entries | text | Footpad Diameter = 6.17 Inches;Relative Density = 0;Run No. 4, M1 = 31 lbs.;Run No. 15, M1 = 41 lbs.;Run No. 16, M1 = 51 lbs. | Run No. 4 M₁=31 lbs.;Run No. 15 M₁=41 lbs.;Run No. 16 M₁=51 lbs. |
| F4-22 | soils | text | RS (text 4-22) | RS |
| F4-22 | states | text | loose (text 4-22) | loose |
| F4-22 | apparatus | text | full-scale oblique impact equipment, 37 inch pad (top); subscale, 6.17 inch pad (bottom) | subscale and full-scale impact rigs |
| F4-22 | rate_or_dynamics | text | vertical impact about 6 fps (text 4-22) | vertical at about 6 fps |
| F4-22 | legend_entries | text | Full Scale Oblique Impact Test No. 16, M1 = 1140 lbs.;Subscale Oblique Impact Test Nc. II-1, M1 = 31 lbs. | Full Scale Test No. 16 M₁=1140 lbs.;Subscale Test No. II-1 M₁=31 lbs. |
| F4-22 | relation | text | unresolved | none |
| F4-22 | relation_target | text | F4-21 |  |
| F4-6a | states | text | loose (Dr 0) | loose |
| F4-6a | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-6a | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-6a | relation | text | unresolved | none |
| F4-6a | relation_target | text | F2-60 |  |
| F4-6b | states | text | loose (Dr 0) | loose |
| F4-6b | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-6b | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-6b | mcc_relevant | text | maybe | no |
| F4-6b | relation | text | unresolved | none |
| F4-6b | relation_target | text | F2-60 |  |
| F4-6c | states | text | loose (Dr 0) | loose |
| F4-6c | apparatus | text | subscale drag equipment; 1/6-scale LM footpad (D per run) | subscale drag rig |
| F4-6c | rate_or_dynamics | text | constant-penetration drag at constant VH per run | constant penetration |
| F4-6c | mcc_relevant | text | maybe | no |
| F4-6c | relation | text | unresolved | none |
| F4-6c | relation_target | text | F2-60 |  |
| F5-10 | soils | text | none | n/a |
| F5-10 | apparatus | text | 1/6-scale LM model shock struts | 1/6-scale LM struts |
| F5-10 | rate_or_dynamics | text | n/a | stroke and crush |
| F5-10 | data_form | text | curve | mixed |
| F5-10 | trace_classes | text | setup-evidence | schematic |
| F5-10 | in_scope | text | yes | maybe |
| F5-10 | priority | number | 1 | 2 |
| F5-11 | soils | text | none | n/a |
| F5-11 | apparatus | text | 1/6-scale LM model; drop rig | 1/6-scale LM model |
| F5-11 | panels | number | 0 | 1 |
| F5-11 | trace_classes | text | setup-evidence | schematic |
| F5-12 | soils | text | none | n/a |
| F5-12 | apparatus | text | six degree of freedom drop rig; soil bed | 6-DOF drop rig |
| F5-12 | rate_or_dynamics | text | n/a | launch |
| F5-12 | panels | number | 0 | 1 |
| F5-12 | trace_classes | text | setup-evidence | schematic |
| F5-13 | soils | text | none | n/a |
| F5-13 | apparatus | text | six degree of freedom drop rig | 6-DOF drop rig |
| F5-13 | rate_or_dynamics | text | n/a | launch |
| F5-14 | soils | text | none | n/a |
| F5-14 | apparatus | text | model drop recording system | 1/6-scale LM model |
| F5-14 | rate_or_dynamics | text | n/a | analog recording |
| F5-14 | panels | number | 0 | 1 |
| F5-14 | trace_classes | text | setup-evidence | schematic |
| F5-15 | soils | text | none | n/a |
| F5-15 | apparatus | text | model drop recording system | LM drop recording system |
| F5-15 | rate_or_dynamics | text | n/a | analog playback |
| F5-15 | panels | number | 0 | 1 |
| F5-15 | trace_classes | text | setup-evidence | schematic |
| F5-16 | soils | text | none | n/a |
| F5-16 | states | text | n/a | rigid |
| F5-16 | apparatus | text | spiked footpad (rigid surface drops) | 1/6-scale LM spiked footpad |
| F5-16 | panels | number | 0 | 1 |
| F5-16 | trace_classes | text | setup-evidence | schematic |
| F5-17 | soils | text | none | n/a |
| F5-17 | states | text | n/a | rigid |
| F5-17 | apparatus | text | spiked footpad | 1/6-scale LM spiked footpad |
| F5-18 | soils | text | none | plywood blocks |
| F5-18 | states | text | n/a | rigid |
| F5-18 | apparatus | text | rigid surface bed (plywood on tables, slope 10 deg) | 6-DOF drop rig |
| F5-19 | soils | text | none | plywood blocks |
| F5-19 | states | text | n/a | rigid |
| F5-19 | apparatus | text | 1/6-scale LM model; rigid surface | 1/6-scale LM with spiked pads |
| F5-19 | rate_or_dynamics | text | n/a | oblique |
| F5-19 | relation | text | none | same-as |
| F5-19 | relation_target | text |  | T5-2 |
| F5-20 | soils | text | none (rigid surface) | plywood blocks |
| F5-20 | states | text | n/a | rigid |
| F5-20 | apparatus | text | 1/6-scale LM model with spiked footpads; plywood surface | 1/6-scale LM with spiked pads |
| F5-20 | rate_or_dynamics | text | free drop, 22 1/2 deg yaw, slope 10 deg | oblique |
| F5-20 | curves | number | 4 | 1 |
| F5-20 | legend_entries | text | Stable;Unstable;Stable but close to Unbalance;22 1/2 deg Yaw;Group Slope = 10 deg;Level Vehicle at Impact | Stable;Unstable;Stable but close to Unbalance |
| F5-20 | relation_target | text | T5-2-p310;T5-2-p311 | T5-2 |
| F5-21 | soils | text | none | n/a |
| F5-21 | apparatus | text | model drop data reduction program | LM drop data reduction |
| F5-21 | rate_or_dynamics | text | n/a | 1 ms reduced time step |
| F5-21 | panels | number | 0 | 1 |
| F5-21 | trace_classes | text | setup-evidence | schematic |
| F5-22 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-22 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-22 | rate_or_dynamics | text | VV -114.9 in/s, VH 0 (T5-3) | vertical |
| F5-22 | y_quantity | text | Absolute Footpad Velocity (VAP) | absolute footpad velocity VAP |
| F5-22 | relation | text | none | same-as |
| F5-22 | relation_target | text |  | T5-3 |
| F5-23 | title_as_printed | text | Footpad Heading With Respect to Vertical (theta) versus Time (NASA Test No. 1) | Footpad Heading With Respect to Vertical (θ) versus Time (NASA Test No. 1) |
| F5-23 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-23 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-23 | rate_or_dynamics | text | VV -114.9 in/s, VH 0 (T5-3) | vertical |
| F5-23 | y_quantity | text | Footpad Heading theta | footpad heading θ |
| F5-23 | relation | text | none | same-as |
| F5-23 | relation_target | text |  | T5-3 |
| F5-24 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-24 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-24 | rate_or_dynamics | text | VV -114.9 in/s, VH 0 (T5-3) | vertical |
| F5-24 | relation | text | none | same-as |
| F5-24 | relation_target | text |  | T5-3 |
| F5-25 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-25 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-25 | rate_or_dynamics | text | VV -114.9 in/s, VH 0 (T5-3) | vertical |
| F5-25 | data_form | text | curve | mixed |
| F5-25 | y_quantity | text | (Tension) Load on Strut No. 3; (Tension) Load on Strut No. 2; (Compression) Load on Strut No. 1 | strut axial load |
| F5-25 | legend_entries | text | n/a | Strut No. 3;Strut No. 2;Strut No. 1 |
| F5-25 | relation | text | none | same-as |
| F5-25 | relation_target | text |  | T5-3 |
| F5-26 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-26 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-26 | rate_or_dynamics | text | VV -114.9 in/s, VH 0 (T5-3) | vertical |
| F5-26 | y_quantity | text | Vertical Acceleration | CG vertical acceleration |
| F5-26 | y_unit | text | In./Sec.^2 (Inch/Second^2) | Inch/Second² |
| F5-26 | relation | text | none | same-as |
| F5-26 | relation_target | text |  | T5-3 |
| F5-27 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-27 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-27 | rate_or_dynamics | text | VV -114.9 in/s, VH 0 (T5-3) | vertical |
| F5-27 | y_quantity | text | Vertical Velocity | CG vertical velocity |
| F5-27 | relation | text | none | same-as |
| F5-27 | relation_target | text |  | T5-3 |
| F5-28 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-28 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-28 | rate_or_dynamics | text | VV -114.9 in/s, VH 0 (T5-3) | vertical |
| F5-28 | y_quantity | text | Vertical Displacement | CG vertical displacement |
| F5-28 | relation | text | none | same-as |
| F5-28 | relation_target | text |  | T5-3 |
| F5-29 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-29 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-29 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-29 | relation | text | none | same-as |
| F5-29 | relation_target | text |  | T5-3 |
| F5-30 | title_as_printed | text | Footpad Heading With Respect to Vertical (theta) versus Time (NASA Test No. 2) | Footpad Heading With Respect to Vertical (θ) versus Time (NASA Test No. 2) |
| F5-30 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-30 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-30 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-30 | y_quantity | text | Footpad Heading (theta) | footpad heading θ |
| F5-30 | relation | text | none | same-as |
| F5-30 | relation_target | text |  | T5-3 |
| F5-31 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-31 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-31 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-31 | relation | text | none | same-as |
| F5-31 | relation_target | text |  | T5-3 |
| F5-32 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-32 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-32 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-32 | data_form | text | curve | mixed |
| F5-32 | y_quantity | text | (Compression) Load on Strut No. 3; (Tension) Load on Strut No. 2; (Compression) Load on Strut No. 1 | strut axial load |
| F5-32 | y_unit | text | (lbs.) | lbs. |
| F5-32 | legend_entries | text | n/a | Strut No. 3;Strut No. 2;Strut No. 1 |
| F5-32 | relation | text | none | same-as |
| F5-32 | relation_target | text |  | T5-3 |
| F5-33 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-33 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-33 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-33 | x_unit | text | (Sec.) | Sec. |
| F5-33 | y_quantity | text | C.G. Vertical Acceleration | CG vertical acceleration |
| F5-33 | y_unit | text | Inch/Second^2 | Inch/Second² |
| F5-33 | relation | text | none | same-as |
| F5-33 | relation_target | text |  | T5-3 |
| F5-34 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-34 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-34 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-34 | y_quantity | text | C.G. Vertical Velocity | CG vertical velocity |
| F5-34 | relation | text | none | same-as |
| F5-34 | relation_target | text |  | T5-3 |
| F5-35 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-35 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-35 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-35 | y_quantity | text | C.G. Vertical Displacement | CG vertical displacement |
| F5-35 | relation | text | none | same-as |
| F5-35 | relation_target | text |  | T5-3 |
| F5-36 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-36 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-36 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-36 | y_quantity | text | C.G. Horizontal Velocity | CG horizontal velocity |
| F5-36 | relation | text | none | same-as |
| F5-36 | relation_target | text |  | T5-3 |
| F5-37 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-37 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-37 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-37 | y_quantity | text | C.G. Horizontal Displacement | CG horizontal displacement |
| F5-37 | relation | text | none | same-as |
| F5-37 | relation_target | text |  | T5-3 |
| F5-38 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-38 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-38 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-38 | relation | text | none | same-as |
| F5-38 | relation_target | text |  | T5-3 |
| F5-39 | states | text | loose (Dr 0, 46.9 pcf) | loose |
| F5-39 | apparatus | text | 1/6-scale LM model; leg set 1 instrumented | 1/6-scale LM model |
| F5-39 | rate_or_dynamics | text | VV -60.5 in/s, VH 83.5 in/s (T5-3) | oblique |
| F5-39 | relation | text | none | same-as |
| F5-39 | relation_target | text |  | T5-3 |
| T-p302 | title_as_printed | text | (unnumbered) summary of the important physical quantities of the LM model |  |
| T-p302 | test_type | text | apparatus | model drop |
| T-p302 | soils | text | none | n/a |
| F5-2-p285 | <row> | missing | absent | present |
| T5-2-p309 | soils | text | RS; SS | RS;SS |
| T5-2-p309 | states | text | intermediate; loose; dense | loose;intermediate;dense |
| T5-2-p309 | apparatus | text | 1/6-scale LM model; six degree of freedom drop rig | 1/6-scale LM model |
| T5-2-p309 | rate_or_dynamics | text | free drop, VV and VH per drop | vertical and oblique |
| T5-2-p310 | soils | text | RS; plywood blocks | RS;plywood blocks |
| T5-2-p310 | states | text | dense; rigid | dense;rigid |
| T5-2-p310 | apparatus | text | 1/6-scale LM model; six degree of freedom drop rig | 1/6-scale LM model |
| T5-2-p310 | rate_or_dynamics | text | free drop, VV and VH per drop | oblique and vertical |
| T5-2-p311 | soils | text | plywood blocks; RSM | plywood blocks;RSM |
| T5-2-p311 | states | text | rigid; rolled; not rolled | rigid;rolled;unrolled |
| T5-2-p311 | apparatus | text | 1/6-scale LM model; six degree of freedom drop rig | 1/6-scale LM model |
| T5-2-p311 | rate_or_dynamics | text | free drop, VV and VH per drop | oblique and vertical |
| T5-2-p312 | apparatus | text | 1/6-scale LM model; six degree of freedom drop rig | 1/6-scale LM model |
| T5-2-p312 | rate_or_dynamics | text | free drop, VV and VH per drop | oblique |
