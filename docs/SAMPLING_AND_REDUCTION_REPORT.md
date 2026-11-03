# Sampling and Reduction Report

## Original Source
Frontend `mockDatabase` (30 daily rows) + backend synthetic generator (21 rows). Synthetic.

## Original Size
~4.4 KB (about 0.004 MB) of source payload.

## Original Record Count
51 daily source rows (plus 6 node KPI/insight records carried on the frontend rows).

## Original Column Count
13 (flat extract).

## Selected Sampling Method
`full_population_retained` - the population is 0.5% of the 10,000-row limit, so no sampling is applied. A stratified fallback (`sample_data.py`) exists for any future growth; it was tested with a 1,020-row input capped at 300 rows.

## Random Seed
42 (backend generator and the fallback sampler).

## Stratification Fields
source_system x facility x team x status x month (fallback only).

## Date-Coverage Method
All dates kept: 2026-10-24 to 2026-10-28 (frontend) and 2026-10-24 to 2026-10-30 (backend).

## Rare-Record Preservation
All Critical rows kept (Facility A Night Watch plus rare backend Critical days). The fallback guarantees >=1 row per stratum.

## Removed Fields
None from the source sample. Canonical keeps only the 20 mandatory columns; source-specific wide fields become metric rows.

## Removed Records
0. (Interpolated 30-day/YTD display series were never extracted - see inventory.)

## Text Truncation
`text_value` capped at 500 characters; longest insight text is under 100, nothing truncated.

## Sensitive-Data Removal
None needed; the scan (e-mail, secret and absolute-path patterns) found nothing.

## Final Source Sample
- Path: `data/source-sample/source_sample.csv`
- Size: 0.0088 MB
- Record count: 51
- Column count: 13

## Representativeness Checks
Distinct sources, facilities, teams, statuses and dates are identical before and after (see `data/quality/sampling_report.md`).

## Known Sampling Limitations
Not a sample of any real process; it is the complete synthetic population. Conclusions from it are demonstrations only.

## Reproduction Command
`python scripts/data_pipeline/run_pipeline.py`
