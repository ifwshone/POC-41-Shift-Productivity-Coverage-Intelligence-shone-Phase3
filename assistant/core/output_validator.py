import re
import json

def validate_grounded_response(llm_text: str, evidence_package: dict) -> bool:
    """
    Validates the LLM output text against the deterministic evidence package.
    Returns True if safe, False if a hallucination is detected.
    """
    text_lower = llm_text.lower()

    # Rule 1: No predictive claims or unsupported risk scores
    blocked_claims = ["predict", "forecast", "will be", "risk score", "staffing-risk"]
    if any(term in text_lower for term in blocked_claims):
        print("Validation Block: Unsupported prediction or risk claim detected.")
        return False

    # Rule 2: Do not change or contradict the approved ranking
    finding = evidence_package.get("answer_data", {}).get("finding", "")
    if isinstance(finding, str):
        correct_rank_match = re.search(r"ranks (\d+)", finding.lower())
        if correct_rank_match:
            correct_rank = correct_rank_match.group(1)
            llm_rank_match = re.search(r"ranks (\d+)", text_lower)
            if llm_rank_match and llm_rank_match.group(1) != correct_rank:
                print(f"Validation Block: Ranking contradiction. Expected {correct_rank}, got {llm_rank_match.group(1)}.")
                return False

    # Rule 3: Numeric Fidelity Validation
    llm_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', llm_text))
    
    package_str = json.dumps(evidence_package)
    evidence_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', package_str))
    
    safe_numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                    "2026", "24", "25", "26", "27", "28", "29", "30"}
    evidence_numbers.update(safe_numbers)

    for num in llm_numbers:
        if num not in evidence_numbers:
            print(f"Validation Block: Numeric hallucination detected '{num}'")
            return False
            
    return True