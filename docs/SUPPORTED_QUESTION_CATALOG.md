# Supported Question Catalog
## Target User: Shift Operations Manager
## Approved Assistant Mode: Mode B (Deterministic + LLM)
## Approved Track: Track A - Comparative
## Data and Method Versions: 1.0.0 / 1.0.0

| Question Pattern | Intent | Parameters | Query Function | Evidence | Limitation |
|---|---|---|---|---|---|
| "Which group ranks highest for review?" | `list_priority_items` | limit (int), result_category (high/low) | `get_priority_items` | output_gap, rank | Synthetic 5-day view only |
| "Why is [entity] flagged?" | `explain_result` | entity_id (string) | `get_result_explanation` | avg_output, avg_overtime | Score is not a combined risk metric |
| "What are the data limitations?" | `explain_limitation` | None | `get_limitations` | Important limitations list | N/A |
| "How was this calculated?" | `explain_method` | None | `get_methodology` | Track A baseline method | N/A |
| "When was this generated?" | `get_data_freshness` | None | `get_freshness` | generated_at timestamps | N/A |

## Unsupported Question Categories: Open-ended operational advice, predictive forecasting, individual worker surveillance, raw SQL queries.
## Suggested Questions: "Which team has the lowest output gap?", "Why is Facility A Night Watch ranked 1?", "What are the limitations of this report?"
## Catalog Version: 1.0.0