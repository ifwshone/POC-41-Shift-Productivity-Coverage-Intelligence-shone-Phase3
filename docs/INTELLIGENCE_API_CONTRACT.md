# /docs/INTELLIGENCE_API_CONTRACT.md
## Integration Pattern
Pattern B (Static Generated JSON)
## Source Files
`/data-science/outputs/intelligence_results.json`, `/data-science/outputs/intelligence_summary.json`
## Generated Files
`/frontend/public/data/intelligence/intelligence_results.json`, `/frontend/public/data/intelligence/intelligence_summary.json`
## Endpoints or Static Paths
`GET /data/intelligence/intelligence_results.json`
`GET /data/intelligence/intelligence_summary.json`
## Request Parameters
None (Static)
## Result Item Contract
Requires `result_id`, `result_type`, `metric_name`, `result_value`, `finding`, `evidence`, `data_version`, `method_version`, `generated_at`, `quality_status`, `limitation`.
## Pagination
Client-side scroll (max 6 items for Track A).
## Sorting
Client-side (pre-sorted ascending by `priority_rank` in JSON).
## Filtering
Client-side array filtering by `result_category`.
## Error Responses
Contract validation throws strict Error caught by React boundary. HTTP 404 handled gracefully.
## Version Validation
Cross-references `summary.data_version` against `results[].data_version`.