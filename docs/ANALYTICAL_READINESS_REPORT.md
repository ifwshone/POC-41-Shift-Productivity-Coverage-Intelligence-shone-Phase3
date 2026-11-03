# Analytical Readiness Report

## Target User
Shift operations manager responsible for staffing and coverage.

## Canonical Data Version
1.0.0 (unchanged in Post #2; no canonical correction was required).

## Confirmed Data Archetype
Time-Series Measurement (short) with Entity Snapshot secondary. See `DATA_ARCHETYPE_CONFIRMATION.md`.

## Primary Analytical Question
Across Facility A and B, which team's output per hour and overtime hours differ most from the other groups during 2026-10-24 to 2026-10-28, and how consistent is that gap day to day?

## Decision to Be Supported
Which facility/team to review first for supervisor coverage and overtime allocation (demonstration decision on synthetic data).

## Data Coverage Summary
129 rows, 20 columns, all synthetic. 6 facility-team nodes x 5 days (frontend) and 3 shifts x 7 days (backend), 2026-10-24 to 2026-10-30. No geography, stages, relationships or scenarios; 6 text values.

## Quality Summary
Post #1 validation PASS (39/39); quality assessment PASS with 0 blocking issues; 129/129 values match the source sample. Five non-blocking observations are listed in `DATA_QUALITY_ASSESSMENT.md`.

## Representativeness Summary
PASS for the 7-day comparative view. Full population retained; no sampling bias, but the population is authored or random. 30-day and year-to-date views are not backed by data.

## Track Readiness Matrix
| Track | Status | Evidence | Missing Requirement | Recommendation |
|---|---|---|---|---|
| A - Comparative | SUPPORTED | 6 facility x team groups, each with 5 daily observations of output and overtime (frontend, facility-level); 3 shifts x 7 days in backend. Quality PASS, representativeness PASS. | Groups are small (5-7 observations): differences are descriptive, not statistically strong. Compare within a source only. | PRIMARY track. |
| B - Trend | CONDITIONAL | Ordered consecutive daily observations exist, but each series has only 5-7 points over one month (2026-10-24 to 2026-10-30). | Fewer than 12 ordered periods; no weekly/seasonal cycle; Last-30-Days and Year-to-Date views are interpolated by the UI, not in the data. | SUPPORTING track, descriptive direction over the 5-7 observed days only. No forecasting. |
| C - Risk & Priority | CONDITIONAL | Explainable factors exist (attendance_rate, output_per_hour, overtime_hours) plus a status label (optimal/warning/critical). | No documented urgency definition; status thresholds are implicit in UI code; backend status is random and unrelated to its metrics (OBS-3); attendance exists only in backend. | Conditional: only a transparent, rule-based frontend 'coverage review priority' using output, overtime and source-stated status, with documented weights. Not a score of real risk. |
| D - Anomaly | REJECTED | Largest comparable baseline is 7 observations per series. | Needs a meaningful baseline (>= 20 comparable observations); backend values are uniform-random, so extremes are generator noise and cannot be separated from errors. | Reject. |
| E - Segmentation | REJECTED | Only 9 entities (6 facility-team nodes, 3 shifts) and 3-4 informative numeric fields. | Segments of 6 nodes carry no business meaning beyond the existing team/facility grouping. | Reject. |
| F - Predictive | REJECTED | Predictive checklist below. | No genuine target (status is authored/random label), no real historical outcomes, <=7 observations per series, no validation split possible, no decision-time inputs, high leakage risk (status is a function of KPI in frontend). | Reject. Row count (129) does not justify prediction. |
| G - Simulation | REJECTED | No scenario records, no parameter columns, record_type 'scenario' absent. | Controlled inputs and comparable scenarios. | Reject. |
| H - Text & Theme | REJECTED | 6 text values, 6 unique, one per node. | Sparse, generic, authored insight sentences; no volume for themes. | Reject. |

## Recommended Primary Track
A - Comparative.

## Optional Supporting Track
B - Trend, descriptive over the 5-7 observed days only. Track C may be explored only as a transparent rule-based review-priority list, clearly labelled synthetic.

## Rejected Tracks
D - Anomaly, E - Segmentation, F - Predictive, G - Simulation, H - Text & Theme.

## Predictive Intelligence Decision
**REJECTED.** Checklist:
- Genuine target: No
- Historical examples: No
- Decision time availability: No
- No leakage: No
- Distribution reported: Yes
- Baseline definable: Yes
- Defensible validation: No
- Decision value: No
Row count does not justify prediction.

## Important Limitations
- All data synthetic; findings demonstrate method, not real operations.
- Frontend (facility-level) and backend (shift-level) are different scopes; never pool or concatenate.
- 5-7 daily points per series, one month only.
- Last-30-Days / Year-to-Date UI views are not backed by source data.
- Frontend status/KPI/text are authored; backend status is random.
- No geography, stages, relationships or scenarios.

## Required Controls for Post #3
- Read only data/canonical/intelligence_data.csv; filter by source_name first.
- Compare groups within a source; report n for every comparison.
- Label every output synthetic and descriptive; no forecast, anomaly flag or predictive score.
- No second dataset; any canonical fix goes through scripts/data_pipeline with a version bump and Post #1 re-validation.
- Do not alter the operational page.

## Final Result
DATA READY FOR ANALYTICAL TRACK DEVELOPMENT
