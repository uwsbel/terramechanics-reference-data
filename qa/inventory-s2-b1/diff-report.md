# Table diff: claude vs codex

Files: `extractions/claude/inventory-s2-b1/inventory-claude.csv` (claude), `extractions/codex/inventory-s2-b1/inventory-codex.csv` (codex). Key: `id`.

Rows: 69 in claude, 69 in codex. Compared columns: 15.
Cells compared: 1035. Agreed: 875 (84.5 percent).
Disagreements: 160 (35 numeric, 125 text, 0 missing rows).

| key | column | kind | claude | codex |
|---|---|---|---|---|
| F2-1 | test_type | text | other | soil model |
| F2-2 | data_form | text | schematic | text |
| F2-3 | test_type | text | other | soil model |
| F2-4 | x_unit | text | none | n/a |
| F2-4 | y_unit | text | none | n/a |
| F2-5 | test_type | text | other | soil model |
| F2-5 | in_scope | text | no | yes |
| F2-5 | mcc_relevant | text | no | yes |
| F2-6 | test_type | text | other | soil properties |
| F2-6 | in_scope | text | no | yes |
| F2-7 | test_type | text | other | soil properties |
| F2-7 | in_scope | text | no | yes |
| F2-7 | mcc_relevant | text | no | yes |
| F2-8 | test_type | text | apparatus | grain size |
| F2-8 | in_scope | text | no | yes |
| F2-8 | priority | number | 3 | 2 |
| F2-9 | in_scope | text | no | yes |
| F2-9 | priority | number | 3 | 2 |
| T1-1 | rotation | number | 0 | 90 |
| T1-1 | priority | number | 2 | 1 |
| T1-1 | mcc_relevant | text | no | yes |
| T2-1 | in_scope | text | yes | no |
| T2-1 | priority | number | 2 | 3 |
| T2-1 | mcc_relevant | text | no | yes |
| T2-2 | in_scope | text | maybe | yes |
| T2-2 | mcc_relevant | text | no | yes |
| T2-3 | mcc_relevant | text | no | yes |
| F2-10 | in_scope | text | no | yes |
| F2-10 | priority | number | 3 | 2 |
| F2-11 | test_type | text | apparatus | grain size |
| F2-11 | in_scope | text | no | yes |
| F2-11 | priority | number | 3 | 2 |
| F2-12 | priority | number | 2 | 1 |
| F2-12 | mcc_relevant | text | no | yes |
| F2-13 | priority | number | 2 | 1 |
| F2-15 | data_form | text | schematic | curve |
| F2-15 | x_unit | text | none | n/a |
| F2-15 | x_axis_type | text | linear | normalized |
| F2-15 | y_axis_type | text | reciprocal (1/gamma linear) | n/a |
| F2-15 | in_scope | text | maybe | yes |
| F2-15 | priority | number | 3 | 2 |
| F2-15 | mcc_relevant | text | no | yes |
| F2-16 | test_type | text | apparatus | bed preparation |
| F2-16 | in_scope | text | no | yes |
| F2-16 | priority | number | 3 | 2 |
| F2-16 | mcc_relevant | text | no | yes |
| F2-17 | x_unit | text | none | n/a |
| F2-17 | x_axis_type | text | linear | normalized |
| F2-17 | y_axis_type | text | reciprocal (1/gamma linear; gamma_min on left; gamma_max on right) | n/a |
| F2-17 | priority | number | 1 | 2 |
| F2-18 | test_type | text | density | bed preparation |
| F2-19 | test_type | text | apparatus | direct shear |
| F2-19 | in_scope | text | no | yes |
| F2-19 | priority | number | 3 | 2 |
| F2-19 | mcc_relevant | text | no | yes |
| F2-20 | mcc_relevant | text | no | yes |
| F2-21 | x_unit | text | inch (thousandths) | In. |
| F2-21 | y_unit | text | psf and thousandths of an inch | psf |
| F2-21 | mcc_relevant | text | no | yes |
| F2-23 | x_unit | text | none | n/a |
| F2-23 | x_axis_type | text | linear | normalized |
| F2-23 | mcc_relevant | text | no | yes |
| F2-24 | test_type | text | other | soil properties |
| F2-24 | in_scope | text | no | yes |
| F2-25 | x_unit | text | none | n/a |
| F2-25 | y_unit | text | none | n/a |
| F2-25 | in_scope | text | no | yes |
| F2-25 | mcc_relevant | text | no | yes |
| F2-26 | in_scope | text | no | yes |
| F2-26 | priority | number | 3 | 2 |
| F2-28 | test_type | text | apparatus | load penetration |
| F2-28 | in_scope | text | no | yes |
| F2-28 | priority | number | 3 | 2 |
| F2-29 | x_unit | text | inch | in. |
| F2-29 | y_unit | text | lb | Lbs. |
| F2-29 | mcc_relevant | text | no | yes |
| F2-30 | test_type | text | apparatus | load penetration |
| F2-30 | in_scope | text | no | yes |
| F2-30 | priority | number | 3 | 2 |
| F2-31 | y_unit | text | none | n/a |
| F2-31 | in_scope | text | maybe | yes |
| F2-31 | priority | number | 2 | 3 |
| F2-32 | data_form | text | curve | mixed |
| F2-32 | x_unit | text | inch | In. |
| F2-33 | data_form | text | curve | mixed |
| F2-33 | x_unit | text | inch | In. |
| F2-34 | data_form | text | curve | mixed |
| F2-34 | x_unit | text | inch | In. |
| F2-34 | y_unit | text | lb (axis printed as Lbs. x 100; see notes) | Lbs. x 100 |
| F2-35 | data_form | text | curve | mixed |
| F2-35 | x_unit | text | inch | In. |
| F2-35 | priority | number | 1 | 2 |
| F2-36 | x_unit | text | none | n/a |
| F2-36 | y_unit | text | none | n/a |
| F2-37 | curves | number | 10 | 11 |
| F2-37 | x_unit | text | none | n/a |
| F2-37 | y_unit | text | none | n/a |
| F2-37 | priority | number | 1 | 2 |
| F2-38 | x_unit | text | none | n/a |
| F2-38 | y_unit | text | none | n/a |
| F2-39 | x_unit | text | none | n/a |
| F2-39 | x_axis_type | text | linear | normalized |
| F2-39 | y_unit | text | none | n/a |
| F2-40 | x_unit | text | inch | Inches |
| F2-40 | y_unit | text | lb | Lbs. |
| F2-40 | priority | number | 1 | 2 |
| F2-40 | mcc_relevant | text | no | yes |
| F2-41 | x_unit | text | inch | In. |
| F2-41 | y_unit | text | lb | Lbs. |
| F2-41 | priority | number | 1 | 2 |
| F2-42 | x_unit | text | inch | In. |
| F2-42 | priority | number | 1 | 2 |
| F2-43 | x_unit | text | inch | In. |
| F2-43 | y_unit | text | lb | Lbs. |
| F2-43 | priority | number | 1 | 2 |
| F2-43 | mcc_relevant | text | no | yes |
| F2-44 | x_unit | text | inch | In. |
| F2-44 | priority | number | 1 | 2 |
| F2-45 | x_unit | text | inch | In. |
| F2-46 | x_unit | text | inch | In. |
| F2-47 | x_unit | text | inch | In. |
| F2-48 | x_unit | text | inch | In. |
| F2-48 | y_unit | text | lb | Lbs. |
| F2-49 | curves | number | 9 | 10 |
| F2-49 | x_unit | text | none | n/a |
| F2-49 | y_unit | text | none | n/a |
| F2-50 | x_unit | text | none | n/a |
| F2-50 | y_unit | text | none | n/a |
| F2-51 | x_unit | text | none | n/a |
| F2-51 | y_unit | text | none | n/a |
| F2-52 | y_unit | text | none | n/a |
| F2-52 | y_axis_type | text | linear | normalized |
| F2-52 | priority | number | 1 | 2 |
| F2-53 | priority | number | 1 | 2 |
| F2-54 | x_unit | text | seconds | sec. |
| F2-54 | y_unit | text | g | G's |
| F2-55 | x_unit | text | none | n/a |
| F2-55 | x_axis_type | text | linear | normalized |
| F2-55 | y_unit | text | g | g's |
| F2-57 | curves | number | 3 | 4 |
| F2-58 | curves | number | 5 | 6 |
| F2-59 | test_type | text | apparatus | density |
| F2-59 | in_scope | text | no | yes |
| F2-59 | priority | number | 3 | 2 |
| F2-59 | mcc_relevant | text | no | yes |
| F2-60 | x_unit | text | count | n/a |
| F2-60 | y_unit | text | lb/ft3 | Pounds/Ft.^3 |
| F2-61 | mcc_relevant | text | no | yes |
| F2-62 | in_scope | text | no | yes |
| F2-62 | priority | number | 3 | 2 |
| F2-62 | mcc_relevant | text | no | yes |
| F2-63 | in_scope | text | no | maybe |
| F2-63 | priority | number | 3 | 2 |
| F2-63 | mcc_relevant | text | no | yes |
| F2-64 | in_scope | text | no | yes |
| F2-64 | priority | number | 3 | 2 |
| F2-64 | mcc_relevant | text | no | yes |
| F2-65 | in_scope | text | no | yes |
| F2-65 | priority | number | 3 | 2 |
| F2-65 | mcc_relevant | text | no | yes |
