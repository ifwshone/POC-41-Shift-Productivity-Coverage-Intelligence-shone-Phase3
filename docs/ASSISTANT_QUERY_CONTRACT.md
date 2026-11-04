# Assistant Query Contract
## Supported Intents: `list_priority_items`, `explain_result`, `explain_limitation`, `explain_method`, `get_data_freshness`.
## Allowed Parameters: `entity_id` (string), `limit` (integer 1-25), `result_category` (string).
## Query Functions: `get_priority_items()`, `get_result_explanation()`, `get_limitations()`, `get_methodology()`, `get_freshness()`.
## Approved Sources: `intelligence_results.json`, `intelligence_summary.json`.
## Evidence Fields: `factor`, `value`, `result_id`, `priority_rank`, `finding`.
## Result Limits: Maximum 10 items returned per query, max 300 character excerpts.
## Error Responses: Returns `{"status": "error", "message": "..."}` matching Grounded Contract.
## Out-of-Scope Handling: Hard refusal, returning `suggested_follow_ups`.
## Unsafe Handling: Returns `{"status": "unsafe", "answer": "Request blocked by security policy."}`
## Version Behaviour: Returns `data_version` and `method_version` alongside every payload.