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
## LLM Integration: Uses `google-genai` Python SDK calling `gemini-3.5-flash-lite` configured securely via environment variables (`GEMINI_API_KEY`).
## LLM Prompting: Strictly prompted to format evidence into natural language without altering numbers.
## Response Validation: Grounded Output Validator enforces the Grounded Response Contract. Analyzes LLM text to ensure zero numeric hallucinations (every number generated must exist in the deterministic evidence package).
## Authentication and Authorization: Inherits existing app middleware.
## Logging: Non-sensitive runtime logs (Intent, Status, Latency). No user-text logged.
## Error Handling: Dual-layer fallback. If the LLM hallucinates, times out, or lacks credentials, the UI gracefully downgrades to display the authoritative Deterministic finding while flagging the LLM as unavailable. Out-of-scope queries return a deterministic `UNAVAILABLE` or `OUT_OF_SCOPE` template.