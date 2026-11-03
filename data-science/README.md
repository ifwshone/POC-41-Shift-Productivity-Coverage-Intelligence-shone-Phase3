# /data-science - Post #2: Validation, Profiling & Analytical Readiness (POC-41)

Reads **only** `data/canonical/intelligence_data.csv` (version 1.0.0, 129 rows x 20 columns, all synthetic). No second dataset, charts, features or models are created. Outputs are JSON assessments and reports.

```bash
pip install pandas numpy
python scripts/data_pipeline/run_pipeline.py          # Post #1 package + validation (39 checks)
cd data-science/scripts
python profile_canonical_data.py                      # -> outputs/canonical_profile.json
python assess_data_quality.py                         # -> outputs/quality_assessment.json (re-runs Post #1 validation)
python assess_representativeness.py                   # -> outputs/representativeness_assessment.json
python assess_analytical_readiness.py                 # -> outputs/analytical_readiness.json
```

Run in that order (readiness reads the quality and representativeness outputs). The notebook `notebooks/01_canonical_data_validation_and_readiness.ipynb` is a read-only walkthrough of the same evidence.

Reports: `docs/CANONICAL_DATA_PROFILE.md`, `DATA_QUALITY_ASSESSMENT.md`, `REPRESENTATIVENESS_ASSESSMENT.md`, `DATA_ARCHETYPE_CONFIRMATION.md`, `ANALYTICAL_READINESS_REPORT.md`.

Result: **DATA READY FOR ANALYTICAL TRACK DEVELOPMENT** (Track A primary, B and C conditional, D-H rejected, predictive rejected). No canonical change was needed, so `data_version` stays 1.0.0.
