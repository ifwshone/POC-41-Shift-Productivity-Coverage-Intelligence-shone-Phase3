## Project: POC-41 Shift Productivity & Coverage Intelligence
## Canonical Data Version: 1.0.0
## Confirmed Data Archetype: Time-Series Measurement (short)
## Target User: Shift operations manager
## Primary Analytical Question: Across Facility A and B, which team's output per hour and overtime hours differ most from the other groups during 2026-10-24 to 2026-10-28?
## Decision to Be Supported: Which facility/team to review first for supervisor coverage.
## Approved Primary Track: A - Comparative
## Approved Supporting Track: B - Trend
## Input Fields: source_name, entity_id, metric_name, metric_value, observed_at
## Excluded Fields: Backend synthetic data (prevents mixed-scope leakage), UI status labels (downstream indicators).
## Baseline: Overall 5-day average for output and overtime across frontend nodes.
## Selected Method: Grouped mean aggregation and dense ranking by gap-to-baseline.
## Validation Approach: Independent recalculation, tie-handling checks, minimum group size (n>=5) validation.
## Expected Intelligence Results: Ranked priority JSON list by entity.
## Stop Conditions: If n < 5 for any frontend node.
## Known Limitations: Purely descriptive due to short 5-day time window. All data synthetic.
