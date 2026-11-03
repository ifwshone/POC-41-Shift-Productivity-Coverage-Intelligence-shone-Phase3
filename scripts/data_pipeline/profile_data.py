"""Step 5 - Structural data profile (counts and ranges only; no analysis or modelling)."""
import json
import pandas as pd
from _common import *


def main():
    df = pd.read_csv(CANONICAL, dtype={"is_synthetic": str})
    cols = {}
    for c in df.columns:
        s = df[c]
        info = {"dtype": str(s.dtype), "non_null": int(s.notna().sum()), "null": int(s.isna().sum()),
                "unique": int(s.nunique(dropna=True))}
        if c == "metric_value":
            info.update(min=float(s.min()), max=float(s.max()), mean=round(float(s.mean()), 4))
        if c == "observed_at":
            d = pd.to_datetime(s.dropna(), utc=True, errors="coerce")
            info.update(min=d.min().strftime("%Y-%m-%dT%H:%M:%SZ"), max=d.max().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        unparseable=int(d.isna().sum()))
        if c in ("record_type", "category", "subcategory", "status", "metric_name", "metric_unit",
                 "source_name", "is_synthetic", "data_version"):
            info["value_counts"] = {str(k): int(v) for k, v in s.value_counts(dropna=False).items()}
        cols[c] = info
    prof = {"rows": len(df), "columns": len(df.columns), "columns_profile": cols}
    PROFILE.write_text(json.dumps(prof, indent=2, sort_keys=True) + "\n", "utf-8")
    print(f"Profile written -> {PROFILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
