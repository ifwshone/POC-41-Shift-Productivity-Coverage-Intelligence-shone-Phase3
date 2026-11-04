import pytest
from assistant.core.response_composer import compose_response
from assistant.core.evidence_builder import build_evidence_package

def test_evidence_builder():
    pkg = build_evidence_package(
        intent="test_intent",
        parameters={"id": 1},
        answer_data={"val": 42},
        evidence=[{"factor": "x", "value": 42}],
        metadata={"data_version": "1.0.0", "quality_status": "validated"},
        limitation="Test limit"
    )
    assert pkg["intent"] == "test_intent"
    assert pkg["metadata"]["quality_status"] == "validated"

def test_response_composer():
    pkg = {
        "evidence": [{"factor": "val", "value": 100}],
        "metadata": {"data_version": "1.0"},
        "limitation": "test limit"
    }
    res = compose_response(
        intent="explain",
        answer="The value is 100.",
        evidence_package=pkg,
        status="answered"
    )
    assert res["status"] == "answered"
    assert "ANS-" in res["answer_id"]
    assert res["limitation"] == "test limit"