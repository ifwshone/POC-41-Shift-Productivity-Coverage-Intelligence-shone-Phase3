# Phase 3 Release Manifest

**Status: DRAFT — not frozen.** Versions below are recorded from the repository as inspected. The manifest cannot be frozen until the blocking findings in `PHASE3_CERTIFICATION_FINDINGS.md` are corrected, a commit exists and a live URL is validated.

## Project
- Project ID: POC-41
- Project Title: Shift Productivity & Coverage Intelligence
- Repository: **not recorded** — the README still points to the Phase 2 repository (`ifwshone/POC-41-Shift-Productivity-Coverage-Intelligence-shone-Phase2`); the Phase 3 repository URL must be entered by the owner.
- Certified Commit SHA: **NOT ASSIGNED** (the supplied Repomix carries no git metadata)
- Release Tag: `phase3-v1.0.0` — prepared, **not created** (see `final-evidence/01-release/RELEASE_TAG_PREPARATION.md`)
- Application Version: **UNDEFINED** — `frontend/package.json` has no `version` (finding B8). Proposed: 1.0.0.

## Data and Analytics
- Canonical Data Version: 1.0.0 (`data/manifest.json`; all 129 canonical rows carry `1.0.0`)
- Canonical CSV SHA-256: `4c1dde605e022631df25283657c71b21e2b75f500dbd57069653cc65725fe9f1`
- Published JSON SHA-256: `239a1b31bda1482161781c93e1014ea4f762caa35035780c00b2ee2d6e9d1e60`
- Canonical size: 129 rows × 20 columns, 0.031 MB (data folder 0.12 MB of 10 MB)
- Approved Analytical Track: Track A — Comparative Intelligence
- Method Version: 1.0.0
- Intelligence Output Contract Version: 1.0.0 (defined by `docs/INTELLIGENCE_OUTPUT_CONTRACT.md`; the contract has no separate version field — recorded as equal to the method version)
- Baseline: mean of frontend facility/team measurements — output 119.4 units/hr, overtime 20.2 hrs
- Pre-certification Repomix: `8a876eac-repomix-output.xml`, SHA-256 `d6257bfcd7c6c865cd8fc1834a77d91ea3b8e074084c00e28bb02f8b04edbd68`

## Product
- Operational Route: `/`
- Data Intelligence Route: `/intelligence`
- Assistant Result: Approved **Mode B — Deterministic + LLM** (Post #5). Not a skip. Certification status of the assistant: **fails** numeric-fidelity requirement (finding B1).
- Deployment Target: **not recorded** (no platform/region in the repository; `docker-compose.yml` is the only configuration)
- Live URL: **NOT PROVIDED / NOT VALIDATED**

## Version Consistency Matrix (inspected)

| Artifact | Field | Value | Matches manifest |
|---|---|---|---|
| `data/manifest.json` | data_version | 1.0.0 | — |
| `intelligence_data.csv` | data_version (129 rows) | 1.0.0 | Yes |
| `data-science/outputs/intelligence_results.json` | data_version / method_version | 1.0.0 / 1.0.0 | Yes |
| `data-science/outputs/intelligence_summary.json` | data_version / method_version | 1.0.0 / 1.0.0 | Yes |
| `data-science/outputs/validation_metrics.json` | data_version / method_version | 1.0.0 / 1.0.0 | Yes |
| `frontend/public/data/intelligence/*` | versions | 1.0.0 / 1.0.0 | Versions yes, **content stale (B4)** |
| Data Intelligence page | displayed versions | read from public copy | Not verified in a browser |
| Assistant response | metadata versions | 1.0.0 / 1.0.0 (harness) | Yes |
| `frontend/package.json` | application version | none | **No (B8)** |

## Certification
- Build Timestamp: not applicable (no build executed)
- Certification Date: 2026-11-06 (review date; not a certification)
- Reviewer: AI-assisted review (Claude); human reviewer sign-off pending
- Final Result: **PHASE 3 FINAL CHANGES REQUIRED**
- Known Limitations: all data synthetic; frontend (facility-team, 5 daily points) and backend (shift-level, 7 days) are separate scopes and are never pooled; Track A ranks by output gap only (overtime is context, not a combined risk score); no statistical significance; no forecasting or prediction; 30-day/YTD operational views are interpolated display values, not source data; Mode B assistant explanations are bounded to approved results.
