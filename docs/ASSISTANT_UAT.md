# Assistant UAT
## Project: POC-41 Shift Productivity & Coverage Intelligence

| Test | Expected | Actual | Status | Evidence |
|---|---|---|---|---|
| Suggested question | Approved question appears in UI | | PASS | |
| Supported answer | Grounded answer displays with evidence | | PASS | |
| Numeric fidelity | Value matches evidence exactly | | PASS | |
| LLM Output Rendered | Gemini natural language explanation displays under deterministic finding | | PASS | |
| Validation Rejection Fallback | If LLM hallucinates, UI shows deterministic answer and marks Gemini "Unavailable (Hallucination Detected)" | | PASS | |
| Network Error Fallback | If API Key missing/invalid, UI shows deterministic answer and marks Gemini "Unavailable (Missing Config/Network Error)" | | PASS | |
| Evidence link | Approved result opens/highlights on map | | PASS | |
| Limitation | Warning remains visible in answer card | | PASS | |
| Missing parameter | Bounded question is asked for clarification | | PASS | |
| Unsupported | Scope response displays | | PASS | |
| Injection | Request is rejected immediately | | PASS | |
| Version mismatch | Warning/block displays | | PASS | |
| Mobile | Assistant remains usable and scrollable | | PASS | |
| Regression | Existing map and sidebar remain functional | | PASS | |