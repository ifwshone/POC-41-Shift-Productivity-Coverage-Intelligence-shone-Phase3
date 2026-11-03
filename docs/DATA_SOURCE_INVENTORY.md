# Data Source Inventory

## Project
POC-41 - Shift Productivity & Coverage Intelligence (Phase 2 repo: `POC-41-Shift-Productivity-Coverage-Intelligence-shone-Phase2`; live: Render URL `poc-41-shift-productivity-coverage-rit9.onrender.com`).

## Existing Application Data Flow
`frontend/app/page.tsx` holds a hard-coded `mockDatabase` (2 facilities x 3 teams) and a 5-date array. The page reads it directly (`useMemo`); filters (Location / Team / Time Horizon) only select from it. "Last 30 Days" and "Year to Date" are produced in the browser by `buildSeries()` from a sine-based `seeded()` function, interpolating around the 5 real points. The CSV export is built client-side. The frontend **never calls the backend**. `backend/main.py` exposes `GET /api/v1/intelligence/coverage`, which generates 21 synthetic rows (NumPy seed 42); `backend/mock_data.json` is an empty (0-byte) fallback.

| Source | Type | Access Method | Current Usage | Raw Size | Record Count | Sensitivity | Phase 3 Decision |
|---|---|---|---|---:|---:|---|---|
| `mockDatabase` + `dates` in `frontend/app/page.tsx` | synthetic (hard-coded) | static file, parsed by regex | Drives every chart/marker/KPI on the page | ~2.2 KB | 30 daily rows (6 nodes x 5 days) + 6 node KPIs/insights | Synthetic | **Use** |
| `generate_synthetic_shift_data()` in `backend/main.py` | synthetic generator | function body extracted via `ast`, run with seed 42 | `/api/v1/intelligence/coverage` (not called by UI) | ~2.2 KB | 21 (7 days x 3 shifts) | Synthetic | **Use** |
| `backend/mock_data.json` | JSON | file | Fallback only | 0 B | 0 | n/a | Exclude (empty) |
| `buildSeries()` 30-day / YTD output in `page.tsx` | derived in browser | computed at render | "Last 30 Days"/"Year to Date" views | n/a | 30 / 10 per node | Synthetic | **Exclude** - interpolated padding, adds no independent information |

## Excluded Sources
Interpolated 30-day/YTD series (above); empty `mock_data.json`; repository screenshots (`*.png`) and test reports (not data).

## Licensing or Access Notes
All data is authored within the project. No external API, licence, key or login is involved. The live Render URL was not reachable from the build sandbox; it is not needed (no runtime data fetch).

## Data Risks
- Synthetic only: no real operational conclusions; every row has `is_synthetic=true`.
- Two sources use different vocabularies (UI `Warning` vs backend `Strained`) - normalised to `warning`.
- Backend rows have no facility; they are shift-level and are not merged into facility rows.
- Frontend and backend values are unrelated generators; do not compare them as one series.
- No personal data, secrets or restricted data found; `.env` is git-ignored.

## Selected Phase 3 Source
Both synthetic sources above, extracted into `data/source-sample/source_sample.csv` (51 rows x 13 columns).
