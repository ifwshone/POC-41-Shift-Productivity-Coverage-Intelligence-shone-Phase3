# POC-41 Shift Productivity & Coverage Intelligence

Operational shift-productivity map (Phase 2) extended in Phase 3 with a reproducible canonical dataset, a comparative analytical track, a Data Intelligence page and a bounded data assistant. **All data is synthetic.**

> **Release status: Phase 3 certification review result — FINAL CHANGES REQUIRED** (2026-11-06). Not yet tagged. See `docs/PHASE3_CERTIFICATION_FINDINGS.md`. Live URL: *not yet validated*.

## Phase 2 capability (unchanged)
`/` — interactive radar map: six markers (Facility A/B × Morning/Evening/Night Watch) showing output per hour with Optimal / Warning / Critical status; Location, Team and Time Horizon selectors drive an intelligence sidebar (output trend, overtime chart, insight text) and a CSV export. Data comes from an in-file synthetic `mockDatabase`; the 30-day and year-to-date views are interpolated in the browser for display only.

## Phase 3 capability
- **Canonical data** `data/canonical/intelligence_data.csv` — 129 rows × 20 columns, **data version 1.0.0**, rebuilt from a 51-row source sample by `scripts/data_pipeline/run_pipeline.py` (39 validation checks, byte-reproducible).
- **Analytical track** Track A — Comparative Intelligence, **method version 1.0.0**: gap of each facility/team's average output and overtime versus the overall baseline (119.4 units/hr, 20.2 overtime hrs); ranked by output gap.
- **Data Intelligence page** `/intelligence` — summary, gap chart, ranking table with category filter, methodology and limitations, loading/error/empty/stale states, contract validation.
- **Assistant** Mode B (deterministic + optional LLM explanation). Answers only five bounded questions about approved results; refuses everything else. Works without an API key (deterministic only).

## Architecture summary
Source (frontend mock + backend generator) → pipeline → canonical CSV → Track A scripts → `intelligence_*.json` → copied to `frontend/public/data/intelligence/` → Data Intelligence page. The assistant (FastAPI router + `assistant/`) reads the same outputs. Details: `docs/PHASE3_FINAL_ARCHITECTURE.md`.

## Technology stack
Next.js (App Router), React, Tailwind CSS, Recharts · FastAPI, pandas, numpy · Python data pipeline · pytest, Selenium, Jest · Docker.

## Routes
`/` operational · `/intelligence` Data Intelligence · `POST /api/assistant/query` · `GET /api/v1/intelligence/coverage`.

## Setup, validation and tests
```bash
# data and analytics (verified)
python scripts/data_pipeline/run_pipeline.py
python data-science/scripts/run_analytical_track.py
python data-science/scripts/validate_analytical_track.py
python scripts/copy_intelligence.py
python scripts/certification/run_phase3_checks.py --regen

# application (confirm in a networked environment)
cd frontend && npm ci && npm run build && npm start     # http://localhost:3000
```
Full test sequence: `docs/FINAL_AUTOMATED_TEST_REPORT.md`. Environment variables: `GEMINI_API_KEY` (optional), `GEMINI_MODEL`, `NEXT_PUBLIC_API_URL` — see `docs/PHASE3_HANDOVER_GUIDE.md`. Do not commit `.env`.

## Build and deployment
`docker compose build && docker compose up` — **currently not working for the backend** (finding B2). No deployment target or live URL has been validated yet.

## Documentation index
Release manifest · clean-clone report · final analytical revalidation · build/environment validation · final operational regression · final Data Intelligence validation · final assistant validation · automated test report · final UAT · deployment validation · final architecture · completion report · handover guide · findings register — all under `docs/` (`PHASE3_*`, `FINAL_*`, `*_VALIDATION_REPORT.md`). Earlier Post #1–#5 documents remain in `docs/`. Evidence: `final-evidence/`.

## Limitations and safety
Synthetic data only; frontend (facility-team) and backend (shift) data are different scopes and are never combined; ranking uses output gap only (overtime is context, not a risk score); descriptive 5-day view, no statistical significance; no forecasting or prediction; not for real staffing or payroll decisions. The assistant refuses out-of-scope, predictive and unsafe questions and is designed to reject LLM text containing numbers not in the approved evidence; the current numeric check has a known gap (finding B1) that must be fixed before this claim can be relied on.

`UAT_CHECKLIST.md` and `VAR_REPORT.md` predate the current layout and are retained for history only.
