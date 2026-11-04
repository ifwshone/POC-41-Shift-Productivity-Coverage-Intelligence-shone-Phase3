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
    
    # Should pass (93.6 is in the evidence)
    assert validate_grounded_response("Output is 93.6", evidence_package) is True
    
    # Should fail due to hallucination (100.0 is not in the evidence)
    assert validate_grounded_response("Output is 100.0", evidence_package) is False