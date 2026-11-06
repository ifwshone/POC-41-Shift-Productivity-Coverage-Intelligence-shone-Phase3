# Phase 3 Handover Guide

> Status: written from the repository as inspected. Commands marked **(verified)** were executed during certification review; the rest are **(unverified)** and must be confirmed in a networked environment before this guide is relied on. Open defects that change these steps are noted inline.

## Purpose
Let another developer set up, validate, regenerate, test, deploy and operate POC-41 Shift Productivity & Coverage Intelligence (Phase 3).

## Repository and Release
Phase 3 repository: *owner to fill in*. Release tag: `phase3-v1.0.0` (to be created on the certified commit). Data 1.0.0, method 1.0.0, application version to be set (B8).

## Live URL
*Not yet available.* Record it in `PHASE3_RELEASE_MANIFEST.md` and `README.md`.

## Owners
*Owner to fill in* (project owner, data owner, deployment owner).

## Prerequisites
Python 3.11+ (analytics verified on 3.13), pandas, numpy; Node 20+ (Dockerfile) with npm; Docker (optional); Chrome + chromedriver for Selenium; a Gemini API key only if LLM explanations are wanted.

## Environment Variables
Create `.env` at the repo root (git-ignored; `.env.example` to be committed — B7/M9):
```
GEMINI_API_KEY=            # optional; empty = deterministic-only assistant
GEMINI_MODEL=gemini-3.5-flash-lite
NEXT_PUBLIC_API_URL=http://localhost:8000   # must be the public backend URL in production
```
Never commit real keys. If a key is ever found in evidence or history, remove it and rotate it.

## Local Setup (unverified)
```
git clone <phase3-repo-url> && cd <repo>
git checkout phase3-v1.0.0
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy -r backend/requirements.txt          # requirements-dev.txt to add
cd frontend && npm ci && cd ..
```

## Canonical Data Pipeline (verified)
`python scripts/data_pipeline/run_pipeline.py` — extracts the 51 source rows from `frontend/app/page.tsx` and `backend/main.py`, keeps the full population, writes `data/canonical/intelligence_data.csv` (129 × 20), published JSON, schema, manifest, profile, and runs 39 checks. Expect `Validation PASS (39/39 checks)` and CSV SHA-256 `4c1dde60…5fe9f1`.

## Data Validation (verified)
`python scripts/data_pipeline/validate_data.py` (exit 1 on any failure; report in `data/quality/validation_report.json`).

## Data Readiness
Post #2 scripts in `data-science/scripts/` (`profile_canonical_data.py`, `assess_data_quality.py`, `assess_representativeness.py`, `assess_analytical_readiness.py`). Results are in `data-science/outputs/` and `docs/`. Re-run only when the data version changes.

## Analytical Regeneration (verified)
```
python data-science/scripts/run_analytical_track.py
python data-science/scripts/validate_analytical_track.py
python scripts/copy_intelligence.py        # copies outputs to frontend/public/data/intelligence/
python scripts/certification/run_phase3_checks.py --regen
```
`generated_at` changes on every run; everything else is deterministic. **Always run the copy step**; the checker fails if the public copy drifts (B4).

## Application Build (unverified)
`cd frontend && npm ci && npm run build && npm start` (port 3000).

## Container Steps (unverified; backend blocked by B2)
After fixing B2: `docker compose build && docker compose up`; frontend :3000, backend :8000. Validate per guide §23.

## Deployment Steps
Not defined yet. Record platform, region, build/start commands, env-var configuration (secrets via the platform, not files) and the live URL. Set `NEXT_PUBLIC_API_URL` at build time to the public backend. Restrict CORS to the live origin.

## Test Commands
See `FINAL_AUTOMATED_TEST_REPORT.md`. Selenium: `BASE_URL=<url> pytest tests/selenium/test_final_journey.py` (headless; writes screenshots and log to `final-evidence/`).

## Routes
`/` operational map · `/intelligence` Data Intelligence · static data at `/data/intelligence/{intelligence_results,intelligence_summary,validation_metrics}.json` · backend `POST /api/assistant/query`, `GET /api/v1/intelligence/coverage` (no health endpoint yet).

## Assistant Mode
Mode B (deterministic + LLM). Supported intents: list priority items, explain a result, explain limitations, data freshness (method explanation pending, M2). With no `GEMINI_API_KEY` the assistant answers deterministically and the UI shows the LLM panel as unavailable. Not a skip.

## Logs and Troubleshooting
| Symptom | Likely cause |
|---|---|
| `Integration Blocked` on `/intelligence` | contract failure in the public JSON; run the checker |
| "Version Mismatch" / "Data Stale" banner | public copy older/mismatched; re-run regeneration + copy |
| Assistant returns `unavailable` | outputs not found (working directory not repo root) |
| LLM panel "Unavailable (Missing Config)" | no `GEMINI_API_KEY` |
| LLM panel "Hallucination Detected" | validator rejected the text; deterministic answer still shown |
| Compose fails immediately | `.env` missing (compose `env_file`) |

## Data-Version Update
Change the data in the sources → run the pipeline → bump `DATA_VERSION` in `scripts/data_pipeline/_common.py` → regenerate analytics → update manifest/reports → run the checker → new release tag.

## Method-Version Update
Change the method in `data-science/scripts/track-specific/` → bump the method version (single source to be introduced, B8) → rerun validation, weak-case review, UAT and assistant grounding tests → new release tag.

## Rollback
`git checkout phase3-v1.0.0` (or the previous tag), rebuild and redeploy; for platform deployments, redeploy the previous image/build. Static JSON is part of the build, so rollback restores data and code together.

## Known Limitations
See `PHASE3_COMPLETION_REPORT.md`: synthetic data, separate scopes, output-gap ranking only, descriptive, no forecasting, bounded assistant.

## Support / Ownership
*Owner to fill in.* Open defects: `PHASE3_CERTIFICATION_FINDINGS.md`.
