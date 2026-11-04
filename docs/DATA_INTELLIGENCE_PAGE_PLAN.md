
## Existing Application
Next.js App Router (React, Tailwind). Operational map tracking facility metrics.
## Existing Operational Route
`/`
## New Intelligence Route
`/intelligence`
## Approved Analytical Track
Track A - Comparative
## Primary Analytical Question
Across Facility A and B, which team's output and overtime differ most from the baseline?
## Decision to Be Supported
Supervisor coverage and overtime allocation review priority.
## Data Version
1.0.0
## Method Version
1.0.0
## Selected Integration Pattern
Pattern B - Static Generated JSON (Build-Time Copy to `public/data/intelligence/`).
## Page Sections
Header (Metadata), Summary Cards (Findings, Priorities), Filters (Category), Results Table (Ranking, Gap, Finding), Footer (Methodology, Limitations).
## Filters
`resultCategory` (High/Low)
## Results Table
Displays Rank, Entity ID, Output Gap vs Baseline, Finding text, and Record Count Evidence.
## Evidence Interaction
Evidence factors (n=count) are displayed directly in the table row.
## Loading / Error / Empty / Stale States
Loading screen visible during fetch/validation. Error boundary active for contract failures. Empty state triggered if filters yield zero results. Stale state banner visible if `data_version` mismatches between summary and results.
## Responsive Behaviour
Tailwind grid collapsing from multi-column to stacked layout on mobile. Tabular data enables horizontal scrolling.
## Testing Plan
Unit test `intelligenceValidator.ts`. UAT for visual layout. Selenium end-to-end regression to verify `/` remains intact.