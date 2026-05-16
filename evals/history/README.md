# Calibration history

The current calibration writeup lives at [`../calibration.md`](../calibration.md) and the per-row hand-grade data is in [`../calibration_partial_worksheet_v2.md`](../calibration_partial_worksheet_v2.md). Those two files are what you should read.

The files in this folder are earlier iterations kept for the story they tell, not for active reference. Each one documents a step on the way to the rubric and methodology that ended up shipping.

## What's here

- **`calibration_key.md`** — Original 10-row "easy regime" calibration sample, scored under judge v1's rubric (the four-bucket version with the muddled 0.7 "thin or imprecise" bucket). Reported 100% within-one-bucket agreement, which was technically correct and operationally misleading: the sample contained no partial-credit rows, so the calibration could not detect central-tendency bias in the middle bucket it was using to score itself.
- **`calibration_worksheet.md`** — Blind hand-grading worksheet for the v1 sample, with per-row scores from the human grader. Pairs with `calibration_key.md`.
- **`calibration_partial.md`** — Second-pass calibration writeup using an 18-row sample drawn from real failure modes in the v5 run. Scored under v1's rubric. Showed judge v1 at 67% exact-match agreement vs human, which under matched-rubric anchoring later turned out to be 39%.
- **`calibration_partial_key.md`** — Per-row hand-grades for the 18-row sample, scored under v1's rubric. Superseded by `calibration_partial_worksheet_v2.md` after the rubric got re-anchored.
- **`calibration_partial_worksheet.md`** — The worksheet that produced `calibration_partial_key.md`. Same v1-rubric grades.

## Why keep them

Two reasons.

First, the methodology lesson in `calibration.md` ("if you score the judge under a different rubric than the one it uses, you get apples-to-oranges agreement numbers") only makes sense if you can see the original apples-to-oranges comparison. Deleting these files would erase the evidence behind the lesson.

Second, the rubric evolution narrative (v1 → v1.1 drafted-and-deleted → v2/v3 drafts → v2 shipped) is the most-likely interview question on this work. The files here are the receipts.
