# Analytical Input Contract

| Canonical Field | Role | Transformation | Required | Decision-Time | Limitation |
|---|---|---|---|---|---|
| source_name | Filter / Scope | Filter strictly to "Frontend mockDatabase" | Yes | Yes | Excludes backend data to prevent mixed-scope leakage. |
| record_type | Filter | Filter to "measurement" | Yes | Yes | Excludes snapshot entities. |
| entity_id | Grouping dimension | None | Yes | Yes | Used to group teams by facility. |
| category | Grouping dimension | None | Yes | Yes | Team name identifier. |
| subcategory | Grouping dimension | None | Yes | Yes | Facility name identifier. |
| metric_name | Metric | Filter to output_per_hour, overtime_hours | Yes | Yes | Relies on synthetic readings. |
| metric_value | Measure | Averaged over 5 days | Yes | Yes | Small sample size (n=5). |