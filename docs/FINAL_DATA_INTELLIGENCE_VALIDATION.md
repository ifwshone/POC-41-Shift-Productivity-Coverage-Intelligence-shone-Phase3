# Final Data Intelligence Validation

Route: `/intelligence` (client component `frontend/app/intelligence/page.tsx`; loader `lib/intelligenceLoader.ts`; validator `lib/intelligenceValidator.ts`). Source reviewed; **not rendered in a browser** (no build possible here).

## Guide §17 Checks
| Check | Expected | Finding | Status |
|---|---|---|---|
| Route | Loads directly and via navigation | Link from `/` exists; back link exists | Code OK; not run |
| Track | Approved track visible | Header shows `approved_track.split(' ')[1]` → the single letter "A" (full name "Track A — Comparative Intelligence" not shown in header) | Partial |
| Versions | Data and method versions visible | `Method v1.0.0`, `Data v1.0.0`, Generated date | Code OK |
| Summary | Approved values display | Key findings and priority items from summary | Code OK |
| Primary view | Result understandable | Bar chart of output gap + ranked table (rank, entity, gap, finding, n) | Code OK |
| Filters | Supported filters work | Category select All/low/high | Code OK; not run |
| Evidence | References accessible | Only `n=` (record_count) per row; no drill-down; other evidence factors not shown | **Weak (M1)** |
| Methodology | Method, **baseline** and validation visible | Shows analytical question and "Status: PASS". **Baseline values and method description are not shown** | **FAIL (M1)** |
| Limitations | Visible and accurate | Summary limitations + first result's limitation shown | OK |
| States | Loading, error, empty, stale | All four implemented (loading text; "Integration Blocked"; "No results match active filters"; Version Mismatch / Data Stale >7 days banners) | Code OK |
| Responsive | Mobile and desktop usable | Tailwind grid stacks; table in `overflow-x-auto` | Not run |
| Contract | Invalid outputs fail safely | Validator checks required strings, numbers, statuses, evidence array, ISO date; collection check for count and duplicate IDs; rejected results filtered | Code OK |

## Contract Certification (§13)
Executed with `scripts/certification/run_phase3_checks.py` on both `data-science/outputs` and the frontend public copies: required fields, unique IDs, quality statuses, evidence structure, limitations, ISO timestamps and summary count all **PASS**. Frontend validator does not check the full required-field list (e.g. `entity_id`, `period_*`) nor evidence element shape — acceptable but weaker than the Python check.

## Data Currency
**FAIL (B4):** the page serves `frontend/public/data/intelligence/*`, which is an older generation than `data-science/outputs/*` (different finding wording, limitation wording, one fewer important limitation, earlier `generated_at`). Once `generated_at` is older than 7 days the page shows "Data Stale".

## Unit and UI Tests
Three Jest files exist (`DataIntelligencePage`, `intelligenceLoader`, `intelligenceValidator`) but there is no runner configuration or `test` script (B7). `tests/intelligence-ui/test_page_render.py` and the intelligence journey need Selenium and a server. None executed.

## Final Result
**FAIL** — contract is sound, but the methodology/baseline and evidence requirements are not met in the UI (M1), the page serves stale data (B4), and nothing was exercised in a browser. Post #4 UAT (PASS, 10/10) remains the claimed baseline; its "Actual" column was empty.
