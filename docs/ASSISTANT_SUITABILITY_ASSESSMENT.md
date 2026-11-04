# Assistant Suitability Assessment
## Target User: Shift operations manager responsible for staffing and coverage.
## Existing Operational and Intelligence Experience: Deterministic dashboard with radar map, Location/Team filters, and tabular Data Intelligence rankings.
## User Questions Not Solved Conveniently Today: Managers require natural-language explanations of why a specific shift is ranked poorly without manually parsing the tabular gaps and evidence factors.
## Proposed Supported Questions: 
1. Which group ranks highest for review?
2. Why is a specific facility/team flagged?
3. What is the limitation of this data?
4. How did you calculate this ranking?
5. When was this data generated?
## Deterministic Retrieval Mapping: All questions map directly to `intelligence_results.json` and `intelligence_summary.json` via strict Python query functions.
## Evidence Availability: Rank, output gap, average output, and average overtime are available per node.
## Security and Privacy: Safe. Data is synthetic. Internal scopes (Frontend vs Backend) are strictly isolated.
## Deployment Feasibility: Feasible via existing FastAPI backend and Next.js frontend.
## Value Beyond Filters and Tables: Provides guided, conversational context and immediate interpretation of the 5-day comparative gaps.
## Deterministic Versus LLM Decision: Mode B (Deterministic + LLM).
## Approved Assistant Mode: Mode B — Deterministic + LLM
## Result
ASSISTANT SUITABLE