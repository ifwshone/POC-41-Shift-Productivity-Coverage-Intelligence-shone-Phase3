import re
import json

def validate_grounded_response(llm_text: str, evidence_package: dict) -> bool:
    """
    Validates the LLM output text against the deterministic evidence package.
    Returns True if safe, False if a numerical hallucination is detected.
    """
    # 1. Extract all numbers from LLM response
    llm_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', llm_text))
    
    # 2. Extract every single allowed number from the entire evidence package payload
    package_str = json.dumps(evidence_package)
    evidence_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', package_str))
    
    # 3. Add safe common numbers (dates, rankings, list formatting, etc.)
    safe_numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                    "2026", "24", "25", "26", "27", "28", "29", "30"}
    evidence_numbers.update(safe_numbers)

    # 4. Reject if any LLM number is not mathematically grounded in the evidence
    for num in llm_numbers:
        if num not in evidence_numbers:
            print(f"Validation Block: Hallucination detected '{num}'")
            return False
            
    return True