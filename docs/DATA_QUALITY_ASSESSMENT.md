# Data Quality Assessment

## Validation Command and Result
`python scripts/data_pipeline/validate_data.py` re-run by `assess_data_quality.py`: **PASS (39/39 checks)**. Quality script result: PASS, 0 blocking issues. Output: `data-science/outputs/quality_assessment.json`.

## Completeness
All required fields (record_id, record_type, source_name, is_synthetic, data_version) are 100% populated. 100% of measurement rows have metric name, value, date and entity. 100% of entity rows have insight text. Empty optional fields are structurally inapplicable.

## Uniqueness
0 duplicate record_ids, 0 duplicate natural keys, 0 duplicate source_record_ids.

## Validity
All dates match `YYYY-MM-DDTHH:MM:SSZ`; all metric values numeric and non-negative; attendance within 0-1; record types allowed; no text over 500 characters.

## Consistency
One unit per metric; lowercase snake_case ids and categories; status vocabulary optimal/warning/critical only; boolean values `true` only; single data version equal to the manifest.

## Accuracy Against Source Sample
Every canonical value was re-derived from `source_record_id` and compared with `source_sample.csv`: 123 of 123 measurement rows and 6 of 6 entity rows match (0 mismatches).

## Provenance
129/129 rows carry source_name and source_record_id; manifest source names match.

## Safety
No e-mail or secret patterns; manifest `contains_personal_data=false`; all data synthetic.

## Reproducibility
Post #1 validation regenerates the canonical CSV and published JSON byte-identically from the source sample.

## Blocking Issues
None.

## Non-Blocking Observations (carry into Post #3)
1. Frontend headline KPI is not derivable from its daily series (differs by up to 4.1 from the latest value and 5.1 from the 5-day mean); treat it as a separate stated value.
2. Frontend status is monotone in the KPI, but thresholds are implicit in UI code.
3. Backend `status` is random and unrelated to backend metrics (mean output: critical 137.97, optimal 127.15, warning 131.18), so it is a label, not an outcome.
4. Same metric names exist at two scopes; do not pool.
5. Series are short and fully synthetic.

## Corrections Applied Through Pipeline
None required.

## Updated Data Version
Unchanged: 1.0.0 (no canonical change).

## Final Quality Result
PASS
