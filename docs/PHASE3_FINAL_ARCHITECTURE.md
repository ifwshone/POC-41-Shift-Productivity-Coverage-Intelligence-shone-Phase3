# Phase 3 Final Architecture

Describes the system **as delivered and inspected** (not as aspired). Divergences from the intended design are marked ⚠ and tracked in `PHASE3_CERTIFICATION_FINDINGS.md`.

## System Context
POC-41 Shift Productivity & Coverage Intelligence: a Next.js operational map (Phase 2) extended in Phase 3 with a reproducible canonical dataset, a Track A comparative analysis, a static-JSON Data Intelligence page and a bounded Mode B assistant. All data is synthetic.

## Repository Structure
`frontend/` Next.js app · `backend/` FastAPI (synthetic shift API + assistant router) · `assistant/` deterministic query/validation modules · `data/` canonical package · `scripts/data_pipeline/` pipeline · `data-science/` analytics scripts, notebooks, outputs · `docs/` · `tests/` · `scripts/certification/` (Post #6) · `final-evidence/`.

## Operational Application
`/` radar map: 6 markers (Facility A/B × Morning/Evening/Night), Location/Team/Time selectors, intelligence sidebar, CSV export. Reads an in-file synthetic `mockDatabase`; does not call the backend. 30-day/YTD views are interpolated for display.

## Source Data
Two separate synthetic scopes: frontend `mockDatabase` (facility-team level, 5 daily points) and backend generator (`main.py`, seed 42; shift level, 7 days). Never pooled.

## Sampling and Standardisation
Pipeline: extract (51 rows) → sample (full population retained) → standardise (129 rows × 20 columns) → publish JSON/schema/manifest → profile → validate. Seed 42. Deterministic.

## Canonical Data Contract
`data/canonical/intelligence_data.csv` — 20 mandatory columns in fixed order (`record_id` … `data_version`); `data/schema.json`, `data/manifest.json`; 39 validation checks including size, privacy, secrets, absolute paths and byte-for-byte reproducibility.

## Data Validation and Readiness
Post #2 outputs: quality PASS, representativeness PASS (scope-limited), archetype Time-Series Measurement + Entity Snapshot, readiness "DATA READY FOR ANALYTICAL TRACK DEVELOPMENT".

## Approved Analytical Track
Track A — Comparative Intelligence.

## Analytical Method and Baseline
Frontend measurement rows only; baseline = overall mean (output 119.4, overtime 20.2); gap = group mean − baseline; dense rank ascending on output gap (lowest output = rank 1); overtime is context only. Independent recomputation in `validate_analytical_track.py`. Method 1.0.0.

## Intelligence Output Contract
`intelligence_results.json` (19 fields per result incl. evidence, limitation, versions, `generated_at`, `quality_status`), `intelligence_summary.json`, `validation_metrics.json`. Contract defined in `docs/INTELLIGENCE_OUTPUT_CONTRACT.md`.

## API or Static Adapter
Pattern B: static JSON copied into `frontend/public/data/intelligence/` and fetched by the browser. ⚠ Copy is a manual script with no build hook; copies were found stale (B4).

## Data Intelligence Page
`/intelligence`: summary cards, bar chart, filterable ranking table, methodology and limitations, loading/error/empty/stale states, client-side contract validation. ⚠ Baseline and evidence drill-down not shown (M1).

## Assistant or Approved Skip
Approved Mode B. Pipeline: scope guard (blocklist) → rule-based intent classifier → parameter validator (catalog) → deterministic query over `data-science/outputs/*` → optional Gemini explanation → output validator (blocked claims, rank check, numeric check) → composed response with evidence, versions and limitation. Failure of the LLM returns the deterministic answer. ⚠ Numeric validator whitelists fixed numbers (B1); ⚠ routing/injection gaps (M2, M3). Assistant reads `data-science/outputs/` while the page reads the public copy (B4).

## Authentication and Security Boundary
No authentication; synthetic data only. Secrets only via environment (`GEMINI_API_KEY`). ⚠ CORS `*` with credentials (M9). Assistant is read-only, session-less (`persistent_memory_enabled: false`), question length ≤ 500.

## Runtime and Deployment
Frontend Docker (Node 20, multi-stage), backend Docker (Python 3.11), `docker-compose.yml`. ⚠ Backend image cannot import the assistant package (B2). No target platform recorded.

## Versioning
`data_version` 1.0.0 (manifest, CSV, outputs); `method_version` 1.0.0 (hard-coded in two scripts); ⚠ no application version (B8). Release tag `phase3-v1.0.0` prepared, not created.

## Testing
pytest (data, contract, assistant unit/grounding/safety/API, Selenium UI/regression), Jest (not runnable), certification checker, final Selenium journey. See `FINAL_AUTOMATED_TEST_REPORT.md`.

## Failure Handling
Pipeline exits 1 on any failed check; page blocks on invalid contract; stale/mismatch banners; assistant degrades to deterministic output on LLM failure or rejection.

## Known Limitations
Synthetic data; 5 daily points per group; descriptive only (no significance, no forecast); ranking by output gap only; frontend and backend scopes separate; 30-day/YTD views not covered by analytics; assistant answers only five bounded intents.
