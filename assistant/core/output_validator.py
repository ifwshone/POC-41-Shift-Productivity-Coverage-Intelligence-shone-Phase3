def validate_grounded_response(response: dict, evidence_package: dict) -> dict:
    """
    Validates the LLM output to ensure it matches the Grounded Response Contract,
    preventing hallucination of values or limitations.
    """
    required_fields = ["answer_id", "status", "intent", "answer", "evidence_references", "metadata", "limitation", "suggested_follow_ups"]
    
    for field in required_fields:
        if field not in response:
            raise ValueError(f"Response missing required field: {field}")
            
    # Numeric fidelity check
    for key_val in response.get("key_values", []):
        val = key_val["value"]
        # Ensure the value exists somewhere in the retrieved evidence factors
        found = any(e["value"] == val for e in evidence_package["evidence"] if "value" in e)
        if not found:
            raise ValueError(f"Numeric hallucination detected: {val} not found in evidence.")
            
    # Limitation fidelity check
    if response["limitation"] != evidence_package["limitation"]:
        raise ValueError("LLM altered the approved limitation.")
        
    return response