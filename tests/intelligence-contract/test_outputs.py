import json
from pathlib import Path

def test_intelligence_results_contract():
    path = Path("frontend/public/data/intelligence/intelligence_results.json")
    assert path.exists(), "Results JSON missing from public folder"
    
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) > 0
    
    for item in data:
        assert "result_id" in item
        assert "finding" in item
        assert item["quality_status"] in ["validated", "conditional", "rejected"]
        assert item["data_version"] == "1.0.0"
        assert item["method_version"] == "1.0.0"

def test_intelligence_summary_contract():
    path = Path("frontend/public/data/intelligence/intelligence_summary.json")
    assert path.exists(), "Summary JSON missing from public folder"
    
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "approved_track" in data
    assert "key_findings" in data
    assert isinstance(data["key_findings"], list)
    assert data["validation_result"] == "PASS"