"""Step 1 - Extract the app's existing (synthetic) data into a flat source extract.

Sources (only these, nothing external):
  1. frontend/app/page.tsx  -> `mockDatabase` + `dates` (parsed, not executed)
  2. backend/main.py        -> generate_synthetic_shift_data() (function body extracted via ast, seed 42)
  3. backend/mock_data.json -> empty fallback file (recorded, contributes 0 rows)
The UI-only interpolated "Last 30 Days"/"Year to Date" series are derived display padding and are excluded.
"""
import ast, json, re
import numpy as np
import pandas as pd
from _common import *

SHIFT_TO_TEAM = {"Morning": "Morning Crew", "Evening": "Evening Crew", "Night": "Night Watch"}


def parse_frontend(src: str):
    dates = re.findall(r"'(\d{4}-\d{2}-\d{2})'", re.search(r"const dates = \[([^\]]*)\]", src).group(1))
    block = re.search(r"const mockDatabase = \{(.*?)\n\};", src, re.S)
    raw_block = block.group(1)
    node_re = re.compile(
        r"'([^']+)':\s*\{\s*kpi:\s*'([\d.]+)',\s*overtime:\s*\[([^\]]*)\],\s*trend:\s*\[([^\]]*)\],"
        r'\s*issue:\s*"(.*?)",\s*status:\s*"(\w+)"\s*\}')
    rows, facility = [], None
    for line in raw_block.splitlines():
        f = re.match(r"\s*'(Facility [A-Z])':\s*\{\s*$", line)
        if f:
            facility = f.group(1)
            continue
        m = node_re.search(line)
        if m:
            team, kpi, ot, tr, issue, status = m.groups()
            ot = [float(x) for x in ot.split(",")]
            tr = [float(x) for x in tr.split(",")]
            assert len(ot) == len(tr) == len(dates), f"length mismatch {facility}/{team}"
            for d, o, t in zip(dates, ot, tr):
                rows.append({
                    "source_system": SRC_FE, "source_row_id": f"FE|{facility}|{team}|{d}",
                    "record_date": d, "facility": facility, "team": team, "shift": "",
                    "output_per_hour": t, "overtime_hours": o, "attendance_rate": "",
                    "node_kpi_output_per_hour": float(kpi), "node_status": status,
                    "node_issue_text": issue, "coverage_status": ""})
    assert len(rows) == 6 * len(dates), f"expected 6 nodes x {len(dates)} dates, got {len(rows)}"
    return rows, len(raw_block.encode("utf-8"))


def run_backend(src: str):
    tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "generate_synthetic_shift_data")
    ns = {"np": np, "pd": pd, "json": json}
    exec(compile(ast.Module([fn], []), str(BACKEND_MAIN), "exec"), ns)
    data = ns["generate_synthetic_shift_data"]()
    rows = []
    for r in data:
        rows.append({
            "source_system": SRC_BE, "source_row_id": f"BE|{r['date']}|{r['shift']}",
            "record_date": r["date"], "facility": "", "team": SHIFT_TO_TEAM[r["shift"]], "shift": r["shift"],
            "output_per_hour": r["output_per_hour"], "overtime_hours": r["overtime_hours"],
            "attendance_rate": r["attendance_rate"], "node_kpi_output_per_hour": "",
            "node_status": "", "node_issue_text": "", "coverage_status": r["coverage_status"]})
    assert len(rows) == 21
    return rows, len(json.dumps(data).encode("utf-8"))


def main():
    fe_rows, fe_bytes = parse_frontend(PAGE_TSX.read_text("utf-8"))
    be_rows, be_bytes = run_backend(BACKEND_MAIN.read_text("utf-8"))
    mock_bytes = BACKEND_MOCK.stat().st_size if BACKEND_MOCK.exists() else 0
    df = pd.DataFrame(fe_rows + be_rows, columns=SOURCE_COLUMNS)
    df = df.sort_values(["source_system", "source_row_id"]).reset_index(drop=True)
    SOURCE_SAMPLE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SOURCE_SAMPLE, index=False, encoding="utf-8", lineterminator="\n")
    raw = fe_bytes + be_bytes + mock_bytes
    save_stats({"original_record_count": len(df), "original_column_count": len(df.columns),
                "original_raw_size_bytes": raw,
                "original_sources": {SRC_FE: len(fe_rows), SRC_BE: len(be_rows), "backend/mock_data.json (empty fallback)": 0}})
    print(f"Extracted {len(df)} rows x {len(df.columns)} cols (raw ~{raw} bytes) -> {SOURCE_SAMPLE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
