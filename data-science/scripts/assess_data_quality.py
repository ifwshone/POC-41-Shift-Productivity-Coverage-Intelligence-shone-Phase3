"""Quality dimensions: completeness, uniqueness, validity, consistency, accuracy, provenance, safety, reproducibility.
Blocking issues fail the run (exit 1). Observations are non-blocking findings that later posts must respect."""
import re, subprocess, sys
import numpy as np
import pandas as pd
from _ds_common import *

ALLOWED = {"record_type": ["entity", "event", "transaction", "measurement", "process", "scenario", "node", "edge", "document"]}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SECRET = re.compile(r"(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*\S{6,}", re.I)


def main():
    df = load()
    schema = json.loads(SCHEMA.read_text("utf-8"))
    man = json.loads(MANIFEST.read_text("utf-8"))
    src = pd.read_csv(SOURCE_SAMPLE, dtype=str, keep_default_na=False)
    issues, dims = [], {}

    def issue(sev, field, msg):
        issues.append({"severity": sev, "field": field, "issue": msg})

    # Structural re-validation (Post #1 gate), run as the guide requires
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "data_pipeline" / "validate_data.py")], capture_output=True, text=True, cwd=ROOT)
    post1 = {"command": "python scripts/data_pipeline/validate_data.py", "result": "PASS" if r.returncode == 0 else "FAIL",
             "summary": r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr[-200:]}
    if r.returncode:
        issue("blocking", "package", "Post #1 structural validation failed")

    # Completeness
    for c in ["record_id", "record_type", "source_name", "is_synthetic", "data_version"]:
        if df[c].isna().any():
            issue("blocking", c, f"{int(df[c].isna().sum())} missing values")
    meas = df[df.record_type == "measurement"]
    ent = df[df.record_type == "entity"]
    comp = {"required_fields_complete": not any(i["field"] in ("record_id", "record_type", "source_name", "is_synthetic", "data_version") for i in issues),
            "measurement_rows_with_metric_name_and_value_pct": round(float((meas.metric_name.notna() & meas.metric_value.notna()).mean() * 100), 2),
            "measurement_rows_with_date_pct": round(float(meas.observed_at.notna().mean() * 100), 2),
            "measurement_rows_with_entity_pct": round(float(meas.entity_id.notna().mean() * 100), 2),
            "entity_rows_with_text_pct": round(float(ent.text_value.notna().mean() * 100), 2),
            "fully_empty_optional_fields": [c for c in df.columns if df[c].isna().all()]}
    dims["completeness"] = comp

    # Uniqueness
    dup_ids = int(df.record_id.duplicated().sum())
    if dup_ids:
        issue("blocking", "record_id", f"{dup_ids} duplicate identifiers")
    dated = df[df.observed_at.notna()]
    dup_nat = int(dated.duplicated(["source_name", "entity_id", "metric_name", "observed_at"]).sum())
    dup_src = int(df.source_record_id.duplicated().sum())
    if dup_nat or dup_src:
        issue("blocking", "natural_key", f"{dup_nat} duplicate (source,entity,metric,date); {dup_src} duplicate source_record_id")
    dims["uniqueness"] = {"duplicate_record_ids": dup_ids, "duplicate_natural_keys": dup_nat, "duplicate_source_record_ids": dup_src}

    # Validity
    parsed = pd.to_datetime(dated.observed_at, format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
    bad_dates = int(parsed.isna().sum())
    if bad_dates:
        issue("blocking", "observed_at", f"{bad_dates} non-ISO-8601 dates")
    bad_type = int((~df.record_type.isin(ALLOWED["record_type"])).sum())
    if bad_type:
        issue("blocking", "record_type", f"{bad_type} values outside the allowed list")
    mv = pd.to_numeric(df.metric_value, errors="coerce")
    bad_num = int((df.metric_value.notna() & mv.isna()).sum())
    if bad_num:
        issue("blocking", "metric_value", f"{bad_num} non-numeric values")
    for col, lo, hi in (("latitude", -90, 90), ("longitude", -180, 180)):
        v = pd.to_numeric(df[col], errors="coerce")
        if (df[col].notna() & ~v.between(lo, hi)).any():
            issue("blocking", col, "out-of-range coordinates")
    att = df[df.metric_name == "attendance_rate"].metric_value
    if ((att < 0) | (att > 1)).any():
        issue("blocking", "metric_value", "attendance_rate outside 0-1")
    if (mv < 0).any():
        issue("blocking", "metric_value", "negative metric values")
    dims["validity"] = {"unparseable_dates": bad_dates, "invalid_record_types": bad_type,
                        "non_numeric_metric_values": bad_num, "schema_fields": len(schema), "text_over_500": int((df.text_value.dropna().str.len() > 500).sum())}

    # Consistency
    units = df.dropna(subset=["metric_name"]).groupby("metric_name").metric_unit.apply(lambda s: sorted(s.dropna().unique()))
    mixed = {k: v for k, v in units.items() if len(v) > 1}
    if mixed:
        issue("blocking", "metric_unit", f"mixed units: {mixed}")
    slug_ok = df.entity_id.dropna().str.fullmatch(r"[a-z0-9_]+").all() and df.category.dropna().str.fullmatch(r"[a-z0-9_]+").all()
    status_vocab = sorted(df.status.dropna().unique())
    if not slug_ok or not set(status_vocab) <= {"optimal", "warning", "critical"}:
        issue("blocking", "category/status", "non-standard category or status vocabulary")
    # entity status must equal the status on that entity's measurement rows (frontend)
    fe_m = meas[meas.source_name.str.startswith("Frontend")].groupby("entity_id").status.nunique()
    if (fe_m > 1).any():
        issue("blocking", "status", "frontend entity status varies within an entity")
    dims["consistency"] = {"metric_units": units.to_dict(), "mixed_unit_metrics": mixed, "status_vocabulary": status_vocab,
                           "snake_case_ids_and_categories": bool(slug_ok), "boolean_values": sorted(df.is_synthetic.unique()),
                           "single_data_version": sorted(df.data_version.astype(str).unique()) == [man["data_version"]]}

    # Accuracy against the source sample (independent re-derivation from source_record_id)
    idx = src.set_index("source_row_id")
    mism, checked = 0, 0
    for _, r_ in meas.iterrows():
        row_id, metric = r_.source_record_id.rsplit("|", 1)
        checked += 1
        if row_id not in idx.index or abs(float(idx.loc[row_id, metric]) - float(r_.metric_value)) > 1e-9:
            mism += 1
    kpi_mism = 0
    for _, r_ in ent.iterrows():
        fac, team = r_.source_record_id.split("|")[1:3]
        s = src[(src.facility == fac) & (src.team == team)].iloc[0]
        kpi_mism += int(abs(float(s.node_kpi_output_per_hour) - float(r_.metric_value)) > 1e-9 or s.node_issue_text != r_.text_value)
    if mism or kpi_mism:
        issue("blocking", "metric_value", f"{mism} measurement and {kpi_mism} entity rows differ from the source sample")
    dims["accuracy"] = {"measurement_rows_checked": checked, "measurement_mismatches": mism, "entity_rows_checked": len(ent), "entity_mismatches": kpi_mism}

    # Provenance, safety, reproducibility
    dims["provenance"] = {"rows_with_source_name": int(df.source_name.notna().sum()), "rows_with_source_record_id": int(df.source_record_id.notna().sum()),
                          "synthetic_rows": int((df.is_synthetic == "true").sum()), "non_synthetic_rows": int((df.is_synthetic == "false").sum()),
                          "manifest_sources_match": sorted(man["source_names"]) == sorted(df.source_name.unique())}
    txt = CANONICAL.read_text("utf-8")
    safe = not EMAIL.search(txt) and not SECRET.search(txt)
    if not safe:
        issue("blocking", "text", "personal-data or secret pattern found")
    dims["safety"] = {"personal_data_patterns_found": bool(EMAIL.search(txt)), "secret_patterns_found": bool(SECRET.search(txt)),
                      "manifest_contains_personal_data": man["contains_personal_data"]}
    dims["reproducibility"] = {"post1_regeneration_check": post1["result"], "note": "validate_data.py regenerates canonical CSV and JSON from the source sample and compares bytes."}

    # Non-blocking observations (source behaviour later tracks must respect)
    obs = []
    fe_ent = ent[ent.source_name.str.startswith("Frontend")]
    ser = meas[(meas.metric_name == "output_per_hour") & meas.source_name.str.startswith("Frontend")].groupby("entity_id").metric_value
    k = fe_ent.set_index("entity_id").metric_value
    diff = (k - ser.last()).abs()
    obs.append({"id": "OBS-1", "finding": "Headline KPI is not derivable from the daily series",
                "detail": f"kpi_output_per_hour differs from the latest daily output by up to {diff.max():.1f} units and from the 5-day mean by up to {(k - ser.mean()).abs().max():.1f}; treat KPI as a separate source-stated value."})
    order = fe_ent.sort_values("metric_value", ascending=False)[["metric_value", "status"]]
    rank = {"optimal": 0, "warning": 1, "critical": 2}
    monotone = all(rank[a] <= rank[b] for a, b in zip(order.status, order.status[1:]))
    obs.append({"id": "OBS-2", "finding": "Frontend status is monotone in the KPI", "detail": f"Statuses ordered by KPI are consistent: {monotone}. Thresholds are implicit in the UI code, not documented."})
    be = meas[meas.source_name.str.startswith("Backend") & (meas.metric_name == "output_per_hour")]
    gm = be.groupby("status").metric_value.agg(["count", "mean"]).round(2)
    obs.append({"id": "OBS-3", "finding": "Backend status is not tied to backend metrics",
                "detail": "Backend coverage_status is drawn at random (70/20/10) independently of output; mean output by status: " + json.dumps(gm["mean"].to_dict()) + ". It is a label, not an outcome derived from the metrics."})
    obs.append({"id": "OBS-4", "finding": "Different scopes share metric names",
                "detail": "output_per_hour and overtime_hours exist in both sources (facility-level vs shift-level). Always filter by source_name; do not pool."})
    obs.append({"id": "OBS-5", "finding": "Short, fully synthetic series", "detail": "Frontend series have 5 daily points, backend 7. All rows are synthetic."})

    blocking = [i for i in issues if i["severity"] == "blocking"]
    dump("quality_assessment.json", {"status": "PASS" if not blocking else "FAIL", "data_version": man["data_version"],
                                     "post1_validation": post1, "dimensions": dims, "issues": issues, "observations": obs})
    if blocking:
        raise SystemExit("Blocking data-quality issues found")


if __name__ == "__main__":
    main()
