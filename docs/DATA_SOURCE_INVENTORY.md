# Data Source Inventory

## Project
POC-41 - Shift Productivity & Coverage Intelligence (Phase 2 repo: `POC-41-Shift-Productivity-Coverage-Intelligence-shone-Phase2`; live: Render URL `poc-41-shift-productivity-coverage-rit9.onrender.com`).

## Existing Application Data Flow
`frontend/app/page.tsx` reads a hard-coded `mockDatabase` directly; Location / Team / Time Horizon filters only select from it. The frontend never calls the backend. The CSV export is built in the browser. "Last 30 Days" and "Year to Date" are interpolated in the browser from the 5 real points (excluded, see below). `backend/main.py` serves `GET /api/v1/intelligence/coverage` from a seeded generator; `backend/mock_data.json` is an empty fallback.

| Source | Type | Access Method | Current Usage | Raw Size | Record Count | Sensitivity | Phase 3 Decision |
|---|---|---|---|---:|---:|---|---|
| `frontend/app/page.tsx` (`mockDatabase`, `dates`) | Synthetic, static | In-file constant, parsed by regex (not executed) | Drives all map markers, KPIs and charts; update pattern: static | ~2.2 KB | 30 daily rows + 6 node KPI/insight records | Synthetic | Use |
| `backend/main.py` (`generate_synthetic_shift_data`) | Synthetic generator, seed 42 | Function extracted via `ast` and run locally | `/api/v1/intelligence/coverage` (not called by the UI); update pattern: generated on request, deterministic | ~2.2 KB | 21 | Synthetic | Use |
| `backend/mock_data.json` | JSON | File | Fallback only | 0 B | 0 | n/a | Exclude (empty) |
| `buildSeries()` 30-day / YTD output | Derived in browser | Computed at render | Time Horizon views | n/a | 30 / 10 per node | Synthetic | Exclude (interpolated padding) |

## Source Granularity & Downstream Analytics Caution
- **Frontend source:** facility/team operational state over 5 dates (2 facilities x 3 teams x 5 dates = 30 rows, 2026-10-24 to 2026-10-28).
- **Backend source:** shift-level records over 7 dates (7 dates x 3 shifts = 21 rows, 2026-10-24 to 2026-10-30) with no facility field; it also carries `attendance_rate` and `coverage_status`, which the frontend lacks.
- **Analytical distinction:** the two streams have different scopes and independent generators. They are kept together in the canonical file for completeness (separated by `source_name`, `entity_id` and `subcategory`), but later Phase 3 work must analyse each according to its own scope and must not concatenate them into one continuous time series.

## Excluded Sources
Interpolated 30-day/YTD series (above); empty `mock_data.json`; repository screenshots (`*.png`) and test reports (not data).

## Licensing or Access Notes
All records are synthetic with deterministic seeds; nothing is scraped. All data is authored within the project. No external API, licence, key or login is involved. The live Render URL was not reachable from the build sandbox; it is not needed (no runtime data fetch).

## Data Risks
- Synthetic only: no real operational conclusions; every row has `is_synthetic=true`.
- Two sources use different vocabularies (UI `Warning` vs backend `Strained`) - normalised to `warning`.
- Backend rows have no facility; they are shift-level and are not merged into facility rows.
- Frontend and backend values are unrelated generators; do not compare them as one series.
- No personal data, secrets or restricted data found; `.env` is git-ignored.

## Selected Phase 3 Source
Both synthetic sources above, extracted into `data/source-sample/source_sample.csv` (51 rows x 13 columns).
