"""Canonical profile: structure, completeness, uniqueness, numeric, temporal, categorical, status, geo, text, provenance."""
import pandas as pd
from _ds_common import *

KEY = ["source_name", "entity_id", "metric_name", "observed_at"]


def main():
    df = load()
    man = json.loads(MANIFEST.read_text("utf-8"))
    n = len(df)
    p = {"structure": {
        "rows": n, "columns": len(df.columns), "file_size_mb": round(CANONICAL.stat().st_size / 1024 ** 2, 4),
        "data_versions": sorted(df.data_version.astype(str).unique()), "manifest_data_version": man["data_version"],
        "source_count": int(df.source_name.nunique()),
        "record_type_distribution": df.record_type.value_counts().to_dict()}}

    p["completeness"] = {c: {"non_null": int(df[c].notna().sum()), "null": int(df[c].isna().sum()),
                             "null_pct": round(float(df[c].isna().mean() * 100), 2)} for c in df.columns}
    p["fully_empty_fields"] = [c for c in df.columns if df[c].isna().all()]

    dated = df[df.observed_at.notna()]
    p["uniqueness"] = {
        "unique_counts": {c: int(df[c].nunique()) for c in df.columns},
        "duplicate_record_ids": int(df.record_id.duplicated().sum()),
        "duplicate_natural_keys(source,entity,metric,observed_at)": int(dated.duplicated(KEY).sum()),
        "entity_rows_per_entity_metric": df[df.record_type == "entity"].groupby(["entity_id", "metric_name"]).size().max(),
        "repeated_entity_relationships": 0, "related_entity_id_populated": int(df.related_entity_id.notna().sum())}

    num = {}
    for (src, m), g in df[df.metric_value.notna()].groupby(["source_name", "metric_name"]):
        v = pd.to_numeric(g.metric_value, errors="coerce")
        num[f"{src} :: {m}"] = {"unit": sorted(g.metric_unit.dropna().unique()), "count": int(v.count()), "min": float(v.min()),
                                "max": float(v.max()), "mean": round(float(v.mean()), 4), "median": float(v.median()),
                                "std": round(float(v.std()), 4), "invalid": int(v.isna().sum()),
                                "negative": int((v < 0).sum())}
    p["numerical"] = num

    d = pd.to_datetime(dated.observed_at, errors="coerce", utc=True)
    days = d.dt.normalize()
    per = {}
    for src, g in dated.assign(_d=days).groupby("source_name"):
        u = sorted(g._d.unique())
        full = pd.date_range(u[0], u[-1], freq="D", tz="UTC")
        series = g.groupby(["entity_id", "metric_name"]).size()
        per[src] = {"earliest": u[0].strftime("%Y-%m-%d"), "latest": u[-1].strftime("%Y-%m-%d"), "unique_dates": len(u),
                    "missing_days_in_span": int(len(full) - len(u)), "unique_months": int(g._d.dt.strftime("%Y-%m").nunique()),
                    "series_count": int(len(series)), "observations_per_series_min": int(series.min()),
                    "observations_per_series_max": int(series.max())}
    p["temporal"] = {"non_null_dates": int(len(dated)), "parse_rate_pct": round(float(d.notna().mean() * 100), 2),
                     "undated_rows": int(n - len(dated)), "earliest": d.min().strftime("%Y-%m-%d"), "latest": d.max().strftime("%Y-%m-%d"),
                     "unique_dates": int(days.nunique()), "max_share_on_single_date_pct": round(float(days.value_counts(normalize=True).max() * 100), 2),
                     "per_source": per}

    cat = {}
    for c in ["category", "subcategory", "status", "metric_name", "metric_unit", "entity_id"]:
        vc = df[c].fillna("<missing>").value_counts()
        cat[c] = {"distribution": vc.to_dict(), "distinct": int(len(vc)), "rare_values_lt_5pct": [k for k, v in vc.items() if v / n < 0.05],
                  "near_constant": bool(vc.iloc[0] / n > 0.95)}
    p["categorical"] = cat
    p["status_stage"] = {"status_distribution": df.status.fillna("<missing>").value_counts().to_dict(),
                         "stage_populated": int(df.stage.notna().sum()), "stage_note": "No lifecycle stages exist in this case study."}
    lat, lon = pd.to_numeric(df.latitude, errors="coerce"), pd.to_numeric(df.longitude, errors="coerce")
    p["geographic"] = {"valid_coordinate_pairs": int((lat.between(-90, 90) & lon.between(-180, 180)).sum()),
                       "populated_latitude": int(lat.notna().sum()), "populated_longitude": int(lon.notna().sum()),
                       "note": "No geography in the source data; the map in the UI is schematic."}
    t = df.text_value.dropna()
    p["text"] = {"non_null": int(len(t)), "unique": int(t.nunique()), "avg_length": round(float(t.str.len().mean()), 1),
                 "max_length": int(t.str.len().max()), "possibly_truncated(len==500)": int((t.str.len() == 500).sum())}
    p["provenance"] = {"source_distribution": df.source_name.value_counts().to_dict(),
                       "synthetic_true": int((df.is_synthetic == "true").sum()), "synthetic_false": int((df.is_synthetic == "false").sum())}
    dump("canonical_profile.json", p)


if __name__ == "__main__":
    main()
