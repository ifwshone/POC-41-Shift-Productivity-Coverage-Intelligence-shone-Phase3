# /docs/INTELLIGENCE_INTEGRATION_MAPPING.md
| Post #3 Output Field | Service/API Field | UI Component | Display Rule | Fallback |
|---|---|---|---|---|
| `summary.key_findings` | `key_findings` | Summary Cards | Render as bulleted list | "No key findings available" |
| `summary.priority_items` | `priority_items` | Summary Cards | Render as badge tags | "No priority items" |
| `result.priority_rank` | `priority_rank` | Results Table | Render ascending int | "-" |
| `result.entity_id` | `entity_id` | Results Table | Render monospaced slug | "Unknown Entity" |
| `result.result_value` | `result_value` | Results Table | Render rounded float with sign | "N/A" |
| `result.finding` | `finding` | Results Table | Render as raw text | "No interpretation provided" |
| `evidence[factor='record_count']` | `evidence` | Results Table | Extract and display 'n' count | "n=N/A" |
| `result.limitation` | `limitation` | Limitations Panel | Display as warning | "No limitations noted." |