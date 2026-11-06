# Build and Environment Validation

## Validation Environment
Cloud sandbox: Python 3.13, Node 22, no package-install network, no Docker daemon. Frontend and container steps could not be executed; they are reported as **NOT EXECUTED**, not as passed.

## Runtime Versions
| Component | Declared | Observation |
|---|---|---|
| Backend image | `python:3.11-slim` | Local analytics ran on Python 3.13; not tested on 3.11. |
| Frontend image | `node:20-alpine` | Next 16 and React 19 declared; Node 20 compatibility not verified. Local Node is 22. |
| Documented runtime versions | none | README does not state Python/Node versions (gap). |

## Dependency Installation
- Frontend: `npm ci` not executed; lock file not visible in Repomix (confirm it is committed).
- Backend: `requirements.txt` has six unpinned packages (`fastapi, uvicorn, pandas, numpy, python-dotenv, google-genai`). No lock/constraints file. Test packages missing (`httpx`, `pytest`, `selenium`).
- Root `package.json` carries unused dependencies (`@google/genai`, npm `pytest@^1.0.0`) — remove.
- Dev tooling to verify: `eslint@^4.0.0` with `eslint-config-next@^0.2.4` and `typescript@7.0.2`.

## Environment Variables
| Variable | Used by | Default | Documented |
|---|---|---|---|
| `GEMINI_API_KEY` | backend assistant (optional; absent → deterministic-only) | none | No `.env.example` |
| `GEMINI_MODEL` | backend assistant | `gemini-3.5-flash-lite` | No |
| `NEXT_PUBLIC_API_URL` | frontend assistant panel | `http://localhost:8000` | No; not passed in compose |
`.env` is git-ignored (good). Nothing secret is committed (scan: 0 hits).

## Data Build Steps
`python scripts/data_pipeline/run_pipeline.py` — **PASS** (39/39), deterministic, reproduces the committed canonical CSV byte-for-byte.

## Analytical Build Steps
`python data-science/scripts/run_analytical_track.py && python data-science/scripts/validate_analytical_track.py` — **PASS** (exit 0, 5/5 checks). Then `python scripts/copy_intelligence.py` (manual; not part of any build — B4).

## Frontend Build
**NOT EXECUTED.** To run: `cd frontend && npm ci && npm run build`.

## Backend Build / Startup
**NOT EXECUTED.** Static finding B2: `uvicorn main:app` inside an image that contains only `backend/` cannot import `backend.api.assistant` or `assistant.*`.

## Static Generation
Not applicable as built: `/intelligence` is a client component that fetches `/data/intelligence/*.json` from `public/` at runtime. The JSON must be present in `public/` at build time (manual copy today).

## Container Build
**NOT EXECUTED** (no daemon). `docker compose build` requires `.env`; frontend build requires a committed lock file; backend per B2.

## Build Warnings
None observed (no build). Expected review items: lint tooling versions; `tsconfig` has `"strict": false`.

## Secret and Client-Bundle Review
Source scan: no keys, tokens or passwords. Only `NEXT_PUBLIC_API_URL` (a URL, not a secret) is read by client code; the Gemini key is read server-side only. Bundle itself not inspected (no build).

## Absolute-Path Review
Scan of all text files: no `/home/…`, `/Users/…`, `C:\Users` or `/mnt/…` paths. Python scripts resolve data paths from `__file__`; **but** `assistant/**` and `backend/api/assistant.py` use paths relative to the current working directory, which only works when started from the repo root.

## Final Result
**FAIL** — data and analytical builds PASS; frontend, backend and container builds are not demonstrated, and static inspection shows the backend container is not buildable-to-working as configured.
