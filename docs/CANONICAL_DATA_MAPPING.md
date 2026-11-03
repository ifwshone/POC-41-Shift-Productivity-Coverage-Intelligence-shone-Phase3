# Canonical Data Mapping

Canonical file: `data/canonical/intelligence_data.csv` (129 rows x 20 columns, long format). Wide source columns become one `measurement` row per metric; each frontend node also gets one `entity` row.

| Source Field | Canonical Field | Transformation | Required | Example | Notes |
|---|---|---|---|---|---|
| (generated) | record_id | `REC-` + 5-digit sequence after deterministic sort | Yes | REC-00001 | Stable across reruns |
| (constant) | record_type | `measurement` for dated metrics, `entity` for node KPI | Yes | measurement | |
| record_date | observed_at | `YYYY-MM-DDT00:00:00Z`; blank for entity rows | No | 2026-10-24T00:00:00Z | Source has dates only, no time |
| facility + team / shift | entity_id | slug; `facility_a_morning_crew`, or `shift_morning` for backend | No | facility_a_morning_crew | |
| - | related_entity_id | blank (no relationships) | No | | |
| facility, team | entity_name | `Facility A - Morning Crew`; backend `Morning Crew (all facilities)` | No | | |
| team / shift | category | snake_case team | No | morning_crew | Backend Morning/Evening/Night mapped to the UI team names |
| facility | subcategory | snake_case facility; blank for backend | No | facility_a | |
| node_status / coverage_status | status | lowercase; `strained` -> `warning` | No | warning | |
| - | stage | blank (no lifecycle) | No | | |
| column name | metric_name | `output_per_hour`, `overtime_hours`, `attendance_rate`, `kpi_output_per_hour` | No | | |
| value column | metric_value | numeric, no symbols | No | 142.1 | |
| - | metric_unit | `units_per_hour`, `hours`, `ratio` | No | hours | |
| node_issue_text | text_value | trimmed to 500 chars; entity rows only | No | "Night shift coverage is critically strained..." | |
| - | latitude / longitude | blank (no geography in source) | No | | The screenshot's map is a schematic, not geographic |
| (constant) | source_name | Frontend mockDatabase (page.tsx) / Backend synthetic shift generator (main.py, seed 42) | Yes | | |
| source_row_id + metric | source_record_id | `FE|Facility A|Morning Crew|2026-10-24|output_per_hour` | No | | |
| (constant) | is_synthetic | `true` for all rows | Yes | true | |
| (constant) | data_version | `1.0.0` | Yes | 1.0.0 | Matches manifest |

## Removed fields and reason
None removed. `node_kpi_output_per_hour` and `node_issue_text` live on `entity` rows; `shift` is folded into `category`/`entity_id`.

## Derived fields and formulas
None computed (no analysis in this post). Record IDs and slugs only.

## Date and time conversions
`YYYY-MM-DD` -> ISO 8601 UTC midnight.

## Category standardization
Team/facility names -> lowercase snake_case; `Strained` -> `warning`; `Optimal`/`Critical` lowercased.

## Unit normalization
Output in `units_per_hour`, overtime in `hours`, attendance as `ratio` (0-1).

## Null handling
Empty string in CSV, `null` in JSON. Always populated: record_id, record_type, source_name, is_synthetic, data_version.

## Record-ID generation
Rows sorted by source, record type, entity, date, metric; IDs assigned sequentially. Deterministic.

## Text cleaning and truncation
500-character cap; none needed.

## Synthetic-data identification
`is_synthetic=true` on all 129 rows; manifest `contains_synthetic_data=true`.
