# Clean Clone Validation Report

## Repository and Release
POC-41 Shift Productivity & Coverage Intelligence — target tag `phase3-v1.0.0` (not yet created).

## Validation Environment
Cloud Linux sandbox, Python 3.13, Node 22, git 2.43, **no network for package installs, no Docker daemon**. pandas 3.0.5, numpy 2.5.3, pytest 9.1.1 present; `fastapi`, `selenium`, `google-genai` not installed.

## Clone Command
**Not executed.** No repository URL or git history was supplied. A substitute was used: the 136 files of the supplied Repomix were unpacked into an empty directory and treated as a clean tree. This proves the committed *files* are self-sufficient for the steps below; it does not prove the repository on GitHub matches the Repomix. The documented clone command in the README points to the Phase 2 repository and `cd frontend`, so it would not set up Phase 3.

## Checked-Out Commit / Tag
Not applicable (no commit). SHA must be recorded at tagging.

## Dependency Installation
| Area | Result |
|---|---|
| Python data/analytics (pandas, numpy) | Worked with the preinstalled packages. No `requirements` file covers `data-science/` and `scripts/` (backend/requirements.txt is unpinned and is for the API). |
| Backend (`backend/requirements.txt`) | **Not executed.** Unpinned; lacks `httpx`/`pytest` needed by the TestClient tests. |
| Frontend (`npm ci`) | **Not executed** (no network). `package-lock.json` was not in the Repomix; Repomix ignores lock files by default, so its presence must be confirmed. |

## Environment Configuration
**Gap:** no `.env.example`. Variables used by code: `GEMINI_API_KEY`, `GEMINI_MODEL` (default `gemini-3.5-flash-lite`), `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`). `docker-compose.yml` requires a `.env` file (`env_file`) that is git-ignored and undocumented, so compose fails on a clean clone.

## Data Validation / Regeneration
`python scripts/data_pipeline/run_pipeline.py` → all 6 steps ran; **Validation PASS (39/39)**. Regenerated `intelligence_data.csv` is byte-identical to the committed file (SHA-256 `4c1dde60…5fe9f1`); published JSON, schema and manifest identical.

## Analytical Output Regeneration
`run_analytical_track.py` and `validate_analytical_track.py` ran without manual edits; validation PASS (5/5). **Committed `intelligence_results.json` is not equivalent to the regenerated file** (two extra baseline evidence factors per result) — finding B3.

## Frontend Build
Not executed (no network).

## Backend Startup
Not executed (FastAPI not installable here). Static inspection: container entrypoint and imports are inconsistent (finding B2).

## Container Build
Not executed (no Docker daemon).

## Test Execution
See `FINAL_AUTOMATED_TEST_REPORT.md`: 10 passed, 1 failed (needs running server), 7 test files could not be collected (missing `fastapi`/`selenium`), 3 Jest files have no runner configured.

## Route Validation
Not executed (no running frontend).

## Assistant or Skip Validation
Approved mode is Mode B. Offline harness run: deterministic mode works; LLM validator accepts invented numbers (B1).

## Undocumented Dependency Check
Found: manual `copy_intelligence.py` step not in any build script (B4); `.env` required by compose but undocumented (no `.env.example`); test-only Python packages in no requirements file; `data-science/` has no dependency file; assistant and data-science code depends on the current working directory being the repo root (relative paths); README clone/setup instructions are for Phase 2.

## Issues and Corrections
All tracked as B1–B8 and M1–M10 in `PHASE3_CERTIFICATION_FINDINGS.md`. No correction has been committed to the repository by this review.

## Final Result
**FAIL** — clone, install, build, container and route steps are not demonstrated, and undocumented dependencies exist. The data and analytics half of the clean-clone flow passes.
