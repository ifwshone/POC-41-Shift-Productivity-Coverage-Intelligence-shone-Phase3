# Post #6 Evidence Reconciliation Checklist

Fill each item with an OBSERVED result only. Do not copy expected values.
Date verified: ____  Verified by: ____

| # | Item | Code change (in patch) | Observed result (fill in) |
|---|------|------------------------|---------------------------|
| 1 | Validator has no hard-coded numeric allowances | assistant/core/output_validator.py | pytest tests/assistant-grounding output: ____ |
| 2 | Invented values (7, 28, 2026, 119.9, 100.0) rejected | test_validator_no_allowances.py | ____ |
| 3 | Backend Docker build from repo root | docker-compose.yml (context ., dockerfile backend/Dockerfile) | `docker compose build` log: ____ |
| 4 | Backend packages present (google-genai etc.) | check backend/requirements.txt | `pip check` / container import: ____ |
| 5 | Real Gemini success | GEMINI_API_KEY set | response with llm_status=____, timestamp ____ |
| 6 | Deterministic fallback | unset key / force failure | response with llm_status=____ |
| 7 | Intelligence page: KPI strip, selectable bars, detail panel, five observations | frontend/app/intelligence/page.tsx | screenshot: ____ |
| 8 | Selected finding opens assistant with scoped question | AssistantPanel initialQuestion | screenshot/video: ____ |
| 9 | Synthetic wording on operations page | frontend/app/page.tsx | screenshot: ____ |
| 10 | Deployed URL and commit SHA | n/a | URL ____ SHA ____ |
| 11 | Frontend + backend + certification tests | run_phase3_checks.py --regen | counts: ____ |
| 12 | Fresh Repomix | `npx repomix` | file/date: ____ |

After filling: update release manifest, UAT, deployment evidence, completion report and stale B1/B2 findings to match this table.
