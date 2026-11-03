# Canonical Data Profile

## Project
POC-41 Shift Productivity & Coverage Intelligence. Source: `data/canonical/intelligence_data.csv` only. Machine-readable: `data-science/outputs/canonical_profile.json`.

## Canonical Data Version
1.0.0 (CSV and manifest agree).

## File Size
0.0313 MB.

## Dataset Dimensions
129 rows x 20 columns; 2 sources; 9 entities; 99 distinct metric values.

## Record-Type Distribution
`measurement` 123 (95.3%), `entity` 6 (4.7%). No event, process, scenario, node, edge or document rows.

## Source Distribution
Frontend `mockDatabase` 66 rows (facility-level); Backend synthetic generator 63 rows (shift-level, no facility).

## Synthetic / Non-Synthetic Distribution
129 synthetic, 0 non-synthetic.

## Field Completeness
Fully populated (0 nulls): record_id, record_type, entity_id, entity_name, category, status, metric_name, metric_value, metric_unit, source_name, source_record_id, is_synthetic, data_version.
Partly populated: observed_at (6 null = entity snapshot rows), subcategory (63 null = backend rows with no facility), text_value (123 null; 6 populated).
Fully empty by design: related_entity_id, stage, latitude, longitude (129 null each).

## Numerical Coverage
| Source :: metric | Unit | n | Min | Max | Mean | Median | Std |
|---|---|---:|---:|---:|---:|---:|---:|
| Frontend :: output_per_hour | units_per_hour | 30 | 85.0 | 142.0 | 119.40 | 121.0 | 15.21 |
| Frontend :: overtime_hours | hours | 30 | 5.0 | 45.0 | 20.23 | 19.0 | 11.53 |
| Frontend :: kpi_output_per_hour | units_per_hour | 6 | 95.2 | 142.1 | 121.58 | 123.45 | 17.22 |
| Backend :: output_per_hour | units_per_hour | 21 | 111.9 | 149.5 | 129.65 | 131.0 | 13.23 |
| Backend :: overtime_hours | hours | 21 | 5.7 | 38.9 | 20.44 | 17.5 | 11.06 |
| Backend :: attendance_rate | ratio | 21 | 0.85 | 0.98 | 0.907 | 0.90 | 0.040 |

Invalid or negative values: 0. Each metric has exactly one unit.

## Date and Time Coverage
123 dated rows, 100% parse as ISO 8601. Frontend 2026-10-24 to 2026-10-28 (5 days); backend 2026-10-24 to 2026-10-30 (7 days). No gaps in either span; one calendar month. 21 series (12 frontend with 5 points, 9 backend with 7 points). Largest single-date share 17.1%. 6 entity rows are undated snapshots.

## Category and Status Coverage
Team (`category`): morning/evening/night 43 each. Facility (`subcategory`): A 33, B 33, blank 63. Status: optimal 61, warning 48, critical 20. No near-constant field; only rare value is the metric `kpi_output_per_hour` (6 rows, 4.7%). No stage values exist.

## Geographic Coverage
No coordinates (0 valid pairs). The UI map is schematic.

## Text Coverage
6 non-null, 6 unique; average length 72.5, maximum 82 characters; none truncated.

## Important Observations
- Duplicate `record_id`: 0. Duplicate (source, entity, metric, date) keys: 0.
- Frontend and backend share metric names at different scopes; always filter by `source_name`.
- Series are short (5-7 points) and wholly synthetic.
