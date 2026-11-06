# Deployment Validation Report

## Result
**NOT PERFORMED — FAIL.** No live URL, platform, region or deployment configuration beyond `docker-compose.yml` and two Dockerfiles was supplied. A local or container run is not a deployment validation (guide §34).

## Matrix (guide §22)
| Area | Required evidence | Finding |
|---|---|---|
| Target | Approved platform and region | **Missing** — not recorded anywhere |
| Build command | Documented and successful | Frontend `npm ci && npm run build` documented (README, partially); not executed |
| Start command | Documented | Frontend `npm start`; backend `uvicorn main:app` (inconsistent with imports — B2) |
| Runtime | Correct version | Dockerfiles: Node 20, Python 3.11; not verified against the project |
| Environment variables | Configured without exposure | No `.env.example`; compose requires `.env`; `NEXT_PUBLIC_API_URL` not passed at build (M9) |
| Static data | Correct public/generated paths | `frontend/public/data/intelligence/` present but stale (B4) |
| API URL | Correct production configuration | Defaults to `http://localhost:8000`; would break any hosted deployment (M9) |
| Health | Endpoint or functional check | **None** — backend has no `/health`; only `/api/v1/intelligence/coverage` |
| CORS/auth | Correct where applicable | `allow_origins=["*"]` with credentials; no authentication (acceptable for synthetic data, must be stated; tighten to the live origin) |
| Payload/file size | Within limits | Data folder 0.12 MB; intelligence JSON < 0.1 MB |
| Logs | No unresolved critical error | Not available |
| Rollback | Documented | Not documented; proposed in `PHASE3_HANDOVER_GUIDE.md` |

## Container validation (guide §23)
| Check | Result |
|---|---|
| Image build | NOT EXECUTED (no Docker daemon) |
| Container start / health / routes | NOT EXECUTED |
| Data files available in image | **Likely NO for backend** (B2); frontend includes `public/` via `COPY . .` |
| Absolute paths | None in source |
| Image size, logs | Not available |
| Secrets | Not in repo; must be injected at run time (`env_file`/platform secrets) |

## Required to pass
1. Choose and record the target platform/region and live URL.
2. Fix B2, M9; add a health endpoint or functional health check.
3. Deploy; record build/start logs (short), `curl` health proof, response for `/`, `/intelligence`, `/data/intelligence/intelligence_summary.json` and one assistant query.
4. Run `BASE_URL=<live> pytest tests/selenium/test_final_journey.py`.
