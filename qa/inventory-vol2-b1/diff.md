# Table diff: claude vs codex

Files: `<local path>` (claude), `extractions/codex/inventory-vol2-b1/inventory.csv` (codex). Key: `id`.

Rows: 112 in claude, 122 in codex. Compared columns: 28.
Cells compared: 3136. Agreed: 2254 (71.9 percent).
Disagreements: 892 (70 numeric, 812 text, 10 missing rows).

| key | column | kind | claude | codex |
|---|---|---|---|---|
| FA-1 | states | text | n/a | soil 1 loose |
| FA-1 | apparatus | text | none | microscope |
| FA-1 | panels | number | 1 | 0 |
| FA-1 | legend_entries | text | scale graduated in 1/32 inch increments | none |
| FA-2 | states | text | unused | soil 1 loose |
| FA-2 | apparatus | text | sieve analysis | sieves |
| FA-2 | data_form | text | curve | mixed |
| FA-2 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-2 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-2 | legend_entries | text | average;range (two dashed);inset table D50 D10 Cu D95 | Average;Range |
| FA-2 | relation | text | derived-from | none |
| FA-2 | relation_target | text | F2-14 |  |
| FA-3 | states | text | loose to dense | soil 1 loose |
| FA-3 | apparatus | text | Burmister min-max density | none |
| FA-3 | trace_classes | text | author-fit | computed |
| FA-3 | x_quantity | text | relative density | Relative Density Dr |
| FA-3 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-3 | legend_entries | text | average (solid);95 percent confidence limits (dashed) | mean;95% confidence limits |
| FA-3 | mcc_relevant | text | yes | no |
| FA-3 | relation | text | reproduces | none |
| FA-3 | relation_target | text | F2-17 |  |
| FA-4 | states | text | loose to dense | soil 1 loose |
| FA-4 | apparatus | text | direct shear | shear box |
| FA-4 | rate_or_dynamics | text | n/a | static |
| FA-4 | x_quantity | text | relative density | Relative Density Dr |
| FA-4 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-4 | legend_entries | text | n/a | none |
| FA-4 | priority | number | 2 | 1 |
| FA-4 | relation | text | derived-from | none |
| FA-4 | relation_target | text | FC-16 |  |
| FA-5 | states | text | n/a | soil 2 loose |
| FA-5 | apparatus | text | none | microscope |
| FA-5 | panels | number | 1 | 0 |
| FA-5 | legend_entries | text | scale 1/32 inch | none |
| FA-6 | states | text | unused | soil 2 loose |
| FA-6 | apparatus | text | sieve analysis | sieves |
| FA-6 | data_form | text | curve | mixed |
| FA-6 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-6 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-6 | legend_entries | text | average;range;inset table | Average;Range |
| FA-6 | relation | text | derived-from | none |
| FA-6 | relation_target | text | F2-14 |  |
| FA-7 | states | text | loose to dense | soil 2 loose |
| FA-7 | apparatus | text | Burmister min-max density | none |
| FA-7 | trace_classes | text | author-fit | computed |
| FA-7 | x_quantity | text | relative density | Relative Density Dr |
| FA-7 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-7 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-7 | mcc_relevant | text | yes | no |
| FA-7 | relation | text | reproduces | none |
| FA-7 | relation_target | text | F2-17 |  |
| FA-8 | states | text | loose to dense | soil 2 loose |
| FA-8 | apparatus | text | direct shear | shear box |
| FA-8 | rate_or_dynamics | text | n/a | static |
| FA-8 | x_quantity | text | relative density | Relative Density Dr |
| FA-8 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-8 | legend_entries | text | n/a | none |
| FA-8 | priority | number | 2 | 1 |
| FA-8 | relation | text | derived-from | none |
| FA-8 | relation_target | text | FC-17 |  |
| FA-9 | states | text | n/a | soil 3 intermediate |
| FA-9 | apparatus | text | none | microscope |
| FA-9 | panels | number | 1 | 0 |
| FA-9 | legend_entries | text | scale 1/32 inch | none |
| FB-1 | title_as_printed | text | Fig. 1 Apparatus for Measurement of Stress Wave Velocity | APPARATUS FOR MEASUREMENT OF STRESS WAVE VELOCITY |
| FB-1 | printed_page | number | 4 (IITRI) | 4 |
| FB-1 | test_type | text | apparatus | sonic |
| FB-1 | soils | text | all | none |
| FB-1 | apparatus | text | shock tube stress wave apparatus | shock tube;confined specimen;stress gages |
| FB-1 | rate_or_dynamics | text | n/a | stress wave |
| FB-1 | panels | number | 1 | 0 |
| FB-1 | legend_entries | text | n/a | none |
| FB-1 | priority | number | 3 | 2 |
| FB-2 | title_as_printed | text | Fig. 2 Stress Gage at Forward End of Specimen | STRESS GAGE AT FORWARD END OF SPECIMEN |
| FB-2 | printed_page | text | 5 (IITRI) | unknown |
| FB-2 | test_type | text | apparatus | sonic |
| FB-2 | soils | text | all | none |
| FB-2 | apparatus | text | piezoelectric stress gage on triaxial specimen | shock tube;confined specimen;stress gages |
| FB-2 | rate_or_dynamics | text | n/a | stress wave |
| FB-2 | panels | number | 1 | 0 |
| FB-2 | legend_entries | text | n/a | none |
| FB-2 | priority | number | 3 | 2 |
| FB-3 | title_as_printed | text | Fig. 3 E Versus sigma3 for RS Soil | E VERSUS sigma3 FOR RS SOIL |
| FB-3 | printed_page | number | 6 (IITRI) | 6 |
| FB-3 | states | text | Dr 0.99 (dense);Dr 0.30 (loose) | dense Dr=0.99;loose Dr=0.30 |
| FB-3 | apparatus | text | stress wave velocity in triaxial specimen under partial vacuum confinement | shock tube;confined specimen;stress gages |
| FB-3 | rate_or_dynamics | text | shock tube pulse under 2 psi | stress wave |
| FB-3 | trace_classes | text | measurement-markers | measurement-markers;author-fit |
| FB-3 | legend_entries | text | Dense Dr = 0.99;Loose Dr = 0.30 | dense Dr=0.99;loose Dr=0.30 |
| FB-3 | priority | number | 1 | 2 |
| FB-3 | relation | text | derived-from | none |
| FB-3 | relation_target | text | T2-3 |  |
| FB-4 | title_as_printed | text | Fig. 4 E Versus sigma3 for PS Soil | E VERSUS sigma3 FOR PS SOIL |
| FB-4 | printed_page | number | 7 (IITRI) | 7 |
| FB-4 | states | text | Dr 0.86 (dense);Dr 0.22 (loose) | dense Dr=0.86;loose Dr=0.22 |
| FB-4 | apparatus | text | stress wave velocity | shock tube;confined specimen;stress gages |
| FB-4 | rate_or_dynamics | text | shock tube pulse | stress wave |
| FB-4 | trace_classes | text | measurement-markers | measurement-markers;author-fit |
| FB-4 | y_quantity | text | modulus E = rho c^2 | Dynamic Modulus E = rho c^2 |
| FB-4 | legend_entries | text | Dense Dr = 0.86;Loose Dr = 0.22 | dense Dr=0.86;loose Dr=0.22 |
| FB-4 | priority | number | 1 | 2 |
| FB-4 | relation | text | derived-from | none |
| FB-4 | relation_target | text | T2-3 |  |
| FB-5 | title_as_printed | text | Fig. 5 E Versus sigma3 for SS Soil | E VERSUS sigma3 FOR SS SOIL |
| FB-5 | printed_page | number | 8 (IITRI) | 8 |
| FB-5 | states | text | Dr 0.84 (dense);Dr 0.26 (loose) | dense Dr=0.84;loose Dr=0.26 |
| FB-5 | apparatus | text | stress wave velocity | shock tube;confined specimen;stress gages |
| FB-5 | rate_or_dynamics | text | shock tube pulse | stress wave |
| FB-5 | trace_classes | text | measurement-markers | measurement-markers;author-fit |
| FB-5 | y_quantity | text | modulus E = rho c^2 | Dynamic Modulus E = rho c^2 |
| FB-5 | legend_entries | text | Dense Dr = 0.84;Loose Dr = 0.26 | dense Dr=0.84;loose Dr=0.26 |
| FB-5 | priority | number | 1 | 2 |
| FB-5 | relation | text | derived-from | none |
| FB-5 | relation_target | text | T2-3 |  |
| FB-6 | title_as_printed | text | Fig. 6 E Versus sigma3 for RC Soil | E VERSUS sigma3 FOR RC SOIL |
| FB-6 | printed_page | number | 9 (IITRI) | 9 |
| FB-6 | soils | text | RC2 | RC |
| FB-6 | states | text | Dr 0.82 (dense);Dr 0.02 (loose) | dense Dr=0.82;loose Dr=0.02 |
| FB-6 | apparatus | text | stress wave velocity | shock tube;confined specimen;stress gages |
| FB-6 | rate_or_dynamics | text | shock tube pulse | stress wave |
| FB-6 | trace_classes | text | measurement-markers | measurement-markers;author-fit |
| FB-6 | y_quantity | text | modulus E = rho c^2 | Dynamic Modulus E = rho c^2 |
| FB-6 | legend_entries | text | Dense Dr = 0.82;Loose Dr = 0.02 | dense Dr=0.82;loose Dr=0.02 |
| FB-6 | priority | number | 1 | 2 |
| FB-6 | relation | text | derived-from | none |
| FB-6 | relation_target | text | T2-3 |  |
| FB-7 | title_as_printed | text | Fig. 7 E Versus sigma3 for LSM Soil | E VERSUS sigma3 FOR LSM SOIL |
| FB-7 | printed_page | text | 10 (IITRI) | ii |
| FB-7 | states | text | Dr 1.04;Dr 0.995;Dr 0.77 | Dr=1.04;Dr=0.995;Dr=0.77 |
| FB-7 | apparatus | text | stress wave velocity | shock tube;confined specimen;stress gages |
| FB-7 | rate_or_dynamics | text | shock tube pulse | stress wave |
| FB-7 | trace_classes | text | measurement-markers | measurement-markers;author-fit |
| FB-7 | y_quantity | text | modulus E = rho c^2 | Dynamic Modulus E = rho c^2 |
| FB-7 | legend_entries | text | Dr = 1.04 (squares);Dr = 0.995 (open circles);Dr = 0.77 (filled circles) | Dr=1.04;Dr=0.995;Dr=0.77 |
| FB-7 | priority | number | 1 | 2 |
| FB-7 | relation | text | derived-from | none |
| FB-7 | relation_target | text | T2-3 |  |
| FB-8 | title_as_printed | text | Fig. 8 Dependency of f(nu) on nu (E = rho c^2 f(nu)) | DEPENDENCY OF f(nu) ON nu (E = rho c^2 f(nu)) |
| FB-8 | printed_page | text | 11 (IITRI) | ii |
| FB-8 | soils | text | all | none |
| FB-8 | x_quantity | text | Poisson ratio | Poisson's Ratio nu |
| FB-8 | legend_entries | text | n/a | none |
| FB-8 | in_scope | text | no | yes |
| FB-8 | priority | number | 3 | 2 |
| FC-8 | states | text | loose (avg density 40.40) | Loose |
| FC-8 | apparatus | text | direct shear; Univac 1107 CAL-COMP plot | shear box;UNIVAC 1107;CALCOMP |
| FC-8 | rate_or_dynamics | text | quasi-static | not stated |
| FC-8 | data_form | text | curve | mixed |
| FC-8 | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-8 | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-8 | legend_entries | text | Avg. Density 40.40;Angle of Friction 38.63;Tan Theta .7992;Cohesion 242.12 | triangle markers;linear fit |
| FA-10 | states | text | unused | soil 3 intermediate |
| FA-10 | apparatus | text | sieve analysis | sieves |
| FA-10 | data_form | text | curve | mixed |
| FA-10 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-10 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-10 | legend_entries | text | average;range;inset table | Average;Range |
| FA-10 | in_scope | text | no | yes |
| FA-10 | priority | number | 2 | 1 |
| FA-11 | states | text | loose to dense | soil 3 intermediate |
| FA-11 | apparatus | text | Burmister min-max density | none |
| FA-11 | trace_classes | text | author-fit | computed |
| FA-11 | x_quantity | text | relative density | Relative Density Dr |
| FA-11 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-11 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-11 | in_scope | text | no | yes |
| FA-11 | priority | number | 2 | 1 |
| FA-12 | states | text | loose to dense | soil 3 intermediate |
| FA-12 | apparatus | text | direct shear | shear box |
| FA-12 | rate_or_dynamics | text | n/a | static |
| FA-12 | x_quantity | text | relative density | Relative Density Dr |
| FA-12 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-12 | legend_entries | text | n/a | none |
| FA-12 | in_scope | text | no | yes |
| FA-12 | priority | number | 3 | 1 |
| FA-13 | states | text | n/a | soil 4 dense |
| FA-13 | apparatus | text | none | microscope |
| FA-13 | panels | number | 1 | 0 |
| FA-13 | legend_entries | text | scale 1/32 inch | none |
| FA-14 | states | text | unused | soil 4 dense |
| FA-14 | apparatus | text | sieve analysis | sieves |
| FA-14 | data_form | text | curve | mixed |
| FA-14 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-14 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-14 | legend_entries | text | average;range;inset table | Average;Range |
| FA-14 | in_scope | text | no | yes |
| FA-14 | priority | number | 2 | 1 |
| FA-15 | states | text | loose to dense | soil 4 dense |
| FA-15 | apparatus | text | Burmister min-max density | none |
| FA-15 | trace_classes | text | author-fit | computed |
| FA-15 | x_quantity | text | relative density | Relative Density Dr |
| FA-15 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-15 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-15 | in_scope | text | no | yes |
| FA-15 | priority | number | 2 | 1 |
| FA-16 | states | text | loose to dense | soil 4 dense |
| FA-16 | apparatus | text | direct shear | shear box |
| FA-16 | rate_or_dynamics | text | n/a | static |
| FA-16 | x_quantity | text | relative density | Relative Density Dr |
| FA-16 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-16 | legend_entries | text | n/a | none |
| FA-16 | in_scope | text | no | yes |
| FA-16 | priority | number | 3 | 1 |
| FA-17 | states | text | n/a | soil 5 loose |
| FA-17 | apparatus | text | none | microscope |
| FA-17 | panels | number | 1 | 0 |
| FA-17 | legend_entries | text | scale 1/32 inch | none |
| FA-18 | states | text | unused | soil 5 loose |
| FA-18 | apparatus | text | sieve analysis | sieves |
| FA-18 | data_form | text | curve | mixed |
| FA-18 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-18 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-18 | legend_entries | text | average;range;inset table | Average;Range |
| FA-18 | relation | text | derived-from | none |
| FA-18 | relation_target | text | F2-14 |  |
| FA-19 | states | text | loose to dense | soil 5 loose |
| FA-19 | apparatus | text | Burmister min-max density | none |
| FA-19 | trace_classes | text | author-fit | computed |
| FA-19 | x_quantity | text | relative density | Relative Density Dr |
| FA-19 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-19 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-19 | mcc_relevant | text | yes | no |
| FA-19 | relation | text | reproduces | none |
| FA-19 | relation_target | text | F2-17 |  |
| FA-20 | states | text | loose to dense | soil 5 loose |
| FA-20 | apparatus | text | direct shear | shear box |
| FA-20 | rate_or_dynamics | text | n/a | static |
| FA-20 | x_quantity | text | relative density | Relative Density Dr |
| FA-20 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-20 | legend_entries | text | n/a | none |
| FA-20 | priority | number | 2 | 1 |
| FA-20 | relation | text | derived-from | none |
| FA-20 | relation_target | text | FC-18 |  |
| FA-21 | states | text | n/a | soil 6 loose |
| FA-21 | apparatus | text | none | microscope |
| FA-21 | panels | number | 1 | 0 |
| FA-21 | legend_entries | text | scale 1/32 inch | none |
| FA-22 | states | text | used and unused combined | soil 6 loose |
| FA-22 | apparatus | text | sieve analysis | sieves |
| FA-22 | data_form | text | curve | mixed |
| FA-22 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-22 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-22 | legend_entries | text | average;range;inset table | Average;Range |
| FA-22 | relation | text | derived-from | none |
| FA-22 | relation_target | text | F2-14 |  |
| FA-23 | states | text | loose to dense | soil 6 loose |
| FA-23 | apparatus | text | Burmister min-max density | none |
| FA-23 | trace_classes | text | author-fit | computed |
| FA-23 | x_quantity | text | relative density | Relative Density Dr |
| FA-23 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-23 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-23 | mcc_relevant | text | yes | no |
| FA-23 | relation | text | reproduces | none |
| FA-23 | relation_target | text | F2-17 |  |
| FA-24 | states | text | loose to dense | soil 6 loose |
| FA-24 | apparatus | text | direct shear | shear box |
| FA-24 | rate_or_dynamics | text | n/a | static |
| FA-24 | x_quantity | text | relative density | Relative Density Dr |
| FA-24 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-24 | legend_entries | text | n/a | none |
| FA-24 | priority | number | 2 | 1 |
| FA-24 | relation | text | derived-from | none |
| FA-24 | relation_target | text | FC-19 |  |
| FA-25 | states | text | n/a | soil 7 loose |
| FA-25 | apparatus | text | none | microscope |
| FA-25 | panels | number | 1 | 0 |
| FA-25 | legend_entries | text | scale 1/32 inch | none |
| FA-26 | states | text | n/a | soil 7 loose |
| FA-26 | apparatus | text | sieve analysis | sieves |
| FA-26 | data_form | text | curve | mixed |
| FA-26 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-26 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-26 | legend_entries | text | average;range;inset table | Average;Range |
| FA-26 | relation | text | derived-from | none |
| FA-26 | relation_target | text | F2-14 |  |
| FA-27 | states | text | loose to dense | soil 7 loose |
| FA-27 | apparatus | text | Burmister min-max density | none |
| FA-27 | trace_classes | text | author-fit | computed |
| FA-27 | x_quantity | text | relative density | Relative Density Dr |
| FA-27 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-27 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-27 | mcc_relevant | text | yes | no |
| FA-27 | relation | text | reproduces | none |
| FA-27 | relation_target | text | F2-17 |  |
| FA-28 | states | text | loose to dense | soil 7 loose |
| FA-28 | apparatus | text | direct shear | shear box |
| FA-28 | rate_or_dynamics | text | n/a | static |
| FA-28 | x_quantity | text | relative density | Relative Density Dr |
| FA-28 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-28 | legend_entries | text | n/a | none |
| FA-28 | priority | number | 2 | 1 |
| FA-28 | relation | text | derived-from | none |
| FA-28 | relation_target | text | FC-20 |  |
| FA-29 | states | text | n/a | soil 8 intermediate |
| FA-29 | apparatus | text | none | microscope |
| FA-29 | panels | number | 1 | 0 |
| FA-29 | legend_entries | text | scale 1/32 inch | none |
| FA-30 | states | text | n/a | soil 8 intermediate |
| FA-30 | apparatus | text | sieve analysis | sieves |
| FA-30 | data_form | text | curve | mixed |
| FA-30 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-30 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-30 | legend_entries | text | average;range;inset table | Average;Range |
| FA-30 | in_scope | text | no | yes |
| FA-30 | priority | number | 2 | 1 |
| FA-31 | states | text | loose to dense | soil 8 intermediate |
| FA-31 | apparatus | text | Burmister min-max density | none |
| FA-31 | trace_classes | text | author-fit | computed |
| FA-31 | x_quantity | text | relative density | Relative Density Dr |
| FA-31 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-31 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-31 | in_scope | text | no | yes |
| FA-31 | priority | number | 2 | 1 |
| FA-32 | states | text | loose to dense | soil 8 intermediate |
| FA-32 | apparatus | text | direct shear | shear box |
| FA-32 | rate_or_dynamics | text | n/a | static |
| FA-32 | x_quantity | text | relative density | Relative Density Dr |
| FA-32 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-32 | legend_entries | text | n/a | none |
| FA-32 | in_scope | text | no | yes |
| FA-32 | priority | number | 3 | 1 |
| FA-33 | states | text | n/a | soil 9 dense |
| FA-33 | apparatus | text | none | microscope |
| FA-33 | panels | number | 1 | 0 |
| FA-33 | legend_entries | text | scale 1/32 inch | none |
| FA-34 | states | text | n/a | soil 9 dense |
| FA-34 | apparatus | text | sieve analysis | sieves |
| FA-34 | data_form | text | curve | mixed |
| FA-34 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-34 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-34 | legend_entries | text | average;range;inset table | Average;Range |
| FA-34 | in_scope | text | no | yes |
| FA-34 | priority | number | 2 | 1 |
| FA-35 | states | text | loose to dense | soil 9 dense |
| FA-35 | apparatus | text | Burmister min-max density | none |
| FA-35 | trace_classes | text | author-fit | computed |
| FA-35 | x_quantity | text | relative density | Relative Density Dr |
| FA-35 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-35 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-35 | in_scope | text | no | yes |
| FA-35 | priority | number | 2 | 1 |
| FA-36 | states | text | loose to dense | soil 9 dense |
| FA-36 | apparatus | text | direct shear | shear box |
| FA-36 | rate_or_dynamics | text | n/a | static |
| FA-36 | x_quantity | text | relative density | Relative Density Dr |
| FA-36 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-36 | legend_entries | text | n/a | none |
| FA-36 | in_scope | text | no | yes |
| FA-36 | priority | number | 3 | 1 |
| FA-37 | states | text | n/a | soil 10 intermediate |
| FA-37 | apparatus | text | none | microscope |
| FA-37 | panels | number | 1 | 0 |
| FA-37 | legend_entries | text | scale 1/32 inch | none |
| FA-38 | states | text | n/a | soil 10 intermediate |
| FA-38 | apparatus | text | sieve analysis | sieves |
| FA-38 | data_form | text | curve | mixed |
| FA-38 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-38 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-38 | legend_entries | text | average;range;inset table | Average;Range |
| FA-38 | relation | text | derived-from | none |
| FA-38 | relation_target | text | F2-14 |  |
| FA-39 | states | text | loose to dense | soil 10 intermediate |
| FA-39 | apparatus | text | Burmister min-max density | none |
| FA-39 | trace_classes | text | author-fit | computed |
| FA-39 | x_quantity | text | relative density | Relative Density Dr |
| FA-39 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-39 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-39 | mcc_relevant | text | yes | no |
| FA-39 | relation | text | reproduces | none |
| FA-39 | relation_target | text | F2-17 |  |
| FA-40 | states | text | Dr .40 to 1.00 | soil 10 intermediate |
| FA-40 | apparatus | text | direct shear | shear box |
| FA-40 | rate_or_dynamics | text | n/a | static |
| FA-40 | x_quantity | text | relative density | Relative Density Dr |
| FA-40 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-40 | legend_entries | text | cross-hatched band 40 to 45 degrees | none |
| FA-40 | priority | number | 2 | 1 |
| FA-40 | mcc_relevant | text | yes | no |
| FA-40 | relation | text | reproduces | none |
| FA-40 | relation_target | text | FC-21 |  |
| FA-41 | states | text | n/a | soil 11 dense |
| FA-41 | apparatus | text | none | microscope |
| FA-41 | panels | number | 1 | 0 |
| FA-41 | legend_entries | text | scale 1/32 inch | none |
| FA-42 | states | text | n/a | soil 11 dense |
| FA-42 | apparatus | text | sieve analysis | sieves |
| FA-42 | data_form | text | curve | mixed |
| FA-42 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-42 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-42 | legend_entries | text | average;range;inset table | Average;Range |
| FA-42 | in_scope | text | no | yes |
| FA-42 | priority | number | 2 | 1 |
| FA-43 | states | text | loose to dense | soil 11 dense |
| FA-43 | apparatus | text | Burmister min-max density | none |
| FA-43 | trace_classes | text | author-fit | computed |
| FA-43 | x_quantity | text | relative density | Relative Density Dr |
| FA-43 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-43 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-43 | in_scope | text | no | yes |
| FA-43 | priority | number | 2 | 1 |
| FA-44 | states | text | Dr .40 to 1.00 | soil 11 dense |
| FA-44 | apparatus | text | direct shear | shear box |
| FA-44 | rate_or_dynamics | text | n/a | static |
| FA-44 | x_quantity | text | relative density | Relative Density Dr |
| FA-44 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-44 | legend_entries | text | cross-hatched band 40 to 45 degrees | none |
| FA-44 | in_scope | text | no | yes |
| FA-44 | priority | number | 3 | 1 |
| FA-45 | states | text | n/a | soil 12 dense |
| FA-45 | apparatus | text | none | microscope |
| FA-45 | panels | number | 1 | 0 |
| FA-45 | legend_entries | text | scale 1/32 inch | none |
| FA-45 | relation | text | none | reproduces |
| FA-45 | relation_target | text |  | FA-17 |
| FA-46 | states | text | unused | soil 12 dense |
| FA-46 | apparatus | text | sieve analysis | sieves |
| FA-46 | data_form | text | curve | mixed |
| FA-46 | trace_classes | text | recorded-trace | measurement-markers;author-fit |
| FA-46 | y_quantity | text | percent finer by weight | Percent Finer Than By Weight |
| FA-46 | legend_entries | text | average;range;inset table | Average;Range |
| FA-47 | states | text | loose to dense | soil 12 dense |
| FA-47 | apparatus | text | Burmister min-max density | none |
| FA-47 | trace_classes | text | author-fit | computed |
| FA-47 | x_quantity | text | relative density | Relative Density Dr |
| FA-47 | y_quantity | text | unit weight | Minimum Density gamma min;Maximum Density gamma max |
| FA-47 | legend_entries | text | average;95 percent limits | mean;95% confidence limits |
| FA-47 | mcc_relevant | text | yes | no |
| FA-48 | states | text | loose to dense | soil 12 dense |
| FA-48 | apparatus | text | direct shear | shear box |
| FA-48 | rate_or_dynamics | text | n/a | static |
| FA-48 | x_quantity | text | relative density | Relative Density Dr |
| FA-48 | y_quantity | text | friction angle | Angle of Internal Friction phi |
| FA-48 | legend_entries | text | n/a | none |
| FA-48 | priority | number | 2 | 1 |
| FA-48 | relation | text | derived-from | none |
| FA-48 | relation_target | text | FC-22 |  |
| FC-12 | states | text | loose (avg density 58.00) | Loose |
| FC-12 | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-12 | rate_or_dynamics | text | quasi-static | not stated |
| FC-12 | data_form | text | curve | mixed |
| FC-12 | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-12 | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-12 | legend_entries | text | Avg. Density 58.00;Angle of Friction 43.07;Tan Theta .9349;Cohesion 145.81 | triangle markers;linear fit |
| FC-12 | relation | text | none | unresolved |
| FC-12 | relation_target | text |  | FC-4B |
| FC-13 | printed_page | text | C-35 | C-33 |
| FC-13 | states | text | loose (avg density 95.20) | Loose |
| FC-13 | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-13 | rate_or_dynamics | text | quasi-static | not stated |
| FC-13 | data_form | text | curve | mixed |
| FC-13 | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-13 | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-13 | legend_entries | text | Avg. Density 95.20;Angle of Friction 29.76;Tan Theta .5718;Cohesion 11.87 | triangle markers;linear fit |
| FC-13 | relation | text | none | unresolved |
| FC-13 | relation_target | text |  | FC-5B |
| FC-14 | states | text | loose (avg density 75.20) | Loose |
| FC-14 | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-14 | rate_or_dynamics | text | quasi-static | not stated |
| FC-14 | data_form | text | curve | mixed |
| FC-14 | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-14 | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-14 | legend_entries | text | Avg. Density 75.20;Angle of Friction 43.95;Tan Theta .9642;Cohesion -109.97 | triangle markers;linear fit |
| FC-14 | relation | text | none | unresolved |
| FC-14 | relation_target | text |  | FC-6B;FC-6D |
| FC-15 | states | text | dense (avg density 91.20) | Dense |
| FC-15 | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-15 | rate_or_dynamics | text | quasi-static | not stated |
| FC-15 | data_form | text | curve | mixed |
| FC-15 | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-15 | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-15 | legend_entries | text | Avg. Density 91.20;Angle of Friction 41.05;Tan Theta .8710;Cohesion 213.06 | triangle markers;linear fit |
| FC-15 | relation | text | none | unresolved |
| FC-15 | relation_target | text |  | FC-6C |
| FC-16 | states | text | all | range of Dr |
| FC-16 | apparatus | text | direct shear | shear box |
| FC-16 | rate_or_dynamics | text | quasi-static | not stated |
| FC-16 | curves | number | 3 | 7 |
| FC-16 | x_quantity | text | relative density | Relative Density Dr |
| FC-16 | legend_entries | text | series means with Dr range bars: about 0 at 38.8;.50 to .57 at 45.8;.73 to .88 at 46.8;1.0 to 1.16 at 50.8;singles near Dr 1.1 at 52.5 49.8 46.8 | circles;average;limits |
| FC-17 | states | text | all | range of Dr |
| FC-17 | apparatus | text | direct shear | shear box |
| FC-17 | rate_or_dynamics | text | quasi-static | not stated |
| FC-17 | curves | number | 3 | 4 |
| FC-17 | x_quantity | text | relative density | Relative Density Dr |
| FC-17 | legend_entries | text | pair .33 to .53 at 46.7;singles at Dr .15 .28 .36 near 43.5 43.9 43.6;one at 50 beyond Dr 1.1 | circles;average;limits |
| FC-18 | states | text | all | range of Dr |
| FC-18 | apparatus | text | direct shear | shear box |
| FC-18 | rate_or_dynamics | text | quasi-static | not stated |
| FC-18 | curves | number | 3 | 4 |
| FC-18 | x_quantity | text | relative density | Relative Density Dr |
| FC-18 | legend_entries | text | markers near Dr 0 (35.9 to 38.3 with a pair 0 to .15 at 38.3);one at Dr 1.0 (47) | circles;average;limits |
| FC-19 | states | text | all | range of Dr |
| FC-19 | apparatus | text | direct shear | shear box |
| FC-19 | rate_or_dynamics | text | quasi-static | not stated |
| FC-19 | x_quantity | text | relative density | Relative Density Dr |
| FC-19 | legend_entries | text | Dr 0 at 43;Dr .95 at 53 | circles;average;limits |
| FC-1A | states | text | Dr .50 to .57;Dr .73 to .88;Dr 1.0 to 1.16 | Dr=0.50-0.57;0.73-0.88;1.0-1.16 |
| FC-1A | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-1A | rate_or_dynamics | text | quasi-static | not stated |
| FC-1A | x_quantity | text | normal stress | Normal Stress sigma |
| FC-1A | y_quantity | text | maximum shear stress | Maximum Shear Stress tau |
| FC-1A | legend_entries | text | gamma 46.7 to 47.4 Lb./Ft.3 (Dr .50 to .57) open circles 45.5 deg;gamma 49.2 to 51.1 (Dr .73 to .88) filled circles 47 deg;gamma 53 to 55.4 (Dr 1.0 to 1.16) triangles 51 deg | gamma=46.7-47.4;49.2-51.1;53-55.4 Lb./Ft.^3 |
| FC-1B | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-1B | states | text | Dr .5 to .57 (gamma 46.7 to 47.4) | Dr=0.5-0.57 |
| FC-1B | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-1B | rate_or_dynamics | text | quasi-static | not stated |
| FC-1B | data_form | text | curve | mixed |
| FC-1B | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-1B | x_unit | text | in. | x 10^3 (in.) |
| FC-1B | y_quantity | text | shear stress tau (upper); dilation displacement delta_sigma x 10^-3 (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-1B | y_unit | text | psf; in. | PSF;x 10^3 (in.) |
| FC-1B | legend_entries | text | sigma (psf) and gamma (pcf): 3520 46.7 (x);2935 46.8 (asterisk);2345 46.7 (square);1760 46.7 (plus);1172 46.8 (inverted triangle);587 47.2 (triangle);294 47.4 (circle) | 3520/46.7;2935/46.8;2345/46.7;1760/46.7;1172/46.8;587/47.2;294/47.4 |
| FC-1B | mcc_relevant | text | maybe | no |
| FC-1C | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-1C | states | text | Dr .73 to .88 (gamma 49.2 to 51.1) | Dr=0.73-0.88 |
| FC-1C | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-1C | rate_or_dynamics | text | quasi-static | not stated |
| FC-1C | data_form | text | curve | mixed |
| FC-1C | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-1C | x_unit | text | in. | x 10^-3 (in.) |
| FC-1C | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-1C | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-1C | legend_entries | text | 3520 49.5;2935 49.7;2345 49.2;1760 50.3;1172 49.4;587 51.1;294 49.4 | 3520/49.5;2935/49.7;2345/49.2;1760/50.3;1172/49.4;587/51.1;294/49.4 |
| FC-1C | mcc_relevant | text | maybe | no |
| FC-1D | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-1D | states | text | Dr 1.0 to 1.16 (gamma 53 to 55.4) | Dr=1.0-1.16 |
| FC-1D | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-1D | rate_or_dynamics | text | quasi-static | not stated |
| FC-1D | data_form | text | curve | mixed |
| FC-1D | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-1D | x_unit | text | in. | x 10^-3 (in.) |
| FC-1D | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-1D | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-1D | legend_entries | text | 3520 54.3;2935 53.6;2345 55.4;1468 53.0;587 54.1;294 54.5;0 54.5 (filled circles) | 3520/54.3;2935/53.6;2345/55.4;1468/53.0;587/54.1;294/54.5;0/54.5 |
| FC-1D | mcc_relevant | text | maybe | no |
| FC-20 | states | text | all | range of Dr |
| FC-20 | apparatus | text | direct shear | shear box |
| FC-20 | rate_or_dynamics | text | quasi-static | not stated |
| FC-20 | curves | number | 3 | 4 |
| FC-20 | x_quantity | text | relative density | Relative Density Dr |
| FC-20 | legend_entries | text | Dr .02 to .13 (29.8 29.1 pair);.30 (33.2);.48 (36.9);.77 (41.5);1.0 (41.5) | circles;average;limits |
| FC-21 | states | text | all | range of Dr |
| FC-21 | apparatus | text | direct shear | shear box |
| FC-21 | rate_or_dynamics | text | quasi-static | not stated |
| FC-21 | curves | number | 2 | 5 |
| FC-21 | x_quantity | text | relative density | Relative Density Dr |
| FC-21 | legend_entries | text | cross-hatched band 40 to 45 degrees;markers at Dr 0 to .38 (44 pair);.17 to .26 (44.5 pair);.38 (44);1.0 to 1.07 (41.9 41.3 pair) | circles;average;limits |
| FC-21 | mcc_relevant | text | yes | no |
| FC-22 | printed_page | text | C-44 | i |
| FC-22 | states | text | all | range of Dr |
| FC-22 | apparatus | text | direct shear | shear box |
| FC-22 | rate_or_dynamics | text | quasi-static | not stated |
| FC-22 | x_quantity | text | relative density | Relative Density Dr |
| FC-22 | legend_entries | text | Dr .53 at 45.2;Dr .95 at 50.5 | circles;average;limits |
| FC-23 | printed_page | text | C-45/C-46 | unknown |
| FC-23 | states | text | all | range of Dr |
| FC-23 | apparatus | text | direct shear | shear box |
| FC-23 | rate_or_dynamics | text | quasi-static | not stated |
| FC-23 | x_quantity | text | relative density | Relative Density Dr |
| FC-2A | states | text | Dr .33 to .53;Dr 1.15 to 1.3 | Dr=0.33-0.53;1.15-1.3 |
| FC-2A | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-2A | rate_or_dynamics | text | quasi-static | not stated |
| FC-2A | legend_entries | text | gamma 25.6 to 26.8 (Dr .33 to .53) squares 49.5 deg;gamma 31.7 to 33.1 (Dr 1.15 to 1.3) circles 46.7 deg | gamma=25.6-26.8;31.7-33.1 Lb./Ft.^3 |
| FC-2B | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-2B | states | text | Dr .33 to .53 (gamma 25.6 to 26.8) | Dr=0.33-0.53 |
| FC-2B | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-2B | rate_or_dynamics | text | quasi-static | not stated |
| FC-2B | data_form | text | curve | mixed |
| FC-2B | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-2B | x_unit | text | in. | x 10^-3 (in.) |
| FC-2B | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-2B | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-2B | legend_entries | text | 4400 25.7;3660 25.9;2935 26.8;2200 25.6;1468 25.6;734 25.6 | 4400/25.7;3660/25.9;2995/26.8;2200/25.6;1468/25.6;734/25.6 |
| FC-2B | mcc_relevant | text | maybe | no |
| FC-2C | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-2C | states | text | Dr 1.15 to 1.3 (gamma 31.7 to 33.1) | Dr=1.15-1.3 |
| FC-2C | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-2C | rate_or_dynamics | text | quasi-static | not stated |
| FC-2C | data_form | text | curve | mixed |
| FC-2C | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-2C | x_unit | text | in. | x 10^-3 (in.) |
| FC-2C | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-2C | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-2C | legend_entries | text | 4400 32.8;3660 32.1;2935 31.7;2200 32.2;1468 31.8;734 33.1 | 4400/32.8;3660/32.1;2995/31.7;2200/32.2;1468/31.8;734/33.1 |
| FC-2C | mcc_relevant | text | maybe | no |
| FC-3A | states | text | Dr 0 to .15;Dr 1.0 to 1.3 | Dr=0-0.15;1.0-1.3 |
| FC-3A | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-3A | rate_or_dynamics | text | quasi-static | not stated |
| FC-3A | legend_entries | text | gamma 57.9 to 59.4 (Dr 0 to .15) circles 38 deg;gamma 75 (Dr 1.0 to 1.3) squares 47 deg | gamma=57.9-59.4;75 Lb./Ft.^3 |
| FC-3B | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-3B | states | text | Dr 0 to .15 (gamma 57.9 to 59.4) | Dr=0-0.15 |
| FC-3B | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-3B | rate_or_dynamics | text | quasi-static | not stated |
| FC-3B | data_form | text | curve | mixed |
| FC-3B | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-3B | x_unit | text | in. | x 10^-3 (in.) |
| FC-3B | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-3B | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-3B | legend_entries | text | 4695 57.9;3815 57.9;2934 57.9;1761 57.9;734 59.4 | 4695/57.9;3815/57.9;2934/57.9;1761/57.9;734/59.4 |
| FC-3B | mcc_relevant | text | yes | no |
| FC-3C | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-3C | states | text | Dr 1.0 to 1.3 (gamma 75) | Dr=1.0-1.3 |
| FC-3C | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-3C | rate_or_dynamics | text | quasi-static | not stated |
| FC-3C | data_form | text | curve | mixed |
| FC-3C | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-3C | x_unit | text | in. | x 10^-3 (in.) |
| FC-3C | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-3C | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-3C | legend_entries | text | 4695 75.0;3815 75.0;2934 75.0;1761 75.0;734 75.0 | 4695/75;3815/75;2934/75;1761/75;734/75 |
| FC-3C | mcc_relevant | text | maybe | no |
| FC-4A | states | text | Dr .95;Dr 0 | Dr=0;0.95 |
| FC-4A | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-4A | rate_or_dynamics | text | quasi-static | not stated |
| FC-4A | y_quantity | text | shear stress tau | Maximum Shear Stress tau |
| FC-4A | legend_entries | text | gamma 81.8 (Dr .95) squares 53 deg;gamma 58.7 (Dr 0) circles 43 deg | gamma=58.7;81.8 Lb./Ft.^3 |
| FC-4B | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-4B | states | text | Dr 0 (gamma 58.7) | Dr=0 |
| FC-4B | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-4B | rate_or_dynamics | text | quasi-static | not stated |
| FC-4B | data_form | text | curve | mixed |
| FC-4B | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-4B | x_unit | text | in. | x 10^-3 (in.) |
| FC-4B | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-4B | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-4B | legend_entries | text | 4695 58.7;3815 58.7;2934 58.7;1761 58.7;734 58.7 | 4695/58.7;3815/58.7;2934/58.7;1761/58.7;734/58.7 |
| FC-4B | mcc_relevant | text | yes | no |
| FC-4C | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-4C | states | text | Dr .95 (gamma 81.8) | Dr=0.95 |
| FC-4C | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-4C | rate_or_dynamics | text | quasi-static | not stated |
| FC-4C | data_form | text | curve | mixed |
| FC-4C | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-4C | x_unit | text | in. | x 10^-3 (in.) |
| FC-4C | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-4C | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-4C | legend_entries | text | 4695 81.8;3815 81.8;2934 81.8;1761 81.8;741 81.8 | 4695/81.8;3815/81.8;2934/81.8;1761/81.8;741/81.8 |
| FC-4C | mcc_relevant | text | maybe | no |
| FC-5A | states | text | Dr .02 to .13;Dr .30;Dr .48;Dr .77 | Dr=0.02-0.13;0.30;0.48;0.77 |
| FC-5A | apparatus | text | direct shear (Notre Dame for the first series; Bendix MM-66-2 for the other three) | shear box |
| FC-5A | rate_or_dynamics | text | quasi-static | not stated |
| FC-5A | y_quantity | text | shear stress tau | Maximum Shear Stress tau |
| FC-5A | legend_entries | text | gamma 95.2 to 97.6 (Dr .02 to .13) circles 29 deg;gamma 100 (Dr .30) squares 32.8 deg;gamma 103 (Dr .48) inverted triangles 36.9 deg;gamma 107 (Dr .77) triangles 41.5 deg | gamma=95.2-97.6;100;103;107 Lb./Ft.^3 |
| FC-5A | relation | text | none | derived-from |
| FC-5A | relation_target | text |  | FC-5B |
| FC-5B | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-5B | states | text | Dr .02 to .13 (gamma 95.2 to 97.6) | Dr=0.02-0.13 |
| FC-5B | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-5B | rate_or_dynamics | text | quasi-static | not stated |
| FC-5B | data_form | text | curve | mixed |
| FC-5B | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-5B | x_unit | text | in. | x 10^-3 (in.) |
| FC-5B | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-5B | y_unit | text | psf; in. | PSF;x 10^-3 (in.) |
| FC-5B | legend_entries | text | 4695 96.4;3815 96.4;2934 97.6;1761 96.4;734 95.2 | 4695/96.4;3815/96.4;2934/97.6;1761/96.4;734/95.2 |
| FC-5B | mcc_relevant | text | maybe | no |
| FC-6A | states | text | Dr .05 to .40;Dr .19 to .28;Dr 1.03 to 1.07 | Dr=0.05-0.40;0.19-0.28;1.03-1.07 |
| FC-6A | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-6A | rate_or_dynamics | text | quasi-static | not stated |
| FC-6A | y_quantity | text | shear stress tau | Maximum Shear Stress tau |
| FC-6A | legend_entries | text | gamma 66.8 to 75.2 (Dr .05 to .40) triangles;gamma 71.1 to 73 (Dr .19 to .28) circles;gamma 91 to 93.3 (Dr 1.03 to 1.07) squares | gamma=66.8-75.2;71.1-73;91-93.3 Lb./Ft.^3 |
| FC-6B | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-6B | states | text | Dr .19 to .28 (gamma 71.1 to 73) | Dr=0.19-0.28 |
| FC-6B | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-6B | rate_or_dynamics | text | quasi-static | not stated |
| FC-6B | data_form | text | curve | mixed |
| FC-6B | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-6B | x_unit | text | in. | x 10^-3 (in.) |
| FC-6B | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-6B | y_unit | text | psf; in | PSF;x 10^-3 (in.) |
| FC-6B | legend_entries | text | 4695 73.0;3815 71.1;2934 71.1;1761 71.1;734 71.1 | 4695/73.0;3815/71.1;2934/71.1;1761/71.1;734/71.1 |
| FC-6B | mcc_relevant | text | yes | no |
| FC-6C | title_as_printed | text | LSM Soil Dense - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | LSM Soil Dense - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-6C | states | text | Dr 1.03 to 1.07 (gamma 91 to 93.3) | Dr=1.03-1.07 |
| FC-6C | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-6C | rate_or_dynamics | text | quasi-static | not stated |
| FC-6C | data_form | text | curve | mixed |
| FC-6C | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-6C | x_unit | text | in | x 10^-3 (in.) |
| FC-6C | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-6C | y_unit | text | psf; in | PSF;x 10^-3 (in.) |
| FC-6C | legend_entries | text | 4695 91.0;3815 91.0;2934 91.0;1961 91.0;714 93.3 | 4695/91.0;3815/91.0;2934/91.0;1961/91.0;714/93.3 |
| FC-6C | mcc_relevant | text | maybe | no |
| FC-6D | title_as_printed | text | Direct Shear Test Data - Shear Stress vs. Shear Displacement; Dilation Displacement vs. Shear Displacement | Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement |
| FC-6D | states | text | Dr .05 to .40 (gamma 66.8 to 75.2) | Dr=0.05-0.40 |
| FC-6D | apparatus | text | direct shear (Notre Dame) | shear box |
| FC-6D | rate_or_dynamics | text | quasi-static | not stated |
| FC-6D | data_form | text | curve | mixed |
| FC-6D | x_quantity | text | shear displacement delta_tau x 10^-3 | Shear Displacement delta_tau |
| FC-6D | x_unit | text | in | x 10^-3 (in.) |
| FC-6D | y_quantity | text | shear stress (upper); dilation displacement (lower) | Shear Stress tau;Dilation Displacement delta_sigma |
| FC-6D | y_unit | text | psf; in | PSF;x 10^-3 (in.) |
| FC-6D | legend_entries | text | 4695 73.0;3814 75.2;2934 66.8;1761 70.3;147 71.9 | 4695/73.0;3814/75.2;2934/66.8;1761/70.3;147/71.9 |
| FC-6D | mcc_relevant | text | yes | no |
| FC-7A | states | text | Dr 0.53;Dr 1.0 | Dr=0.53;1.0 |
| FC-7A | apparatus | text | direct shear (apparatus in psi units) | shear box |
| FC-7A | rate_or_dynamics | text | quasi-static | not stated |
| FC-7A | legend_entries | text | gamma 82 lb/ft3 (Dr 0.53) circles with dot 45 deg;gamma 89 lb/ft3 (Dr 1.0) triangles 50.5 deg | gamma=82;89 Lb/ft^3 |
| FC-7B | states | text | Dr 1.0 (gamma 89) | Dr=1.0 |
| FC-7B | apparatus | text | direct shear (psi apparatus) | shear box |
| FC-7B | rate_or_dynamics | text | quasi-static | not stated |
| FC-7B | data_form | text | curve | mixed |
| FC-7B | legend_entries | text | (psi)(pcf): 27.1 89;13.8 89;10.2 89;6.6 89;5.1 89;3.4 89 | 27.1/89;13.8/89;10.2/89;6.6/89;5.1/89;3.4/89 |
| FC-7C | states | text | Dr 0.53 (gamma 82) | Dr=0.53 |
| FC-7C | apparatus | text | direct shear (psi apparatus) | shear box |
| FC-7C | rate_or_dynamics | text | quasi-static | not stated |
| FC-7C | data_form | text | curve | mixed |
| FC-7C | legend_entries | text | (psi)(pcf): 26.5 82;13.8 82;10.2 82;6.6 82;5.1 82;3.4 82 | 26.5/82;13.8/82;10.2/82;6.6/82;5.1/82;3.4/82 |
| FC-9A | states | text | dense (avg density 54.20) | Dense |
| FC-9A | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-9A | rate_or_dynamics | text | quasi-static | not stated |
| FC-9A | data_form | text | curve | mixed |
| FC-9A | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-9A | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-9A | legend_entries | text | Avg. Density 54.20;Angle of Friction 52.55;Tan Theta 1.3059;Cohesion 634.20 | triangle markers;linear fit |
| FC-9A | relation | text | none | derived-from |
| FC-9A | relation_target | text |  | FC-1D |
| FC-9B | states | text | dense (avg density 54.40) | Dense |
| FC-9B | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-9B | rate_or_dynamics | text | quasi-static | not stated |
| FC-9B | data_form | text | curve | mixed |
| FC-9B | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-9B | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-9B | legend_entries | text | Avg. Density 54.40;Angle of Friction 46.65;Tan Theta 1.0594;Cohesion 698.23 | triangle markers;linear fit |
| FC-9C | states | text | dense (avg density 54.30) | Dense |
| FC-9C | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-9C | rate_or_dynamics | text | quasi-static | not stated |
| FC-9C | data_form | text | curve | mixed |
| FC-9C | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-9C | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-9C | legend_entries | text | Avg. Density 54.30;Angle of Friction 49.39;Tan Theta 1.1663;Cohesion 700.44 | triangle markers;linear fit |
| FC-10A | states | text | loose (avg density 25.90) | Loose |
| FC-10A | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-10A | rate_or_dynamics | text | quasi-static | not stated |
| FC-10A | data_form | text | curve | mixed |
| FC-10A | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-10A | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-10A | legend_entries | text | Avg. Density 25.90;Angle of Friction 43.44;Tan Theta .9471;Cohesion 488.69 | triangle markers;linear fit |
| FC-10A | relation | text | none | derived-from |
| FC-10A | relation_target | text |  | FC-2B |
| FC-10B | states | text | loose (avg density 24.60) | Loose |
| FC-10B | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-10B | rate_or_dynamics | text | quasi-static | not stated |
| FC-10B | data_form | text | curve | mixed |
| FC-10B | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-10B | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-10B | legend_entries | text | Avg. Density 24.60;Angle of Friction 43.40;Tan Theta .9459;Cohesion 169.22 | triangle markers;linear fit |
| FC-10C | states | text | loose (avg density 25.40) | Loose |
| FC-10C | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-10C | rate_or_dynamics | text | quasi-static | not stated |
| FC-10C | data_form | text | curve | mixed |
| FC-10C | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-10C | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-10C | legend_entries | text | Avg. Density 25.40;Angle of Friction 43.70;Tan Theta .9558;Cohesion 359.69 | triangle markers;linear fit |
| FC-11A | states | text | loose (avg density 58.20) | Loose |
| FC-11A | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-11A | rate_or_dynamics | text | quasi-static | not stated |
| FC-11A | data_form | text | curve | mixed |
| FC-11A | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-11A | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-11A | legend_entries | text | Avg. Density 58.20;Angle of Friction 35.92;Tan Theta .7244;Cohesion 444.69 | triangle markers;linear fit |
| FC-11A | relation | text | none | derived-from |
| FC-11A | relation_target | text |  | FC-3B |
| FC-11B | states | text | loose (avg density 58.30) | Loose |
| FC-11B | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-11B | rate_or_dynamics | text | quasi-static | not stated |
| FC-11B | data_form | text | curve | mixed |
| FC-11B | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-11B | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-11B | legend_entries | text | Avg. Density 58.30;Angle of Friction 37.38;Tan Theta .7641;Cohesion 785.77 | triangle markers;linear fit |
| FC-11C | printed_page | text | C-33 | C-35 |
| FC-11C | states | text | loose (avg density 58.20) | Loose |
| FC-11C | apparatus | text | direct shear; computer plot | shear box;UNIVAC 1107;CALCOMP |
| FC-11C | rate_or_dynamics | text | quasi-static | not stated |
| FC-11C | data_form | text | curve | mixed |
| FC-11C | x_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-11C | y_unit | text | psf x 10^1 | PSF (x 10^1) |
| FC-11C | legend_entries | text | Avg. Density 58.20;Angle of Friction 37.07;Tan Theta .7556;Cohesion 584.29 | triangle markers;linear fit |
| TA-p003 | title_as_printed | text | Specification for Soil No. 1 (chemical analysis) | Chemical Analysis |
| TA-p003 | states | text | loose | material composition |
| TA-p003 | apparatus | text | none | not stated |
| TA-p003 | trace_classes | text | n/a | setup-evidence |
| TA-p003 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p003 | priority | number | 2 | 1 |
| TA-p004 | <row> | missing | absent | present |
| TA-p011 | title_as_printed | text | Specification for Soil No. 2 (chemical analysis) | Chemical Analysis |
| TA-p011 | states | text | loose | material composition |
| TA-p011 | apparatus | text | none | not stated |
| TA-p011 | trace_classes | text | n/a | setup-evidence |
| TA-p011 | legend_entries | text | n/a | pumice |
| TA-p011 | priority | number | 2 | 1 |
| TA-p018 | title_as_printed | text | Specification for Soil No. 3 (chemical analysis) | Chemical Analysis |
| TA-p018 | states | text | intermediate | material composition |
| TA-p018 | apparatus | text | none | not stated |
| TA-p018 | trace_classes | text | n/a | setup-evidence |
| TA-p018 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p018 | in_scope | text | no | yes |
| TA-p018 | priority | number | 3 | 1 |
| TA-p018 | relation | text | same-as | reproduces |
| TA-p018 | relation_target | text | TA-s1-chem | TA-p003 |
| TA-p019 | <row> | missing | absent | present |
| TA-p026 | title_as_printed | text | Specification for Soil No. 4 (chemical analysis) | Chemical Analysis |
| TA-p026 | states | text | dense | material composition |
| TA-p026 | apparatus | text | none | not stated |
| TA-p026 | trace_classes | text | n/a | setup-evidence |
| TA-p026 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p026 | in_scope | text | no | yes |
| TA-p026 | priority | number | 3 | 1 |
| TA-p026 | relation | text | same-as | reproduces |
| TA-p026 | relation_target | text | TA-s1-chem | TA-p003 |
| TA-p027 | <row> | missing | absent | present |
| TA-p035 | title_as_printed | text | Specification for Soil No. 5 (chemical analysis) | Chemical Analysis |
| TA-p035 | printed_page | text | A-33 to A-34 | A-34 |
| TA-p035 | pdf_page | number | 34 | 35 |
| TA-p035 | states | text | loose | material composition |
| TA-p035 | apparatus | text | none | not stated |
| TA-p035 | trace_classes | text | n/a | setup-evidence |
| TA-p035 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p035 | priority | number | 2 | 1 |
| TA-p035 | relation | text | none | reproduces |
| TA-p035 | relation_target | text |  | TA-p003 |
| TA-p037 | <row> | missing | absent | present |
| TA-p043 | title_as_printed | text | Specification for Soil No. 6 (chemical analysis) | Chemical Analysis |
| TA-p043 | states | text | loose | material composition |
| TA-p043 | apparatus | text | none | not stated |
| TA-p043 | trace_classes | text | n/a | setup-evidence |
| TA-p043 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p043 | in_scope | text | no | yes |
| TA-p043 | priority | number | 3 | 1 |
| TA-p043 | relation | text | same-as | reproduces |
| TA-p043 | relation_target | text | TA-s1-chem | TA-p003 |
| TA-p044 | <row> | missing | absent | present |
| TA-p051 | title_as_printed | text | Specification for Soil No. 7 (chemical analysis) | Chemical Analysis |
| TA-p051 | states | text | loose | material composition |
| TA-p051 | apparatus | text | none | not stated |
| TA-p051 | trace_classes | text | n/a | setup-evidence |
| TA-p051 | legend_entries | text | n/a | silica sand |
| TA-p051 | priority | number | 2 | 1 |
| TA-p058 | title_as_printed | text | Specification for Soil No. 8 (chemical analysis) | Chemical Analysis |
| TA-p058 | states | text | intermediate | material composition |
| TA-p058 | apparatus | text | none | not stated |
| TA-p058 | trace_classes | text | n/a | setup-evidence |
| TA-p058 | legend_entries | text | n/a | silica sand |
| TA-p058 | in_scope | text | no | yes |
| TA-p058 | priority | number | 3 | 1 |
| TA-p058 | relation | text | same-as | reproduces |
| TA-p058 | relation_target | text | TA-s7-chem | TA-p051 |
| TA-p065 | title_as_printed | text | Specification for Soil No. 9 (chemical analysis) | Chemical Analysis |
| TA-p065 | states | text | dense | material composition |
| TA-p065 | apparatus | text | none | not stated |
| TA-p065 | trace_classes | text | n/a | setup-evidence |
| TA-p065 | legend_entries | text | n/a | silica sand |
| TA-p065 | in_scope | text | no | yes |
| TA-p065 | priority | number | 3 | 1 |
| TA-p065 | relation | text | same-as | reproduces |
| TA-p065 | relation_target | text | TA-s7-chem | TA-p051 |
| TA-p072 | title_as_printed | text | Specification for Soil No. 10 (chemical analyses of cinders and clay) | Chemical Analysis |
| TA-p072 | printed_page | text | A-71 to A-72 | A-71 |
| TA-p072 | pdf_page | number | 73 | 72 |
| TA-p072 | states | text | intermediate | material composition |
| TA-p072 | apparatus | text | none | not stated |
| TA-p072 | trace_classes | text | n/a | setup-evidence |
| TA-p072 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p072 | priority | number | 2 | 1 |
| TA-p072 | relation | text | none | unresolved |
| TA-p072 | relation_target | text |  | TA-p003 |
| TA-p073 | <row> | missing | absent | present |
| TA-p074 | <row> | missing | absent | present |
| TA-p081 | title_as_printed | text | Specification for Soil No. 11 (chemical analyses of cinders and clay) | Chemical Analysis |
| TA-p081 | printed_page | text | A-80 to A-81 | A-80 |
| TA-p081 | pdf_page | number | 82 | 81 |
| TA-p081 | states | text | dense | material composition |
| TA-p081 | apparatus | text | none | not stated |
| TA-p081 | trace_classes | text | n/a | setup-evidence |
| TA-p081 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p081 | in_scope | text | no | yes |
| TA-p081 | priority | number | 3 | 1 |
| TA-p081 | relation | text | same-as | unresolved |
| TA-p081 | relation_target | text | TA-s10-chem | TA-p003 |
| TA-p082 | <row> | missing | absent | present |
| TA-p083 | <row> | missing | absent | present |
| TA-p090 | title_as_printed | text | Specification for Soil No. 12 (chemical analysis) | Chemical Analysis |
| TA-p090 | printed_page | text | A-89 to A-90 | A-89 |
| TA-p090 | pdf_page | number | 91 | 90 |
| TA-p090 | states | text | dense | material composition |
| TA-p090 | apparatus | text | none | not stated |
| TA-p090 | trace_classes | text | n/a | setup-evidence |
| TA-p090 | legend_entries | text | n/a | Volcalite;Hypersthene Andesite |
| TA-p090 | priority | number | 2 | 1 |
| TA-p090 | relation | text | none | reproduces |
| TA-p090 | relation_target | text |  | TA-p003 |
| TA-p093 | <row> | missing | absent | present |
