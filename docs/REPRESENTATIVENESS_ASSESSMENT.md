# Representativeness Assessment

## Project and Case-Study Purpose
Compare shift output, overtime and coverage status across 2 facilities x 3 teams for a shift operations manager.

## Canonical Data Version
1.0.0

## Original Sampling Method
`full_population_retained`: 51 source records, 51 retained, 129 canonical records. Nothing was removed.

## Source Sample Summary
51 rows x 13 columns (30 frontend, 21 backend).

## Canonical Record Summary
129 rows: 123 measurements, 6 entity snapshots.

## Coverage Assessment
### Categories
All 3 teams and both facilities present. Each of the 6 facility-team nodes has exactly 11 rows. Every source group and date carries into the canonical file (0 missing).
### Time Periods
2026-10-24 to 2026-10-30 (7 days max). The UI's Last 7 Days is partly backed (5-7 days). Last 30 Days and Year to Date are interpolated by the UI and **not** backed by source data.
### Geography
Not applicable: no coordinates; the map is schematic.
### Status and Process Stages
Optimal 61, warning 48, critical 20 rows. No lifecycle stages exist in this case study.
### Severity and Rare Records
Critical rows: 20 (15.5%) - 1 frontend node (Facility A Night Watch) and 3 backend shift-days. All retained.
### Scenario Boundaries
Not applicable; no scenario inputs.
### Text Groups
6 authored insight sentences, one per frontend node.
### Network Relationships
Not applicable; `related_entity_id` empty.

## Underrepresented Areas
- Only 5-7 consecutive days; no weekly, monthly or annual behaviour.
- Facility comparison exists only in the frontend source (backend has no facility).
- Critical cases are few (1 node, 3 shift-days).

## Missing Case-Study Behaviour
30-day and year-to-date history; real overtime causes; staffing levels; shift handover.

## Sampling Bias
No sampling bias against the source (full population kept). Population bias remains: frontend values are hand-authored (night shift designed to look critical) and backend values are uniform-random, so neither represents real operations.

## Impact on Future Analysis
Supports a descriptive, within-source comparison over one week. Effects found are designed or random artefacts; present them as method demonstrations. No claims about real facilities.

## Required Correction
None.

## Representativeness Result
PASS (scope: 7-day comparative view of 2 facilities x 3 teams; not valid for 30-day or year-to-date horizons).
