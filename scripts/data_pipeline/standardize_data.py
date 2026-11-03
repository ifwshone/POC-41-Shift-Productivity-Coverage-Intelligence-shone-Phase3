"""Step 3 - Map the source sample to the 20-column canonical schema (long/tidy format)."""
import re
import pandas as pd
from _common import *

STATUS_MAP = {"strained": "warning"}  # backend vocabulary -> UI vocabulary (Optimal/Warning/Critical)
FE_METRICS = [("output_per_hour", "units_per_hour"), ("overtime_hours", "hours")]
BE_METRICS = [("attendance_rate", "ratio"), ("output_per_hour", "units_per_hour"), ("overtime_hours", "hours")]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")


def status(s):
    s = slug(s)
    return STATUS_MAP.get(s, s) or None


def num(v):
    return pd.to_numeric(v, errors="coerce")


def blank(v):
    return None if v in ("", None) else v


def build(src: pd.DataFrame) -> pd.DataFrame:
    recs = []

    def rec(**k):
        base = dict.fromkeys(MANDATORY_COLUMNS)
        base.update(related_entity_id=None, stage=None, latitude=None, longitude=None,
                    is_synthetic=True, data_version=DATA_VERSION)
        base.update(k)
        recs.append(base)

    fe = src[src.source_system == SRC_FE]
    be = src[src.source_system == SRC_BE]

    for _, r in fe.iterrows():
        eid = f"{slug(r.facility)}_{slug(r.team)}"
        for m, unit in FE_METRICS:
            rec(record_type="measurement", observed_at=f"{r.record_date}T00:00:00Z", entity_id=eid,
                entity_name=f"{r.facility} - {r.team}", category=slug(r.team), subcategory=slug(r.facility),
                status=status(r.node_status), metric_name=m, metric_value=num(r[m]), metric_unit=unit,
                source_name=SRC_FE, source_record_id=f"{r.source_row_id}|{m}")
    for _, r in fe.drop_duplicates(["facility", "team"]).iterrows():  # one headline KPI + insight text per node
        rec(record_type="entity", observed_at=None, entity_id=f"{slug(r.facility)}_{slug(r.team)}",
            entity_name=f"{r.facility} - {r.team}", category=slug(r.team), subcategory=slug(r.facility),
            status=status(r.node_status), metric_name="kpi_output_per_hour", metric_value=num(r.node_kpi_output_per_hour),
            metric_unit="units_per_hour", text_value=str(r.node_issue_text)[:MAX_TEXT], source_name=SRC_FE,
            source_record_id=f"FE|{r.facility}|{r.team}|kpi")
    for _, r in be.iterrows():
        for m, unit in BE_METRICS:
            rec(record_type="measurement", observed_at=f"{r.record_date}T00:00:00Z", entity_id=f"shift_{slug(r["shift"])}",
                entity_name=f"{r.team} (all facilities)", category=slug(r.team), subcategory=None,
                status=status(r.coverage_status), metric_name=m, metric_value=num(r[m]), metric_unit=unit,
                source_name=SRC_BE, source_record_id=f"{r.source_row_id}|{m}")

    df = pd.DataFrame(recs, columns=MANDATORY_COLUMNS)
    df["_src"] = (df.source_name != SRC_FE).astype(int)
    df["_ty"] = (df.record_type != "entity").astype(int)
    df = df.sort_values(["_src", "_ty", "entity_id", "observed_at", "metric_name"], na_position="first", kind="stable")
    df = df.drop(columns=["_src", "_ty"]).reset_index(drop=True)
    df["record_id"] = [f"REC-{i + 1:05d}" for i in range(len(df))]
    df["is_synthetic"] = df["is_synthetic"].map({True: "true", False: "false"})
    return df[MANDATORY_COLUMNS]


def to_csv_bytes(df):
    return df.to_csv(index=False, encoding="utf-8", lineterminator="\n", float_format="%.10g").encode("utf-8")


def main():
    src = pd.read_csv(SOURCE_SAMPLE, dtype=str, keep_default_na=False)
    df = build(src)
    CANONICAL.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL.write_bytes(to_csv_bytes(df))
    print(f"Canonical: {len(df)} rows x {len(df.columns)} cols -> {CANONICAL.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
