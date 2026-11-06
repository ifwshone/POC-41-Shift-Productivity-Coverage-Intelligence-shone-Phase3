# Phase 3 Final UAT

Status: **NOT PERFORMED in a browser.** UAT needs a running or deployed build. The "Actual" column below records what could be established from source and executed scripts; where nothing could be observed it says so. Post #4 and Post #5 UAT tables (all PASS, empty "Actual" columns) are not accepted as final evidence.

| Area | Expected | Actual | Status | Evidence |
|---|---|---|---|---|
| Operational | Primary use case works (map, filters, sidebar, CSV export) | Code present for all; not exercised | NOT VERIFIED | FINAL_OPERATIONAL_REGRESSION_REPORT.md |
| Intelligence | Primary question answered (which team differs most from baseline) | Data answers it: Facility A Night Watch rank 1 (−25.8), Facility B Night Watch rank 2 (−8.4), reproduced from canonical data | PASS (data) / NOT VERIFIED (UI) | FINAL_ANALYTICAL_REVALIDATION.md |
| Filters | Approved filter works | Category filter coded; low = 3 rows, high = 3 rows per results data | NOT VERIFIED | outputs JSON |
| Evidence | Supporting evidence opens | Only `n=5` shown; no drill-down or other evidence factors | **FAIL (M1)** | page.tsx |
| Methodology | Method and baseline visible | Question and PASS shown; baseline (119.4 / 20.2) not shown | **FAIL (M1)** | page.tsx |
| Limitations | Warnings visible | Summary and result limitations rendered in source | PASS (source) | page.tsx |
| Freshness | Versions/timestamp visible | Versions and generated date rendered; page serves stale copy (B4); stale banner after 7 days (M7) | **FAIL (B4)** | contract_check.json |
| Error state | Controlled failure is safe | "Integration Blocked" view on contract failure; rejected results filtered | PASS (source) | intelligenceValidator.ts |
| Mobile | Main flow usable | Responsive classes present; not tested | NOT VERIFIED | — |
| Assistant | Approved experience confirmed (Mode B) | Deterministic path and fallbacks work offline; numeric validator permissive; routing gaps | **FAIL (B1, M2, M3)** | FINAL_ASSISTANT_VALIDATION.md |
| Navigation | Routes work | Links `/` → `/intelligence` and back present | NOT VERIFIED | — |
| Deployment | Live URL works | No URL | **NOT PERFORMED** | DEPLOYMENT_VALIDATION_REPORT.md |

## Final UAT Result
**FAIL / INCOMPLETE** — UAT cannot be signed off. Re-run after corrections with the final Selenium journey and screenshots, and fill every Actual cell from observation.
