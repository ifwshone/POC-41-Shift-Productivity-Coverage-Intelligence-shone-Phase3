# Assistant Architecture
## Existing Application: Next.js frontend, FastAPI backend.
## Assistant Mode: Mode B (Deterministic retrieval -> Evidence Package -> LLM summarization).
## Integration Route / Component: Slide-out `<AssistantPanel />` on `/intelligence` route.
## Scope Guard: Regex/Keyword boundary blocking restricted terms (SQL, system prompt, predict).
## Intent Classification: Rule-based routing mapping user text to 5 approved intents.
## Parameter Validation: Pydantic models enforcing type, bounds (e.g., limit <= 25), and entity_id enums.
## Query Catalog: Mapped in `/assistant/config/query_catalog.json`.
## Deterministic Retrieval: Python functions reading `/public/data/intelligence/` JSON files strictly.
## Evidence Builder: Constructs standard JSON package for the LLM context window.
## Optional LLM Explanation: Gemini/OpenAI API strictly prompted to format evidence into natural language without altering numbers.
## Response Validation: Output parser enforcing the Grounded Response Contract (answer, key_values, metadata, limitations).
## Authentication and Authorization: Inherits existing app middleware.
## Logging: Non-sensitive runtime logs (Intent, Status, Latency). No user-text logged.
## Error Handling: Safe fallback to `UNAVAILABLE` or `OUT_OF_SCOPE` templates.