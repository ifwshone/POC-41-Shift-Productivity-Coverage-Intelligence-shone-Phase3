# Final Analytical Revalidation

## Approved Track
Track A — Comparative Intelligence. Question: "Across Facility A and B, which team's output and overtime differ most from the baseline?" Decision supported: supervisor coverage and overtime allocation review priority.

## Canonical Data Version
1.0.0 — `intelligence_data.csv`, 129 rows × 20 columns, SHA-256 `4c1dde605e022631df25283657c71b21e2b75f500dbd57069653cc65725fe9f1`. Re-validated: 39/39 checks; full regeneration byte-identical.

## Method Version
1.0.0 (literal in `export_intelligence_results.py` and `validate_analytical_track.py`; not read from a single configuration — finding B8).

## Baseline Execution
Executed. Baseline = mean of the 60 frontend measurement rows: output 119.4 units/hr, overtime 20.2 hrs. Matches `ANALYTICAL_VALIDATION_REPORT.md`.

## Analytical Script Execution
`run_analytical_track.py` → exit 0, no manual edits. Frontend measurement rows only; backend rows excluded.

## Validation Result
`validate_analytical_track.py` → PASS. It recomputes the baseline and each group's gap and rank independently and compares to the exported results.

## Validation Metrics
| Check | Result |
|---|---|
| no_leakage_from_backend (60 frontend rows used) | true |
| minimum_group_size_met (n ≥ 5) | true |
| baseline_calculation_accurate | true |
| tie_handling_deterministic | true |
| all_frontend_nodes_ranked (6) | true |
Overall: PASS. Note: the leakage check is `len(fe_data) == 60`, a count check rather than a source-identity check.

## Regenerated Ranking (reproduced exactly)
| Rank | Entity | Output gap vs baseline | Category |
|---|---|---|---|
| 1 | facility_a_night_watch | −25.8 | low |
| 2 | facility_b_night_watch | −8.4 | low |
| 3 | facility_a_evening_crew | −2.4 | low |
| 4 | facility_b_evening_crew | +7.0 | high |
| 5 | facility_b_morning_crew | +12.0 | high |
| 6 | facility_a_morning_crew | +17.6 | high |

## Weak-Case Review
Still valid: Facility A Night Watch is deterministic/authored (artificially clean); backend shift data excluded because the granularity differs. Small samples (n=5) and no significance testing remain stated limitations. No update needed.

## Intelligence Results Regeneration
Executes from scripts. **FAIL on equivalence:** the committed `intelligence_results.json` lacks the `baseline_output_per_hour` and `baseline_overtime_hours` evidence factors the current exporter emits. Values, ranks, categories, findings and limitation text are otherwise identical; only `generated_at` and those factors differ (B3).

## Intelligence Summary Consistency
Committed summary equals the regenerated summary except `generated_at`. `result_count` (6) matches results.

## Version Consistency
Data and method versions agree across outputs and manifest. Frontend public copies carry matching versions but older content (B4).

## Manual-Edit Check
No evidence of hand-edited numbers: every committed value reproduces from the script. The stale files are older script output, not manual edits (the public copy's text differs from the current exporter's wording, consistent with an earlier exporter version).

## LLM Boundary Check
Analytical numbers are produced only by pandas code. The assistant's LLM may phrase explanations, but its number validator is too permissive (B1), so the boundary is **not** fully enforced at the assistant layer.

## Final Result
**FAIL** — the method, baseline, validation and determinism are sound (PASS), but regenerated outputs are not equivalent to the committed ones (B3) and the LLM numeric boundary is leaky (B1). Re-run and commit regenerated outputs, then re-check.
