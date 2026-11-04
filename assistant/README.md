# Grounded Natural-Language Data Assistant (POC-41)

## Architecture Overview
This directory contains the Mode B (Deterministic + LLM) Data Assistant for the Shift Productivity & Coverage Intelligence dashboard. It operates as a strict natural-language explanation layer over the approved Post #3 deterministic intelligence outputs (Track A - Comparative). 

The assistant **does not** have unrestricted access to the canonical dataset, database, or arbitrary query execution tools. It routes natural-language questions to a predefined catalog of deterministic Python query functions.

## Request Lifecycle
1. **Scope Guard (`core/scope_guard.py`):** Pre-filters restricted terms and prompt injection attempts.
2. **Intent Classification (`core/intent_classifier.py`):** Maps the user's string to one of the 5 approved intents defined in `config/supported_intents.json`.
3. **Parameter Validation (`core/parameter_validator.py`):** Extracts and strictly bounds parameters (e.g., entity IDs, result limits) using `config/query_catalog.json`.
4. **Deterministic Retrieval (`queries/*`):** Executes fixed functions to retrieve data exclusively from `/public/data/intelligence/` JSON files.
5. **Evidence Builder (`core/evidence_builder.py`):** Constructs a strict JSON evidence package.
6. **LLM Generation:** The LLM receives the evidence package and `prompts/grounded_explanation_prompt.txt` to generate a natural-language response.
7. **Output Validator (`core/output_validator.py`):** Validates numeric fidelity against the evidence package and ensures the approved limitation text was preserved.
8. **Response Composer (`core/response_composer.py`):** Formats the final payload to the UI according to `docs/GROUNDED_RESPONSE_CONTRACT.md`.

## Security & Privacy
- **No Direct Data Access:** The LLM cannot query the source `/data/canonical/intelligence_data.csv`.
- **No Calculation:** The LLM is strictly prohibited from generating numbers, scores, or rankings not explicitly present in the evidence.
- **Stateless:** Zero conversational memory is retained between turns to prevent context poisoning.
- **Fail-Safe:** Ambiguous or out-of-scope queries return a deterministic `UNAVAILABLE` or `OUT_OF_SCOPE` template with suggested follow-ups.

## Testing
Run the assistant test suite from the repository root:
```bash
pytest tests/assistant-unit/
pytest tests/assistant-grounding/
pytest tests/assistant-safety/
pytest tests/assistant-api/
pytest tests/assistant-ui/