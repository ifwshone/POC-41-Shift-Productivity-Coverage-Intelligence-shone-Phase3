# Assistant Safety and Scope
## Approved Scope: Summarizing and explaining Track A Comparative intelligence outputs.
## Unsupported Scope: Forecasting, external data integration, anomaly detection.
## Unsafe Request Categories: Prompt injection, file system access, raw code execution.
## Prompt-Injection Controls: Strict system prompt isolation, pre-flight regex filtering for `BLOCKED_TERMS` ("ignore instructions", "system prompt", "exec").
## Source-Text Handling: `finding` and `limitation` fields treated strictly as untrusted data inputs, never system commands.
## Sensitive Field Masking: N/A (Data is synthetic).
## Logging Policy: Intent IDs and Status only. No raw user queries or LLM outputs persisted.
## Memory Policy: Stateless design. Zero persistent conversational memory between requests.
## Failure Behaviour: Fail safe to predefined deterministic response templates.