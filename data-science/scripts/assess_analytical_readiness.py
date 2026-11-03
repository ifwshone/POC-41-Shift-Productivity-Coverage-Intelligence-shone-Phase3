"""Analytical-track readiness (A-H) driven by measured evidence from the canonical CSV and the earlier outputs. No modelling."""
import pandas as pd
from _ds_common import *

MIN_GROUP_OBS = 5        # comparative groups need at least this many observations
TREND_SUPPORTED = 12     # ordered periods needed for an unconditional trend track
TREND_CONDITIONAL = 3    # fewer than this cannot even describe direction
BASELINE_MIN = 20        # comparable observations per baseline for anomaly work


def main():
    df = load()
    man = json.loads(MANIFEST.read_text("utf-8"))
    q, rep = read_out("quality_assessment.json"), read_out("representativeness_assessment.json")
    meas = df[df.record_type == "measurement"]
    fe = meas[meas.source_name.str.startswith("Frontend")]
    be = meas[meas.source_name.str.startswith("Backend")]
    gsize = fe[fe.metric_name == "output_per_hour"].groupby(["subcategory", "category"]).size()
    series = meas.groupby(["source_name", "entity_id", "metric_name"]).size()
    max_series = int(series.max())
    n_ent, n_txt = int(df.entity_id.nunique()), int(df.text_value.nunique())
    factors = sorted(meas.metric_name.unique())
    base_ok = q["status"] == "PASS" and rep["result"] == "PASS"

    A = ("SUPPORTED" if base_ok and gsize.size >= 2 and gsize.min() >= MIN_GROUP_OBS else "REJECTED")
    B = ("SUPPORTED" if max_series >= TREND_SUPPORTED else "CONDITIONAL" if max_series >= TREND_CONDITIONAL else "REJECTED")
    C = "CONDITIONAL" if len(factors) >= 2 and df.status.notna().any() else "REJECTED"
    tracks = [
        {"track": "A - Comparative", "status": A,
         "evidence": f"{gsize.size} facility x team groups, each with {int(gsize.min())} daily observations of output and overtime (frontend, facility-level); 3 shifts x 7 days in backend. Quality PASS, representativeness PASS.",
         "missing_requirement": "Groups are small (5-7 observations): differences are descriptive, not statistically strong. Compare within a source only.",
         "recommendation": "PRIMARY track."},
        {"track": "B - Trend", "status": B,
         "evidence": f"Ordered consecutive daily observations exist, but each series has only {int(series.min())}-{max_series} points over one month (2026-10-24 to 2026-10-30).",
         "missing_requirement": f"Fewer than {TREND_SUPPORTED} ordered periods; no weekly/seasonal cycle; Last-30-Days and Year-to-Date views are interpolated by the UI, not in the data.",
         "recommendation": "SUPPORTING track, descriptive direction over the 5-7 observed days only. No forecasting."},
        {"track": "C - Risk & Priority", "status": C,
         "evidence": f"Explainable factors exist ({', '.join(factors)}) plus a status label (optimal/warning/critical).",
         "missing_requirement": "No documented urgency definition; status thresholds are implicit in UI code; backend status is random and unrelated to its metrics (OBS-3); attendance exists only in backend.",
         "recommendation": "Conditional: only a transparent, rule-based frontend 'coverage review priority' using output, overtime and source-stated status, with documented weights. Not a score of real risk."},
        {"track": "D - Anomaly", "status": "REJECTED",
         "evidence": f"Largest comparable baseline is {max_series} observations per series.",
         "missing_requirement": f"Needs a meaningful baseline (>= {BASELINE_MIN} comparable observations); backend values are uniform-random, so extremes are generator noise and cannot be separated from errors.",
         "recommendation": "Reject."},
        {"track": "E - Segmentation", "status": "REJECTED",
         "evidence": f"Only {n_ent} entities (6 facility-team nodes, 3 shifts) and 3-4 informative numeric fields.",
         "missing_requirement": "Segments of 6 nodes carry no business meaning beyond the existing team/facility grouping.",
         "recommendation": "Reject."},
        {"track": "F - Predictive", "status": "REJECTED",
         "evidence": "Predictive checklist below.",
         "missing_requirement": "No genuine target (status is authored/random label), no real historical outcomes, <=7 observations per series, no validation split possible, no decision-time inputs, high leakage risk (status is a function of KPI in frontend).",
         "recommendation": "Reject. Row count (129) does not justify prediction."},
        {"track": "G - Simulation", "status": "REJECTED",
         "evidence": "No scenario records, no parameter columns, record_type 'scenario' absent.",
         "missing_requirement": "Controlled inputs and comparable scenarios.", "recommendation": "Reject."},
        {"track": "H - Text & Theme", "status": "REJECTED",
         "evidence": f"{int(df.text_value.notna().sum())} text values, {n_txt} unique, one per node.",
         "missing_requirement": "Sparse, generic, authored insight sentences; no volume for themes.", "recommendation": "Reject."}]
    pred = {"genuine_target": False, "historical_examples": False, "decision_time_availability": False, "no_leakage": False,
            "distribution_reported": True, "baseline_definable": True, "defensible_validation": False, "decision_value": False}
    status = {t["status"] for t in tracks}
    supported = [t["track"] for t in tracks if t["status"] == "SUPPORTED"]
    final = ("DATA READY FOR ANALYTICAL TRACK DEVELOPMENT" if supported and base_ok
             else "CANONICAL DATA CHANGES REQUIRED" if not base_ok else "DATA INSUFFICIENT FOR PHASE 3")
    dump("analytical_readiness.json", {
        "final_result": final, "data_version": man["data_version"], "data_version_changed_in_post2": False,
        "confirmed_archetype": {"primary": "Time-Series Measurement (short, frontend facility-level)", "secondary": "Entity / Snapshot (node KPI + insight)",
                                "note": "Backend shift-level series are a second, separate measurement scope."},
        "primary_question": {
            "target_user": "Shift operations manager responsible for staffing and coverage",
            "operational_problem": "Output per hour and overtime differ by facility and team; managers need to know where coverage review is most needed.",
            "question": "Across Facility A and B, which team's output per hour and overtime hours differ most from the other groups during 2026-10-24 to 2026-10-28, and how consistent is that gap day to day?",
            "decision_supported": "Which facility/team to review first for supervisor coverage and overtime allocation (demonstration decision on synthetic data).",
            "primary_track": "A - Comparative", "supporting_track": "B - Trend (descriptive, 5 days)",
            "rejected_tracks": [t["track"] for t in tracks if t["status"] == "REJECTED"]},
        "tracks": tracks, "supported": supported, "conditional": [t["track"] for t in tracks if t["status"] == "CONDITIONAL"],
        "rejected": [t["track"] for t in tracks if t["status"] == "REJECTED"],
        "predictive_intelligence": {"status": "REJECTED", "checklist": pred},
        "thresholds_used": {"min_group_obs": MIN_GROUP_OBS, "trend_supported_periods": TREND_SUPPORTED, "trend_conditional_periods": TREND_CONDITIONAL, "anomaly_baseline_min": BASELINE_MIN},
        "limitations": ["All data synthetic; findings demonstrate method, not real operations.", "Frontend (facility-level) and backend (shift-level) are different scopes; never pool or concatenate.",
                        "5-7 daily points per series, one month only.", "Last-30-Days / Year-to-Date UI views are not backed by source data.",
                        "Frontend status/KPI/text are authored; backend status is random.", "No geography, stages, relationships or scenarios."],
        "controls_for_post3": ["Read only data/canonical/intelligence_data.csv; filter by source_name first.", "Compare groups within a source; report n for every comparison.",
                               "Label every output synthetic and descriptive; no forecast, anomaly flag or predictive score.",
                               "No second dataset; any canonical fix goes through scripts/data_pipeline with a version bump and Post #1 re-validation.",
                               "Do not alter the operational page."]})
    print("Final:", final)


if __name__ == "__main__":
    main()
