# /data - Canonical Data Package (POC-41 Shift Productivity & Coverage Intelligence)

Phase 3 - Post #1. Version **1.0.0**. All data is **synthetic** (the app has no live or personal data source).

| Path | Purpose |
|---|---|
| `canonical/intelligence_data.csv` | **Single source of truth** - 20 mandatory columns, long format |
| `published/intelligence_data.json` | Generated from the canonical CSV (never edit by hand) |
| `source-sample/source_sample.csv` | Flat extract of the app's own synthetic data (full population, no reduction needed) |
| `manifest.json` / `schema.json` | Package metadata and column contract |
| `quality/` | `data_profile.json`, `validation_report.json`, `sampling_report.md`, `pipeline_stats.json` |

## Regenerate and validate (needs Python 3.10+, `pandas`, `numpy`)

```bash
pip install pandas numpy
python scripts/data_pipeline/run_pipeline.py     # extract -> sample -> standardize -> publish -> profile -> validate
python scripts/data_pipeline/validate_data.py    # validation only
```

Never hand-edit files under `/data`; change the scripts and regenerate. The pipeline is deterministic (seed 42), so a rerun leaves `git diff` empty.

## Canonical row types

- `measurement` - one dated metric reading (`output_per_hour`, `overtime_hours`, `attendance_rate`)
- `entity` - one headline KPI + insight text per facility/team node (`kpi_output_per_hour`, undated snapshot)

Details: `docs/CANONICAL_DATA_MAPPING.md`, `docs/DATA_SOURCE_INVENTORY.md`, `docs/SAMPLING_AND_REDUCTION_REPORT.md`, `docs/CANONICAL_DATA_PACKAGE_VALIDATION.md`.
