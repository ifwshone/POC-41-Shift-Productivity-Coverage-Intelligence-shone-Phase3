# /docs/INTELLIGENCE_OUTPUT_CONTRACT.md
| Field | Purpose | Required |
|---|---|---|
| result_id | Unique identifier (e.g., RES-COMP-facility_a_night_watch) | Yes |
| result_type | ranking | Yes |
| record_id | Null (aggregated metric) | No |
| entity_id | Related canonical entity (e.g., facility_a_night_watch) | Yes |
| group_key | Team category (e.g., night_watch) | Yes |
| period_start | 2026-10-24T00:00:00Z | Yes |
| period_end | 2026-10-28T00:00:00Z | Yes |
| metric_name | output_gap_vs_baseline | Yes |
| result_value | Numeric difference from baseline | Yes |
| result_unit | units_per_hour | Yes |
| result_category | "low" (below baseline) or "high" (above baseline) | Yes |
| priority_rank | Integer (1 = highest priority for review) | Yes |
| finding | Short validated interpretation | Yes |
| evidence | Row count and baseline factors used | Yes |
| method_version | 1.0.0 | Yes |
| data_version | 1.0.0 | Yes |
| generated_at | ISO 8601 generation time | Yes |
| quality_status | validated | Yes |
| limitation | Synthetic and descriptive limitation warning | Yes |