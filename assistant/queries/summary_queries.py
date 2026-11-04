import json
from pathlib import Path

SUMMARY_PATH = Path("data-science/outputs/intelligence_summary.json")

def get_data_freshness():
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    
    return {
        "intent": "get_data_freshness",
        "answer_data": {
            "generated_at": summary["generated_at"],
            "data_version": summary["data_version"],
            "method_version": summary["method_version"]
        },
        "evidence": [
            {"factor": "generation_timestamp", "value": summary["generated_at"]}
        ],
        "metadata": {
            "data_version": summary["data_version"],
            "method_version": summary["method_version"],
            "quality_status": summary["validation_result"]
        },
        "limitation": "Freshness applies to the synthetic generation batch only."
    }