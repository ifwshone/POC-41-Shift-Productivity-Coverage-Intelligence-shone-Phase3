# /assistant/queries/evidence_queries.py
import json
from pathlib import Path

RESULTS_PATH = Path("data-science/outputs/intelligence_results.json")

def get_raw_evidence(result_id: str):
    """
    Returns the raw evidence array for a specific result ID to ensure UI tracing.
    """
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    for r in results:
        if r.get("result_id") == result_id:
            return {
                "intent": "get_raw_evidence",
                "answer_data": {"result_id": result_id},
                "evidence": r.get("evidence", []),
                "metadata": {"data_version": r["data_version"], "method_version": r["method_version"]},
                "limitation": r["limitation"]
            }
    return {"status": "unavailable", "answer": "Evidence not found."}