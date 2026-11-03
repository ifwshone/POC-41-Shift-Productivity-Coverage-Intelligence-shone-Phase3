# Data Archetype Confirmation

## What One Canonical Record Represents
A `measurement` row = one metric reading for one entity on one day (e.g. Facility A Night Watch, output_per_hour, 2026-10-26). An `entity` row = one headline KPI plus insight text for a facility-team node (undated snapshot).

## Primary Archetype
Time-Series Measurement (short): repeated daily metrics per entity across ordered, consecutive days.

## Secondary Archetype
Entity / Snapshot: 6 node-level KPI + insight records.

## Evidence
123 of 129 rows are dated measurements; 21 series, each complete with no gaps (12 frontend series of 5 points, 9 backend series of 7 points).

## Populated Canonical Fields
record_id, record_type, observed_at (123), entity_id, entity_name, category, subcategory (66), status, metric_name, metric_value, metric_unit, text_value (6), source_name, source_record_id, is_synthetic, data_version.

## Time Behaviour
Daily, consecutive, one month. Enough to describe day-to-day movement; not enough for seasonality, trend significance or forecasting.

## Entity Behaviour
6 facility-team nodes (frontend) and 3 shift entities (backend), each repeated across days. Nodes are comparable with each other.

## Relationship Behaviour
None.

## Text Behaviour
6 unique authored sentences; descriptive annotation, not analysable text.

## Archetypes Considered but Rejected
- Event/Transaction: rows are readings, not incidents.
- Process Lifecycle: no stage, ageing or outcome.
- Simulation/Scenario: no controllable inputs.
- Network: no edges.
- Text-Enriched: too little text.
- Hybrid: not essential to the primary question.

## Final Confirmation
Time-Series Measurement (primary, short, descriptive only) with Entity Snapshot (secondary). The two sources are separate scopes (facility-level vs shift-level) and are not one series.
