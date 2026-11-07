import re
import json


def validate_numeric_fidelity(text: str, result_data: dict) -> bool:
    """
    Validates that all numbers in LLM-generated text exist within the evidence.
    Satisfies Phase 3 Finding B1.
    result_data shape: the full query result dict (has 'answer_data', 'evidence', etc.)
    """
    if not text:
        return False

    llm_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', text))

    # Extract all allowed numbers from the deterministic payload
    result_str = json.dumps(result_data)
    allowed_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', result_str))

    # B1 Exception: allow ordinal ranks explicitly
    items = result_data.get("answer_data", {}).get("items", [])
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and "priority_rank" in item:
                allowed_numbers.add(str(item["priority_rank"]))

    # Allow standard dataset context numbers
    allowed_numbers.update(["2026", "10", "24", "30", "28", "7", "1"])

    hallucinated = llm_numbers - allowed_numbers
    if hallucinated:
        print(f"\n--- B1 HALLUCINATION BLOCKED! Unauthorized numbers: {hallucinated} ---\n")
        return False

    return True


def validate_grounded_response(text: str, evidence_package: dict) -> bool:
    """
    Public alias used by tests and grounding harness.
    Accepts either:
      - an evidence_package with an 'evidence' key  (test shape)
      - a full result_data dict with 'answer_data'  (backend shape)
    Both are handled by normalising into the validate_numeric_fidelity format.
    """
    if not text:
        return False

    # Build allowed numbers from every numeric value in the package
    package_str = json.dumps(evidence_package)
    allowed_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', package_str))
    allowed_numbers.update(["2026", "10", "24", "30", "28", "7", "1"])

    llm_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', text))
    hallucinated = llm_numbers - allowed_numbers

    if hallucinated:
        print(f"\n--- GROUNDING CHECK FAILED: unauthorized numbers {hallucinated} ---\n")
        return False

    return True