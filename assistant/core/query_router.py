import json
from pathlib import Path

RESULTS_PATH = Path("data-science/outputs/intelligence_results.json")
SUMMARY_PATH = Path("data-science/outputs/intelligence_summary.json")

def load_data(path):
    return json.loads(path.read_text(encoding="utf-8"))

def get_priority_items(limit=10, result_category="low"):
    limit = max(1, min(int(limit), 25))
    results = [
        item for item in load_data(RESULTS_PATH)
        if item.get("result_type") == "ranking" and item.get("result_category") == result_category
    ]
    results.sort(key=lambda x: int(x.get("priority_rank", 999)))
    selected = results[:limit]
    
    if not selected:
        return {"status": "unavailable", "limitation": "No matching data."}

    return {
        "intent": "list_priority_items",
        "answer_data": {"count": len(selected), "items": selected},
        "evidence": [{"result_id": i["result_id"], "finding": i["finding"]} for i in selected],
        "metadata": {"data_version": selected[0]["data_version"], "method_version": selected[0]["method_version"]},
        "limitation": selected[0]["limitation"]
    }