You are extracting a data table from a scanned 1968 NASA report for Dan Negrut's Apollo-era soil-test data project. Work only from the page image. Do not use em-dashes or en-dashes.

## The page

`nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf` (read-only), PDF page 41, printed page 2-16: "TABLE 2-3. TEST SOILS AND PROPERTIES". The table is printed rotated on the page. Render it with Ghostscript (on PATH):

```
gswin64c -q -dNOPAUSE -dBATCH -sDEVICE=pnggray -r300 -dFirstPage=41 -dLastPage=41 -sOutputFile=<your temp folder>/p0041.png nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf
```

Rotate the image so the table reads upright before reading it, and zoom into the cells. Read every row and every column, including the three footnotes under the table. Do not read `corpus/1968/page-map.csv` or anything else; the page is the only evidence.

## Output

Return, in your final message, a fenced CSV block with exactly these columns and one row per soil number as printed:

`soil_no,bendix_designation,description_verbatim,family,state,relative_density,unit_weight_native,unit_weight_unit,friction_angle_deg,elastic_modulus_native,elastic_modulus_unit,mean_grain_size_native,mean_grain_size_unit,uniformity_coeff,percent_passing_200_native,d95_native,d95_unit,read_flags,source_locator`

Rules:

- Transcribe exactly what is printed, including spelling as printed and symbols such as "<3%". Do not correct or round. Where a cell is a word rather than a number, keep the word.
- `family` is the designation prefix (RS, PS, RSM, RC2, SS, LSM); `state` is loose, intermediate or dense from the designation.
- `read_flags`: a short token for anything you were unsure about in that row (damaged glyph, ambiguous decimal, spelling), empty if the row read cleanly.
- `source_locator`: `1968 AM-68-1 Table 2-3, printed 2-16, PDF 41, row N`.

Then, under a heading "Header and footnotes", give the column headers exactly as printed (including the symbol used for mean grain size and the superscript footnote markers) and the three footnotes verbatim. Under "Reading notes", list every cell you were not certain of and what the alternatives are.
