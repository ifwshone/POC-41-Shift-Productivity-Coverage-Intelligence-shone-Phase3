# Final Automated Test Report

Run: 2026-11-06, sandbox without package-install network, no running frontend. Raw output: `final-evidence/10-automated-tests/pytest_raw.txt`. **No test was deleted, skipped or edited.** Items that did not run are listed as *not executed*, with the reason.

| Test Group | Command | Passed | Failed | Not executed | Result |
|---|---|---|---|---|---|
| Data pipeline | `python scripts/data_pipeline/run_pipeline.py` (39 built-in checks) | 39 | 0 | 0 | PASS |
| Data readiness | `python data-science/scripts/assess_*.py` / notebooks | — | — | not re-run (outputs and reports inspected, consistent) | NOT RE-RUN |
| Analytical | `python data-science/scripts/run_analytical_track.py && …/validate_analytical_track.py` (5 checks) | 5 | 0 | 0 | PASS |
| Output contract | `pytest tests/intelligence-contract` | 2 | 0 | 0 | PASS (note: runs against the stale public copy) |
| Output contract (certification) | `python scripts/certification/run_phase3_checks.py --regen` | 39 | 4 | 0 | **FAIL** (see below) |
| API / loader | `pytest tests/assistant-api` | 0 | 0 | 3 (collection error: `fastapi` missing) | NOT EXECUTED |
| API / loader | `pytest tests/intelligence-api` | 0 | 1 | 0 | **FAIL** (needs `npm run dev` on :3000; none running) |
| Frontend unit | Jest ×3 files | 0 | 0 | 3 files (no runner/`test` script — B7) | NOT EXECUTABLE |
| Operational UI | `pytest tests/regression/test_operational_page.py` | 0 | 0 | 1 (selenium missing) | NOT EXECUTED |
| Intelligence UI | `pytest tests/intelligence-ui` | 0 | 0 | 1 (selenium missing) | NOT EXECUTED |
| Assistant (unit) | `pytest tests/assistant-unit` | 2 | 0 | 0 | PASS |
| Assistant (grounding) | `pytest tests/assistant-grounding` | 3 | 0 | 0 | PASS |
| Assistant (safety) | `pytest tests/assistant-safety` | 3 | 0 | 0 | PASS |
| Assistant (UI) | `pytest tests/assistant-ui` | 0 | 0 | 1 (selenium missing) | NOT EXECUTED |
| Regression | `pytest tests/regression/test_assistant_regression.py` | 0 | 0 | 2 (selenium missing) | NOT EXECUTED |
| Selenium | `pytest tests/selenium` (assistant + intelligence journeys) | 0 | 0 | 2 (selenium missing) | NOT EXECUTED |
| Selenium (final) | `BASE_URL=<live> pytest tests/selenium/test_final_journey.py` | 0 | 0 | 2 (written, not run) | NOT EXECUTED |

**pytest totals this session:** 10 passed, 1 failed, 7 test files not collectable (10 test functions in unrun files by static count).

## Certification-checker failures (4)
`ver_application_version_defined` (B8), `public_copy_identical` for results and summary (B4), `regen_equivalent_ignoring_generated_at:intelligence_results.json` (B3).

## Known coupling to resolve
`tests/selenium/test_intelligence_journey.py:31` asserts text that exists only in the stale public copy (B5). It must be updated, not removed, when the public copy is refreshed. `tests/assistant-grounding` does not cover the whitelisted-number weakness (B1/M5).

## Documented test commands (proposed single sequence)
```
pip install -r backend/requirements.txt -r requirements-dev.txt   # file to be created (B7)
python scripts/data_pipeline/run_pipeline.py
python data-science/scripts/run_analytical_track.py && python data-science/scripts/validate_analytical_track.py
python scripts/copy_intelligence.py
python scripts/certification/run_phase3_checks.py --regen
pytest tests/intelligence-contract tests/assistant-unit tests/assistant-grounding tests/assistant-safety tests/assistant-api
(cd frontend && npm ci && npm test && npm run build && npm start &)
BASE_URL=http://localhost:3000 pytest tests/intelligence-api tests/intelligence-ui tests/regression tests/assistant-ui tests/selenium
```

## Final Result
**FAIL** — one test failure, one checker failure group, and most UI/API tests not executed. Blocking tests have not passed.
