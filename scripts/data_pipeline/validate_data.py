"""Step 6 - Validate the whole /data package. Exit code 1 on any failure."""
import hashlib, json, re
import pandas as pd
from _common import *
import standardize_data as std
import publish_data as pub

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SECRET = re.compile(r"(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*\S{6,}", re.I)
ABSPATH = re.compile(r"(/home/|/Users/|/mnt/|[A-Za-z]:\\)")


def main():
    checks = []

    def chk(name, ok, detail=""):
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": str(detail)})

    required = [DATA / "README.md", MANIFEST, SCHEMA, SOURCE_SAMPLE, CANONICAL, PUBLISHED,
                PROFILE, SAMPLING_REPORT]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    chk("required_paths", not missing, missing or "all present")
    if missing:
        return finish(checks)

    files = [p for p in DATA.rglob("*") if p.is_file() and p != VALIDATION]
    total = sum(p.stat().st_size for p in files) + 0
    chk("total_data_size_le_10mb", total <= MAX_DATA_MB * 1024 ** 2, f"{total / 1024 ** 2:.4f} MB")
    big = [p.name for p in files if p.stat().st_size > MAX_FILE_MB * 1024 ** 2]
    chk("each_file_le_5mb", not big, big or "ok")
    chk("allowed_file_types_only", all(p.suffix in {".md", ".json", ".csv"} for p in files),
        sorted({p.suffix for p in files}))

    df = pd.read_csv(CANONICAL, dtype=str, keep_default_na=False, na_values=[""])
    man = json.loads(MANIFEST.read_text("utf-8"))
    schema = json.loads(SCHEMA.read_text("utf-8"))
    src = pd.read_csv(SOURCE_SAMPLE, dtype=str, keep_default_na=False)

    chk("row_count_le_10000", len(df) <= MAX_ROWS, len(df))
    chk("column_count_le_50", len(df.columns) <= MAX_COLS and len(src.columns) <= MAX_COLS, f"{len(df.columns)}/{len(src.columns)}")
    chk("source_sample_rows_le_10000", len(src) <= MAX_ROWS, len(src))
    chk("canonical_columns_in_order", list(df.columns[:20]) == MANDATORY_COLUMNS, list(df.columns))
    chk("columns_snake_case", all(re.fullmatch(r"[a-z][a-z0-9_]*", c) for c in df.columns), "")
    chk("schema_keys_match_columns", list(schema) == MANDATORY_COLUMNS, "")
    chk("record_id_non_null_unique", df.record_id.notna().all() and df.record_id.is_unique, f"{df.record_id.nunique()} unique")
    chk("entity_id_clean_slug", df.entity_id.dropna().str.fullmatch(r"[a-z0-9_]{1,40}").all(), sorted(df.entity_id.dropna().unique()))
    chk("record_type_allowed", df.record_type.isin(RECORD_TYPES).all(), sorted(df.record_type.unique()))
    for c in ("record_type", "source_name", "is_synthetic", "data_version"):
        chk(f"{c}_not_null", df[c].notna().all(), "")
    chk("is_synthetic_boolean", df.is_synthetic.isin(["true", "false"]).all(), sorted(df.is_synthetic.unique()))
    d = pd.to_datetime(df.observed_at.dropna(), format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
    chk("observed_at_iso8601_parses", d.notna().all(), f"{int(d.isna().sum())} bad of {len(d)}")
    mv = pd.to_numeric(df.metric_value.dropna(), errors="coerce")
    chk("metric_value_numeric", mv.notna().all(), "")
    for c, lo, hi in (("latitude", -90, 90), ("longitude", -180, 180)):
        v = pd.to_numeric(df[c].dropna(), errors="coerce")
        chk(f"{c}_numeric_in_range", v.notna().all() and v.between(lo, hi).all(), f"{len(v)} populated")
    chk("text_value_le_500", df.text_value.dropna().str.len().le(MAX_TEXT).all(), "")
    chk("utf8_no_bom", not CANONICAL.read_bytes().startswith(b"\xef\xbb\xbf"), "")

    # privacy / secrets / portability on every text file in /data
    txt = "\n".join(p.read_text("utf-8") for p in files)
    chk("no_personal_data_patterns", not EMAIL.search(txt), "no e-mail addresses")
    chk("no_secrets_patterns", not SECRET.search(txt), "")
    chk("no_absolute_paths", not ABSPATH.search(txt), "")
    chk("manifest_contains_personal_data_false", man["contains_personal_data"] is False, "")

    # manifest consistency
    chk("manifest_data_version_matches", set(df.data_version) == {man["data_version"]}, man["data_version"])
    chk("manifest_record_counts", man["canonical_record_count"] == len(df) and man["sample_record_count"] == len(src), "")
    chk("manifest_column_count", man["canonical_column_count"] == len(df.columns), "")
    chk("manifest_sizes_match", all(abs(man[k] - mb(p)) < 1e-9 for k, p in (
        ("source_sample_size_mb", SOURCE_SAMPLE), ("canonical_file_size_mb", CANONICAL), ("published_file_size_mb", PUBLISHED))), "")
    chk("manifest_synthetic_flag", man["contains_synthetic_data"] == (df.is_synthetic == "true").any(), "")
    chk("manifest_paths_exist", (ROOT / man["canonical_file"]).exists() and (ROOT / man["published_file"]).exists(), "")
    chk("manifest_source_names_match", sorted(man["source_names"]) == sorted(df.source_name.unique()), "")

    # published JSON == canonical CSV, and full regeneration is byte-identical
    full = pd.read_csv(CANONICAL, dtype={"is_synthetic": str})
    recs = json.loads(PUBLISHED.read_text("utf-8"))
    chk("published_json_matches_csv", recs == json.loads(pub.json_bytes(pub.build_records(full)).decode()) and len(recs) == len(df), len(recs))
    chk("published_json_le_5mb", PUBLISHED.stat().st_size <= MAX_FILE_MB * 1024 ** 2, "")
    regen = std.to_csv_bytes(std.build(src))
    chk("reproducible_canonical_csv", regen == CANONICAL.read_bytes(), "regenerated from source sample is byte-identical")
    chk("reproducible_published_json", pub.json_bytes(pub.build_records(pd.read_csv(__import__("io").BytesIO(regen), dtype={"is_synthetic": str}))) == PUBLISHED.read_bytes(), "")

    extra = {"total_data_size_mb_excluding_validation_report": round(total / 1024 ** 2, 4),
             "canonical_rows": len(df), "canonical_columns": len(df.columns),
             "sha256_canonical_csv": hashlib.sha256(CANONICAL.read_bytes()).hexdigest(),
             "sha256_published_json": hashlib.sha256(PUBLISHED.read_bytes()).hexdigest()}
    return finish(checks, extra)


def finish(checks, extra=None):
    failed = [c for c in checks if c["status"] == "FAIL"]
    rep = {"status": "PASS" if not failed else "FAIL", "checks_total": len(checks),
           "checks_failed": len(failed), "errors": [f"{c['check']}: {c['detail']}" for c in failed],
           **(extra or {}), "checks": checks}
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION.write_text(json.dumps(rep, indent=2) + "\n", "utf-8")
    print(f"Validation {rep['status']} ({len(checks) - len(failed)}/{len(checks)} checks)")
    for e in rep["errors"]:
        print("  FAIL", e)
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
