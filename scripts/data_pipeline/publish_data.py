"""Step 4 - Generate published JSON from the canonical CSV, plus schema.json and manifest.json."""
import json
import pandas as pd
from _common import *

DESCRIPTIONS = {
    "record_id": "Stable unique canonical record identifier (REC-00001...)",
    "record_type": "entity (node KPI snapshot) or measurement (dated metric reading)",
    "observed_at": "Observation time, ISO 8601 UTC; blank for undated snapshot rows",
    "entity_id": "Facility+team node id (facility_a_morning_crew) or shift id (shift_morning)",
    "related_entity_id": "Unused in this project (no relationships)",
    "entity_name": "Readable node/shift name",
    "category": "Team / shift (morning_crew, evening_crew, night_watch)",
    "subcategory": "Facility (facility_a, facility_b); blank for backend rows with no facility",
    "status": "Coverage status: optimal, warning, critical",
    "stage": "Unused in this project (no lifecycle)",
    "metric_name": "output_per_hour, overtime_hours, attendance_rate, kpi_output_per_hour",
    "metric_value": "Numeric value, no symbols",
    "metric_unit": "units_per_hour, hours, ratio",
    "text_value": "Operational insight text (<=500 chars), entity rows only",
    "latitude": "Not applicable (no geography in source data)",
    "longitude": "Not applicable (no geography in source data)",
    "source_name": "Originating source or generator",
    "source_record_id": "Source-side identifier plus metric suffix",
    "is_synthetic": "true for every record (all supplied sources are synthetic)",
    "data_version": "Package version; must equal manifest.data_version",
}
SPEC = {
    "record_id": ("string", True, False, {"unique": True}),
    "record_type": ("string", True, False, {"allowed_values": RECORD_TYPES}),
    "observed_at": ("datetime", False, True, {"format": "ISO-8601"}),
    "entity_id": ("string", False, True, {}), "related_entity_id": ("string", False, True, {}),
    "entity_name": ("string", False, True, {}), "category": ("string", False, True, {}),
    "subcategory": ("string", False, True, {}), "status": ("string", False, True, {}),
    "stage": ("string", False, True, {}), "metric_name": ("string", False, True, {}),
    "metric_value": ("number", False, True, {}), "metric_unit": ("string", False, True, {}),
    "text_value": ("string", False, True, {"max_length": MAX_TEXT}),
    "latitude": ("number", False, True, {"min": -90, "max": 90}),
    "longitude": ("number", False, True, {"min": -180, "max": 180}),
    "source_name": ("string", True, False, {}), "source_record_id": ("string", False, True, {}),
    "is_synthetic": ("boolean", True, False, {}), "data_version": ("string", True, False, {}),
}


def build_records(df: pd.DataFrame):
    out = df.astype(object).where(df.notna(), None)
    recs = out.to_dict(orient="records")
    for r in recs:
        r["is_synthetic"] = r["is_synthetic"] in (True, "true")
        if r["metric_value"] is not None:
            r["metric_value"] = float(r["metric_value"])
    return recs


def json_bytes(recs):
    return json.dumps(recs, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def main():
    df = pd.read_csv(CANONICAL, dtype={"is_synthetic": str})
    recs = build_records(df)
    PUBLISHED.parent.mkdir(parents=True, exist_ok=True)
    PUBLISHED.write_bytes(json_bytes(recs))

    schema = {}
    for c in MANDATORY_COLUMNS:
        t, req, nul, extra = SPEC[c]
        schema[c] = {"type": t, "required": req, "nullable": nul, **extra, "description": DESCRIPTIONS[c]}
    SCHEMA.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", "utf-8")

    s = load_stats()
    manifest = {
        "project_id": PROJECT_ID, "project_title": PROJECT_TITLE, "data_version": DATA_VERSION,
        "canonical_file": "data/canonical/intelligence_data.csv",
        "published_file": "data/published/intelligence_data.json",
        "source_type": "synthetic",
        "source_names": [SRC_FE, SRC_BE],
        "is_sampled": s["sampling_method"] != "full_population_retained",
        "sampling_method": s["sampling_method"], "random_seed": RANDOM_SEED,
        "original_record_count": s["original_record_count"],
        "sample_record_count": s["sample_record_count"],
        "canonical_record_count": len(df), "canonical_column_count": len(df.columns),
        "source_sample_size_mb": mb(SOURCE_SAMPLE), "canonical_file_size_mb": mb(CANONICAL),
        "published_file_size_mb": mb(PUBLISHED),
        "contains_synthetic_data": bool(df["is_synthetic"].astype(str).str.lower().eq("true").any()),
        "contains_personal_data": False,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", "utf-8")
    print(f"Published {len(recs)} records -> {PUBLISHED.relative_to(ROOT)}; wrote schema.json + manifest.json")


if __name__ == "__main__":
    main()
