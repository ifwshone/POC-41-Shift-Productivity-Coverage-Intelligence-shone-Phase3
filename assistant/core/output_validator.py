import re

def validate_grounded_response(llm_text: str, evidence_package: dict) -> bool:
    """
    Validates the LLM output text against the deterministic evidence package.
    Returns True if safe, False if a numerical hallucination is detected.
    """
    # 1. Extract all numbers from LLM response
    llm_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', llm_text))
    
    # 2. Extract allowed numbers from evidence
    evidence_numbers = set(["1", "2", "3", "4", "5", "6", "7", "10", "2026", "24", "25", "26", "27", "28", "29", "30"]) # Safe temporal/ranking defaults
    
    for ev in evidence_package.get("evidence", []):
        val = ev.get("value")
        if isinstance(val, (int, float)):
            evidence_numbers.add(str(val))
            evidence_numbers.add(str(abs(val)))
            
    # Include baseline items if present
    for k, v in evidence_package.get("answer_data", {}).items():
        if isinstance(v, (int, float)):
            evidence_numbers.add(str(v))
            evidence_numbers.add(str(abs(v)))

    # 3. Reject if any LLM number is not mathematically grounded in the evidence
    for num in llm_numbers:
        if num not in evidence_numbers:
            print(f"Validation Block: Hallucination detected '{num}'")
            return False
            
    return True