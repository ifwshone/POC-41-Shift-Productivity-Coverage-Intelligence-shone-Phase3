# /docs/DATA_INTELLIGENCE_UI_SPEC.md
## Route and Navigation
`/intelligence`. Accessed via top-right "Data Intel" button on the operational view.
## Page Header
Displays title, current analytical track, method version, data version, and ISO generation date. Includes back navigation.
## Summary Cards
Two cards: "Key Findings" (bullet list) and "Priority Review Items" (inline tags).
## Filters
HTML Select dropdown filtering by `result_category` (All, High, Low).
## Primary Intelligence View
Tabular ranking of Comparative track outputs.
## Results / Priority Table
Columns: Rank, Entity, Output Gap, Finding, Evidence (n).
## Evidence Panel
Rendered inline in the table under Evidence column.
## Methodology
Bottom panel displaying primary question and validation status.
## Limitations
Bottom panel rendering important constraints from summary and results.
## Data Freshness
Generated ISO string displayed in header.
## Loading State
Full screen "Validating Contract & Loading Intelligence..." indicator.
## Error State
Full screen red text boundary "Integration Blocked" displaying exact validator rejection reason.
## Empty State
Dashed container "No results match active filters."
## Stale State
Yellow banner "Stale Versions Detected" in header if version mismatch occurs.
## Responsive Layout
Single column on mobile, horizontal scroll for table, side-by-side methodology/limitations on desktop.