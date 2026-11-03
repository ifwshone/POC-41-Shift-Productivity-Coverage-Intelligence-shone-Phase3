# /docs/ANALYTICAL_METHOD_REPORT.md
## Project: POC-41 Shift Productivity & Coverage Intelligence
## Canonical Data Version: 1.0.0
## Method Version: 1.0.0
## Target User: Shift operations manager
## Analytical Question: Across Facility A and B, which team's output per hour and overtime differ most from the baseline?
## Decision to Be Supported: Review queue prioritisation for supervisor coverage.
## Approved Track: Track A - Comparative
## Baseline: Overall frontend mean for output (119.4) and overtime (20.2).
## Selected Method: Group-by aggregation (mean) across the 5-day observation window, followed by calculating the absolute difference from the baseline. Nodes are dense-ranked by their output gap (Rank 1 = largest negative gap).
## Data Leakage Assessment: UI-derived status labels and KPIs are strictly excluded from the inputs. Backend random statuses are excluded by source filtering.
## Intelligence Results: 6 facility-team nodes ranked by performance gap.
## Explainability: Direct mathematical comparison (Team Mean - Baseline Mean).
## Limitations: Purely descriptive. 5-day window lacks seasonality.
## Unsupported Uses: Not a predictive model. Does not forecast future output.