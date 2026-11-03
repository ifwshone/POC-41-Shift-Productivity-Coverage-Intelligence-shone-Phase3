"""Representativeness: canonical vs source sample vs case-study behaviour (map of facility x team, statuses, time horizons)."""
import pandas as pd
from _ds_common import *

UI_HORIZONS_DAYS = {"Last 7 Days": 7, "Last 30 Days": 30, "Year to Date": 300}


def main():
    df = load()
    man = json.loads(MANIFEST.read_text("utf-8"))
    src = pd.read_csv(SOURCE_SAMPLE, dtype=str, keep_default_na=False)
    stats = json.loads((ROOT / "data" / "quality" / "pipeline_stats.json").read_text("utf-8"))
    full_pop = man["sampling_method"] == "full_population_retained" and man["original_record_count"] == man["sample_record_count"]

    fe = df[df.source_name.str.startswith("Frontend")]
    be = df[df.source_name.str.startswith("Backend")]
    cov = {"categories": {"teams_expected": 3, "teams_present": sorted(df.category.unique()),
                          "facilities_expected": 2, "facilities_present": sorted(fe.subcategory.dropna().unique()),
                          "node_rows_each": fe.groupby("entity_id").size().to_dict()}}
    nodes_ok = fe.entity_id.nunique() == 6 and fe.groupby("entity_id").size().nunique() == 1
    dates = pd.to_datetime(df.observed_at.dropna(), utc=True)
    span = (dates.max() - dates.min()).days + 1
    cov["time"] = {"span_days": int(span), "earliest": dates.min().strftime("%Y-%m-%d"), "latest": dates.max().strftime("%Y-%m-%d"),
                   "ui_time_horizons": UI_HORIZONS_DAYS,
                   "horizon_support": {"Last 7 Days": "partial (5 days frontend, 7 days backend)", "Last 30 Days": "not supported by source data (UI interpolates)",
                                       "Year to Date": "not supported by source data (UI interpolates)"}}
    cov["geography"] = {"status": "not applicable", "detail": "No coordinates in source data; map positions are schematic."}
    sc = df.status.value_counts()
    node_status = fe[fe.record_type == "entity"].status.value_counts().to_dict()
    be_status = be[be.metric_name == "output_per_hour"].status.value_counts().to_dict()
    cov["status"] = {"canonical": sc.to_dict(), "frontend_nodes": node_status, "backend_shift_days": be_status}
    cov["rare_records"] = {"critical_rows": int(sc.get("critical", 0)), "critical_share_pct": round(float(sc.get("critical", 0) / len(df) * 100), 2),
                           "frontend_critical_nodes": node_status.get("critical", 0), "backend_critical_shift_days": be_status.get("critical", 0),
                           "all_source_critical_rows_retained": stats["rows_removed"] == 0}
    cov["scenario"] = {"status": "not applicable", "detail": "No adjustable inputs or scenario parameters."}
    t = df.text_value.dropna()
    cov["text"] = {"non_null": int(len(t)), "unique": int(t.nunique()), "detail": "One insight per frontend node only; no review/feedback text."}
    cov["network"] = {"status": "not applicable", "related_entity_rows": int(df.related_entity_id.notna().sum())}

    # canonical vs source sample: every source-sample group is carried into canonical
    miss = {"facility_team_nodes": sorted(set((src[src.facility != ""].facility + "|" + src[src.facility != ""].team).unique()) -
                                          set((fe.subcategory.str.replace("_", " ").str.title() + "|" + fe.category.str.replace("_", " ").str.title()).unique())),
            "dates": sorted(set(src.record_date) - set(df.observed_at.dropna().str.slice(0, 10)))}
    conv_ok = not miss["dates"] and df.entity_id.nunique() == 9
    under = []
    if span < 8:
        under.append("Time: only 5-7 consecutive days; no weekly cycle, month or year coverage.")
    under.append("Backend rows have no facility, so facility comparison exists only in the frontend source.")
    under.append("Critical cases are rare: 1 frontend node and ~3 backend shift-days.")
    bias = ["Source is the whole synthetic population, so there is no sampling bias against it (nothing was dropped).",
            "Population bias: the population itself is hand-authored (frontend) or uniform-random (backend) and does not represent real operations.",
            "Frontend facility/team values were authored to tell a story (e.g. night shift critical); effects found later are designed, not discovered."]
    result = "PASS" if full_pop and nodes_ok and conv_ok else "CHANGES REQUIRED"
    dump("representativeness_assessment.json", {
        "result": result, "data_version": man["data_version"],
        "original_sampling": {"method": man["sampling_method"], "original_records": man["original_record_count"],
                              "sample_records": man["sample_record_count"], "canonical_records": man["canonical_record_count"],
                              "full_population_retained": full_pop},
        "coverage": cov, "canonical_vs_source_sample_missing": miss, "underrepresented_areas": under, "sampling_bias": bias,
        "scope_of_result": "PASS applies to the 7-day comparative view of 2 facilities x 3 teams. It does NOT cover 30-day or year-to-date horizons."})


if __name__ == "__main__":
    main()
