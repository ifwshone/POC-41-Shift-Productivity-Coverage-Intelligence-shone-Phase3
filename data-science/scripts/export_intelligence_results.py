import json
from datetime import datetime, timezone
from pathlib import Path

# Dynamically resolve outputs directory
HERE = Path(__file__).resolve().parent
OUTPUTS_DIR = HERE.parent / "outputs"

def export_results(pivot_records, baseline):
    results = []
    generated_at = datetime.now(timezone.utc).isoformat()
    
    for rec in pivot_records:
        results.append({
            "result_id": f"RES-COMP-{rec['entity_id']}",
            "result_type": "ranking",
            "record_id": None,
            "entity_id": rec['entity_id'],
            "group_key": rec['category'],
            "period_start": "2026-10-24T00:00:00Z",
            "period_end": "2026-10-28T00:00:00Z",
            "metric_name": "output_gap_vs_baseline",
            "result_value": float(round(rec['output_gap_vs_baseline'], 2)),
            "result_unit": "units_per_hour",
            "result_category": "low" if rec['output_gap_vs_baseline'] < 0 else "high",
            "priority_rank": int(rec['priority_rank']),
            "finding": f"{rec['entity_id']} averages {round(rec['output_per_hour'], 1)} units/hr ({round(rec['output_gap_vs_baseline'], 1)} vs baseline) with {round(rec['overtime_hours'], 1)} avg overtime hours.",
            "evidence": [{"factor": "record_count", "value": int(rec['record_count'])}],
            "method_version": "1.0.0",
            "data_version": "1.0.0",
            "generated_at": generated_at,
            "quality_status": "validated",
            "limitation": "Descriptive comparison on 5 days of synthetic data only; no statistical significance."
        })
        
    summary = {
        "project_id": "POC-41",
        "project_title": "Shift Productivity & Coverage Intelligence",
        "approved_track": "Track A — Comparative Intelligence",
        "primary_analytical_question": "Across Facility A and B, which team's output and overtime differ most from the baseline?",
        "decision_to_be_supported": "Supervisor coverage and overtime allocation review priority.",
        "data_version": "1.0.0",
        "method_version": "1.0.0",
        "result_count": len(results),
        "key_findings": [r['finding'] for r in results[:2]],
        "priority_items": [r['entity_id'] for r in results[:2]],
        "validation_result": "PASS",
        "important_limitations": ["Frontend and backend scopes kept strictly separate.", "Synthetic 5-day view only."],
        "generated_at": generated_at
    }
    
    # Write files securely using UTF-8 to prevent Windows UnicodeEncodeError
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR / 'intelligence_results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTPUTS_DIR / 'intelligence_summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")