# Page diff: claude vs codex

Submissions: `extractions/claude/pages-vol2-ab-b5` (claude), `extractions/codex/pages-vol2-ab-b5` (codex).

Pages 17: agreed 7, resolved 10, pending 0. Differences: number 5, reference 0, symbol 2, wording 19, markup 0; header fields 4.

## p0098

Header differences:

- `sections`: claude `[]` | codex `[14]`

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0098-d1 | wording | ...(nothing) | (nothing) | # | a: numbered item kept as a list paragraph (see the header decision) |
| p0098-d2 | wording | ...14. | Special | Special. | a: measured: the dot after Special is 6 x 5 px, against about 10 x 12 px for a typed period in this type; a speck (rule 10); credit Claude |
| p0098-d3 | wording | ...14. Special Comments | (nothing) | [sic] | a: the [sic] Codex placed belonged to the period it read after Special (see d2) |

Body differences: 3 (0 blocking, 3 wording or markup); decided 3; status **resolved**.

## p0099

Header differences:

- `printed_page`: claude `""` | codex `"unknown"`

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0099-d1 | symbol | ...determination of the sonic | modulus of | modulus_of [sic] | a: the mark between modulus and of lies at the baseline, an underline remnant (rule 10, batch 3 decision 2), not a typed underscore |
| p0099-d2 | wording | ...of the test scils | [sic] | (nothing) | text: the second letter of scils is an open c shape on a page where many letters are broken (dctermination, complcte); both agents typed scils; Codex's doubt marker fits a damaged o better than Claude's misprint marker; credit Codex; text=[?] |

Body differences: 2 (1 blocking, 1 wording or markup); decided 2; status **resolved**.

## p0100

Header differences:

- `printed_page`: claude `""` | codex `"unknown"`

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0100-d1 | wording | ...P.O. No. 5800191M [paragraph break] | (nothing) | # | a: the report title on the cover is part of the cover block, not a heading; the title is a heading once, where the report body starts (PDF 104) |

Body differences: 1 (0 blocking, 1 wording or markup); decided 1; status **resolved**.

## p0101

Header differences:

- `printed_page`: claude `""` | codex `"unknown"`

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0101-d1 | wording | ...[paragraph break] (Final Report) [paragraph break] | (nothing) | # | a: the report title on the title page is part of the title block, not a heading (see p0100-d1) |
| p0101-d2 | wording | ...[paragraph break] South, Bend, Indiana | (nothing) | [sic] | b: South, Bend is printed with a comma after South; a visible misprint takes [sic] (rule 10); Claude missed it; credit Codex |

Body differences: 2 (0 blocking, 2 wording or markup); decided 2; status **resolved**.

## p0102

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0102-d1 | wording | ...(nothing) | (nothing) | # | b: FOREWORD is the printed title of a part of the report, underlined and centered; a heading, as Codex wrote; credit Codex |
| p0102-d2 | wording | ...IIT RESEARCH INSTITUTE [paragraph break] | [signature] [paragraph break] | (nothing) | b: a handwritten signature is not printed text; Claude's [signature] notes were invented text; rule 10 ignores handwriting; credit Codex |
| p0102-d3 | wording | ...Research Engineer [paragraph break] APPROVED: | [paragraph break] [signature] | (nothing) | b: a handwritten signature is not printed text (see d2); credit Codex |
| p0102-d4 | wording | ...Research Division [paragraph break] JDN:is | [paragraph break] IIT RESEARCH INSTITUTE | (nothing) | b: IIT RESEARCH INSTITUTE at the foot of each IITRI page is the report's running footer, which rule 1 omits; Claude kept it; credit Codex |

Body differences: 4 (0 blocking, 4 wording or markup); decided 4; status **resolved**.

## p0103

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0103-d1 | wording | ...(nothing) | (nothing) | # | b: TABLE OF CONTENTS is the printed title of a part of the report; a heading, as Codex wrote; credit Codex |
| p0103-d2 | wording | ...RESULTS \| 3 \| | [paragraph break] IIT RESEARCH INSTITUTE | (nothing) | b: IIT RESEARCH INSTITUTE at the foot of each IITRI page is the report's running footer, which rule 1 omits; Claude kept it; credit Codex |

Body differences: 2 (0 blocking, 2 wording or markup); decided 2; status **resolved**.

## p0104

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0104-d1 | wording | ...(nothing) | (nothing) | # | b: the report title at the start of the body is the heading over sections A to D; credit Codex |
| p0104-d2 | wording | ...difference between arrival [paragraph break] | IIT RESEARCH INSTITUTE [paragraph break] | (nothing) | b: IIT RESEARCH INSTITUTE at the foot of each IITRI page is the report's running footer, which rule 1 omits; Claude kept it; credit Codex |
| p0104-d3 | wording | ...INSTITUTE [paragraph break] Footnotes: [paragraph break] | ¹Vey, | ¹ Vey, | a: the superscript marker is printed against the author's name with no space, and rule 7 starts a footnote with its marker |
| p0104-d4 | wording | ...to be published. [paragraph break] | ²Selig, | ² Selig, | a: the superscript marker is printed against the author's name with no space (see d3) |

Body differences: 4 (0 blocking, 4 wording or markup); decided 4; status **resolved**.

## p0105

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0105-d1 | number | ...equation [paragraph break] $$E = | \rho c^2$$ | ρc^2$$ | a: display equations may use LaTeX macros (rule 5) and every Volume I display equation writes Greek as macros (\sigma, \gamma, \phi); Claude's form kept for consistency |
| p0105-d2 | wording | ...quite low and hence, | [paragraph break] IIT RESEARCH INSTITUTE | (nothing) | b: IIT RESEARCH INSTITUTE at the foot of each IITRI page is the report's running footer, which rule 1 omits; Claude kept it; credit Codex |

Body differences: 2 (1 blocking, 1 wording or markup); decided 2; status **resolved**.

## p0106

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0106-d1 | number | ...equation [paragraph break] $$E = | \rho c^2 \frac{(1+\nu)(1-2\nu)}{(1-\nu)}$$ | ρc^2 \frac{(1+ν)(1-2ν)}{(1-ν)}$$ | a: display equations may use LaTeX macros (rule 5) and every Volume I display equation writes Greek as macros (\sigma, \gamma, \phi); Claude's form kept for consistency |
| p0106-d2 | symbol | ...ratio. The factor [paragraph break] | $$f(\nu) | $$f(ν) | a: display equations may use LaTeX macros (rule 5) and every Volume I display equation writes Greek as macros (\sigma, \gamma, \phi); Claude's form kept for consistency |
| p0106-d3 | number | ...factor [paragraph break] $$f(\nu) = | \frac{(1+\nu)(1-2\nu)}{(1-\nu)}$$ | \frac{(1+ν)(1-2ν)}{(1-ν)}$$ | a: display equations may use LaTeX macros (rule 5) and every Volume I display equation writes Greek as macros (\sigma, \gamma, \phi); Claude's form kept for consistency |
| p0106-d4 | wording | ...to influence the results. | [paragraph break] IIT RESEARCH INSTITUTE | (nothing) | b: IIT RESEARCH INSTITUTE at the foot of each IITRI page is the report's running footer, which rule 1 omits; Claude kept it; credit Codex |

Body differences: 4 (3 blocking, 1 wording or markup); decided 4; status **resolved**.

## p0107

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 0 (0 blocking, 0 wording or markup); decided 0; status **agreed**.

## p0108

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 0 (0 blocking, 0 wording or markup); decided 0; status **agreed**.

## p0109

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 0 (0 blocking, 0 wording or markup); decided 0; status **agreed**.

## p0110

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 0 (0 blocking, 0 wording or markup); decided 0; status **agreed**.

## p0111

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 0 (0 blocking, 0 wording or markup); decided 0; status **agreed**.

## p0112

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 0 (0 blocking, 0 wording or markup); decided 0; status **agreed**.

## p0113

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 0 (0 blocking, 0 wording or markup); decided 0; status **agreed**.

## p0114

| id | class | after | claude | codex | decision |
|---|---|---|---|---|---|
| p0114-d1 | number | ...caption FB-8: f(ν) ON ν | (E=ρc² | ($E=ρc^2$ | a: rule 4 puts only subscripted symbols in math; a superscript is written with the Unicode sign, as kips/in.² and Ft.³ are throughout the corpus |
| p0114-d2 | number | ...numbers printed on the page (outside descriptions), present in one reading only | (nothing) | 2 | a: the 2 is the superscript of c, written ² (see d1) |

Figure page (caption, numbers, symbols compared; descriptions ignored). Body differences: 2 (2 blocking, 0 wording or markup); decided 2; status **resolved**.

