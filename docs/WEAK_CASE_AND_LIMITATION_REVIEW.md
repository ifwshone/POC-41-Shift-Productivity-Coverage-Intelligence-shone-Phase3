# Weak Case and Limitation Review

| Record / Group | Output | Concern | Likely Cause | Impact | Action / Limitation |
|---|---|---|---|---|---|
| Facility A Night Watch | Rank 1 (Priority) | Highly deterministic poor performance | Synthetic data authoring intent | Results look artificially clean | Label as synthetic demonstration only. |
| Backend Shift Data | Excluded | Not compared against frontend facilities | Data granularity mismatch | Limits overall scope | Enforce source-separation rule. |

## Important Limitations
- All data synthetic; findings demonstrate method, not real operations.
- Frontend (facility-level) and backend (shift-level) are different scopes; never pool or concatenate.
- 5-7 daily points per series, one month only.