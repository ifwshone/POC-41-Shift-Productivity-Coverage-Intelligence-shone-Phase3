#!/usr/bin/env python3
"""Phase 3 Post #6 certification checks (read-only on the repo; regeneration runs in a temp copy).

Usage:  python scripts/certification/run_phase3_checks.py [--regen] [--out final-evidence/06-intelligence-contract/contract_check.json]

Checks performed (guide sections 6, 9, 11, 13, 14):
  * version consistency matrix across manifest, canonical CSV, outputs, frontend public copies
  * intelligence output contract (fields, unique ids, statuses, evidence, limitations, ISO timestamps, summary count)
  * frontend public copies == data-science outputs (ignoring nothing: stale copies FAIL)
  * secret / absolute-path / e-mail scan of text files
  * --regen: copy repo to a temp dir, run data pipeline + analytics there, compare with committed files
Exit code 1 if any check fails. Failures are reported, never suppressed.
"""
import argparse, json, re, shutil, subprocess, sys, tempfile
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data-science" / "outputs"
PUB = ROOT / "frontend" / "public" / "data" / "intelligence"
REQUIRED = ["result_id", "result_type", "record_id", "entity_id", "group_key", "period_start", "period_end",
            "metric_name", "result_value", "result_unit", "result_category", "priority_rank", "finding",
            "evidence", "method_version", "data_version", "generated_at", "quality_status", "limitation"]
STATUSES = {"validated", "conditional", "rejected"}
checks = []


def chk(name, ok, detail=""):
    checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": str(detail)})


def jload(p):
    return json.loads(Path(p).read_text("utf-8"))


def strip_ts(o):
    if isinstance(o, dict):
        return {k: strip_ts(v) for k, v in o.items() if k != "generated_at"}
    if isinstance(o, list):
        return [strip_ts(x) for x in o]
    return o


def iso(s):
    try:
        datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def versions():
    man = jload(ROOT / "data/manifest.json")
    csv = pd.read_csv(ROOT / "data/canonical/intelligence_data.csv", dtype=str)
    res, summ, met = jload(OUT / "intelligence_results.json"), jload(OUT / "intelligence_summary.json"), jload(OUT / "validation_metrics.json")
    pres, psumm = jload(PUB / "intelligence_results.json"), jload(PUB / "intelligence_summary.json")
    dv = man["data_version"]
    chk("ver_csv_data_version_eq_manifest", set(csv.data_version) == {dv}, sorted(set(csv.data_version)))
    chk("ver_results_data_version", {r["data_version"] for r in res} == {dv})
    chk("ver_results_method_version_single", len({r["method_version"] for r in res}) == 1, {r["method_version"] for r in res})
    mv = res[0]["method_version"]
    chk("ver_summary_versions", (summ["data_version"], summ["method_version"]) == (dv, mv))
    chk("ver_metrics_versions", (met["data_version"], met["method_version"]) == (dv, mv))
    chk("ver_public_copy_versions", all(r["data_version"] == dv and r["method_version"] == mv for r in pres) and (psumm["data_version"], psumm["method_version"]) == (dv, mv))
    pkg = jload(ROOT / "frontend/package.json")
    chk("ver_application_version_defined", "version" in pkg, "frontend/package.json has no 'version' field" if "version" not in pkg else pkg["version"])


def contract(tag, res, summ):
    chk(f"{tag}_is_nonempty_list", isinstance(res, list) and len(res) > 0, len(res))
    miss = [(r.get("result_id"), f) for r in res for f in REQUIRED if f not in r]
    chk(f"{tag}_required_fields", not miss, miss[:5] or "all present")
    ids = [r["result_id"] for r in res]
    chk(f"{tag}_unique_ids", len(ids) == len(set(ids)), len(ids))
    chk(f"{tag}_quality_status_allowed", all(r["quality_status"] in STATUSES for r in res))
    chk(f"{tag}_no_rejected_in_approved_set", all(r["quality_status"] != "rejected" for r in res))
    chk(f"{tag}_evidence_structure", all(isinstance(r["evidence"], list) and r["evidence"] and all("factor" in e and "value" in e for e in r["evidence"]) for r in res))
    chk(f"{tag}_limitation_present", all(isinstance(r["limitation"], str) and r["limitation"].strip() for r in res))
    chk(f"{tag}_generated_at_iso", all(iso(r["generated_at"]) for r in res) and iso(summ["generated_at"]))
    chk(f"{tag}_summary_count_matches", summ["result_count"] == len(res), f"{summ['result_count']} vs {len(res)}")
    chk(f"{tag}_summary_priority_items_in_results", set(summ["priority_items"]) <= {r["entity_id"] for r in res})


def sync():
    for f in ("intelligence_results.json", "intelligence_summary.json", "validation_metrics.json"):
        a, b = jload(OUT / f), jload(PUB / f)
        chk(f"public_copy_identical:{f}", a == b, "identical" if a == b else "frontend/public copy differs from data-science/outputs (stale copy)")


SECRET = re.compile(r"(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.I)
GKEY = re.compile(r"AIza[0-9A-Za-z_\-]{20,}")
ABS = re.compile(r"(/home/\w+|/Users/\w+|C:\\Users|/mnt/user)")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SKIP = {".git", "node_modules", ".next", "__pycache__", "final-evidence"}


def scan():
    hits = {"secret": [], "abs_path": [], "email": []}
    for p in ROOT.rglob("*"):
        if not p.is_file() or SKIP & set(p.relative_to(ROOT).parts) or p.suffix.lower() not in {".py", ".ts", ".tsx", ".json", ".md", ".yml", ".yaml", ".csv", ".txt", ".js", ".mjs", ".css", ""}:
            continue
        if p.name == "run_phase3_checks.py":
            continue
        t = p.read_text("utf-8", errors="ignore")
        rel = str(p.relative_to(ROOT))
        if SECRET.search(t) or GKEY.search(t): hits["secret"].append(rel)
        if ABS.search(t): hits["abs_path"].append(rel)
        if EMAIL.search(t): hits["email"].append(rel)
    chk("scan_no_secrets", not hits["secret"], hits["secret"] or "none found")
    chk("scan_no_local_absolute_paths", not hits["abs_path"], hits["abs_path"] or "none found")
    chk("scan_no_email_addresses", not hits["email"], hits["email"] or "none found")


def regen():
    tmp = Path(tempfile.mkdtemp(prefix="p3regen_"))
    try:
        dst = tmp / "repo"
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "node_modules", ".next", "__pycache__", "final-evidence"))
        env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": __import__("os").environ["PATH"]}
        for cmd in (["scripts/data_pipeline/run_pipeline.py"], ["data-science/scripts/run_analytical_track.py"], ["data-science/scripts/validate_analytical_track.py"]):
            r = subprocess.run([sys.executable, *cmd], cwd=dst, capture_output=True, text=True, env=env)
            chk(f"regen_exec:{cmd[0]}", r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")
        for rel in ("data/canonical/intelligence_data.csv", "data/published/intelligence_data.json", "data/schema.json", "data/manifest.json"):
            chk(f"regen_identical:{rel}", (ROOT / rel).read_bytes().rstrip() == (dst / rel).read_bytes().rstrip())
        for f in ("intelligence_results.json", "intelligence_summary.json", "validation_metrics.json"):
            same = strip_ts(jload(ROOT / "data-science/outputs" / f)) == strip_ts(jload(dst / "data-science/outputs" / f))
            chk(f"regen_equivalent_ignoring_generated_at:{f}", same, "equivalent" if same else "committed output differs from regenerated output (stale or manually edited)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regen", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    versions()
    contract("outputs", jload(OUT / "intelligence_results.json"), jload(OUT / "intelligence_summary.json"))
    contract("public", jload(PUB / "intelligence_results.json"), jload(PUB / "intelligence_summary.json"))
    sync(); scan()
    if a.regen: regen()
    failed = [c for c in checks if c["status"] == "FAIL"]
    rep = {"status": "PASS" if not failed else "FAIL", "checks_total": len(checks), "checks_failed": len(failed), "checks": checks}
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(rep, indent=2) + "\n", "utf-8")
    for c in checks:
        print(f"{c['status']:4} {c['check']}  {c['detail'] if c['status']=='FAIL' else ''}")
    print(f"\n{rep['status']}: {len(checks)-len(failed)}/{len(checks)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
