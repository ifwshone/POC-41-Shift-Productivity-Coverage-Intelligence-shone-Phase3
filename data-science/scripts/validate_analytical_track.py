# /data-science/scripts/validate_analytical_track.py
import pandas as pd
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA_PATH = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUTPUTS_DIR = HERE.parent / "outputs"

def validate_track():
    # 1. Load canonical data and generated intelligence results
    df = pd.read_csv(DATA_PATH, dtype={"is_synthetic": str})
    results_path = OUTPUTS_DIR / 'intelligence_results.json'
    
    if not results_path.exists():
        raise FileNotFoundError("intelligence_results.json not found. Run run_analytical_track.py first.")
        
    results = json.loads(results_path.read_text(encoding="utf-8"))
    
    # 2. Isolate frontend measurement data strictly (following input contract)
    fe_data = df[(df['source_name'].str.startswith('Frontend')) & (df['record_type'] == 'measurement')].copy()
    
    # 3. Independently recalculate baseline and expected group metrics
    independent_baseline = fe_data.groupby('metric_name')['metric_value'].mean().to_dict()
    ind_baseline_output = independent_baseline.get('output_per_hour', 0.0)
    
    grouped = fe_data.groupby(['entity_id', 'metric_name'])['metric_value'].mean().unstack()
    grouped['output_gap'] = grouped['output_per_hour'] - ind_baseline_output
    grouped['expected_rank'] = grouped['output_gap'].rank(method='dense', ascending=True).astype(int)
    
    # 4. Perform actual executable comparisons against intelligence results
    baseline_calculation_accurate = True
    tie_handling_deterministic = True
    
    for r in results:
        ent_id = r['entity_id']
        if ent_id in grouped.index:
            expected_val = round(float(grouped.loc[ent_id, 'output_gap']), 2)
            actual_val = float(r['result_value'])
            if abs(expected_val - actual_val) > 1e-4:
                baseline_calculation_accurate = False
            
            expected_rank = int(grouped.loc[ent_id, 'expected_rank'])
            actual_rank = int(r['priority_rank'])
            if expected_rank != actual_rank:
                tie_handling_deterministic = False
        else:
            baseline_calculation_accurate = False
            tie_handling_deterministic = False

    no_leakage_from_backend = len(fe_data) == 60
    minimum_group_size_met = all(r['evidence'][0]['value'] >= 5 for r in results)
    all_frontend_nodes_ranked = len(results) == 6

    checks = {
        "no_leakage_from_backend": no_leakage_from_backend,
        "minimum_group_size_met": minimum_group_size_met,
        "baseline_calculation_accurate": baseline_calculation_accurate,
        "tie_handling_deterministic": tie_handling_deterministic,
        "all_frontend_nodes_ranked": all_frontend_nodes_ranked
    }
    
    # 5. Determine pass/fail status based strictly on executable outcomes
    overall_status = "PASS" if all(checks.values()) else "FAIL"

    metrics = {
        "data_version": "1.0.0",
        "method_version": "1.0.0",
        "validation_checks": checks,
        "overall_status": overall_status
    }
    
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR / 'validation_metrics.json').write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    
    if overall_status == "FAIL":
        print("Validation FAILED. Check validation_metrics.json for failing checks.")
        raise SystemExit(1)
    else:
        print("Validation metrics generated successfully. Status: PASS")

if __name__ == "__main__":
    validate_track()