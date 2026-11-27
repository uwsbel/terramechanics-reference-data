# Claude's answers (written before Codex ran)

1. **Canonical calibration.** The tick-based maps (Codex's on FC-2A to FC-4A). Rule change: a
   residual counts as evidence only over anchors that are printed marks (detected grid lines or
   measured ticks); a reading whose interior anchors were predicted from the frame cannot win on
   residual, and where both readings are anchored on printed marks the smaller residual decides as
   before. Mechanically: diff_curves reports the share of `predicted` lines, and the batch's
   overlays.csv may name the canonical reader with a reason (`canonical` column), recorded in the
   review. The arbiter confirms the direction (Codex's map 14 to 17 psf closer on FC-3A).
   Change my mind: if the sheets' peaks were themselves read with a frame-biased map.
2. **Triangle center.** The centroid: it is the geometric center drafters' templates are built on
   (the template hole's center is the triangle's center of mass for an equilateral triangle, and the
   centroid is also what a symmetric blob detector finds). The bound of a triangle should be at least
   the centroid-to-box-center offset (about h/6, 3 to 4 px) so that either convention agrees within
   bounds; readings already made under the bounding-box convention stand, and any disagreement that
   is exactly this offset is resolved as `both` in adjudication. Change my mind: evidence that the
   1968 drafters centered triangles on the box (for example triangles systematically off their line
   by the offset).
3. **Legend vs line.** The legend shape decides identity; the line is evidence but a drawn line can
   pass through another group's symbol near the axis (dashed extensions are extrapolations). The
   data-sheet comparison is legitimate and the strongest evidence available, because the envelope
   points are by definition the sheets' peaks; it settles all three FC-1A cases for Claude's
   assignment. The brief's rule should change to: shape first, line second, sheets when available.
4. **FC-2A.** Yes: rename at the canonical stage with the evidence, submissions untouched; the
   experiment rows `b68-ds-fc-2a-dr33-53` and `-dr115-130` keep their printed legend text but their
   notes (and `qa/experiments-vol2c-b1`) record that the printed legend is swapped, so the points
   attached to each row are the correct density group; `insights/` gets a note, since a user
   reading the printed figure would draw the wrong conclusion (loose stronger than dense).
5. **FC-7B/7C.** Yes: the reading is the pixels and the calibration; `apply` is a deterministic
   transformation; re-deriving it with a fixed tool changes no judgment of the reader, and keeping the
   derived file under qa/ with the reason leaves the submission immutable.
