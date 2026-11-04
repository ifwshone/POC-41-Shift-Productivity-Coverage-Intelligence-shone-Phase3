import json
from pathlib import Path

RESULTS_PATH = Path("data-science/outputs/intelligence_results.json")
SUMMARY_PATH = Path("data-science/outputs/intelligence_summary.json")

def get_result_explanation(entity_id: str):
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    
    for item in results:
        if item.get("entity_id") == entity_id and item.get("quality_status") == "validated":
            return {
                "intent": "explain_result",
                "answer_data": {
                    "finding": item["finding"],
                    "result_value": item["result_value"],
                    "result_category": item["result_category"]
                },
                "evidence": item["evidence"],
                "metadata": {
                    "data_version": item["data_version"],
                    "method_version": item["method_version"],
                    "quality_status": item["quality_status"]
                },
                "limitation": item["limitation"]
            }
            
    return {"status": "unavailable", "limitation": "No validated matching result is available."}

def get_limitations():
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    limitations = summary.get("important_limitations", [])
    
    return {
        "intent": "explain_limitation",
        "answer_data": {"count": len(limitations), "items": limitations},
        "evidence": [{"factor": "limitation", "value": l} for l in limitations],
        "metadata": {
            "data_version": summary["data_version"],
            "method_version": summary["method_version"],
            "quality_status": summary["validation_result"]
        },
        "limitation": "Limitations are descriptive and bound to synthetic data."
    }