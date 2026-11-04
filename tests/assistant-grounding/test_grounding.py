import pytest
from assistant.core.intent_classifier import classify_intent
from assistant.core.parameter_validator import validate_parameters
from assistant.core.output_validator import validate_grounded_response

def test_intent_accuracy():
    assert classify_intent("Which group ranks highest?")["intent"] == "list_priority_items"
    assert classify_intent("What are the limitations?")["intent"] == "explain_limitation"
    assert classify_intent("Why is facility_a_night_watch flagged?")["intent"] == "explain_result"
    assert classify_intent("Predict output for tomorrow")["intent"] == "OUT_OF_SCOPE"

def test_parameter_accuracy():
    intent_data = classify_intent("Which group ranks lowest?")
    params = validate_parameters(intent_data["intent"], intent_data["parameters"])
    assert params["result_category"] == "low"
    assert params["limit"] == 3

def test_numeric_fidelity():
    evidence_package = {
        "evidence": [{"factor": "avg_output_per_hour", "value": 93.6}],
        "limitation": "Descriptive 5-day view."
    }
    valid_response = {
        "answer_id": "ANS-01", "status": "answered", "intent": "explain_result",
        "answer": "Output is 93.6", "evidence_references": [], "metadata": {},
        "limitation": "Descriptive 5-day view.", "suggested_follow_ups": [],
        "key_values": [{"name": "output", "value": 93.6}]
    }
    
    # Should pass
    validate_grounded_response(valid_response, evidence_package)
    
    # Should fail due to hallucination
    invalid_response = dict(valid_response)
    invalid_response["key_values"] = [{"name": "output", "value": 100.0}]
    with pytest.raises(ValueError, match="Numeric hallucination detected"):
        validate_grounded_response(invalid_response, evidence_package)