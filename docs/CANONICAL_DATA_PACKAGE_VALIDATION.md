# Canonical Data Package Validation

Command: `python scripts/data_pipeline/validate_data.py` (or `run_pipeline.py` for the full chain). Full machine-readable results: `data/quality/validation_report.json`.

## Result: PASS (39 / 39 checks)

| Area | Result |
|---|---|
| Total `/data` size | 0.12 MB (limit 10 MB) |
| Largest file | `published/intelligence_data.json` 0.07 MB (limit 5 MB) |
| Source sample | 51 rows x 13 columns, 0.009 MB |
| Canonical CSV | 129 rows x 20 columns, 0.031 MB |
| Required columns and order | All 20 present in the mandated order; lowercase snake_case; UTF-8, no BOM |
| `record_id` | Non-null and unique (129) |
| Types and dates | `observed_at` all ISO 8601 (`...T00:00:00Z`); `metric_value` numeric; lat/long blank (not applicable) |
| Flags | `source_name`, `is_synthetic` (all `true`), `data_version` (`1.0.0`) populated on every row |
| Manifest consistency | Counts, column count, sizes, version, synthetic flag, source names and paths all match the files |
| Published JSON | Equals the canonical CSV (129 records) and is regenerated, not hand-edited |
| Reproducibility | Canonical CSV and JSON regenerate byte-identically from the source sample; a clean copy of the repo reproduced every data file byte-for-byte |
| Safety scans | No e-mail addresses, secret patterns, absolute paths or binary files in `/data` |

## Build and deployment readiness
- Existing app files (`frontend/`, `backend/`) are **unchanged**; this post only adds `/data`, `/scripts/data_pipeline`, `/docs`.
- The app does not read `/data` at runtime and needs no live API, so deployment is unaffected. `package.json` was deliberately not given a `prebuild` hook: the frontend Docker build context is `./frontend` and the Node image has no Python.
- Local `npm ci && npm run build` and the Render deploy must be confirmed on your machine (see submission notes); the cloud sandbox used here could not complete `npm ci` (npm crashed) and could not reach the live URL.
